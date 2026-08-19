"""Hibrit arama: dense + sparse → RRF → reranker."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Sequence

import numpy as np

from doqqy.config import (
    DEFAULT_TOP_K,
    RETRIEVAL_TOP_K,
    get_logger,
)
from doqqy.infra.settings import Settings
from doqqy.workspace import Workspace

if TYPE_CHECKING:
    from doqqy.infra.models import ModelManager
    from doqqy.infra.vectorstore.base import TagFilter, VectorStore

_LOG = get_logger("doqqy.query")


def _safe_section_path(val) -> list[str]:
    if val is None:
        return []
    try:
        lst = list(val)
        return [str(x) for x in lst] if lst else []
    except TypeError:
        return []


@dataclass
class SearchHit:
    score: float
    doc_id: str
    source: str
    section_path: list[str]
    content: str
    extra: dict = field(default_factory=dict)


@dataclass
class ExpandedContext:
    """A hit's content plus its neighboring chunks, walked via prev_chunk/next_chunk."""
    before: list[str]
    after: list[str]
    hit: str

    def __str__(self) -> str:
        SEP = "\n\n— · —\n\n"
        return SEP.join([*self.before, self.hit, *self.after])


def _model(models: ModelManager | None = None, settings: Settings | None = None):
    from doqqy.infra.models import get_default_model_manager

    mgr = models if models is not None else get_default_model_manager(settings)
    return mgr.get_embedder()


def _embed_query(
    text: str,
    models: ModelManager | None = None,
    settings: Settings | None = None,
) -> tuple[np.ndarray, dict[int, float]]:
    out = _model(models=models, settings=settings).encode(
        [text],
        max_length=1024,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=False,
    )
    dense = np.asarray(out["dense_vecs"][0], dtype=np.float32)
    sparse = {int(k): float(v) for k, v in out["lexical_weights"][0].items()}
    return dense, sparse


def search(
    ws: Workspace,
    query: str,
    *,
    k: int = DEFAULT_TOP_K,
    rerank: bool = True,
    tag: str | None = None,
    tag_filter: TagFilter | Sequence[str] | None = None,
    settings: Settings | None = None,
    models: ModelManager | None = None,
    store: VectorStore | None = None,
) -> list[SearchHit]:
    from doqqy.infra.vectorstore.base import TagFilter
    from doqqy.infra.vectorstore.factory import make_store

    if tag_filter is not None:
        if isinstance(tag_filter, TagFilter):
            flt = tag_filter
        else:
            flt = TagFilter(tags=tuple(tag_filter))
    elif tag:
        flt = TagFilter(tags=(tag,))
    else:
        flt = None

    if models is not None or settings is not None:
        dense_vec, sparse_vec = _embed_query(query, models=models, settings=settings)
    else:
        dense_vec, sparse_vec = _embed_query(query)

    if store is not None:
        fused_chunks = store.hybrid_search(dense_vec, sparse_vec, limit=RETRIEVAL_TOP_K, flt=flt)
    else:
        with contextlib.closing(make_store(ws, settings)) as s:
            fused_chunks = s.hybrid_search(dense_vec, sparse_vec, limit=RETRIEVAL_TOP_K, flt=flt)

    if rerank and fused_chunks:
        from doqqy.rerank import rerank as do_rerank

        candidates = []
        for c in fused_chunks:
            rec = c.record
            candidates.append({
                "chunk_id": rec.chunk_id,
                "doc_id": rec.doc_id,
                "source": rec.source,
                "doc_type": rec.doc_type,
                "tags": rec.tags,
                "content": rec.content,
                "section_path": rec.section_path,
                "char_count": rec.char_count,
                "prev_chunk": rec.prev_chunk,
                "next_chunk": rec.next_chunk,
                "dense_rank": c.dense_rank,
                "sparse_rank": c.sparse_rank,
                "rrf_score": c.fused_score,
            })
        reranked = do_rerank(query, candidates, top_k=k, models=models, settings=settings)
        hits = []
        for r in reranked:
            hits.append(SearchHit(
                score=r.get("rerank_score", 0.0),
                doc_id=r.get("doc_id", ""),
                source=r.get("source", ""),
                section_path=_safe_section_path(r.get("section_path")),
                content=r.get("content", ""),
                extra={
                    "chunk_id": r.get("chunk_id"),
                    "doc_type": r.get("doc_type"),
                    "dense_rank": r.get("dense_rank"),
                    "sparse_rank": r.get("sparse_rank"),
                    "rrf_score": r.get("rrf_score"),
                    "rerank_score": r.get("rerank_score"),
                    "prev_chunk": r.get("prev_chunk"),
                    "next_chunk": r.get("next_chunk"),
                },
            ))
        return hits

    # --no-rerank: top k from RRF
    hits = []
    for c in fused_chunks[:k]:
        rec = c.record
        hits.append(SearchHit(
            score=c.fused_score,
            doc_id=rec.doc_id,
            source=rec.source,
            section_path=rec.section_path,
            content=rec.content,
            extra={
                "chunk_id": rec.chunk_id,
                "doc_type": rec.doc_type,
                "dense_rank": c.dense_rank,
                "sparse_rank": c.sparse_rank,
                "rrf_score": c.fused_score,
                "prev_chunk": rec.prev_chunk,
                "next_chunk": rec.next_chunk,
            },
        ))
    return hits


def expand_context(store: VectorStore, hit: SearchHit, n: int) -> ExpandedContext:
    """Walk *n* steps in each direction from *hit* via prev_chunk/next_chunk.

    Reranking already happened by this point — expansion is purely additive,
    display-only, and never affects which hits were selected or their order.
    """
    if n <= 0:
        return ExpandedContext(before=[], after=[], hit=hit.content)

    def _walk(chunk_id: str | None, attr: str) -> list[str]:
        contents = []
        current_id = chunk_id
        for _ in range(n):
            if not current_id:
                break
            records = store.get_by_ids([current_id])
            if not records:
                break
            contents.append(records[0].content)
            current_id = getattr(records[0], attr)
        return contents

    before = list(reversed(_walk(hit.extra.get("prev_chunk"), "prev_chunk")))
    after = _walk(hit.extra.get("next_chunk"), "next_chunk")
    return ExpandedContext(before=before, after=after, hit=hit.content)
