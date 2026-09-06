"""FastAPI application factory with model warmup lifespan and health routes."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from doqqy.config import get_logger
from doqqy.infra.jobs import InProcessQueue
from doqqy.infra.models import ModelManager
from doqqy.infra.settings import Settings
from doqqy.infra.store import StoreManager
from doqqy.server.routers.query import router as query_router

_LOG = get_logger("doqqy.server")


def create_app(settings: Settings | None = None) -> FastAPI:
    """FastAPI uygulama örneğini oluşturan fabrika fonksiyonu."""
    app_settings = settings or Settings()

    models = ModelManager(app_settings)
    stores = StoreManager(app_settings)
    queue = InProcessQueue()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """Sunucu yaşam döngüsü: Açılışta modelleri arka planda ısıtır, kapanışta temizler."""
        app.state.is_ready = False

        async def _warmup_task() -> None:
            try:
                await run_in_threadpool(models.warmup)
                app.state.is_ready = True
            except Exception as e:  # noqa: BLE001
                _LOG.error("Model warmup başarısız: %s", e)
                app.state.is_ready = False

        warmup_task = asyncio.create_task(_warmup_task())
        app.state.warmup_task = warmup_task

        yield

        # Kapanış (Shutdown): Temizlik işlemleri
        app.state.is_ready = False
        if not warmup_task.done():
            warmup_task.cancel()
        stores.close_all()

    app = FastAPI(
        title="doqqy API",
        version="1.0.0",
        description="Local-first neural search & RAG server",
        lifespan=lifespan,
    )

    # State değişkenlerini uygulamaya bağla (Dependency Injection için)
    app.state.settings = app_settings
    app.state.models = models
    app.state.stores = stores
    app.state.queue = queue
    app.state.is_ready = False

    # Sağlık ve durum rotaları (Meta Routers):
    @app.get("/healthz", summary="Liveness Probe")
    async def healthz() -> dict[str, str]:
        """Sunucunun çalışır durumda olduğunu doğrular."""
        return {"status": "ok"}

    @app.get("/readyz", summary="Readiness Probe")
    async def readyz() -> JSONResponse:
        """Modellerin yüklendiğini ve sunucunun sorgu almaya hazır olduğunu doğrular."""
        if getattr(app.state, "is_ready", False):
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "ready", "models_loaded": True},
            )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "models_loaded": False},
        )

    # Store katmanı, indekslenmemiş bir workspace için FileNotFoundError fırlatır
    # (bkz. LanceDBStore._table()). Rotadaki is_indexed() kontrolü bunu normalde
    # daha erken yakalar; bu handler, kontrolü atlatan her yolu 500 yerine yine
    # 409'a bağlayan bir son savunma. Ortaya çıkan durum her hâlükârda
    # "indekslenmemiş workspace" olduğu için sunucu arızası olarak raporlanmamalı.
    #
    # Kapsamı hakkında dürüst olmak gerekirse: kontrol geçtikten sonra store
    # diskten silinirse bu handler devreye girmez — LanceDB tablo tutamacı süreç
    # genelinde önbelleklendiği için arama, silinmiş dizinden bellekteki manifest
    # ile servis etmeye devam eder ve boş sonuçla 200 döner. Önbellek tazeliği
    # ayrı bir sorun; burası onu çözmüyor.
    @app.exception_handler(FileNotFoundError)
    async def store_not_indexed_handler(request: Request, exc: FileNotFoundError) -> JSONResponse:
        """Store dosyaları bulunamadığında 500 yerine 409 döndürür."""
        workspace_id = str(request.path_params.get("workspace_id", ""))
        _LOG.warning("Store bulunamadı (%s): %s", request.url.path, exc)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": (
                    f"Workspace is not indexed: '{workspace_id}'. "
                    "Run `doqqy embed` first."
                )
            },
        )

    # Rotaları (Routers) bağlama
    app.include_router(query_router)

    return app
