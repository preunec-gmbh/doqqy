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
def test_sync_duplicate_documents_alias(
    mock_embed_texts: MagicMock,
    mock_load_model: MagicMock,
    temp_ws: Workspace,
) -> None:
    """Issue #18: the same file under raw/a/ and raw/b/ → one embedded doc, tags [a, b]."""
    mock_load_model.return_value = MagicMock()
    mock_embed_texts.return_value = (
        np.zeros((2, 1024), dtype=np.float32),
        ['{"1": 0.5}', '{"1": 0.5}'],
    )

    content = "# Shared Policy\n\nIdentical content placed in two folders."
    (temp_ws.raw_dir / "a").mkdir(parents=True, exist_ok=True)
    (temp_ws.raw_dir / "b").mkdir(parents=True, exist_ok=True)
    (temp_ws.raw_dir / "a" / "x.md").write_text(content, encoding="utf-8")
    (temp_ws.raw_dir / "b" / "x.md").write_text(content, encoding="utf-8")

    from doqqy.infra.vectorstore.base import ChunkRecord

    with patch("doqqy.infra.vectorstore.factory.make_store") as mock_make_store:
        mock_store = MagicMock()
        mock_store.get_by_doc.return_value = [
            ChunkRecord(
                chunk_id="c1", doc_id="raw/a/x.md", source="raw/a/x.md", doc_type="md",
                tags=["a"], content=content, section_path=[], char_count=len(content),
                prev_chunk=None, next_chunk=None,
                dense=np.zeros(1024, dtype=np.float32), sparse={1: 0.5},
            )
        ]
        mock_make_store.return_value = mock_store

        report = sync(temp_ws)

        assert report.added == 2
        assert report.has_failures is False

    manifest = Manifest.load(temp_ws)
    canonical = manifest.get("raw/a/x.md")
    alias = manifest.get("raw/b/x.md")

    assert canonical is not None
    assert canonical.tags == ["a", "b"]
    assert canonical.alias_of is None

    assert alias is not None
    assert alias.alias_of == "raw/a/x.md"
    assert alias.chunk_count == 0
    assert alias.status == "aliased"

    # The canonical's chunks must have been re-upserted with the unioned tags.
    upserted_tag_sets = [
        sorted(rec.tags) for call in mock_store.upsert.call_args_list for rec in call.args[0]
    ]
    assert ["a", "b"] in upserted_tag_sets


@patch("doqqy.sync._load_embed_model")
@patch("doqqy.sync._embed_texts")
def test_sync_self_heals_alias_after_canonical_deleted(
    mock_embed_texts: MagicMock,
    mock_load_model: MagicMock,
    temp_ws: Workspace,
) -> None:
    """Review fix (issue #18): deleting the canonical must not strand its alias.

    raw/a (canonical) + raw/b (alias) -> delete raw/a -> raw/b's own bytes never
    changed, so plain content_hash diffing would call it "unchanged" forever and
    its content would silently vanish from the index. It must instead be picked
    up as modified and re-indexed as a standalone doc on the run *after* the
    deletion is processed (manifest.diff() only sees the canonical's entry gone
    once _process_deletions has actually removed it).
    """
    mock_load_model.return_value = MagicMock()
    mock_embed_texts.side_effect = lambda _model, texts: (
        np.zeros((len(texts), 1024), dtype=np.float32),
        ['{"1": 0.5}'] * len(texts),
    )

    content = "# Shared Policy\n\nIdentical content placed in two folders."
    (temp_ws.raw_dir / "a").mkdir(parents=True, exist_ok=True)
    (temp_ws.raw_dir / "b").mkdir(parents=True, exist_ok=True)
    (temp_ws.raw_dir / "a" / "x.md").write_text(content, encoding="utf-8")
    (temp_ws.raw_dir / "b" / "x.md").write_text(content, encoding="utf-8")

    from doqqy.infra.vectorstore.base import ChunkRecord

    with patch("doqqy.infra.vectorstore.factory.make_store") as mock_make_store:
        mock_store = MagicMock()
        mock_store.get_by_doc.return_value = [
            ChunkRecord(
                chunk_id="c1", doc_id="raw/a/x.md", source="raw/a/x.md", doc_type="md",
                tags=["a"], content=content, section_path=[], char_count=len(content),
                prev_chunk=None, next_chunk=None,
                dense=np.zeros(1024, dtype=np.float32), sparse={1: 0.5},
            )
        ]
        mock_make_store.return_value = mock_store

        # Run 1: both new -> raw/a canonical (tags [a,b]), raw/b aliased.
        sync(temp_ws)
        manifest = Manifest.load(temp_ws)
        assert manifest.get("raw/b/x.md").alias_of == "raw/a/x.md"

        # Delete the canonical, then sync (run 2): this is the run that processes
        # the deletion itself — diff() still sees raw/a/x.md's entry (it hasn't
        # been removed yet when diff() runs), so raw/b is not touched this round.
        (temp_ws.raw_dir / "a" / "x.md").unlink()
        report2 = sync(temp_ws)
        assert report2.deleted == 1

        manifest2 = Manifest.load(temp_ws)
        assert manifest2.get("raw/a/x.md") is None
        stranded = manifest2.get("raw/b/x.md")
        assert stranded is not None
        assert stranded.alias_of == "raw/a/x.md"  # still points at a doc_id that's now gone
        assert stranded.chunk_count == 0

        # Run 3, no further disk changes: diff() must now flag raw/b/x.md as
        # modified (its alias_of target is gone) and re-embed it standalone.
        report3 = sync(temp_ws)
        assert report3.modified == 1
        assert report3.added == 0

    manifest3 = Manifest.load(temp_ws)
    healed = manifest3.get("raw/b/x.md")
    assert healed is not None
    assert healed.alias_of is None
    assert healed.status == "indexed"
    assert healed.chunk_count == 1
    # Tags shed back to its own folder's tag — the stale ["a", "b"] union is gone.
    assert healed.tags == ["b"]


