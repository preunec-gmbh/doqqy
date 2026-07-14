"""Unit tests for the LanceDBStore vector store implementation."""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord, TagFilter
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore


def test_tag_filter_exact_match_and_escaping(tmp_path: Path):
    """Verify that TagFilter exact matching behaves correctly and escapes single quotes safely."""
    store = LanceDBStore(tmp_path / "store.lance")
    store.recreate(dim=128)

    rec_exact = ChunkRecord(
        chunk_id="chunk-exact",
        doc_id="doc-1",
        source="doc1.md",
        doc_type="markdown",
        tags=["bulut"],
        content="exact tag match",
        section_path=["Root"],
        char_count=15,
        prev_chunk=None,
        next_chunk=None,
        dense=np.ones(128, dtype=np.float32) * 0.1,
        sparse={101: 1.0},
    )
    rec_partial = ChunkRecord(
        chunk_id="chunk-partial",
        doc_id="doc-1",
        source="doc1.md",
        doc_type="markdown",
        tags=["bulut-saha"],
        content="partial tag match",
        section_path=["Root"],
        char_count=17,
        prev_chunk=None,
        next_chunk=None,
        dense=np.ones(128, dtype=np.float32) * 0.2,
        sparse={101: 1.0},
    )
    rec_quote = ChunkRecord(
        chunk_id="chunk-quote",
        doc_id="doc-1",
        source="doc1.md",
        doc_type="markdown",
        tags=["bulut'lar"],
        content="quote in tag match",
        section_path=["Root"],
        char_count=18,
        prev_chunk=None,
        next_chunk=None,
        dense=np.ones(128, dtype=np.float32) * 0.3,
        sparse={101: 1.0},
    )

    store.upsert([rec_exact, rec_partial, rec_quote])

    # 1. Search with "bulut" filter: must match rec_exact, but NOT rec_partial
    flt_exact = TagFilter(tags=("bulut",))
    res_exact = store.hybrid_search(
        dense=np.ones(128, dtype=np.float32) * 0.1,
        sparse={101: 1.0},
        limit=5,
        flt=flt_exact,
    )
    assert len(res_exact) == 1
    assert res_exact[0].record.chunk_id == "chunk-exact"

    # 2. Search with "bulut'lar" filter containing a single quote: must match rec_quote safely
    flt_quote = TagFilter(tags=("bulut'lar",))
    res_quote = store.hybrid_search(
        dense=np.ones(128, dtype=np.float32) * 0.1,
        sparse={101: 1.0},
        limit=5,
        flt=flt_quote,
    )
    assert len(res_quote) == 1
    assert res_quote[0].record.chunk_id == "chunk-quote"

    store.close()


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
