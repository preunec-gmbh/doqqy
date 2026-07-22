"""Klasör yapısı → tag türetimi testleri — bkz. docs/DEVELOPER-HANDOVER.md §5."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pytest

from doqqy.cli import tags as cli_tags
from doqqy.infra.vectorstore.base import ChunkRecord, ScoredChunk, TagFilter
from doqqy.ingest.base import base_metadata
from doqqy.workspace import Workspace


def test_folder_structure_becomes_tags(tmp_path):
    meta = base_metadata(Path("raw/erp12/billing/api.md"), tmp_path, kind="md")
    assert meta["tags"] == ["erp12", "billing"]


def test_root_file_has_no_tags(tmp_path):
    meta = base_metadata(Path("raw/readme.md"), tmp_path, kind="md")
    assert meta["tags"] == []


def test_folder_with_space_is_sanitized_and_queryable(tmp_path):
    """raw/a b/x.md -> tag 'a-b', which round-trips against --tag (issue #38)."""
    from doqqy.infra.vectorstore.base import TagFilter

    meta = base_metadata(Path("raw/a b/x.md"), tmp_path, kind="md")
    assert meta["tags"] == ["a-b"]
    # Must not raise InvalidTagError — the produced tag is filterable.
    TagFilter(tags=tuple(meta["tags"]))


def test_turkish_folder_name_unchanged(tmp_path):
    """Turkish letters already conform to TAG_PATTERN (\\w covers them)."""
    meta = base_metadata(Path("raw/türkçe/x.md"), tmp_path, kind="md")
    assert meta["tags"] == ["türkçe"]


def test_symbol_only_folder_name_dropped(tmp_path):
    """A folder name with no conforming characters left produces no tag."""
    meta = base_metadata(Path("raw/!!!/x.md"), tmp_path, kind="md")
    assert meta["tags"] == []


def test_sanitization_is_idempotent_across_reingest(tmp_path):
    """Re-running ingest on already-sanitized output is stable."""
    first = base_metadata(Path("raw/a b/x.md"), tmp_path, kind="md")
    reingested_source = Path("raw") / first["tags"][0] / "x.md"
    second = base_metadata(reingested_source, tmp_path, kind="md")
    assert second["tags"] == first["tags"]


# ---------------------------------------------------------------------------
# `doqqy tags` CLI — flags legacy stored tags that don't match TAG_PATTERN
# ---------------------------------------------------------------------------

class _StubVectorStore:
    """Minimal duck-typed VectorStore whose list_tags() returns canned tags."""

    def __init__(self, stored_tags: list[str]) -> None:
        self._stored_tags = stored_tags

    def recreate(self, dim: int) -> None:
        pass

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        return len(records)

    def full_rebuild(self, records: Sequence[ChunkRecord], dim: int) -> int:
        return len(records)

    def delete_by_doc(self, doc_id: str) -> int:
        return 0

    def hybrid_search(self, dense, sparse, *, limit: int, flt: TagFilter | None = None) -> list[ScoredChunk]:
        return []

    def get_by_ids(self, chunk_ids: Sequence[str]) -> list[ChunkRecord]:
        return []

    def all_vectors(self, flt: TagFilter | None = None):
        return np.zeros((0, 1024), dtype=np.float32), []

    def list_tags(self) -> list[str]:
        return self._stored_tags

    def count(self) -> int:
        return 0

    def close(self) -> None:
        pass


def test_cli_tags_flags_legacy_non_conforming_tags(tmp_path, monkeypatch, capsys):
    """Stored tags that predate sanitization (e.g. embedded before this fix) must be
    flagged as unfilterable, while conforming tags still get a --tag usage example."""
    ws = Workspace(tmp_path)
    stub = _StubVectorStore(["erp12", "a b"])

    monkeypatch.setattr("doqqy.cli._workspace", lambda: ws)
    monkeypatch.setattr("doqqy.infra.vectorstore.factory.make_store", lambda _ws, _s=None: stub)

    cli_tags(backend=None)

    out = capsys.readouterr().out
    assert "erp12" in out
    assert "a b" in out
    assert "filtrelenemez" in out
    assert 'doqqy query "sorgu" --tag erp12' in out


def test_cli_tags_no_warning_when_all_tags_conform(tmp_path, monkeypatch, capsys):
    """When every stored tag matches TAG_PATTERN, no legacy warning panel is shown."""
    ws = Workspace(tmp_path)
    stub = _StubVectorStore(["erp12", "bulut-saha"])

    monkeypatch.setattr("doqqy.cli._workspace", lambda: ws)
    monkeypatch.setattr("doqqy.infra.vectorstore.factory.make_store", lambda _ws, _s=None: stub)

    cli_tags(backend=None)

    out = capsys.readouterr().out
    assert "filtrelenemez" not in out
