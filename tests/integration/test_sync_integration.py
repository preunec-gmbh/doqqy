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

    # Call _build_manifest_from_records as build_index does
    from doqqy.dedup import resolve_duplicates
    from doqqy.embed import _build_manifest_from_records
    manifest0 = _build_manifest_from_records(temp_ws, records)
    resolve_duplicates(temp_ws, manifest0, settings=None)
    manifest0.save(temp_ws)

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



# ---------------------------------------------------------------------------
# Same-stem collisions (issue #76): an incremental sync must land on exactly the
# file set a full `doqqy ingest` would produce, in both directions.
# ---------------------------------------------------------------------------


def _write_doc(ws: Workspace, folder: str, name: str) -> Path:
    directory = ws.raw_dir / folder
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(f"# Belge {name}\n\n{name} icin govde metni.\n", encoding="utf-8")
    return path


def _outputs(ws: Workspace) -> list[str]:
    return sorted(
        str(p.relative_to(ws.processed_dir)).replace("\\", "/")
        for p in ws.processed_dir.rglob("*.md")
    )


def _full_ingest_outputs(tmp_path: Path, names: list[str]) -> list[str]:
    """The file set a from-scratch `doqqy ingest` produces for *names* — the convergence target."""
    from doqqy.ingest.router import ingest_directory

    # Test workspace'inin dışında: ws.root altına kurulsaydı ileride ws.root'u
    # gezen herhangi bir yardımcı ikinci bir korpus görürdü.
    reference = Workspace(tmp_path.parent / f"{tmp_path.name}-reference")
    reference.ensure_dirs()
    for name in names:
        _write_doc(reference, "x", name)
    ingest_directory(reference)
    return _outputs(reference)


def test_sync_converges_with_full_ingest_when_a_colliding_sibling_appears(
    temp_ws: Workspace, stub_embeddings: None, tmp_path: Path
) -> None:
    """Dropping a same-stem sibling next to an indexed document renames both outputs."""
    _write_doc(temp_ws, "x", "rapor.md")
    sync(temp_ws)
    assert _outputs(temp_ws) == ["x/rapor.md"]

    _write_doc(temp_ws, "x", "rapor.txt")
    report = sync(temp_ws)

    # rapor.md'nin baytlari degismedi, ama hedef adi degisti — sync onu yine de
    # yeniden islemezse artimli yol tam ingest'ten ayrisirdi.
    assert report.modified == 1, f"adi degisen belge modified sayilmali: {report}"
    assert not report.failed
    assert _outputs(temp_ws) == _full_ingest_outputs(tmp_path, ["rapor.md", "rapor.txt"])

    # Iki belge de store'da kendi doc_id'siyle duruyor. Issue'nun sikayeti tam
    # olarak buydu: cakisan kaynaklardan yalnizca biri indekse ulasiyordu.
    with contextlib.closing(make_store(temp_ws)) as store:
        assert store.get_by_doc("raw/x/rapor.md"), "rapor.md indekste yok"
        assert store.get_by_doc("raw/x/rapor.txt"), "rapor.txt indekste yok"


def test_sync_removes_the_output_of_a_deleted_colliding_sibling(
    temp_ws: Workspace, stub_embeddings: None, tmp_path: Path
) -> None:
    """Deleting one of a colliding pair leaves no orphan behind in processed/.

    The regression this guards: the deletion path used to re-derive the output
    name from the source, which by then is gone — so it computed a name that was
    never written, unlinked nothing, and left the real file for chunk/map/inject
    to keep feeding deleted content back into the index.
    """
    _write_doc(temp_ws, "x", "rapor.md")
    _write_doc(temp_ws, "x", "rapor.txt")
    sync(temp_ws)
    assert _outputs(temp_ws) == ["x/rapor-md.md", "x/rapor-txt.md"]

    (temp_ws.raw_dir / "x" / "rapor.txt").unlink()
    report = sync(temp_ws)

    assert report.deleted == 1
    assert not report.failed
    assert _outputs(temp_ws) == _full_ingest_outputs(tmp_path, ["rapor.md"])

    # Silinen belge indekste iz birakmamali — oksuz bir .md kalsaydi chunk_directory
    # onu processed/*.md taramasinda bulup geri getirirdi.
    with contextlib.closing(make_store(temp_ws)) as store:
        assert store.get_by_doc("raw/x/rapor.txt") == []


