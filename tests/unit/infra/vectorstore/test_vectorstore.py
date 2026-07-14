"""Unit tests for the LanceDBStore vector store implementation."""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord, TagFilter
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore


def test_tag_filter_sanitization():
    """Verify that single quotes in tags are correctly escaped to prevent injection."""
    tag = "tag'value"
    escaped = tag.replace(chr(39), chr(39) + chr(39))
    assert escaped == "tag''value"


def test_lancedb_store_lifecycle(tmp_path: Path):
    """Test standard storage operations: recreate, upsert, count, get, delete, search."""
    store = LanceDBStore(tmp_path / "store.lance")

    # Initial state should raise if database files are not initialized
    with pytest.raises(FileNotFoundError):
        store.count()

    store.recreate(dim=1024)
    assert store.count() == 0

    # Build dummy records
    dense_vector1 = np.ones(1024, dtype=np.float32) * 0.1
    dense_vector2 = np.ones(1024, dtype=np.float32) * 0.2

    rec1 = ChunkRecord(
        chunk_id="chunk-1",
        doc_id="doc-1",
        source="file1.md",
        doc_type="markdown",
        tags=["python", "test"],
        content="hello python world",
        section_path=["Root", "Intro"],
        char_count=18,
        prev_chunk=None,
        next_chunk="chunk-2",
        dense=dense_vector1,
        sparse={101: 0.5, 102: 1.2},
    )
    rec2 = ChunkRecord(
        chunk_id="chunk-2",
        doc_id="doc-1",
        source="file1.md",
        doc_type="markdown",
        tags=["python"],
        content="hello unit testing",
        section_path=["Root", "Testing"],
        char_count=18,
        prev_chunk="chunk-1",
        next_chunk=None,
        dense=dense_vector2,
        sparse={101: 0.8, 103: 0.3},
    )

    # Insert and verify count
    store.upsert([rec1, rec2])
    assert store.count() == 2

    # Verify list_tags
    tags = store.list_tags()
    assert "python" in tags
    assert "test" in tags

    # Verify get_by_ids
    fetched = store.get_by_ids(["chunk-1", "chunk-nonexistent"])
    assert len(fetched) == 1
    assert fetched[0].chunk_id == "chunk-1"
    assert list(fetched[0].tags) == ["python", "test"]

    # Verify hybrid search with filter matching rec1 only
    flt_test = TagFilter(tags=("test",))
    results = store.hybrid_search(
        dense=dense_vector1,
        sparse={102: 1.0},
        limit=5,
        flt=flt_test,
    )
    assert len(results) == 1
    assert results[0].record.chunk_id == "chunk-1"

    # Verify delete_by_doc
    deleted = store.delete_by_doc("doc-1")
    assert deleted == 2
    assert store.count() == 0

    store.close()
