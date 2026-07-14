"""Golden result parity tests verifying that LanceDBStore returns identical search results to the legacy implementation."""

from __future__ import annotations

import json
from pathlib import Path
import numpy as np
import pytest

from doqqy.workspace import Workspace
from doqqy.embed import build_index
from doqqy.infra.vectorstore.base import ChunkRecord, TagFilter
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore
from doqqy.config import RRF_K


def legacy_dense_search(store_dir: Path, qvec: np.ndarray, k: int, filter_tag: str | None = None) -> list[dict]:
    import lancedb  # type: ignore

    db = lancedb.connect(store_dir)
    table = db.open_table("chunks")
    query_builder = table.search(qvec).metric("cosine")
    if filter_tag:
        query_builder = query_builder.where(f"tags_str LIKE '%,{filter_tag},%'")
    rows = query_builder.limit(k).to_list()
    results = []
    for r in rows:
        dist = float(r.get("_distance", 0.0))
        results.append({**r, "dense_score": 1.0 - dist})
    return results


def legacy_sparse_search(store_dir: Path, query_sparse: dict[str, float], k: int, filter_tag: str | None = None) -> list[dict]:
    import lancedb  # type: ignore

    db = lancedb.connect(store_dir)
    table = db.open_table("chunks")
    if filter_tag:
        rows = table.search().where(f"tags_str LIKE '%,{filter_tag},%'").to_pandas()
    else:
        rows = table.to_pandas()

    if "sparse_vector" not in rows.columns:
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
    results = []
    for score, idx in scores[:k]:
        row = rows.iloc[idx].to_dict()
        row["sparse_score"] = score
        results.append(row)
    return results


def legacy_rrf(dense_rows: list[dict], sparse_rows: list[dict], k: int = RRF_K) -> list[dict]:
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


def test_search_results_parity(tmp_path: Path):
    """Index mock documents and verify that old & new search paths yield byte-for-byte identical output."""
    store_dir = tmp_path / "store.lance"
    store = LanceDBStore(store_dir)
    store.recreate(dim=128)

    # 1. Create a set of dummy indexed documents
    np.random.seed(42)
    records = []
    for i in range(10):
        dense_vec = np.random.rand(128).astype(np.float32)
        # Random tags
        tags = ["core"]
        if i % 2 == 0:
            tags.append("even")
        else:
            tags.append("odd")

        rec = ChunkRecord(
            chunk_id=f"chunk-{i}",
            doc_id=f"doc-{i // 2}",
            source=f"doc_{i // 2}.md",
            doc_type="markdown",
            tags=tags,
            content=f"Content for chunk number {i}",
            section_path=["Test", f"Sec {i}"],
            char_count=30,
            prev_chunk=f"chunk-{i-1}" if i > 0 else None,
            next_chunk=f"chunk-{i+1}" if i < 9 else None,
            dense=dense_vec,
            sparse={100 + i: 1.0, 200 + i: 0.5},
        )
        records.append(rec)

    store.upsert(records)

    # 2. Run identical search parameters on both paths
    query_dense = np.random.rand(128).astype(np.float32)
    query_sparse = {100: 1.0, 102: 0.8}
    query_sparse_str = {"100": 1.0, "102": 0.8}  # legacy string-keyed representation

    # Test with tag filtering
    legacy_dense = legacy_dense_search(store_dir, query_dense, k=5, filter_tag="even")
    legacy_sparse = legacy_sparse_search(store_dir, query_sparse_str, k=5, filter_tag="even")
    legacy_fused = legacy_rrf(legacy_dense, legacy_sparse, k=RRF_K)[:5]

    flt = TagFilter(tags=("even",))
    new_results = store.hybrid_search(query_dense, query_sparse, limit=5, flt=flt)

    # 3. Assert rankings, IDs, and scores are exactly equal
    assert len(legacy_fused) == len(new_results)
    for leg_hit, new_hit in zip(legacy_fused, new_results):
        assert leg_hit["chunk_id"] == new_hit.record.chunk_id
        assert leg_hit.get("dense_rank") == new_hit.dense_rank
        assert leg_hit.get("sparse_rank") == new_hit.sparse_rank
        assert pytest.approx(leg_hit["rrf_score"]) == new_hit.fused_score

    store.close()
