"""Tests for doqqy HTTP server (create_app, healthz, readyz, query, SLOs)."""

from fastapi.testclient import TestClient

from doqqy.infra.settings import Settings
from doqqy.server.app import create_app


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
    # with TestClient(app) şeklinde çağrıldığında lifespan tetiklenir
    with TestClient(app) as client:
        resp = client.get("/readyz")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ready", "models_loaded": True}


def test_query_round_trip():
    """Sorgu rotasına POST /v1/workspaces/{wid}/query isteği atma testi."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        payload = {
            "q": "test sorgusu",
            "top_k": 5,
            "rerank": True,
        }
        resp = client.post("/v1/workspaces/demo-ws/query", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "hits" in data
        assert "took_ms" in data
        assert data["workspace"] == "demo-ws"


# SLO (Service Level Objectives) Testleri:
def test_slo_readiness_duration_under_120s():
    """SLO: Modellerin açılışta yüklenme süresi (Readiness) < 120 saniye olmalı."""
    import time
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    t0 = time.perf_counter()
    with TestClient(app) as client:
        startup_duration = time.perf_counter() - t0
        resp = client.get("/readyz")
        assert resp.status_code == 200
        assert resp.json()["models_loaded"] is True
        assert startup_duration < 120.0, f"Açılış süresi ({startup_duration:.2f}s) 120s sınırını aştı!"


def test_slo_query_warm_with_rerank_under_800ms():
    """SLO: Modeller sıcakken rerank açık p95 arama süresi < 800 ms olmalı."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        # 1. Warm-up ön hazırlık sorgusu
        client.post("/v1/workspaces/demo-ws/query", json={"q": "warmup", "top_k": 5, "rerank": True})

        # 2. Çoklu sorgu ile p95 gecikme dağılımını ölçme (20 iterasyon)
        latencies: list[int] = []
        for i in range(20):
            resp = client.post(
                "/v1/workspaces/demo-ws/query",
                json={"q": f"fatura iptal süreci sorgu {i}", "top_k": 5, "rerank": True},
            )
            assert resp.status_code == 200
            latencies.append(resp.json()["took_ms"])

        latencies.sort()
        p95_idx = int(len(latencies) * 0.95)
        p95_ms = latencies[min(p95_idx, len(latencies) - 1)]

        assert p95_ms < 800, f"Rerank p95 süresi ({p95_ms} ms) 800 ms sınırını aştı! Tüm süreler: {latencies}"


def test_slo_query_warm_no_rerank_under_250ms():
    """SLO: Modeller sıcakken rerank kapalı p95 arama süresi < 250 ms olmalı."""
    settings = Settings(auth_mode="none")
    app = create_app(settings)

    with TestClient(app) as client:
        latencies: list[int] = []
        for i in range(20):
            resp = client.post(
                "/v1/workspaces/demo-ws/query",
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
