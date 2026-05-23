"""Dense sorgu — LanceDB üzerinde cosine benzerliği."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np

from docq.config import (
    DEFAULT_TOP_K,
    EMBEDDING_MODEL,
    LANCE_TABLE,
    STORE_DIR,
    detect_device,
    get_logger,
)

_LOG = get_logger("docq.query")


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
        raise FileNotFoundError(
            f"{STORE_DIR} yok — önce `docq embed` çalıştır."
        )
    db = lancedb.connect(STORE_DIR)
    if LANCE_TABLE not in db.table_names():
        raise RuntimeError(f"tablo bulunamadı: {LANCE_TABLE}")
    return db.open_table(LANCE_TABLE)


def _embed_query(text: str) -> np.ndarray:
    out = _model().encode(
        [text],
        max_length=8192,
        return_dense=True,
        return_sparse=False,
        return_colbert_vecs=False,
    )
    return np.asarray(out["dense_vecs"][0], dtype=np.float32)


def search(query: str, k: int = DEFAULT_TOP_K) -> list[SearchHit]:
    qvec = _embed_query(query)
    table = _table()
    raw = (
        table.search(qvec)
        .metric("cosine")
        .limit(k)
        .to_list()
    )
    hits: list[SearchHit] = []
    for r in raw:
        # LanceDB'nin verdiği uzaklık (cosine) → benzerlik
        dist = float(r.get("_distance", 0.0))
        score = 1.0 - dist
        hits.append(
            SearchHit(
                score=score,
                doc_id=r.get("doc_id", ""),
                source=r.get("source", ""),
                section_path=list(r.get("section_path", []) or []),
                content=r.get("content", ""),
                extra={
                    "chunk_id": r.get("chunk_id"),
                    "doc_type": r.get("doc_type"),
                },
            )
        )
    return hits
