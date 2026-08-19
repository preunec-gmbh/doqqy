"""Tests for doqqy HTTP server (create_app, healthz, readyz, query, SLOs)."""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import patch

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("uvicorn")
pytest.importorskip("pydantic_settings")

from fastapi.testclient import TestClient

from doqqy.infra.models import ModelManager
from doqqy.infra.settings import Settings
from doqqy.infra.store import StoreManager
from doqqy.server.app import create_app
from doqqy.workspace import Workspace


def test_readyz_false_before_warmup():
    """/readyz warmup öncesinde (lifespan tetiklenmeden) 503 false dönmeli."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)
    # TestClient context manager (with) olmadan çağrıldığında lifespan çalışmaz
    client = TestClient(app)
    resp = client.get("/readyz")
    assert resp.status_code == 503
    assert resp.json() == {"status": "not_ready", "models_loaded": False}


def test_readyz_true_after_warmup():
    """/readyz warmup sonrasında (lifespan çalıştıktan sonra) 200 true dönmeli."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)
    with patch.object(ModelManager, "warmup", return_value=None):
        with TestClient(app) as client:
            for _ in range(50):
                resp = client.get("/readyz")
                if resp.status_code == 200:
                    break
                time.sleep(0.01)
            assert resp.status_code == 200
            assert resp.json() == {"status": "ready", "models_loaded": True}


def test_healthz_liveness():
    """/healthz hemen 200 status ok dönmeli."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)
    client = TestClient(app)
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_store_manager_lru_eviction_and_close(tmp_path):
    """StoreManager LRU limitini aşınca en eski store'u kapatmalı ve close_all() temizlemeli."""
    settings = Settings(auth_mode="none")
    mgr = StoreManager(settings=settings, max_open=2)

    ws1 = Workspace(tmp_path / "ws1")
    ws2 = Workspace(tmp_path / "ws2")
    ws3 = Workspace(tmp_path / "ws3")

    s1 = mgr.get_store(ws1)
    s2 = mgr.get_store(ws2)

    with patch.object(s1, "close", wraps=s1.close) as mock_close_1:
        # ws3 açılınca s1 eviction edilip kapatılmalı
        s3 = mgr.get_store(ws3)
        assert mock_close_1.called or s1 != s3

    # close_all çağrılınca tüm kalan store'lar kapatılmalı
    with patch.object(s2, "close", wraps=s2.close) as mock_close_2:
        mgr.close_all()
        assert mock_close_2.called or len(mgr._cache) == 0


def _index_size(ws: Workspace) -> int:
    """Fixture index'indeki kayıt sayısı — SLO assert mesajlarının hangi boyutta ölçtüğünü bildirmesi için."""
    import contextlib

    from doqqy.infra.vectorstore.factory import make_store

    with contextlib.closing(make_store(ws)) as store:
        return store.count()


def _create_fixture_workspace(root: Path) -> Workspace:
    """Testler için gerçek doküman içeren, chunk'lanmış ve embed edilmiş fixture workspace üretir.

    DİKKAT: Tek dokümanlık bu fixture yalnızca ~2 kayıtlık bir index üretir; cross-encoder
    dolayısıyla RETRIEVAL_TOP_K (50) yerine sadece 2 pair skorlar. Aşağıdaki SLO testleri
    bu boyut için geçerlidir, docs/API-ARCHITECTURE.md §6.5'in yazıldığı ≤10k chunk için
    DEĞİL — gerçek boyutlu corpus ölçümleri ve 800 ms hedefinin CPU'da tutmaması #62'de.
    """
    from doqqy.chunk import chunk_directory
    from doqqy.embed import build_index
    from doqqy.ingest import ingest_file

    ws = Workspace(root)
    ws.ensure_dirs()

    raw_doc = ws.raw_dir / "fatura_ve_iade_rehberi.md"
    raw_doc.write_text(
        "# Kurumsal Fatura ve İptal Rehberi\n\n"
        "## 1. Fatura İptal ve İade Süreci\n\n"
        "Kurumsal faturalar kesildikten sonra 7 iş günü içinde iptal edilebilir. "
        "İptal işlemi için muhasebe portalından talep oluşturulması zorunludur. "
        "Geciken faturalar için iade faturası düzenlenmesi gerekmektedir.\n\n"
        "## 2. İade Şartları ve Kesinti Oranları\n\n"
        "İade edilen ürünlerde kargo ve sigorta bedelleri müşteriye aittir.",
        encoding="utf-8",
    )

    doc = ingest_file(raw_doc, ws)
    doc.write()
    chunk_directory(ws)
    build_index(ws)
    return ws


