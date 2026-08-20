"""Unit tests for the LanceDBStore vector store implementation."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord, TagFilter
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore


def test_tag_filter_exact_match_and_escaping(tmp_path: Path):
    """Verify TagFilter exact matching and that invalid tags (e.g. with quotes) are rejected.

    Design note: TagFilter.__post_init__ validates all tags against TAG_PATTERN, so
    a tag containing a single quote (SQL injection risk) is rejected before it can
    ever reach a LanceDB where() clause.
    """
    from doqqy.infra.vectorstore.base import InvalidTagError

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

    store.upsert([rec_exact, rec_partial])

    # 1. Exact match: "bulut" must match rec_exact only, NOT "bulut-saha"
    flt_exact = TagFilter(tags=("bulut",))
    res_exact = store.hybrid_search(
        dense=np.ones(128, dtype=np.float32) * 0.1,
        sparse={101: 1.0},
        limit=5,
        flt=flt_exact,
    )
    assert len(res_exact) == 1
    assert res_exact[0].record.chunk_id == "chunk-exact"

    # 2. Tags containing a single quote are rejected at TagFilter construction —
    #    the SQL injection path (where() clause) is never reached.
    with pytest.raises(InvalidTagError, match="Tag format must match"):
        TagFilter(tags=("bulut'lar",))

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


def test_lancedb_iter_records_lossless_roundtrip(tmp_path: Path):
    """Verify LanceDBStore.iter_records yields all records losslessly in configured batches."""
    store = LanceDBStore(tmp_path / "store.lance")
    store.recreate(dim=4)

    # 1. Edge case: Empty store yields 0 records
    empty_records = list(store.iter_records(batch_size=2))
    assert len(empty_records) == 0

    # Build 5 distinct records
    records = []
    for i in range(5):
        records.append(
            ChunkRecord(
                chunk_id=f"chunk-{i}",
                doc_id=f"doc-{i % 2}",
                source=f"raw/doc{i % 2}.md",
                doc_type="markdown",
                tags=[f"tag-{i}", "common"],
                content=f"Sample content for chunk {i}",
                section_path=["Root", f"Section-{i}"],
                char_count=25 + i,
                prev_chunk=f"chunk-{i-1}" if i > 0 else None,
                next_chunk=f"chunk-{i+1}" if i < 4 else None,
                dense=np.asarray([0.1 * (i + 1), 0.2, 0.3, 0.4], dtype=np.float32),
                sparse={100 + i: 0.5 * (i + 1)},
            )
        )

    store.full_rebuild(records, dim=4)

    # 2. Batched streaming: batch_size=2 for 5 records -> 3 batches of lengths [2, 2, 1]
    batches = list(store.iter_records(batch_size=2))
    assert len(batches) == 3
    assert [len(b) for b in batches] == [2, 2, 1]

    all_yielded = [rec for batch in batches for rec in batch]
    assert len(all_yielded) == 5

    # Lossless verification for every field
    by_id = {r.chunk_id: r for r in all_yielded}
    for orig in records:
        yielded = by_id[orig.chunk_id]
        assert yielded.chunk_id == orig.chunk_id
        assert yielded.doc_id == orig.doc_id
        assert yielded.source == orig.source
        assert yielded.doc_type == orig.doc_type
        assert list(yielded.tags) == list(orig.tags)
        assert yielded.content == orig.content
        assert list(yielded.section_path) == list(orig.section_path)
        assert yielded.char_count == orig.char_count
        assert yielded.prev_chunk == orig.prev_chunk
        assert yielded.next_chunk == orig.next_chunk
        assert np.array_equal(yielded.dense, orig.dense)
        assert yielded.sparse == orig.sparse

    # 3. Edge case: batch_size larger than store count (e.g. batch_size=100 for 5 records)
    large_batch = list(store.iter_records(batch_size=100))
    assert len(large_batch) == 1
    assert len(large_batch[0]) == 5

    store.close()
