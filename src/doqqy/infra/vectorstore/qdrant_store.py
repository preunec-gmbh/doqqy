"""Qdrant implementation of the VectorStore port."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from doqqy.config import get_logger
from doqqy.infra.vectorstore.base import ChunkRecord, ScoredChunk, TagFilter, VectorStore

_LOG = get_logger("doqqy.infra.vectorstore.qdrant")


class QdrantStore(VectorStore):
    """Adapter implementing server-side vector search using Qdrant."""

    def __init__(self, url: str, api_key: str, collection: str, tenant_key: str) -> None:
        self.url = url
        self.api_key = api_key
        self.collection = collection
        self.tenant_key = tenant_key
        self._client_instance = None

    @property
    def _client(self):
        if self._client_instance is None:
            try:
                from qdrant_client import QdrantClient  # type: ignore
            except ImportError as exc:
                raise ImportError(
                    "qdrant-client is required for the Qdrant backend. "
                    "Install it via `pip install doqqy[qdrant]`."
                ) from exc
            self._client_instance = QdrantClient(url=self.url, api_key=self.api_key or None)
        return self._client_instance

    def ensure_collection(self, dim: int) -> None:
        """Ensure the target collection and payload indices exist in Qdrant."""
        from qdrant_client import models  # type: ignore

        client = self._client
        if client.collection_exists(self.collection):
            return

        _LOG.info("Creating Qdrant collection: %s (dim=%d)", self.collection, dim)
        client.create_collection(
            collection_name=self.collection,
            vectors_config={
                "dense": models.VectorParams(size=dim, distance=models.Distance.COSINE),
            },
            sparse_vectors_config={
                "sparse": models.SparseVectorParams(
                    index=models.SparseIndexParams(on_disk=False),
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
        _LOG.info("Qdrant collection %s created with payload indexes.", self.collection)

    def recreate(self, dim: int) -> None:
        """Drop the collection if it exists and recreate it with the given dimension."""
        client = self._client
        if client.collection_exists(self.collection):
            _LOG.info("Dropping Qdrant collection %s for recreate.", self.collection)
            client.delete_collection(self.collection)
        self.ensure_collection(dim)

    @staticmethod
    def _infer_dim(records: Sequence[ChunkRecord]) -> int:
        """Infer vector dimension from the first non-null dense vector in records."""
        for rec in records:
            if rec.dense is not None:
                return int(np.asarray(rec.dense).shape[-1])
        raise ValueError("Cannot infer dimension: no record contains a dense vector.")

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        """Upsert a sequence of ChunkRecords as Qdrant Points."""
        if not records:
            return 0

        from qdrant_client import models  # type: ignore

        dim = self._infer_dim(records)
        self.ensure_collection(dim)

        points = []
        for rec in records:
            dense_vec = rec.dense.tolist() if rec.dense is not None else []
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

        self._client.upsert(collection_name=self.collection, points=points)
        _LOG.debug("Upserted %d points to Qdrant collection %s", len(points), self.collection)
        return len(points)

    def full_rebuild(self, records: Sequence[ChunkRecord], dim: int) -> int:
        """Atomically recreate collection and upsert all records."""
        self.recreate(dim)
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

    def hybrid_search(
        self, dense: np.ndarray, sparse: dict[int, float],
        *, limit: int, flt: TagFilter | None = None,
    ) -> list[ScoredChunk]:
        raise NotImplementedError("QdrantStore phase 3 implementation pending.")

    def get_by_ids(self, chunk_ids: Sequence[str]) -> list[ChunkRecord]:
        raise NotImplementedError("QdrantStore phase 3 implementation pending.")

    def all_vectors(self, flt: TagFilter | None = None) -> tuple[np.ndarray, list[ChunkRecord]]:
        raise NotImplementedError("QdrantStore phase 3 implementation pending.")

    def list_tags(self) -> list[str]:
        raise NotImplementedError("QdrantStore phase 3 implementation pending.")

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
