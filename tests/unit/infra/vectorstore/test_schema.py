"""Tests for Issue #33: explicit pyarrow schema and atomic full_rebuild().

Three scenarios:
1. Schema round-trip: recreate + upsert preserves types and nullable fields.
2. Interrupted rebuild: calling recreate only leaves a detectably empty store;
   a subsequent full_rebuild recovers correctly.
3. Atomic overwrite: full_rebuild replaces old data in a single operation.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore, _LANCE_SCHEMA_BASE, _build_schema


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DIM = 128


def _make_record(
    chunk_id: str = "c1",
    doc_id: str = "doc-1",
    tags: list[str] | None = None,
    prev_chunk: str | None = None,
    next_chunk: str | None = None,
    content: str = "hello world",
) -> ChunkRecord:
    return ChunkRecord(
        chunk_id=chunk_id,
        doc_id=doc_id,
        source="test.md",
        doc_type="markdown",
        tags=tags if tags is not None else [],
        content=content,
        section_path=["Root", "Section"],
        char_count=len(content),
        prev_chunk=prev_chunk,
        next_chunk=next_chunk,
        dense=np.ones(DIM, dtype=np.float32) * 0.5,
        sparse={101: 1.0, 202: 0.5},
    )


# ---------------------------------------------------------------------------
# Test 1: Schema round-trip
# ---------------------------------------------------------------------------

class TestSchemaRoundTrip:
    """recreate() + upsert() must preserve field types and nullability."""

    def test_nullable_prev_next_chunk_roundtrip(self, tmp_path: Path):
        """prev_chunk=None and next_chunk=None must survive a store round-trip as None."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(DIM)

        rec = _make_record(chunk_id="c-none-links", prev_chunk=None, next_chunk=None)
        store.upsert([rec])

        fetched = store.get_by_ids(["c-none-links"])
        assert len(fetched) == 1
        assert fetched[0].prev_chunk is None
        assert fetched[0].next_chunk is None

    def test_empty_tags_roundtrip(self, tmp_path: Path):
        """A record with tags=[] must come back with an empty tags list."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(DIM)

        rec = _make_record(chunk_id="c-no-tags", tags=[])
        store.upsert([rec])

        fetched = store.get_by_ids(["c-no-tags"])
        assert len(fetched) == 1
        assert list(fetched[0].tags) == []

    def test_doc_type_is_string(self, tmp_path: Path):
        """doc_type column must be stored and retrieved as a plain string."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(DIM)

        rec = _make_record(chunk_id="c-doctype")
        store.upsert([rec])

        fetched = store.get_by_ids(["c-doctype"])
        assert isinstance(fetched[0].doc_type, str)
        assert fetched[0].doc_type == "markdown"

    def test_char_count_is_integer(self, tmp_path: Path):
        """char_count must come back as a Python int (int64 in schema)."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(DIM)

        rec = _make_record(chunk_id="c-charcount", content="exactly 14 chars")
        store.upsert([rec])

        fetched = store.get_by_ids(["c-charcount"])
        assert isinstance(fetched[0].char_count, int)


# ---------------------------------------------------------------------------
# Test 2: Interrupted rebuild detection
# ---------------------------------------------------------------------------

class TestInterruptedRebuild:
    """recreate() alone must leave a detectably empty, non-crashing store."""

    def test_recreate_only_leaves_empty_store(self, tmp_path: Path):
        """After recreate() without upsert, count() must return 0."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(DIM)
        assert store.count() == 0

    def test_hybrid_search_on_empty_store_returns_empty_list(self, tmp_path: Path):
        """hybrid_search on a just-recreated (empty) store must return [] not raise."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(DIM)

        results = store.hybrid_search(
            dense=np.ones(DIM, dtype=np.float32),
            sparse={101: 1.0},
            limit=5,
        )
        assert results == []

    def test_full_rebuild_recovers_after_interrupted_recreate(self, tmp_path: Path):
        """full_rebuild must succeed and make the store searchable after an interrupted recreate."""
        store = LanceDBStore(tmp_path / "store.lance")

        # Simulate interrupted rebuild: recreate without upsert
        store.recreate(DIM)
        assert store.count() == 0

        # Recovery via full_rebuild
        records = [_make_record("c-recovery")]
        n = store.full_rebuild(records, dim=DIM)

        assert n == 1
        assert store.count() == 1
        fetched = store.get_by_ids(["c-recovery"])
        assert len(fetched) == 1


# ---------------------------------------------------------------------------
# Test 3: full_rebuild atomicity / overwrite semantics
# ---------------------------------------------------------------------------

class TestFullRebuildAtomicity:
    """full_rebuild must atomically replace the entire store contents."""

    def test_full_rebuild_replaces_old_records(self, tmp_path: Path):
        """Old records must be gone after full_rebuild; only new ones remain."""
        store = LanceDBStore(tmp_path / "store.lance")
        store.recreate(DIM)
        store.upsert([_make_record("old-1"), _make_record("old-2")])
        assert store.count() == 2

        new_records = [_make_record("new-1"), _make_record("new-2"), _make_record("new-3")]
        n = store.full_rebuild(new_records, dim=DIM)

        assert n == 3
        assert store.count() == 3
        # Old records must not exist
        assert store.get_by_ids(["old-1"]) == []
        assert store.get_by_ids(["old-2"]) == []

    def test_full_rebuild_on_fresh_store(self, tmp_path: Path):
        """full_rebuild must work even when no table exists yet."""
        store = LanceDBStore(tmp_path / "store.lance")

        records = [_make_record("fresh-1"), _make_record("fresh-2")]
        n = store.full_rebuild(records, dim=DIM)

        assert n == 2
        assert store.count() == 2

    def test_full_rebuild_preserves_nullable_fields(self, tmp_path: Path):
        """full_rebuild must honour nullable prev_chunk / next_chunk just like upsert."""
        store = LanceDBStore(tmp_path / "store.lance")

        rec = _make_record("c-nullable", prev_chunk=None, next_chunk="c-next", tags=[])
        store.full_rebuild([rec], dim=DIM)

        fetched = store.get_by_ids(["c-nullable"])
        assert fetched[0].prev_chunk is None
        assert fetched[0].next_chunk == "c-next"
        assert list(fetched[0].tags) == []

    def test_full_rebuild_returns_record_count(self, tmp_path: Path):
        """full_rebuild must return the exact number of records written."""
        store = LanceDBStore(tmp_path / "store.lance")
        records = [_make_record(f"c-{i}") for i in range(7)]
        n = store.full_rebuild(records, dim=DIM)
        assert n == 7


# ---------------------------------------------------------------------------
# Test 4: _LANCE_SCHEMA_BASE and _build_schema
# ---------------------------------------------------------------------------

class TestSchema:
    """Verify the pyarrow schema constant and the dim-override helper."""

    def test_schema_base_has_expected_fields(self):
        """_LANCE_SCHEMA_BASE must contain all required column names."""
        field_names = {f.name for f in _LANCE_SCHEMA_BASE}
        expected = {
            "chunk_id", "doc_id", "source", "doc_type",
            "tags", "section_path", "char_count",
            "prev_chunk", "next_chunk", "content",
            "vector", "sparse_vector", "section_path_str", "tags_str",
        }
        assert expected == field_names

    def test_prev_next_chunk_are_nullable(self):
        """prev_chunk and next_chunk must be nullable=True in the base schema."""
        schema = _LANCE_SCHEMA_BASE
        assert schema.field("prev_chunk").nullable is True
        assert schema.field("next_chunk").nullable is True

    def test_chunk_id_is_not_nullable(self):
        """chunk_id must be nullable=False (primary key equivalent)."""
        assert _LANCE_SCHEMA_BASE.field("chunk_id").nullable is False

    def test_build_schema_overrides_vector_dim(self):
        """_build_schema(dim) must produce a fixed-size list field for vector."""
        import pyarrow as pa
        schema = _build_schema(256)
        vector_field = schema.field("vector")
        assert isinstance(vector_field.type, pa.FixedSizeListType)
        assert vector_field.type.list_size == 256

    def test_build_schema_preserves_other_fields(self):
        """Fields other than vector must be unchanged by _build_schema."""
        schema = _build_schema(512)
        assert schema.field("chunk_id").type == _LANCE_SCHEMA_BASE.field("chunk_id").type
        assert schema.field("char_count").type == _LANCE_SCHEMA_BASE.field("char_count").type
