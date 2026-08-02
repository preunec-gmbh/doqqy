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
        raise NotImplementedError("QdrantStore phase 2 implementation pending.")

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        raise NotImplementedError("QdrantStore phase 2 implementation pending.")

    def full_rebuild(self, records: Sequence[ChunkRecord], dim: int) -> int:
        raise NotImplementedError("QdrantStore phase 2 implementation pending.")

    def delete_by_doc(self, doc_id: str) -> int:
        raise NotImplementedError("QdrantStore phase 2 implementation pending.")

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
        raise NotImplementedError("QdrantStore phase 2 implementation pending.")

    def close(self) -> None:
        """Close the underlying Qdrant client connection if initialized."""
        if self._client_instance is not None:
            try:
                self._client_instance.close()
            except Exception as exc:  # noqa: BLE001
                _LOG.warning("Error closing QdrantClient: %s", exc)
            finally:
                self._client_instance = None