def test_sync_fails_a_document_whose_output_path_is_already_taken(
    temp_ws: Workspace, stub_embeddings: None
) -> None:
    """Sync holds the same invariant as ingest: two documents may not share one .md file.

    Disambiguation resolves most collisions but not all — `a.txt` becomes
    `a-txt.md` while a source genuinely named `a-txt.csv` is a singleton and
    keeps that name. Without a guard here the incremental path would silently
    overwrite one of them and report success, which is the bug this whole change
    exists to remove.
    """
    _write_doc(temp_ws, "x", "a.md")
    _write_doc(temp_ws, "x", "a.txt")
    _write_doc(temp_ws, "x", "a-txt.csv")

    report = sync(temp_ws)

    assert len(report.failed) == 1, f"cakisan belge hata olarak raporlanmali: {report}"
    doc_id, message = report.failed[0]
    assert "çıktı yolu çakıştı" in message
    # Kaybeden taraf belirli olmali: sirali gezildigi icin ('-' < '.') gercek
    # a-txt.csv once yazilir, ayristirma sonucu ayni ada dusen a.txt reddedilir.
    assert doc_id == "raw/x/a.txt"
    # Hicbir belge sessizce kaybolmadi: kalan ikisi kendi dosyalarinda ve
    # a-txt.md gercekten a-txt.csv'nin icerigini tasiyor.
    assert _outputs(temp_ws) == ["x/a-md.md", "x/a-txt.md"]
    body = (temp_ws.processed_dir / "x" / "a-txt.md").read_text(encoding="utf-8")
    assert "source: raw/x/a-txt.csv" in body


def test_sync_keeps_the_output_a_replacement_document_just_wrote(
    temp_ws: Workspace, stub_embeddings: None
) -> None:
    """Replacing a source with a same-stem sibling in one run must not delete the new output.

    `_process_changed` runs before `_process_deletions`, so the new document has
    already written `rapor.md` by the time the removed one is processed. Trusting
    the recorded path blindly would unlink the live file and leave `processed/`
    empty, with nothing in any later run to put it back.
    """
    _write_doc(temp_ws, "x", "rapor.md")
    sync(temp_ws)
    assert _outputs(temp_ws) == ["x/rapor.md"]

    (temp_ws.raw_dir / "x" / "rapor.md").unlink()
    _write_doc(temp_ws, "x", "rapor.txt")
    report = sync(temp_ws)

    assert not report.failed
    assert _outputs(temp_ws) == ["x/rapor.md"], "yeni belgenin ciktisi silinmis"

    with contextlib.closing(make_store(temp_ws)) as store:
        assert store.get_by_doc("raw/x/rapor.txt"), "yeni belge indekste yok"
        assert store.get_by_doc("raw/x/rapor.md") == [], "silinen belge indekte kalmis"


def test_sync_does_not_steal_the_output_of_an_untouched_document(
    temp_ws: Workspace, stub_embeddings: None
) -> None:
    """A document sync is not even processing this run still owns its output file.

    Sync only touches the delta, so a guard fed solely from this run's documents
    is blind to the rest of the corpus: a newly disambiguated name can land on an
    untouched document's file and overwrite it with zero failures reported, and
    the diff never re-flags the victim because nothing about it changed.
    """
    _write_doc(temp_ws, "x", "a.md")
    _write_doc(temp_ws, "x", "a-md.md")
    sync(temp_ws)
    assert _outputs(temp_ws) == ["x/a-md.md", "x/a.md"]

    # a.txt gelince a.md'nin hedefi a-md.md olur — ama orasi a-md.md'nin.
    _write_doc(temp_ws, "x", "a.txt")
    report = sync(temp_ws)

    assert len(report.failed) == 1, f"cakisma raporlanmali: {report}"
    assert report.failed[0][0] == "raw/x/a.md"

    body = (temp_ws.processed_dir / "x" / "a-md.md").read_text(encoding="utf-8")
    assert "source: raw/x/a-md.md" in body, "dokunulmamis belgenin ciktisi ezilmis"

    # Manifest'te iki doc_id tek dosyayi gostermemeli.
    manifest = Manifest.load(temp_ws)
    recorded = [e.processed_path for e in manifest.docs.values() if e.processed_path]
    assert len(recorded) == len(set(recorded)), f"cift sahiplik: {recorded}"


def test_sync_guard_repeats_its_rejection_when_nothing_changes(
    temp_ws: Workspace, stub_embeddings: None
) -> None:
    """A rejected document stays rejected on the next run instead of winning it.

    Rejection records `content_hash=""`, which makes the rejected document the
    only changed source next time. A run-scoped guard would be empty then and let
    it overwrite the document that won — turning a loud failure into silent data
    loss one command later, with nothing on disk having changed.
    """
    _write_doc(temp_ws, "x", "a.md")
    _write_doc(temp_ws, "x", "a.txt")
    _write_doc(temp_ws, "x", "a-md.md")

    first = sync(temp_ws)
    assert len(first.failed) == 1
    winner = (temp_ws.processed_dir / "x" / "a-md.md").read_text(encoding="utf-8")
    assert "source: raw/x/a-md.md" in winner

    # Diskte hicbir sey degismedi.
    second = sync(temp_ws)
    assert len(second.failed) == 1, f"red tekrar etmeli: {second}"
    assert (temp_ws.processed_dir / "x" / "a-md.md").read_text(encoding="utf-8") == winner

    third = sync(temp_ws)
    assert len(third.failed) == 1
    assert (temp_ws.processed_dir / "x" / "a-md.md").read_text(encoding="utf-8") == winner
