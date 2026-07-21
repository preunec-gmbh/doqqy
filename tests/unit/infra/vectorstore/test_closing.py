"""Unit tests verifying contextlib.closing usage for VectorStore adapters.

Guarantees that store.close() is unconditionally invoked upon exiting a `with contextlib.closing(store)` block,
both on normal completion and when an exception occurs inside the block.
"""

from __future__ import annotations

import contextlib
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
    """Spy implementation of VectorStore to verify contextlib.closing lifecycle."""

    def __init__(self) -> None:
        self.close_called = False

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


# ---------------------------------------------------------------------------
# Test Suites
# ---------------------------------------------------------------------------

class TestClosingVectorStore:
    """Verify contextlib.closing behavior on VectorStore implementations."""

    def test_spy_store_normal_exit_calls_close(self) -> None:
        """Exiting a contextlib.closing block normally must call close()."""
        store = SpyVectorStore()
        assert not store.close_called

        with contextlib.closing(store) as s:
            assert s is store
            assert not store.close_called

        assert store.close_called

    def test_spy_store_exception_exit_calls_close(self) -> None:
        """An exception raised inside contextlib.closing must still trigger close()."""
        store = SpyVectorStore()

        with pytest.raises(RuntimeError, match="Operation failed"):
            with contextlib.closing(store):
                raise RuntimeError("Operation failed")

        assert store.close_called

    def test_lancedb_store_closing_normal_exit(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """LanceDBStore wrapped in contextlib.closing must call close() on normal exit."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(dim=128)

        calls = []
        monkeypatch.setattr(store, "close", lambda: calls.append(1))

        with contextlib.closing(store) as s:
            assert s.count() == 0

        assert calls == [1]

    def test_lancedb_store_closing_exception_exit(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """LanceDBStore wrapped in contextlib.closing must call close() and propagate exceptions."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(dim=128)

        calls = []
        monkeypatch.setattr(store, "close", lambda: calls.append(1))

        with pytest.raises(ValueError, match="Database query error"):
            with contextlib.closing(store):
                raise ValueError("Database query error")

        assert calls == [1]

    def test_qdrant_store_closing_normal_exit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """QdrantStore stub wrapped in contextlib.closing must call close() on normal exit."""
        store = QdrantStore("http://localhost:6333", "key", "collection", "tenant")

        calls = []
        monkeypatch.setattr(store, "close", lambda: calls.append(1))

        with contextlib.closing(store) as s:
            assert s.collection == "collection"

        assert calls == [1]

    def test_qdrant_store_closing_exception_exit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """QdrantStore stub wrapped in contextlib.closing must call close() and propagate exceptions."""
        store = QdrantStore("http://localhost:6333", "key", "collection", "tenant")

        calls = []
        monkeypatch.setattr(store, "close", lambda: calls.append(1))

        with pytest.raises(RuntimeError, match="Network timeout"):
            with contextlib.closing(store):
                raise RuntimeError("Network timeout")

        assert calls == [1]
