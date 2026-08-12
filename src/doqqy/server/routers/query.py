"""Query API router handling search requests safely off the main event loop."""

from __future__ import annotations

import time

from fastapi import APIRouter, Request
from starlette.concurrency import run_in_threadpool

from doqqy.config import get_logger
from doqqy.server.schemas import HitOut, QueryRequest, QueryResponse, ScoreBreakdown

_LOG = get_logger("doqqy.server.query")
router = APIRouter(prefix="/v1", tags=["query"])


@router.post("/workspaces/{workspace_id:path}/query", response_model=QueryResponse)
async def query_workspace(
    workspace_id: str,
    req: QueryRequest,
    request: Request,
) -> QueryResponse:
    """Çalışma alanında hibrit arama yapar (event loop'u kilitlemeden threadpool üzerinde)."""
    t0 = time.perf_counter()

    models = request.app.state.models
    stores = request.app.state.stores
    settings = request.app.state.settings

    # Ağır yapay zeka çıkarımı ve vektör aramasını threadpool üzerinde çalıştırıyoruz
    def _do_search() -> list[HitOut]:
        with models.semaphore:
            from pathlib import Path

            from doqqy.query import search
            from doqqy.workspace import Workspace

            # Workspace yolunu çöz
            if Path(workspace_id).exists():
                ws = Workspace(Path(workspace_id))
            elif (settings.data_root / workspace_id).exists():
                ws = Workspace(settings.data_root / workspace_id)
            else:
                ws = Workspace(Path("./"))

            store = stores.get_store(ws)

            try:
                raw_hits = search(
                    ws,
                    req.q,
                    k=req.top_k,
                    rerank=req.rerank,
                    tag=req.tag,
                    settings=settings,
                    models=models,
                    store=store,
                )
            except Exception as e:  # noqa: BLE001
                _LOG.warning("Arama sırasında hata oluştu: %s", e)
                return []

            out: list[HitOut] = []
            for h in raw_hits:
                ex = h.extra or {}
                scores = ScoreBreakdown(
                    dense_rank=ex.get("dense_rank"),
                    sparse_rank=ex.get("sparse_rank"),
                    rrf_score=ex.get("rrf_score"),
                    rerank_score=ex.get("rerank_score"),
                )
                out.append(
                    HitOut(
                        score=float(h.score),
                        doc_id=str(h.doc_id),
                        source=str(h.source),
                        section_path=h.section_path or [],
                        content=str(h.content),
                        scores=scores,
                    )
                )
            return out

    hits = await run_in_threadpool(_do_search)
    took_ms = int((time.perf_counter() - t0) * 1000)

    return QueryResponse(
        hits=hits,
        took_ms=took_ms,
        workspace=workspace_id,
    )