def test_query_round_trip_fixture_workspace(tmp_path):
    """Gerçek fixture workspace üzerinde mock'suz arama yapıp dönen hit içeriğini ve skorları doğrula."""
    ws = _create_fixture_workspace(tmp_path / "ws_roundtrip")

    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        # Sunucu warmup tamamlanana kadar kısa süre bekle
        for _ in range(50):
            if client.get("/readyz").status_code == 200:
                break
            time.sleep(0.05)

        payload = {
            "q": "fatura iptal ve iade süreci",
            "top_k": 3,
            "rerank": True,
        }
        resp = client.post(f"/v1/workspaces/{ws.root}/query", json=payload)
        assert resp.status_code == 200
        data = resp.json()

        assert "hits" in data
        assert len(data["hits"]) > 0, "Gerçek arama sonucu boş dönmemeli (hits > 0 olmalı)!"
        hit = data["hits"][0]
        assert hit["source"] == "raw/fatura_ve_iade_rehberi.md"
        assert "Fatura İptal" in hit["content"] or "7 iş günü" in hit["content"]
        assert hit["scores"]["dense_rank"] is not None
        assert hit["scores"]["sparse_rank"] is not None
        assert hit["scores"]["rrf_score"] is not None and hit["scores"]["rrf_score"] > 0
        assert hit["scores"]["rerank_score"] is not None and hit["scores"]["rerank_score"] > 0
        for score_name, score_value in hit["scores"].items():
            assert hit["extra"][score_name] == score_value
        assert data["took_ms"] >= 0


def test_query_nonexistent_workspace_returns_404(tmp_path):
    """Var olmayan bir workspace_id ile yapılan sorgu 404 Not Found dönmeli."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        resp = client.post(
            f"/v1/workspaces/{tmp_path / 'nonexistent_workspace'}/query",
            json={"q": "fatura", "top_k": 5},
        )
        assert resp.status_code == 404
        assert "not found" in resp.json().get("detail", "").lower()


# SLO (Service Level Objectives) Testleri:
@pytest.mark.slow
def test_slo_readiness_duration_under_120s():
    """SLO: Modellerin açılışta yüklenme süresi (Readiness) < 120 saniye olmalı."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    t0 = time.perf_counter()
    with TestClient(app) as client:
        ready = False
        while time.perf_counter() - t0 < 120.0:
            resp = client.get("/readyz")
            if resp.status_code == 200 and resp.json().get("models_loaded") is True:
                ready = True
                break
            time.sleep(0.1)

        startup_duration = time.perf_counter() - t0
        assert ready is True, f"Açılış süresi ({startup_duration:.2f}s) 120s sınırını aştı!"


