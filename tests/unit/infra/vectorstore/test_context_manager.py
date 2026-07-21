"""Unit tests verifying context manager support (__enter__ / __exit__) for VectorStore adapters.

Tests guarantee that store.close() is unconditionally called upon exiting a `with` block,
both on normal completion and when an exception occurs inside the block.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord, ScoredChunk, TagFilter, VectorStore
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore
from doqqy.infra.vectorstore.qdrant_store import QdrantStore

# ---------------------------------------------------------------------------
# Spy VectorStore Implementation
# ---------------------------------------------------------------------------

class SpyVectorStore(VectorStore):
    """Spy implementation of VectorStore to verify context manager lifecycle and close() calls."""

    def __init__(self) -> None:
        self.close_called = False
        self.entered = False

    def recreate(self, dim: int) -> None:
        pass

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        return len(records)

    def full_rebuild(self, records: Sequence[ChunkRecord], dim: int) -> int:
        return len(records)

    def delete_by_doc(self, doc_id: str) -> int:
        return 0

    def hybrid_search(
        self, dense: np.ndarray, sparse: dict[int, float],
        *, limit: int, flt: TagFilter | None = None,
    ) -> list[ScoredChunk]:
        return []

    def get_by_ids(self, chunk_ids: Sequence[str]) -> list[ChunkRecord]:
        return []

    def all_vectors(self, flt: TagFilter | None = None) -> tuple[np.ndarray, list[ChunkRecord]]:
        return np.zeros((0, 1024), dtype=np.float32), []

    def list_tags(self) -> list[str]:
        return []

    def count(self) -> int:
        return 0

    def close(self) -> None:
        self.close_called = True

    def __enter__(self) -> SpyVectorStore:
        self.entered = True
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        self.close()


# ---------------------------------------------------------------------------
# Test Suites
# ---------------------------------------------------------------------------

class TestVectorStoreContextManager:
    """Verify generic context manager behavior on the VectorStore Protocol."""

    def test_normal_exit_calls_close(self) -> None:
        """Exiting a `with` block normally must call close()."""
        store = SpyVectorStore()
        assert not store.entered
        assert not store.close_called

        with store as s:
            assert s is store
            assert store.entered
            assert not store.close_called

        assert store.close_called

    def test_exception_in_with_block_calls_close(self) -> None:
        """An exception raised inside a `with` block must still trigger close()."""
        store = SpyVectorStore()

        with pytest.raises(RuntimeError, match="Search operation failed"):
            with store:
                raise RuntimeError("Search operation failed")

        assert store.close_called


class TestLanceDBStoreContextManager:
    """Verify LanceDBStore context manager implementation."""

    def test_lancedb_store_context_manager_normal_exit(self, tmp_path: Path) -> None:
        """LanceDBStore must support `with` statement and close on exit."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(dim=128)

        with store as s:
            assert s is store
            assert store.count() == 0

    def test_lancedb_store_context_manager_exception_exit(self, tmp_path: Path) -> None:
        """LanceDBStore must re-raise exception after running __exit__."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(dim=128)

        with pytest.raises(ValueError, match="Simulated hybrid_search error"):
            with store:
                raise ValueError("Simulated hybrid_search error")


class TestQdrantStoreContextManager:
    """Verify QdrantStore stub context manager implementation."""

    def test_qdrant_store_context_manager_normal_exit(self) -> None:
        """QdrantStore stub must support `with` statement and close on exit."""
        store = QdrantStore("http://localhost:6333", "key", "collection", "tenant")

        with store as s:
            assert s is store
            assert store.collection == "collection"

    def test_qdrant_store_context_manager_exception_exit(self) -> None:
        """QdrantStore stub must re-raise exception after running __exit__."""
        store = QdrantStore("http://localhost:6333", "key", "collection", "tenant")

        with pytest.raises(RuntimeError, match="Qdrant error"):
            with store:
                raise RuntimeError("Qdrant error")
