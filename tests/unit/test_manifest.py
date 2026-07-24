"""Unit tests for doqqy.manifest module (Manifest, ManifestEntry, DiffResult)."""

from __future__ import annotations

from pathlib import Path

import pytest

from doqqy.manifest import Manifest, ManifestEntry
from doqqy.workspace import Workspace


@pytest.fixture
def temp_ws(tmp_path: Path) -> Workspace:
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    return ws


def test_empty_manifest_load(temp_ws: Workspace) -> None:
    manifest = Manifest.load(temp_ws)
    assert len(manifest.docs) == 0
    assert manifest.totals() == {"docs": 0, "chunks": 0}


def test_save_and_reload(temp_ws: Workspace) -> None:
    manifest = Manifest()
    entry = ManifestEntry(
        source="raw/doc1.md",
        content_hash="abc1234567890123",
        tags=["project-a"],
        chunk_count=5,
        status="indexed",
        indexed_at="2026-07-23T12:00:00Z",
    )
    manifest.update_entry("raw/doc1.md", entry)
    saved_path = manifest.save(temp_ws)

    assert saved_path == temp_ws.manifest_path
    assert saved_path.exists()

    reloaded = Manifest.load(temp_ws)
    assert len(reloaded.docs) == 1
    loaded_entry = reloaded.get("raw/doc1.md")
    assert loaded_entry is not None
    assert loaded_entry.source == "raw/doc1.md"
    assert loaded_entry.content_hash == "abc1234567890123"
    assert loaded_entry.tags == ["project-a"]
    assert loaded_entry.chunk_count == 5
    assert loaded_entry.status == "indexed"
    assert loaded_entry.indexed_at == "2026-07-23T12:00:00Z"
    assert reloaded.totals() == {"docs": 1, "chunks": 5}


def test_atomic_write(temp_ws: Workspace) -> None:
    manifest = Manifest()
    manifest.update_entry("doc1", ManifestEntry(source="doc1", content_hash="h1", chunk_count=2))
    manifest.save(temp_ws)

    # Ensure no leftover temporary files in .doqqy
    tmp_files = list(temp_ws.state_dir.glob(".manifest_*.tmp"))
    assert len(tmp_files) == 0
    assert temp_ws.manifest_path.exists()


def test_update_and_remove_entry(temp_ws: Workspace) -> None:
    manifest = Manifest()
    manifest.update_entry("doc1", ManifestEntry(source="doc1", content_hash="h1"))
    manifest.update_entry("doc2", ManifestEntry(source="doc2", content_hash="h2"))

    assert len(manifest.docs) == 2
    assert manifest.remove_entry("doc1") is True
    assert len(manifest.docs) == 1
    assert manifest.get("doc1") is None
    assert manifest.remove_entry("nonexistent") is False


def test_diff_detects_new_files(temp_ws: Workspace) -> None:
    raw_file = temp_ws.raw_dir / "new_doc.md"
    raw_file.write_text("# New Document\n\nContent here.", encoding="utf-8")

    manifest = Manifest()
    diff = manifest.diff(temp_ws)

    assert len(diff.added) == 1
    assert diff.added[0] == raw_file
    assert len(diff.modified) == 0
    assert len(diff.deleted) == 0
    assert len(diff.unchanged) == 0
    assert diff.has_changes is True


def test_diff_detects_modified_files(temp_ws: Workspace) -> None:
    raw_file = temp_ws.raw_dir / "doc.md"
    raw_file.write_text("# Document\n\nOriginal content.", encoding="utf-8")

    # Ingest file to produce processed file with content_hash
    from doqqy.ingest import ingest_file
    doc = ingest_file(raw_file, temp_ws)
    doc.write()

    doc_id = str(raw_file.relative_to(temp_ws.root)).replace("\\", "/")
    manifest = Manifest()
    manifest.update_entry(doc_id, ManifestEntry(source=doc_id, content_hash="old_hash_1234567"))

    diff = manifest.diff(temp_ws)
    assert len(diff.modified) == 1
    assert diff.modified[0] == raw_file
    assert diff.has_changes is True


def test_diff_detects_deleted_files(temp_ws: Workspace) -> None:
    manifest = Manifest()
    manifest.update_entry("raw/deleted.md", ManifestEntry(source="raw/deleted.md", content_hash="hash123"))

    diff = manifest.diff(temp_ws)
    assert len(diff.deleted) == 1
    assert diff.deleted[0] == "raw/deleted.md"
    assert diff.has_changes is True


def test_diff_unchanged_files(temp_ws: Workspace) -> None:
    raw_file = temp_ws.raw_dir / "doc.md"
    raw_file.write_text("# Document\n\nContent.", encoding="utf-8")

    from doqqy.manifest import read_content_hash
    doc_id = str(raw_file.relative_to(temp_ws.root)).replace("\\", "/")
    current_hash = read_content_hash(raw_file) or ""

    manifest = Manifest()
    manifest.update_entry(doc_id, ManifestEntry(source=doc_id, content_hash=current_hash))

    diff = manifest.diff(temp_ws)
    assert len(diff.unchanged) == 1
    assert diff.unchanged[0] == doc_id
    assert diff.has_changes is False


def test_corrupt_manifest_load(temp_ws: Workspace) -> None:
    temp_ws.manifest_path.write_text("invalid json {{{", encoding="utf-8")
    manifest = Manifest.load(temp_ws)
    assert len(manifest.docs) == 0


def test_totals_computation() -> None:
    manifest = Manifest()
    manifest.update_entry("d1", ManifestEntry(source="d1", content_hash="h1", chunk_count=10))
    manifest.update_entry("d2", ManifestEntry(source="d2", content_hash="h2", chunk_count=15))
    manifest.update_entry("d3", ManifestEntry(source="d3", content_hash="h3", chunk_count=0))

    assert manifest.totals() == {"docs": 3, "chunks": 25}
