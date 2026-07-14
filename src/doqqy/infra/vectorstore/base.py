"""Vector store port - embed/query/map only interface with this contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

import numpy as np


@dataclass(frozen=True)
class ChunkRecord:
    """Backend-independent chunk record (LanceDB row / Qdrant point equivalent)."""

    chunk_id: str
    doc_id: str
    source: str
    doc_type: str
    tags: list[str]
    content: str
    section_path: list[str]
    char_count: int
    prev_chunk: str | None
    next_chunk: str | None
    dense: np.ndarray | None = None            # float32[1024]
    sparse: dict[int, float] | None = None     # bge-m3 lexical_weights: token_id -> weight


@dataclass(frozen=True)
class ScoredChunk:
    """Represents a matched chunk record with RRF/reranker scores."""

    record: ChunkRecord
    dense_rank: int | None = None
    sparse_rank: int | None = None
    fused_score: float = 0.0                   # Reciprocal Rank Fusion score


@dataclass(frozen=True)
class TagFilter:
    """Structured tag filter value object supporting exact match AND query semantics."""

    tags: tuple[str, ...] = ()                 # AND semantics


class VectorStore(Protocol):
    """VectorStore port interface definition."""

    def recreate(self, dim: int) -> None:
        """Drop the existing store table/collection and recreate it with correct dimensions."""
        ...

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        """Upsert a sequence of chunk records into the store. Returns the number of upserted records."""
        ...

    def delete_by_doc(self, doc_id: str) -> int:
        """Delete all chunks belonging to a document ID. Returns the number of deleted records."""
        ...

    def hybrid_search(
        self, dense: np.ndarray, sparse: dict[int, float],
        *, limit: int, flt: TagFilter | None = None,
    ) -> list[ScoredChunk]:
        """Perform dense + sparse hybrid search with RRF fusion.

        Returns a single fused list up to limit.
        """
        ...

    def get_by_ids(self, chunk_ids: Sequence[str]) -> list[ChunkRecord]:
        """Retrieve chunks by their unique IDs."""
        ...

    def all_vectors(self, flt: TagFilter | None = None) -> tuple[np.ndarray, list[ChunkRecord]]:
        """Retrieve all dense vectors as a (N, 1024) matrix along with their records."""
        ...

    def list_tags(self) -> list[str]:
        """List all unique tags present in the workspace."""
        ...

    def count(self) -> int:
        """Count the total number of chunks in the store."""
        ...

    def close(self) -> None:
        """Release database connections or handles."""
        ...
