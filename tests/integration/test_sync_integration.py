"""Integration test for doqqy sync (end-to-end embed -> sync handoff).

Deliberately **not** marked `slow`: this is the regression guard for the
doc_id / content_hash handoff between embed and sync, so it has to run in the
fast CI lane.  To stay there it stubs out the two embedding helpers — the
vectors themselves are irrelevant here, while the real ingest, real chunking,
and real vector store are exactly what the test exists to exercise.
"""

from __future__ import annotations

import contextlib
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from doqqy.chunk import chunk_file
from doqqy.config import EMBEDDING_DIM
from doqqy.infra.vectorstore.base import ChunkRecord
from doqqy.infra.vectorstore.factory import make_store
from doqqy.ingest import ingest_file
from doqqy.manifest import Manifest
from doqqy.sync import sync
from doqqy.workspace import Workspace


@pytest.fixture
def temp_ws(tmp_path: Path) -> Workspace:
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    return ws


@pytest.fixture
def stub_embeddings():
    """Replace bge-m3 with zero vectors so the fast lane never downloads ~2 GB."""

    def fake_embed(_model, texts: list[str]) -> tuple[np.ndarray, list[str]]:
        dense = np.zeros((len(texts), EMBEDDING_DIM), dtype=np.float32)
        return dense, ['{"1": 0.5}'] * len(texts)

    with patch("doqqy.sync._load_embed_model", return_value=MagicMock()), \
         patch("doqqy.sync._embed_texts", side_effect=fake_embed):
        yield


def test_embed_sync_roundtrip(temp_ws: Workspace, stub_embeddings: None) -> None:
    # 1. Create initial raw files
    raw1 = temp_ws.raw_dir / "doc1.md"
    raw1.write_text("# Document One\n\nInitial content for document one.", encoding="utf-8")

    raw2 = temp_ws.raw_dir / "doc2.md"
    raw2.write_text("# Document Two\n\nInitial content for document two.", encoding="utf-8")

    # Ingest + Chunk
    doc1 = ingest_file(raw1, temp_ws)
    doc1.write()
    doc2 = ingest_file(raw2, temp_ws)
    doc2.write()

    chunks1 = chunk_file(doc1.processed_path, temp_ws)
    chunks2 = chunk_file(doc2.processed_path, temp_ws)

    assert len(chunks1) > 0
    assert len(chunks2) > 0

    # Build initial ChunkRecords (dummy vectors for test speed)
    records: list[ChunkRecord] = []
    for c in chunks1 + chunks2:
        records.append(
            ChunkRecord(
                chunk_id=c.chunk_id,
                doc_id=c.doc_id,
                source=c.source,
                doc_type=c.doc_type,
                tags=c.tags,
                content=c.content,
                section_path=c.section_path,
                char_count=c.char_count,
                prev_chunk=c.prev_chunk,
                next_chunk=c.next_chunk,
                dense=np.zeros(EMBEDDING_DIM, dtype=np.float32),
                sparse={1: 1.0},
            )
        )

    # Initial build_index creates the store + manifest baseline
    with contextlib.closing(make_store(temp_ws)) as store:
        store.full_rebuild(records, dim=EMBEDDING_DIM)

    # Call _save_manifest_from_records as build_index does
    from doqqy.embed import _save_manifest_from_records
    _save_manifest_from_records(temp_ws, records)

    # Verify baseline manifest contains raw/doc1.md and raw/doc2.md
    manifest = Manifest.load(temp_ws)
    assert len(manifest.docs) == 2
    assert "raw/doc1.md" in manifest.docs
    assert "raw/doc2.md" in manifest.docs

    # 2. Run sync with zero changes -> expect 0 processed, 2 unchanged
    report1 = sync(temp_ws)
    assert report1.total_processed == 0
    assert report1.unchanged == 2

    # 3. Modify raw/doc1.md -> run sync -> expect 1 modified
    raw1.write_text("# Document One Modified\n\nNew updated content for document one.", encoding="utf-8")
    report2 = sync(temp_ws)
    assert report2.modified == 1
    assert report2.added == 0
    assert report2.deleted == 0

    # Verify manifest updated
    manifest2 = Manifest.load(temp_ws)
    assert manifest2.get("raw/doc1.md") is not None

    # 4. Add raw/doc3.md -> run sync -> expect 1 added
    raw3 = temp_ws.raw_dir / "doc3.md"
    raw3.write_text("# Document Three\n\nContent for document three.", encoding="utf-8")
    report3 = sync(temp_ws)
    assert report3.added == 1

    manifest3 = Manifest.load(temp_ws)
    assert "raw/doc3.md" in manifest3.docs

    # 5. Delete raw/doc2.md -> run sync -> expect 1 deleted
    raw2.unlink()
    report4 = sync(temp_ws)
    assert report4.deleted == 1

    manifest4 = Manifest.load(temp_ws)
    assert "raw/doc2.md" not in manifest4.docs
    assert len(manifest4.docs) == 2  # doc1.md and doc3.md remain

    # The store must agree with the manifest: doc2's chunks are really gone.
    with contextlib.closing(make_store(temp_ws)) as store:
        assert store.count() == sum(e.chunk_count for e in manifest4.docs.values())


def test_sync_bootstraps_store_without_prior_embed(temp_ws: Workspace, stub_embeddings: None) -> None:
    """`doqqy sync` on a corpus that never ran `doqqy embed` must build a usable table.

    The first batch is deliberately degenerate — a doc directly in raw/ (no tags)
    whose single chunk has no prev_chunk. Inferring the schema from it would type
    those columns list<null>/null and break every later upsert.
    """
    (temp_ws.raw_dir / "solo.md").write_text("# Solo\n\nOnly document.", encoding="utf-8")

    report = sync(temp_ws)
    assert report.added == 1
    assert not report.has_failures

    # A tagged document arriving later must merge into that table, not blow up.
    tagged = temp_ws.raw_dir / "erp12" / "api.md"
    tagged.parent.mkdir(parents=True, exist_ok=True)
    tagged.write_text("# API\n\nTagged document body.", encoding="utf-8")

    report2 = sync(temp_ws)
    assert report2.added == 1
    assert not report2.has_failures

    with contextlib.closing(make_store(temp_ws)) as store:
        assert store.count() == 2
        assert store.list_tags() == ["erp12"]


def test_sync_records_documents_that_produce_no_chunks(temp_ws: Workspace, stub_embeddings: None) -> None:
    """An empty document still gets a manifest entry, or it re-syncs forever."""
    empty = temp_ws.raw_dir / "empty.md"
    empty.write_text("", encoding="utf-8")

    report = sync(temp_ws)
    assert report.added == 1

    entry = Manifest.load(temp_ws).get("raw/empty.md")
    assert entry is not None
    assert entry.chunk_count == 0

    # Second run sees nothing to do — this is the regression being guarded.
    report2 = sync(temp_ws)
    assert report2.total_processed == 0
    assert report2.unchanged == 1


def test_sync_dry_run_creates_no_directories(tmp_path: Path) -> None:
    """--dry-run must not touch the filesystem."""
    ws = Workspace(tmp_path)
    (tmp_path / "raw").mkdir()
    (tmp_path / "raw" / "doc.md").write_text("# Doc\n\nBody.", encoding="utf-8")

    report = sync(ws, dry_run=True)
    assert report.added == 1
    assert not ws.state_dir.exists()
    assert not ws.processed_dir.exists()
