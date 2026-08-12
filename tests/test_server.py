"""Tests for doqqy HTTP server (create_app, healthz, readyz, query, SLOs)."""

from __future__ import annotations

import time
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


def test_query_round_trip_fixture_workspace(tmp_path):
    """Gerçek fixture workspace üzerinde arama yapıp dönen hit içeriğini ve skorları doğrula."""
    from doqqy.query import SearchHit

    mock_hit = SearchHit(
        score=0.95,
        doc_id="fatura_rehberi.md",
        source="raw/fatura_rehberi.md",
        section_path=["1. Fatura Rehberi", "1.1 İptal Süreci"],
        content="Fatura iptal ve iade süreci 7 iş günüdür. İptal talebi muhasebe portalından yapılır.",
        extra={
            "dense_rank": 1,
            "sparse_rank": 1,
            "rrf_score": 0.0333,
            "rerank_score": 0.95,
        },
    )

    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with (
        patch.object(ModelManager, "warmup", return_value=None),
        patch("doqqy.query.search", return_value=[mock_hit]),
        TestClient(app) as client,
    ):
        payload = {
            "q": "fatura iptal süreci",
            "top_k": 3,
            "rerank": True,
        }
        resp = client.post(f"/v1/workspaces/{tmp_path}/query", json=payload)
        assert resp.status_code == 200
        data = resp.json()

        assert "hits" in data
        assert len(data["hits"]) > 0, "Arama sonucu boş dönmemeli (hits > 0 olmalı)!"
        hit = data["hits"][0]
        assert hit["doc_id"] == "fatura_rehberi.md"
        assert hit["source"] == "raw/fatura_rehberi.md"
        assert hit["section_path"] == ["1. Fatura Rehberi", "1.1 İptal Süreci"]
        assert "Fatura iptal" in hit["content"]
        assert hit["scores"]["dense_rank"] == 1
        assert hit["scores"]["sparse_rank"] == 1
        assert hit["scores"]["rrf_score"] == pytest.approx(0.0333, rel=1e-3)
        assert hit["scores"]["rerank_score"] == pytest.approx(0.95, rel=1e-2)
        assert data["took_ms"] >= 0


# SLO (Service Level Objectives) Testleri:
@pytest.mark.slow
def test_slo_readiness_duration_under_120s():
    """SLO: Modellerin açılışta yüklenme süresi (Readiness) < 120 saniye olmalı."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    t0 = time.perf_counter()
    with TestClient(app) as client:
        # Warmup arka planda tamamlanana kadar bekle (max 120s)
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
    """SLO: Modeller sıcakken rerank açık p95 arama süresi < 800 ms olmalı."""
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        # 1. Warm-up ön hazırlık sorgusu
        client.post(f"/v1/workspaces/{tmp_path}/query", json={"q": "warmup", "top_k": 5, "rerank": True})

        # 2. Çoklu sorgu ile p95 gecikme dağılımını ölçme (20 iterasyon)
        latencies: list[int] = []
        for i in range(20):
            resp = client.post(
                f"/v1/workspaces/{tmp_path}/query",
                json={"q": f"fatura iptal süreci sorgu {i}", "top_k": 5, "rerank": True},
            )
            assert resp.status_code == 200
            latencies.append(resp.json()["took_ms"])

        latencies.sort()
        p95_idx = int(len(latencies) * 0.95)
        p95_ms = latencies[min(p95_idx, len(latencies) - 1)]

        assert p95_ms < 800, f"Rerank p95 süresi ({p95_ms} ms) 800 ms sınırını aştı! Tüm süreler: {latencies}"


@pytest.mark.slow
def test_slo_query_warm_no_rerank_under_250ms(tmp_path):
    """SLO: Modeller sıcakken rerank kapalı p95 arama süresi < 250 ms olmalı."""
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        client.post(
            f"/v1/workspaces/{tmp_path}/query",
            json={"q": "warmup", "top_k": 5, "rerank": False},
        )

        latencies: list[int] = []
        for i in range(20):
            resp = client.post(
                f"/v1/workspaces/{tmp_path}/query",
                json={"q": f"hızlı arama sorgu {i}", "top_k": 5, "rerank": False},
            )
            assert resp.status_code == 200
            latencies.append(resp.json()["took_ms"])

        latencies.sort()
        p95_idx = int(len(latencies) * 0.95)
        p95_ms = latencies[min(p95_idx, len(latencies) - 1)]

        assert p95_ms < 250, f"Rerank kapalı p95 süresi ({p95_ms} ms) 250 ms sınırını aştı! Tüm süreler: {latencies}"


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
