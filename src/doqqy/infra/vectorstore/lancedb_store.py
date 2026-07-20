"""LanceDB implementation of the VectorStore port."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
import pyarrow as pa

from doqqy.config import LANCE_TABLE, RRF_K, get_logger
from doqqy.infra.vectorstore.base import ChunkRecord, ScoredChunk, TagFilter, VectorStore

_LOG = get_logger("doqqy.infra.vectorstore.lancedb")

# Global table cache to prevent re-opening tables repeatedly within the same process.
# Maps store_dir resolved path -> lancedb Table object.
_TABLE_CACHE: dict[Path, object] = {}


def invalidate_table_cache_by_path(store_dir: Path) -> None:
    """Evict a table handle from cache when its database files are modified/recreated."""
    _TABLE_CACHE.pop(store_dir.resolve(), None)


def _rrf(dense_rows: list[dict], sparse_rows: list[dict], k: int = RRF_K) -> list[dict]:
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


# ---------------------------------------------------------------------------
# Schema — single source of truth for column types and nullability.
# The vector field dimension is resolved at runtime; _build_schema(dim)
# takes this base and overrides the vector field with the exact fixed-size list.
# ---------------------------------------------------------------------------
_LANCE_SCHEMA_BASE = pa.schema([
    pa.field("chunk_id",         pa.utf8(),              nullable=False),
    pa.field("doc_id",           pa.utf8(),              nullable=False),
    pa.field("source",           pa.utf8(),              nullable=False),
    pa.field("doc_type",         pa.utf8(),              nullable=False),
    pa.field("tags",             pa.list_(pa.utf8()),    nullable=False),
    pa.field("section_path",     pa.list_(pa.utf8()),    nullable=False),
    pa.field("char_count",       pa.int64(),             nullable=False),
    pa.field("prev_chunk",       pa.utf8(),              nullable=True),   # None for first/last chunk
    pa.field("next_chunk",       pa.utf8(),              nullable=True),
    pa.field("content",          pa.utf8(),              nullable=False),
    pa.field("vector",           pa.list_(pa.float32()), nullable=False),  # dim overridden in _build_schema
    pa.field("sparse_vector",    pa.utf8(),              nullable=False),  # JSON string: {token_id: weight}
    pa.field("section_path_str", pa.utf8(),              nullable=False),  # " > ".join(section_path)
    pa.field("tags_str",         pa.utf8(),              nullable=False),  # ",tag1,tag2," — query filter
])


def _build_schema(dim: int) -> pa.Schema:
    """Return a schema identical to _LANCE_SCHEMA_BASE with the vector field fixed to *dim* elements."""
    fields = []
    for field in _LANCE_SCHEMA_BASE:
        if field.name == "vector":
            fields.append(pa.field("vector", pa.list_(pa.float32(), list_size=dim), nullable=False))
        else:
            fields.append(field)
    return pa.schema(fields)


class LanceDBStore(VectorStore):
    """Adapter implementing local-first vector search using LanceDB."""

    def __init__(self, store_dir: Path) -> None:
        self._store_dir = store_dir

    def _table(self):
        import lancedb  # type: ignore

        key = self._store_dir.resolve()
        cached = _TABLE_CACHE.get(key)
        if cached is not None:
            return cached

        if not self._store_dir.exists():
            raise FileNotFoundError(f"{self._store_dir} does not exist. Run `doqqy embed` first.")

        db = lancedb.connect(self._store_dir)
        if LANCE_TABLE not in db.list_tables().tables:
            raise RuntimeError(f"Table not found: {LANCE_TABLE}")

        table = db.open_table(LANCE_TABLE)
        _TABLE_CACHE[key] = table
        return table

    def _invalidate_cache(self) -> None:
        invalidate_table_cache_by_path(self._store_dir)

    def recreate(self, dim: int) -> None:
        """Drop the LanceDB table if it exists and recreate an empty table with the correct schema.

        Schema is derived from the module-level _LANCE_SCHEMA_BASE constant — no dummy row,
        no post-create delete. Column types and nullability are explicit and stable.
        Use full_rebuild() for doqqy embed (atomic overwrite). This method is reserved
        for the incremental path (doqqy sync / issue #16).
        """
        import lancedb  # type: ignore

        self._invalidate_cache()
        self._store_dir.mkdir(parents=True, exist_ok=True)
        db = lancedb.connect(self._store_dir)

        if LANCE_TABLE in db.list_tables().tables:
            db.drop_table(LANCE_TABLE)

        schema = _build_schema(dim)
        db.create_table(LANCE_TABLE, schema=schema)
        _LOG.debug("Empty table created: %s (dim=%d)", LANCE_TABLE, dim)

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        """Insert or update chunks, deriving storage-specific columns (tags_str, section_path_str)."""
        if not records:
            return 0

        import lancedb  # type: ignore

        self._invalidate_cache()

        data = []
        for rec in records:
            section_path_str = " > ".join(rec.section_path)
            tags_str = f",{','.join(rec.tags)}," if rec.tags else ""
            sparse_json = json.dumps({str(k): float(v) for k, v in rec.sparse.items()}) if rec.sparse else "{}"

            data.append({
                "chunk_id": rec.chunk_id,
                "doc_id": rec.doc_id,
                "source": rec.source,
                "doc_type": rec.doc_type,
                "tags": rec.tags,
                "section_path": rec.section_path,
                "char_count": rec.char_count,
                "prev_chunk": rec.prev_chunk,
                "next_chunk": rec.next_chunk,
                "content": rec.content,
                "vector": rec.dense,
                "sparse_vector": sparse_json,
                "section_path_str": section_path_str,
                "tags_str": tags_str,
            })

        df = pd.DataFrame(data)
        db = lancedb.connect(self._store_dir)

        if LANCE_TABLE not in db.list_tables().tables:
            db.create_table(LANCE_TABLE, data=df, mode="overwrite")
        else:
            table = db.open_table(LANCE_TABLE)
            table.merge_insert(on="chunk_id").when_matched_update_all().when_not_matched_insert_all().execute(df)

        return len(records)

    def delete_by_doc(self, doc_id: str) -> int:
        """Remove all chunks associated with doc_id from the store."""
        import lancedb  # type: ignore

        db = lancedb.connect(self._store_dir)
        if LANCE_TABLE not in db.list_tables().tables:
            return 0

        self._invalidate_cache()
        table = db.open_table(LANCE_TABLE)
        count_before = len(table)
        doc_id_escaped = doc_id.replace("'", "''")
        table.delete(f"doc_id = '{doc_id_escaped}'")
        return count_before - len(table)

    def _dense_search(self, qvec: np.ndarray, k: int, flt: TagFilter | None = None) -> list[dict]:
        query_builder = self._table().search(qvec).metric("cosine")

        if flt and flt.tags:
            clauses = [f"tags_str LIKE '%,{t.replace(chr(39), chr(39)+chr(39))},%'" for t in flt.tags]
            query_builder = query_builder.where(" AND ".join(clauses))

        rows = query_builder.limit(k).to_list()
        results = []
        for r in rows:
            dist = float(r.get("_distance", 0.0))
            results.append({**r, "dense_score": 1.0 - dist})
        return results

    def _sparse_search(self, query_sparse: dict[int, float], k: int, flt: TagFilter | None = None) -> list[dict]:
        table = self._table()
        if flt and flt.tags:
            clauses = [f"tags_str LIKE '%,{t.replace(chr(39), chr(39)+chr(39))},%'" for t in flt.tags]
            rows = table.search().where(" AND ".join(clauses)).to_pandas()
        else:
            rows = table.to_pandas()

        if "sparse_vector" not in rows.columns:
            _LOG.warning("sparse_vector column missing - using dense only.")
            return []

        scores: list[tuple[float, int]] = []
        for idx, row in rows.iterrows():
            try:
                chunk_sparse: dict[str, float] = json.loads(row["sparse_vector"])
            except (json.JSONDecodeError, TypeError):
                scores.append((0.0, idx))
                continue

            dot = sum(query_sparse.get(int(tok), 0.0) * w for tok, w in chunk_sparse.items())
            scores.append((dot, idx))

        scores.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, idx in scores[:k]:
            row = rows.iloc[idx].to_dict()
            row["sparse_score"] = score
            results.append(row)
        return results


    def _to_record(self, row: dict) -> ChunkRecord:
        sparse_vec = {}
        sparse_str = row.get("sparse_vector")
        if sparse_str:
            try:
                sparse_vec = {int(k): float(v) for k, v in json.loads(sparse_str).items()}
            except (json.JSONDecodeError, TypeError):
                pass

        def to_list(val) -> list[str]:
            if val is None:
                return []
            try:
                return [str(x) for x in list(val)]
            except TypeError:
                return []

        section_path = to_list(row.get("section_path"))
        tags = to_list(row.get("tags"))

        return ChunkRecord(
            chunk_id=str(row.get("chunk_id", "")),
            doc_id=str(row.get("doc_id", "")),
            source=str(row.get("source", "")),
            doc_type=str(row.get("doc_type", "")),
            tags=tags,
            content=str(row.get("content", "")),
            section_path=section_path,
            char_count=int(row.get("char_count", 0)),
            prev_chunk=str(row.get("prev_chunk")) if row.get("prev_chunk") is not None else None,
            next_chunk=str(row.get("next_chunk")) if row.get("next_chunk") is not None else None,
            dense=np.asarray(row["vector"], dtype=np.float32) if row.get("vector") is not None else None,
            sparse=sparse_vec,
        )

    def hybrid_search(
        self, dense: np.ndarray, sparse: dict[int, float],
        *, limit: int, flt: TagFilter | None = None,
    ) -> list[ScoredChunk]:
        """Query dense and sparse indexes separately, merge via client-side RRF."""
        dense_rows = self._dense_search(dense, limit, flt)
        sparse_rows = self._sparse_search(sparse, limit, flt)
        fused = _rrf(dense_rows, sparse_rows)[:limit]

        scored_chunks = []
        for item in fused:
            scored_chunks.append(ScoredChunk(
                record=self._to_record(item),
                dense_rank=item.get("dense_rank"),
                sparse_rank=item.get("sparse_rank"),
                fused_score=item.get("rrf_score", 0.0),
            ))
        return scored_chunks

    def get_by_ids(self, chunk_ids: Sequence[str]) -> list[ChunkRecord]:
        """Retrieve records with matching chunk IDs."""
        if not chunk_ids:
            return []

        table = self._table()
        ids_str = ", ".join(f"'{cid.replace(chr(39), chr(39)+chr(39))}'" for cid in chunk_ids)
        rows = table.search().where(f"chunk_id IN ({ids_str})").to_list()
        return [self._to_record(r) for r in rows]

    def all_vectors(self, flt: TagFilter | None = None) -> tuple[np.ndarray, list[ChunkRecord]]:
        """Retrieve all dense vectors and records, optionally filtered by tag."""
        import lancedb  # type: ignore

        db = lancedb.connect(self._store_dir)
        if LANCE_TABLE not in db.list_tables().tables:
            return np.zeros((0, 1024), dtype=np.float32), []

        table = db.open_table(LANCE_TABLE)
        query_builder = table.search()
        if flt and flt.tags:
            clauses = [f"tags_str LIKE '%,{t.replace(chr(39), chr(39)+chr(39))},%'" for t in flt.tags]
            query_builder = query_builder.where(" AND ".join(clauses))

        rows = query_builder.to_list()
        if not rows:
            return np.zeros((0, 1024), dtype=np.float32), []

        records = [self._to_record(r) for r in rows]
        vecs = np.vstack([r.dense for r in records]).astype(np.float32)
        return vecs, records

    def list_tags(self) -> list[str]:
        """List all unique tags by scanning the store table."""
        table = self._table()
        df = table.to_pandas()
        if "tags" in df.columns:
            all_tags = set()
            for tags_list in df["tags"].dropna():
                for t in tags_list:
                    all_tags.add(t)
            return sorted(list(all_tags))
        return []

    def count(self) -> int:
        """Return the count of rows in the table."""
        return len(self._table())

    def close(self) -> None:
        """No-op connection close for local LanceDB."""
        pass
