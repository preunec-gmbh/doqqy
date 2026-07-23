"""Incremental sync pipeline — ingest/chunk/embed only changed documents.

``sync(ws, settings)`` compares the raw/ directory against the persisted
manifest to detect added, modified, and deleted files. Only the delta is
processed, making single-document updates seconds instead of minutes.

Typical usage (CLI)::

    doqqy sync            # incremental update
    doqqy sync --dry-run  # preview changes without modifying anything
"""

from __future__ import annotations

import contextlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from doqqy.config import get_logger
from doqqy.manifest import DiffResult, Manifest, ManifestEntry
from doqqy.workspace import Workspace

if TYPE_CHECKING:
    from doqqy.infra.settings import Settings

_LOG = get_logger("doqqy.sync")


@dataclass
class SyncReport:
    """Summary of a single sync run."""

    added: int = 0
    modified: int = 0
    deleted: int = 0
    unchanged: int = 0
    failed: list[tuple[str, str]] = field(default_factory=list)

    @property
    def total_processed(self) -> int:
        return self.added + self.modified + self.deleted

    @property
    def has_failures(self) -> bool:
        return bool(self.failed)


def sync(
    ws: Workspace,
    *,
    settings: Settings | None = None,
    dry_run: bool = False,
) -> SyncReport:
    """Run the incremental pipeline: ingest → chunk → embed for changed docs only.

    Parameters
    ----------
    ws:
        Workspace root (determines raw/, processed/, .doqqy/ paths).
    settings:
        Optional Settings override (vector backend selection).
    dry_run:
        If True, compute the diff and return the report without modifying anything.

    Returns
    -------
    SyncReport with counts of added/modified/deleted/unchanged documents.
    """
    ws.ensure_dirs()

    manifest = Manifest.load(ws)
    diff = manifest.diff(ws)

    report = SyncReport(unchanged=len(diff.unchanged))

    if dry_run:
        report.added = len(diff.added)
        report.modified = len(diff.modified)
        report.deleted = len(diff.deleted)
        _LOG.info(
            "Dry run: %d added, %d modified, %d deleted, %d unchanged.",
            report.added, report.modified, report.deleted, report.unchanged,
        )
        return report

    if not diff.has_changes:
        _LOG.info("Nothing to sync — %d documents unchanged.", report.unchanged)
        return report

    # Process additions and modifications (embed together for efficiency).
    changed_sources = diff.added + diff.modified
    if changed_sources:
        _process_changed(ws, manifest, changed_sources, diff, report, settings)

    # Process deletions.
    if diff.deleted:
        _process_deletions(ws, manifest, diff.deleted, report, settings)

    # Persist the updated manifest atomically.
    manifest.save(ws)
    _LOG.info(
        "Sync complete: +%d ~%d -%d =%d (failed: %d).",
        report.added, report.modified, report.deleted,
        report.unchanged, len(report.failed),
    )
    return report


# ---------------------------------------------------------------------------
# Internal pipeline stages
# ---------------------------------------------------------------------------


