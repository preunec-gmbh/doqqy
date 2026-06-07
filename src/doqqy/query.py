"""Hibrit arama: dense + sparse → RRF → reranker."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np

from doqqy.config import (
    DEFAULT_TOP_K,
    EMBEDDING_MODEL,
    LANCE_TABLE,
    RETRIEVAL_TOP_K,
    STORE_DIR,
    detect_device,
    get_logger,
)

_LOG = get_logger("doqqy.query")

RRF_K = 60


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


@lru_cache(maxsize=1)
def _model():
    from FlagEmbedding import BGEM3FlagModel  # type: ignore

    device = detect_device()
    return BGEM3FlagModel(EMBEDDING_MODEL, use_fp16=(device == "cuda"), device=device)


@lru_cache(maxsize=1)
def _table():
    import lancedb  # type: ignore

    if not STORE_DIR.exists():
        raise FileNotFoundError(f"{STORE_DIR} yok — önce `doqqy embed` çalıştır.")
    db = lancedb.connect(STORE_DIR)
    if LANCE_TABLE not in db.table_names():
        raise RuntimeError(f"tablo bulunamadı: {LANCE_TABLE}")
    return db.open_table(LANCE_TABLE)


def _embed_query(text: str) -> tuple[np.ndarray, dict[str, float]]:
    out = _model().encode(
        [text],
        max_length=1024,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=False,
    )
    dense = np.asarray(out["dense_vecs"][0], dtype=np.float32)
    sparse = {str(k): float(v) for k, v in out["lexical_weights"][0].items()}
    return dense, sparse


def _dense_search(qvec: np.ndarray, k: int, filter_tag: str | None = None) -> list[dict]:
    query_builder = _table().search(qvec).metric("cosine")

    if filter_tag:
        # Array'i string olarak kaydettiğimiz formatta arıyoruz
        query_builder = query_builder.where(f"tags_str LIKE '%,{filter_tag},%'")

    rows = query_builder.limit(k).to_list()
    results = []
    for r in rows:
        dist = float(r.get("_distance", 0.0))
        results.append({**r, "dense_score": 1.0 - dist})
    return results


def _sparse_search(query_sparse: dict[str, float], k: int, filter_tag: str | None = None) -> list[dict]:
    """Tüm chunk'ların sparse vektörleriyle dot product hesapla, top-k döndür."""
    table = _table()
    if filter_tag:
        rows = table.search().where(f"tags_str LIKE '%,{filter_tag},%'").to_pandas()
    else:
        rows = table.to_pandas()

    if "sparse_vector" not in rows.columns:
        _LOG.warning("sparse_vector kolonu yok — sadece dense kullanılıyor.")
        return []

    scores: list[tuple[float, int]] = []
    for idx, row in rows.iterrows():
        try:
            chunk_sparse: dict[str, float] = json.loads(row["sparse_vector"])
        except (json.JSONDecodeError, TypeError):
            scores.append((0.0, idx))
            continue
        dot = sum(query_sparse.get(tok, 0.0) * w for tok, w in chunk_sparse.items())
        scores.append((dot, idx))

    scores.sort(key=lambda x: x[0], reverse=True)
    top_indices = [idx for _, idx in scores[:k]]
    results = []
    for score, idx in scores[:k]:
        row = rows.iloc[idx].to_dict()
        row["sparse_score"] = score
        results.append(row)
    return results


def _rrf(
    dense_rows: list[dict],
    sparse_rows: list[dict],
    k: int = RRF_K,
) -> list[dict]:
    """Reciprocal Rank Fusion — chunk_id başına skor birleştir."""
    by_id: dict[str, dict] = {}

    for rank, row in enumerate(dense_rows):
        cid = row.get("chunk_id", str(rank))
        by_id.setdefault(cid, row)
        by_id[cid]["rrf_score"] = by_id[cid].get("rrf_score", 0.0) + 1.0 / (k + rank)
        by_id[cid]["dense_rank"] = rank + 1

    for rank, row in enumerate(sparse_rows):
        cid = row.get("chunk_id", str(rank))
        by_id.setdefault(cid, row)
        by_id[cid]["rrf_score"] = by_id[cid].get("rrf_score", 0.0) + 1.0 / (k + rank)
        by_id[cid]["sparse_rank"] = rank + 1

    return sorted(by_id.values(), key=lambda x: x.get("rrf_score", 0.0), reverse=True)


def search(query: str, k: int = DEFAULT_TOP_K, rerank: bool = True, tag: str | None = None) -> list[SearchHit]:
    dense_vec, sparse_vec = _embed_query(query)

    dense_rows = _dense_search(dense_vec, RETRIEVAL_TOP_K, filter_tag=tag)
    sparse_rows = _sparse_search(sparse_vec, RETRIEVAL_TOP_K, filter_tag=tag)
    fused = _rrf(dense_rows, sparse_rows)[:RETRIEVAL_TOP_K]

    if rerank and fused:
        from doqqy.rerank import rerank as do_rerank
        candidates = [{"content": r.get("content", ""), **r} for r in fused]
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

    # --no-rerank: RRF sonrası ilk k
    hits = []
    for r in fused[:k]:
        hits.append(SearchHit(
            score=r.get("rrf_score", 0.0),
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
            },
        ))
    return hits