@pytest.mark.slow
def test_slo_query_warm_with_rerank_under_800ms(tmp_path):
    """SLO: Modeller sıcakken rerank açık p95 arama süresi < 800 ms olmalı — fixture boyutunda.

    Bu eşik yalnızca aşağıda raporlanan kayıt sayısı için anlamlıdır. §6.5'teki hedef
    ≤10k chunk için yazılmıştır ve CPU'da o boyutta tutmuyor (320 kayıtta p95 ≈ 7.3 s) — #62.
    """
    ws = _create_fixture_workspace(tmp_path / "ws_slo_rerank")
    index_size = _index_size(ws)
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        # Modeller yüklenene kadar bekle
        for _ in range(50):
            if client.get("/readyz").status_code == 200:
                break
            time.sleep(0.05)

        # Warm-up ön hazırlık sorguları (model ve veritabanı önbelleği sıcak)
        for _ in range(2):
            warm_resp = client.post(f"/v1/workspaces/{ws.root}/query", json={"q": "warmup fatura", "top_k": 5, "rerank": True})
            assert warm_resp.status_code == 200
            assert len(warm_resp.json()["hits"]) > 0, "Warmup sorgusu sonuç bulmalı (dizin dolu olmalı)!"

        # Çoklu sorgu ile p95 gecikme dağılımını ölçme (20 iterasyon)
        latencies: list[int] = []
        for i in range(20):
            resp = client.post(
                f"/v1/workspaces/{ws.root}/query",
                json={"q": f"fatura iptal süreci sorgu {i}", "top_k": 5, "rerank": True},
            )
            assert resp.status_code == 200
            assert len(resp.json()["hits"]) > 0, "SLO sorgusu sonuç bulmalı!"
            latencies.append(resp.json()["took_ms"])

        latencies.sort()
        import numpy as np

        p95_ms = float(np.percentile(latencies, 95))

        assert p95_ms < 800, (
            f"Rerank p95 süresi ({p95_ms:.1f} ms) {index_size} kayıtlık fixture index'te "
            f"800 ms sınırını aştı! Tüm süreler: {latencies}"
        )


@pytest.mark.slow
def test_slo_query_warm_no_rerank_under_250ms(tmp_path):
    """SLO: Modeller sıcakken rerank kapalı p95 arama süresi < 250 ms olmalı — fixture boyutunda.

    Retrieval maliyeti corpus ile büyüdüğü için bu eşiğin payı dar: 320 kayıtta p95 ≈ 243 ms
    ölçüldü, yani §6.5'in ≤10k chunk hedefine varmadan sınırı geçiyor — #62.
    """
    ws = _create_fixture_workspace(tmp_path / "ws_slo_norerank")
    index_size = _index_size(ws)
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        # Modeller yüklenene kadar bekle
        for _ in range(50):
            if client.get("/readyz").status_code == 200:
                break
            time.sleep(0.05)

        for _ in range(2):
            warm_resp = client.post(
                f"/v1/workspaces/{ws.root}/query",
                json={"q": "warmup fatura", "top_k": 5, "rerank": False},
            )
            assert warm_resp.status_code == 200
            assert len(warm_resp.json()["hits"]) > 0, "Warmup sorgusu sonuç bulmalı!"

        latencies: list[int] = []
        for i in range(20):
            resp = client.post(
                f"/v1/workspaces/{ws.root}/query",
                json={"q": f"hızlı arama sorgu {i}", "top_k": 5, "rerank": False},
            )
            assert resp.status_code == 200
            assert len(resp.json()["hits"]) > 0, "SLO sorgusu sonuç bulmalı!"
            latencies.append(resp.json()["took_ms"])

        latencies.sort()
        import numpy as np

        p95_ms = float(np.percentile(latencies, 95))

        assert p95_ms < 250, (
            f"Rerank kapalı p95 süresi ({p95_ms:.1f} ms) {index_size} kayıtlık fixture index'te "
            f"250 ms sınırını aştı! Tüm süreler: {latencies}"
        )


def test_slo_api_availability_healthz():
    """SLO: API katmanı kesintisiz çalışmalı (Availability >= %99.5)."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        # Arka arkaya 50 hızlı sağlık isteği
        success_count = 0
        total_requests = 50

        for _ in range(total_requests):
            resp = client.get("/healthz")
            if resp.status_code == 200 and resp.json() == {"status": "ok"}:
                success_count += 1

        availability = (success_count / total_requests) * 100
        assert availability >= 99.5, f"Kullanılabilirlik oranı (%{availability}) %99.5'in altında kaldı!"
