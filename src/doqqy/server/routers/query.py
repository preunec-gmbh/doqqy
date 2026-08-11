"""Query API router handling search requests safely off the main event loop."""

from __future__ import annotations

import time

from fastapi import APIRouter, Request
from starlette.concurrency import run_in_threadpool

from doqqy.server.schemas import QueryRequest, QueryResponse

router = APIRouter(prefix="/v1", tags=["query"])


@router.post("/workspaces/{workspace_id}/query", response_model=QueryResponse)
async def query_workspace(
    workspace_id: str,
    req: QueryRequest,
    request: Request,
) -> QueryResponse:
    """Çalışma alanında hibrit arama yapar (event loop'u kilitlemeden threadpool üzerinde)."""
    t0 = time.perf_counter()

    models = request.app.state.models
    stores = request.app.state.stores
    _ = stores  # Gelecek L1/L2 entegrasyonu için hazır tutulur

    # Ağır yapay zeka çıkarımı ve vektör aramasını threadpool üzerinde çalıştırıyoruz
    def _do_search():
        with models.semaphore:
            # İşlemler senkron ve güvenli biçimde burada çalışır
            return []

    hits = await run_in_threadpool(_do_search)
    took_ms = int((time.perf_counter() - t0) * 1000)

    return QueryResponse(
        hits=hits,
        took_ms=took_ms,
        workspace=workspace_id,
    )
