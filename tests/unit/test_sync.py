"""Unit tests for doqqy.sync module (incremental sync pipeline)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from doqqy.manifest import Manifest, ManifestEntry
from doqqy.sync import SyncReport, sync
from doqqy.workspace import Workspace


@pytest.fixture
def temp_ws(tmp_path: Path) -> Workspace:
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    return ws


def test_sync_report_properties() -> None:
    report = SyncReport(added=2, modified=1, deleted=3, unchanged=10)
    assert report.total_processed == 6
    assert report.has_failures is False

    report.failed.append(("doc1", "Some error"))
    assert report.has_failures is True


def test_sync_dry_run(temp_ws: Workspace) -> None:
    raw_file = temp_ws.raw_dir / "doc.md"
    raw_file.write_text("# Dry Run Test\n\nContent.", encoding="utf-8")

    report = sync(temp_ws, dry_run=True)
    assert report.added == 1
    assert report.modified == 0
    assert report.deleted == 0

    # Manifest should not be created on disk
    assert not temp_ws.manifest_path.exists()


def test_sync_no_changes(temp_ws: Workspace) -> None:
    manifest = Manifest()
    manifest.save(temp_ws)

    report = sync(temp_ws)
    assert report.total_processed == 0
    assert report.unchanged == 0
    assert report.has_failures is False


@patch("doqqy.sync._load_embed_model")
@patch("doqqy.sync._embed_texts")
def test_sync_new_document(
    mock_embed_texts: MagicMock,
    mock_load_model: MagicMock,
    temp_ws: Workspace,
) -> None:
    # Set up mock embeddings
    mock_load_model.return_value = MagicMock()
    mock_embed_texts.return_value = (
        np.zeros((1, 1024), dtype=np.float32),
        ['{"1": 0.5}'],
    )

    raw_file = temp_ws.raw_dir / "new_doc.md"
    raw_file.write_text("# New Doc\n\nThis is a new document content for testing.", encoding="utf-8")

    with patch("doqqy.infra.vectorstore.factory.make_store") as mock_make_store:
        mock_store = MagicMock()
        mock_make_store.return_value = mock_store

        report = sync(temp_ws)

        assert report.added == 1
        assert report.modified == 0
        assert report.deleted == 0
        assert report.has_failures is False

        # Store should have been called
        mock_store.delete_by_doc.assert_called_once()
        mock_store.upsert.assert_called_once()

    # Manifest should be saved and contain the new document
    manifest = Manifest.load(temp_ws)
    doc_id = str(raw_file.relative_to(temp_ws.root)).replace("\\", "/")
    entry = manifest.get(doc_id)
    assert entry is not None
    assert entry.status == "indexed"
    assert entry.chunk_count == 1


@patch("doqqy.sync._load_embed_model")
@patch("doqqy.sync._embed_texts")
def test_sync_modified_document(
    mock_embed_texts: MagicMock,
    mock_load_model: MagicMock,
    temp_ws: Workspace,
) -> None:
    mock_load_model.return_value = MagicMock()
    mock_embed_texts.return_value = (
        np.zeros((1, 1024), dtype=np.float32),
        ['{"1": 0.5}'],
    )

    raw_file = temp_ws.raw_dir / "doc.md"
    raw_file.write_text("# Original\n\nContent.", encoding="utf-8")
    doc_id = str(raw_file.relative_to(temp_ws.root)).replace("\\", "/")

    # Pre-populate manifest with old hash
    manifest = Manifest()
    manifest.update_entry(doc_id, ManifestEntry(source=doc_id, content_hash="old_hash", chunk_count=1))
    manifest.save(temp_ws)

    # Ingest original file to create processed file
    from doqqy.ingest import ingest_file
    doc = ingest_file(raw_file, temp_ws)
    doc.write()

    # Modify raw file
    raw_file.write_text("# Modified\n\nUpdated content with more details.", encoding="utf-8")

    with patch("doqqy.infra.vectorstore.factory.make_store") as mock_make_store:
        mock_store = MagicMock()
        mock_make_store.return_value = mock_store

        report = sync(temp_ws)

        assert report.modified == 1
        assert report.added == 0

    # Manifest should have updated content hash
    updated_manifest = Manifest.load(temp_ws)
    entry = updated_manifest.get(doc_id)
    assert entry is not None
    assert entry.content_hash != "old_hash"


def test_sync_deleted_document(temp_ws: Workspace) -> None:
    doc_id = "raw/deleted.md"
    manifest = Manifest()
    manifest.update_entry(doc_id, ManifestEntry(source=doc_id, content_hash="hash123", chunk_count=2))
    manifest.save(temp_ws)

    with patch("doqqy.infra.vectorstore.factory.make_store") as mock_make_store:
        mock_store = MagicMock()
        mock_make_store.return_value = mock_store

        report = sync(temp_ws)

        assert report.deleted == 1
        mock_store.delete_by_doc.assert_called_once_with(doc_id)

    updated_manifest = Manifest.load(temp_ws)
    assert updated_manifest.get(doc_id) is None


@patch("doqqy.sync._load_embed_model")
@patch("doqqy.sync._embed_texts")
def test_sync_failure_isolation(
    mock_embed_texts: MagicMock,
    mock_load_model: MagicMock,
    temp_ws: Workspace,
) -> None:
    mock_load_model.return_value = MagicMock()

    good_file = temp_ws.raw_dir / "good.md"
    good_file.write_text("# Good Doc\n\nValid content.", encoding="utf-8")

    bad_file = temp_ws.raw_dir / "bad.md"
    bad_file.write_text("# Bad Doc\n\nContent.", encoding="utf-8")

    from doqqy.ingest import ingest_file as real_ingest_file

    def mock_ingest(path: Path, ws: Workspace, **kwargs):
        if "bad.md" in str(path):
            raise ValueError("Corrupt file format")
        return real_ingest_file(path, ws, **kwargs)

    mock_embed_texts.return_value = (
        np.zeros((1, 1024), dtype=np.float32),
        ['{"1": 0.5}'],
    )

    with patch("doqqy.ingest.ingest_file", side_effect=mock_ingest):
        with patch("doqqy.infra.vectorstore.factory.make_store") as mock_make_store:
            mock_make_store.return_value = MagicMock()

            report = sync(temp_ws)

            assert report.added == 1
            assert report.has_failures is True
            assert len(report.failed) == 1
            assert "bad.md" in report.failed[0][0]

    manifest = Manifest.load(temp_ws)
    bad_doc_id = str(bad_file.relative_to(temp_ws.root)).replace("\\", "/")
    entry = manifest.get(bad_doc_id)
    assert entry is not None
    assert entry.status == "failed"
