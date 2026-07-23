"""Integration test for doqqy sync (end-to-end embed -> sync handoff)."""

from __future__ import annotations

import contextlib
from pathlib import Path

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


def test_embed_sync_roundtrip(temp_ws: Workspace) -> None:
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
    import numpy as np
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