def _process_changed(
    ws: Workspace,
    manifest: Manifest,
    sources: list[Path],
    diff: DiffResult,
    report: SyncReport,
    settings: Settings | None,
) -> None:
    """Ingest, chunk, and embed each changed source file."""
    from doqqy.chunk import Chunk, chunk_file
    from doqqy.infra.vectorstore.base import ChunkRecord
    from doqqy.infra.vectorstore.factory import make_store
    from doqqy.ingest import ingest_file

    added_set = set(str(p) for p in diff.added)

    # Collect all chunks that need embedding.
    doc_chunks: list[tuple[str, str, list[str], list[Chunk]]] = []  # (doc_id, source_str, tags, chunks)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]sync ingest+chunk[/bold cyan]"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("ingest+chunk", total=len(sources))
        for source_path in sources:
            progress.update(task, description=f"[dim]{source_path.name}[/dim]", advance=1)
            try:
                doc = ingest_file(source_path, ws)
                doc.write()

                chunks = chunk_file(doc.processed_path, ws)
                if not chunks:
                    _LOG.warning("No chunks produced for %s — skipping.", source_path)
                    continue

                doc_id = _doc_id(source_path, ws)
                tags = doc.metadata.get("tags", [])
                content_hash = doc.metadata.get("content_hash", "")
                doc_chunks.append((doc_id, content_hash, tags, chunks))

                is_new = str(source_path) in added_set
                if is_new:
                    report.added += 1
                else:
                    report.modified += 1

            except Exception as exc:  # noqa: BLE001
                doc_id = _doc_id(source_path, ws)
                _LOG.exception("Failed to process %s: %s", source_path, exc)
                report.failed.append((doc_id, f"{type(exc).__name__}: {exc}"))
                manifest.update_entry(doc_id, ManifestEntry(
                    source=str(source_path),
                    content_hash="",
                    status="failed",
                ))

    if not doc_chunks:
        return

    # Embed all chunks in batches.
    all_chunks: list[Chunk] = []
    chunk_doc_map: list[int] = []  # chunk index → doc_chunks index
    for idx, (_, _, _, chunks) in enumerate(doc_chunks):
        for c in chunks:
            all_chunks.append(c)
            chunk_doc_map.append(idx)

    texts = [c.content for c in all_chunks]
    model = _load_embed_model()
    dense_vecs, sparse_jsons = _embed_texts(model, texts)

    # Build ChunkRecords and group by doc.
    doc_records: dict[int, list[ChunkRecord]] = {}
    for i, chunk in enumerate(all_chunks):
        sparse_vec = {int(k): float(v) for k, v in json.loads(sparse_jsons[i]).items()}
        rec = ChunkRecord(
            chunk_id=chunk.chunk_id,
            doc_id=chunk.doc_id,
            source=chunk.source,
            doc_type=chunk.doc_type,
            tags=chunk.tags,
            content=chunk.content,
            section_path=chunk.section_path,
            char_count=chunk.char_count,
            prev_chunk=chunk.prev_chunk,
            next_chunk=chunk.next_chunk,
            dense=np.asarray(dense_vecs[i], dtype=np.float32),
            sparse=sparse_vec,
        )
        doc_idx = chunk_doc_map[i]
        doc_records.setdefault(doc_idx, []).append(rec)

    # Upsert into the store: delete old chunks, insert new ones.
    with contextlib.closing(make_store(ws, settings)) as store:
        for idx, (doc_id, content_hash, tags, chunks) in enumerate(doc_chunks):
            records = doc_records.get(idx, [])
            if not records:
                continue
            store.delete_by_doc(chunks[0].doc_id)
            store.upsert(records)

            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            manifest.update_entry(doc_id, ManifestEntry(
                source=doc_id,
                content_hash=content_hash,
                tags=tags,
                chunk_count=len(records),
                status="indexed",
                indexed_at=now,
            ))


def _process_deletions(
    ws: Workspace,
    manifest: Manifest,
    deleted_doc_ids: list[str],
    report: SyncReport,
    settings: Settings | None,
) -> None:
    """Remove deleted documents from the store and manifest."""
    from doqqy.infra.vectorstore.factory import make_store

    with contextlib.closing(make_store(ws, settings)) as store:
        for doc_id in deleted_doc_ids:
            try:
                store.delete_by_doc(doc_id)

                # Remove corresponding processed file if it exists.
                processed = ws.processed_dir / Path(doc_id).relative_to("raw") if doc_id.startswith("raw/") else None
                if processed and processed.with_suffix(".md").exists():
                    processed.with_suffix(".md").unlink()

                manifest.remove_entry(doc_id)
                report.deleted += 1
            except Exception as exc:  # noqa: BLE001
                _LOG.exception("Failed to delete %s: %s", doc_id, exc)
                report.failed.append((doc_id, f"{type(exc).__name__}: {exc}"))


# ---------------------------------------------------------------------------
# Embedding helpers (shared model loading)
# ---------------------------------------------------------------------------


def _load_embed_model():
    """Load the embedding model (reuses embed.py's singleton pattern)."""
    from doqqy.embed import _load_model
    return _load_model()


def _embed_texts(model, texts: list[str]) -> tuple[np.ndarray, list[str]]:
    """Embed a list of texts, returning (dense_vecs, sparse_json_list)."""
    from doqqy.embed import _embed_texts as _do_embed
    return _do_embed(model, texts)


def _doc_id(source_path: Path, ws: Workspace) -> str:
    """Derive a stable doc_id from a source path."""
    try:
        return str(source_path.relative_to(ws.root)).replace("\\", "/")
    except ValueError:
        return source_path.name
