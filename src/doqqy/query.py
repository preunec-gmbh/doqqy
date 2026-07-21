"""Hibrit arama: dense + sparse → RRF → reranker."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np

from doqqy.config import (
    DEFAULT_TOP_K,
    EMBEDDING_MODEL,
    RETRIEVAL_TOP_K,
    detect_device,
    get_logger,
)
from doqqy.infra.settings import Settings
from doqqy.workspace import Workspace

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


# Model korpus-bağımsız → process-global singleton kalır.
@lru_cache(maxsize=1)
def _model():
    from FlagEmbedding import BGEM3FlagModel  # type: ignore

    device = detect_device()
    return BGEM3FlagModel(EMBEDDING_MODEL, use_fp16=(device == "cuda"), device=device)


def _embed_query(text: str) -> tuple[np.ndarray, dict[int, float]]:
    out = _model().encode(
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
    settings: Settings | None = None,
) -> list[SearchHit]:

    from doqqy.infra.vectorstore.base import TagFilter
    from doqqy.infra.vectorstore.factory import make_store

    # Validate tag early — raises InvalidTagError before loading the embedding model.
    flt = TagFilter(tags=(tag,)) if tag else None

    dense_vec, sparse_vec = _embed_query(query)
    with make_store(ws, settings) as store:
        fused_chunks = store.hybrid_search(dense_vec, sparse_vec, limit=RETRIEVAL_TOP_K, flt=flt)


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
        reranked = do_rerank(query, candidates, top_k=k)
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
            },
        ))
    return hits
