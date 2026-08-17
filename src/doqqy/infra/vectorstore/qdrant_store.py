"""Qdrant implementation of the VectorStore port."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

import numpy as np

from doqqy.config import EMBEDDING_DIM, QDRANT_SPARSE_ON_DISK, QDRANT_UPSERT_BATCH_SIZE, get_logger
from doqqy.infra.vectorstore.base import ChunkRecord, ScoredChunk, TagFilter, VectorStore

if TYPE_CHECKING:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models

_LOG = get_logger("doqqy.infra.vectorstore.qdrant")


class QdrantStore(VectorStore):
    """Adapter implementing server-side vector search using Qdrant."""

    def __init__(self, url: str, api_key: str, collection: str, tenant_key: str) -> None:
        self.url = url
        self.api_key = api_key
        self.collection = collection
        self.tenant_key = tenant_key
        self._client_instance: QdrantClient | None = None
        self._collection_verified: bool = False

    @property
    def _client(self) -> QdrantClient:
        if self._client_instance is None:
            try:
                from qdrant_client import QdrantClient  # type: ignore
            except ImportError as exc:
                raise ImportError(
                    "qdrant-client is required for the Qdrant backend. "
                    "Install it via `pip install doqqy[qdrant]`."
                ) from exc
            self._client_instance = QdrantClient(
                url=self.url,
                api_key=self.api_key or None,
                check_compatibility=False,
            )
        return self._client_instance

    def ensure_collection(self, dim: int) -> None:
        """Ensure the target collection and payload indices exist in Qdrant."""
        if self._collection_verified:
            return

        from qdrant_client import models  # type: ignore

        client = self._client
        if client.collection_exists(self.collection):
            info = client.get_collection(self.collection)
            existing_vectors = info.config.params.vectors
            if isinstance(existing_vectors, dict) and "dense" in existing_vectors:
                existing_dim = existing_vectors["dense"].size
            elif hasattr(existing_vectors, "size"):
                existing_dim = existing_vectors.size
            else:
                existing_dim = None

            if isinstance(existing_dim, int) and existing_dim != dim:
                raise ValueError(
                    f"Collection '{self.collection}' exists with dense dimension {existing_dim}, "
                    f"but requested dimension is {dim}."
                )
            self._collection_verified = True
            return

        _LOG.info("Creating Qdrant collection: %s (dim=%d)", self.collection, dim)
        client.create_collection(
            collection_name=self.collection,
            vectors_config={
                "dense": models.VectorParams(size=dim, distance=models.Distance.COSINE),
            },
            sparse_vectors_config={
                "sparse": models.SparseVectorParams(
                    index=models.SparseIndexParams(on_disk=QDRANT_SPARSE_ON_DISK),
                    modifier=models.Modifier.IDF,
                ),
            },
        )

        client.create_payload_index(
            self.collection,
            "tenant",
            models.KeywordIndexParams(
                type=models.KeywordIndexType.KEYWORD,
                is_tenant=True,
            ),
        )
        client.create_payload_index(
            self.collection,
            "tags",
            models.PayloadSchemaType.KEYWORD,
        )
        client.create_payload_index(
            self.collection,
            "doc_id",
            models.PayloadSchemaType.KEYWORD,
        )
        self._collection_verified = True
        _LOG.info("Qdrant collection %s created with payload indexes.", self.collection)

    def recreate(self, dim: int) -> None:
        """Clear points for the current tenant and ensure collection exists."""
        from qdrant_client import models  # type: ignore

        self.ensure_collection(dim)
        client = self._client
        if client.collection_exists(self.collection):
            tenant_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant",
                        match=models.MatchValue(value=self.tenant_key),
                    )
                ]
            )
            client.delete(
                collection_name=self.collection,
                points_selector=models.FilterSelector(filter=tenant_filter),
            )

    @staticmethod
    def _infer_dim(records: Sequence[ChunkRecord]) -> int:
        """Infer vector dimension from the first non-null dense vector in records."""
        for rec in records:
            if rec.dense is not None:
                return int(np.asarray(rec.dense).shape[-1])
        raise ValueError("Cannot infer dimension: no record contains a dense vector.")

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        """Upsert a sequence of ChunkRecords as Qdrant Points in batches."""
        if not records:
            return 0

        from qdrant_client import models  # type: ignore

        dim = self._infer_dim(records)
        self.ensure_collection(dim)

        points = []
        for rec in records:
            if rec.dense is None:
                _LOG.warning("Skipping record %s: dense vector is None", rec.chunk_id)
                continue
            dense_vec = rec.dense.tolist()
            if rec.sparse:
                indices = list(rec.sparse.keys())
                values = [float(v) for v in rec.sparse.values()]
                sparse_vec = models.SparseVector(indices=indices, values=values)
            else:
                sparse_vec = models.SparseVector(indices=[], values=[])

            point = models.PointStruct(
                id=rec.chunk_id,
                vector={
                    "dense": dense_vec,
                    "sparse": sparse_vec,
                },
                payload={
                    "tenant": self.tenant_key,
                    "doc_id": rec.doc_id,
                    "source": rec.source,
                    "doc_type": rec.doc_type,
                    "tags": rec.tags,
                    "content": rec.content,
                    "section_path": rec.section_path,
                    "char_count": rec.char_count,
                    "prev_chunk": rec.prev_chunk,
                    "next_chunk": rec.next_chunk,
                },
            )
            points.append(point)

        if not points:
            return 0

        batch_size = QDRANT_UPSERT_BATCH_SIZE
        for i in range(0, len(points), batch_size):
            batch = points[i : i + batch_size]
            self._client.upsert(collection_name=self.collection, points=batch)

        _LOG.debug("Upserted %d points to Qdrant collection %s", len(points), self.collection)
        return len(points)

    def full_rebuild(self, records: Sequence[ChunkRecord], dim: int) -> int:
        """Delete all points for the current tenant and re-insert records.

        Note: This is NOT fully atomic across tenants — if interrupted mid-upsert,
        the current tenant's data will be partially empty. True atomicity (new
        collection + alias swap) is incompatible with the shared-collection model.
        """
        from qdrant_client import models  # type: ignore

        self.ensure_collection(dim)
        client = self._client
        if client.collection_exists(self.collection):
            tenant_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant",
                        match=models.MatchValue(value=self.tenant_key),
                    )
                ]
            )
            client.delete(
                collection_name=self.collection,
                points_selector=models.FilterSelector(filter=tenant_filter),
            )

        return self.upsert(records)

    def delete_by_doc(self, doc_id: str) -> int:
        """Delete all points belonging to *doc_id* for the current tenant."""
        from qdrant_client import models  # type: ignore

        client = self._client
        if not client.collection_exists(self.collection):
            return 0

        doc_filter = models.Filter(
            must=[
                models.FieldCondition(key="tenant", match=models.MatchValue(value=self.tenant_key)),
                models.FieldCondition(key="doc_id", match=models.MatchValue(value=doc_id)),
            ]
        )

        count_before = client.count(collection_name=self.collection, count_filter=doc_filter).count
        if count_before == 0:
            return 0

        client.delete(
            collection_name=self.collection,
            points_selector=models.FilterSelector(filter=doc_filter),
        )
        _LOG.debug("Deleted %d points for doc_id=%s in collection %s", count_before, doc_id, self.collection)
        return count_before

    def _build_filter(self, flt: TagFilter | None = None) -> models.Filter:
        """Construct structured Qdrant filter for tenant and optional tags."""
        from qdrant_client import models  # type: ignore

        conditions: list[Any] = [
            models.FieldCondition(key="tenant", match=models.MatchValue(value=self.tenant_key)),
        ]
        if flt and flt.tags:
            for tag in flt.tags:
                conditions.append(models.FieldCondition(key="tags", match=models.MatchValue(value=tag)))
        return models.Filter(must=conditions)

    def _to_record(self, point: Any) -> ChunkRecord:
        """Convert a Qdrant PointStruct/ScoredPoint to ChunkRecord."""
        payload = point.payload or {}
        dense_vec = None
        if hasattr(point, "vector") and point.vector:
            if isinstance(point.vector, dict) and "dense" in point.vector:
                dense_vec = np.asarray(point.vector["dense"], dtype=np.float32)
            elif isinstance(point.vector, list):
                dense_vec = np.asarray(point.vector, dtype=np.float32)

        return ChunkRecord(
            chunk_id=str(point.id),
            doc_id=str(payload.get("doc_id", "")),
            source=str(payload.get("source", "")),
            doc_type=str(payload.get("doc_type", "")),
            tags=list(payload.get("tags", [])),
            content=str(payload.get("content", "")),
            section_path=list(payload.get("section_path", [])),
            char_count=int(payload.get("char_count", 0)),
            prev_chunk=payload.get("prev_chunk"),
            next_chunk=payload.get("next_chunk"),
            dense=dense_vec,
            sparse=None,
        )

    def get_by_doc(self, doc_id: str) -> list[ChunkRecord]:
        """Retrieve all chunk records belonging to a single document ID for the current tenant."""
        from qdrant_client import models  # type: ignore

        client = self._client
        if not client.collection_exists(self.collection):
            return []

        doc_filter = models.Filter(
            must=[
                models.FieldCondition(key="tenant", match=models.MatchValue(value=self.tenant_key)),
                models.FieldCondition(key="doc_id", match=models.MatchValue(value=doc_id)),
            ]
        )

        all_points = []
        offset = None
        while True:
            scroll_res, offset = client.scroll(
                collection_name=self.collection,
                scroll_filter=doc_filter,
                with_payload=True,
                with_vectors=["dense"],
                limit=256,
                offset=offset,
            )
            all_points.extend(scroll_res)
            if offset is None:
                break

        return [self._to_record(p) for p in all_points]

    def hybrid_search(
        self, dense: np.ndarray, sparse: dict[int, float],
        *, limit: int, flt: TagFilter | None = None,
    ) -> list[ScoredChunk]:
        """Perform dense + sparse hybrid search with server-side RRF fusion."""
        from qdrant_client import models  # type: ignore

        client = self._client
        if not client.collection_exists(self.collection):
            return []

        qfilter = self._build_filter(flt)

        sparse_indices = list(sparse.keys())
        sparse_values = [float(v) for v in sparse.values()]
        sparse_vec = models.SparseVector(indices=sparse_indices, values=sparse_values)

        res = client.query_points(
            collection_name=self.collection,
            prefetch=[
                models.Prefetch(
                    query=dense.tolist(),
                    using="dense",
                    filter=qfilter,
                    limit=limit,
                ),
                models.Prefetch(
                    query=sparse_vec,
                    using="sparse",
                    filter=qfilter,
                    limit=limit,
                ),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=limit,
            with_payload=True,
        )

        scored_chunks = []
        for p in res.points:
            scored_chunks.append(
                ScoredChunk(
                    record=self._to_record(p),
                    fused_score=float(p.score),
                )
            )
        return scored_chunks

    def get_by_ids(self, chunk_ids: Sequence[str]) -> list[ChunkRecord]:
        """Retrieve chunks by their unique IDs."""
        if not chunk_ids:
            return []

        client = self._client
        if not client.collection_exists(self.collection):
            return []

        points = client.retrieve(
            collection_name=self.collection,
            ids=list(chunk_ids),
            with_payload=True,
        )

        records = []
        for p in points:
            payload = p.payload or {}
            if payload.get("tenant") == self.tenant_key:
                records.append(self._to_record(p))
        return records

    def all_vectors(self, flt: TagFilter | None = None) -> tuple[np.ndarray, list[ChunkRecord]]:
        """Retrieve all dense vectors as a (N, EMBEDDING_DIM) matrix along with their records."""
        client = self._client
        if not client.collection_exists(self.collection):
            return np.zeros((0, EMBEDDING_DIM), dtype=np.float32), []

        qfilter = self._build_filter(flt)
        all_points = []
        offset = None

        while True:
            scroll_res, offset = client.scroll(
                collection_name=self.collection,
                scroll_filter=qfilter,
                with_payload=True,
                with_vectors=["dense"],
                limit=256,
                offset=offset,
            )
            all_points.extend(scroll_res)
            if offset is None:
                break

        if not all_points:
            return np.zeros((0, EMBEDDING_DIM), dtype=np.float32), []

        records = [self._to_record(p) for p in all_points]
        vecs = np.vstack([r.dense for r in records]).astype(np.float32)
        return vecs, records

    def list_tags(self) -> list[str]:
        """List all unique tags present for the current tenant."""
        client = self._client
        if not client.collection_exists(self.collection):
            return []

        qfilter = self._build_filter()
        all_tags: set[str] = set()
        offset = None

        while True:
            scroll_res, offset = client.scroll(
                collection_name=self.collection,
                scroll_filter=qfilter,
                with_payload=["tags"],
                limit=256,
                offset=offset,
            )
            for p in scroll_res:
                payload = p.payload or {}
                for tag in payload.get("tags", []):
                    all_tags.add(str(tag))
            if offset is None:
                break

        return sorted(list(all_tags))

    def count(self) -> int:
        """Return the count of points for the current tenant in the collection."""
        from qdrant_client import models  # type: ignore

        client = self._client
        if not client.collection_exists(self.collection):
            return 0

        tenant_filter = models.Filter(
            must=[
                models.FieldCondition(key="tenant", match=models.MatchValue(value=self.tenant_key)),
            ]
        )
        res = client.count(collection_name=self.collection, count_filter=tenant_filter)
        return res.count

    def close(self) -> None:
        """Close the underlying Qdrant client connection if initialized."""
        if self._client_instance is not None:
            try:
                self._client_instance.close()
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("Error closing QdrantClient: %s", exc)
            finally:
                self._client_instance = None
