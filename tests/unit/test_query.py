"""Unit tests for context expansion (expand_context) in query.py."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore
from doqqy.query import SearchHit, expand_context


def _record(chunk_id: str, prev_chunk: str | None, next_chunk: str | None) -> ChunkRecord:
    return ChunkRecord(
        chunk_id=chunk_id,
        doc_id="doc-1",
        source="file1.md",
        doc_type="markdown",
        tags=["python"],
        content=f"content-{chunk_id}",
        section_path=["Root"],
        char_count=10,
        prev_chunk=prev_chunk,
        next_chunk=next_chunk,
        dense=np.ones(8, dtype=np.float32),
        sparse={1: 1.0},
    )


@pytest.fixture
def chained_store(tmp_path: Path):
    """A 5-chunk chain A -> B -> C -> D -> E within a single document."""
    store = LanceDBStore(tmp_path / "store.lance")
    store.recreate(dim=8)
    store.upsert([
        _record("A", None, "B"),
        _record("B", "A", "C"),
        _record("C", "B", "D"),
        _record("D", "C", "E"),
        _record("E", "D", None),
    ])
    yield store
    store.close()


def _hit_for(chunk_id: str, prev_chunk: str | None, next_chunk: str | None) -> SearchHit:
    return SearchHit(
        score=1.0,
        doc_id="doc-1",
        source="file1.md",
        section_path=["Root"],
        content=f"content-{chunk_id}",
        extra={"chunk_id": chunk_id, "prev_chunk": prev_chunk, "next_chunk": next_chunk},
    )


def test_expand_context_mid_document_returns_prev_and_next(chained_store):
    hit = _hit_for("C", prev_chunk="B", next_chunk="D")

    result = expand_context(chained_store, hit, n=1)

    assert result.before == ["content-B"]
    assert result.hit == "content-C"
    assert result.after == ["content-D"]
    assert str(result) == "content-B\n\n— · —\n\ncontent-C\n\n— · —\n\ncontent-D"


def test_expand_context_walks_multiple_steps_in_document_order(chained_store):
    hit = _hit_for("C", prev_chunk="B", next_chunk="D")

    result = expand_context(chained_store, hit, n=2)

    # Oldest-first on the "before" side, chronological on the "after" side.
    assert result.before == ["content-A", "content-B"]
    assert result.after == ["content-D", "content-E"]


def test_expand_context_stops_at_document_start(chained_store):
    hit = _hit_for("A", prev_chunk=None, next_chunk="B")

    result = expand_context(chained_store, hit, n=2)

    assert result.before == []
    assert result.after == ["content-B", "content-C"]


def test_expand_context_stops_at_document_end(chained_store):
    hit = _hit_for("E", prev_chunk="D", next_chunk=None)

    result = expand_context(chained_store, hit, n=2)

    assert result.before == ["content-C", "content-D"]
    assert result.after == []


def test_expand_context_n_zero_is_noop(chained_store):
    hit = _hit_for("C", prev_chunk="B", next_chunk="D")

    result = expand_context(chained_store, hit, n=0)

    assert result.before == []
    assert result.after == []
    assert result.hit == "content-C"