@patch("doqqy.sync._load_embed_model")
@patch("doqqy.sync._embed_texts")
def test_sync_sheds_stale_tag_union_when_alias_deleted(
    mock_embed_texts: MagicMock,
    mock_load_model: MagicMock,
    temp_ws: Workspace,
) -> None:
    """Review fix, other direction: delete the *alias* (raw/b), not the canonical.

    raw/a/x.md keeps tags=[a, b] otherwise, even though raw/b/ no longer exists
    — so `--tag b` would still (wrongly) return it. Unlike the stranded-alias
    case, this self-heals in the *same* sync run as the deletion, since
    resolve_duplicates recomputes it directly rather than waiting on diff().
    """
    mock_load_model.return_value = MagicMock()
    mock_embed_texts.side_effect = lambda _model, texts: (
        np.zeros((len(texts), 1024), dtype=np.float32),
        ['{"1": 0.5}'] * len(texts),
    )

    content = "# Shared Policy\n\nIdentical content placed in two folders."
    (temp_ws.raw_dir / "a").mkdir(parents=True, exist_ok=True)
    (temp_ws.raw_dir / "b").mkdir(parents=True, exist_ok=True)
    (temp_ws.raw_dir / "a" / "x.md").write_text(content, encoding="utf-8")
    (temp_ws.raw_dir / "b" / "x.md").write_text(content, encoding="utf-8")

    from doqqy.infra.vectorstore.base import ChunkRecord

    with patch("doqqy.infra.vectorstore.factory.make_store") as mock_make_store:
        mock_store = MagicMock()
        mock_store.get_by_doc.return_value = [
            ChunkRecord(
                chunk_id="c1", doc_id="raw/a/x.md", source="raw/a/x.md", doc_type="md",
                tags=["a"], content=content, section_path=[], char_count=len(content),
                prev_chunk=None, next_chunk=None,
                dense=np.zeros(1024, dtype=np.float32), sparse={1: 0.5},
            )
        ]
        mock_make_store.return_value = mock_store

        sync(temp_ws)
        assert Manifest.load(temp_ws).get("raw/a/x.md").tags == ["a", "b"]

        # Delete the alias this time.
        (temp_ws.raw_dir / "b" / "x.md").unlink()
        report2 = sync(temp_ws)
        assert report2.deleted == 1

    manifest2 = Manifest.load(temp_ws)
    assert manifest2.get("raw/b/x.md") is None
    survivor = manifest2.get("raw/a/x.md")
    assert survivor is not None
    assert survivor.alias_of is None
    assert survivor.chunk_count == 1
    assert survivor.tags == ["a"]  # shed back — "b" is gone with the folder


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
