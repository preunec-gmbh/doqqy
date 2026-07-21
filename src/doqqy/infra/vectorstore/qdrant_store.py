"""Qdrant adapter stub for Phase 1.5."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from doqqy.infra.vectorstore.base import ChunkRecord, ScoredChunk, TagFilter, VectorStore


class QdrantStore(VectorStore):
    """Placeholder adapter for Qdrant server-side vector store (Phase 1.5)."""

    def __init__(self, url: str, api_key: str, collection: str, tenant_key: str) -> None:
        self.url = url
        self.api_key = api_key
        self.collection = collection
        self.tenant_key = tenant_key

    def recreate(self, dim: int) -> None:
        raise NotImplementedError("QdrantStore is not implemented yet (Phase 1.5).")

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        raise NotImplementedError("QdrantStore is not implemented yet (Phase 1.5).")

    def delete_by_doc(self, doc_id: str) -> int:
        raise NotImplementedError("QdrantStore is not implemented yet (Phase 1.5).")

    def hybrid_search(
        self, dense: np.ndarray, sparse: dict[int, float],
        *, limit: int, flt: TagFilter | None = None,
    ) -> list[ScoredChunk]:
        raise NotImplementedError("QdrantStore is not implemented yet (Phase 1.5).")

    def get_by_ids(self, chunk_ids: Sequence[str]) -> list[ChunkRecord]:
        raise NotImplementedError("QdrantStore is not implemented yet (Phase 1.5).")

    def all_vectors(self, flt: TagFilter | None = None) -> tuple[np.ndarray, list[ChunkRecord]]:
        raise NotImplementedError("QdrantStore is not implemented yet (Phase 1.5).")

    def list_tags(self) -> list[str]:
        raise NotImplementedError("QdrantStore is not implemented yet (Phase 1.5).")

    def count(self) -> int:
        raise NotImplementedError("QdrantStore is not implemented yet (Phase 1.5).")

    def close(self) -> None:
        pass
