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
import os
import tempfile
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
    from doqqy.infra.vectorstore.base import ChunkRecord

_LOG = get_logger("doqqy.sync")


@dataclass
class SyncReport:
    """Summary of a single sync run."""

    added: int = 0
    modified: int = 0
    deleted: int = 0
    unchanged: int = 0
    failed: list[tuple[str, str]] = field(default_factory=list)
    # Gövde adı bir kardeşiyle çakıştığı için çıktısı <stem>-<ext>.md olarak
    # yazılan belge sayısı (issue #76). `doqqy ingest` bunu raporluyor; sync de
    # aynı yeniden adlandırmayı yapıyor, dolayısıyla aynı görünürlüğü borçlu.
    disambiguated: int = 0

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
    # A dry run must not touch the filesystem — only create directories when
    # we are actually going to write into them.
    if not dry_run:
        ws.ensure_dirs()

    # Kardeş taraması önbelleği bir çalışmadan uzun yaşamamalı: `doqqy watch`
    # arka arkaya sync çalıştırır ve aralarında raw/ değişir.
    from doqqy.ingest.base import reset_stem_group_cache
    reset_stem_group_cache()

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

    # Bu çalışmada processed/ altına yazılan hedefler: yol -> onu yazan doc_id.
    # İki yerde gerekiyor. (1) Aynı yola ikinci kez yazmak isteyen bir belgeyi
    # reddetmek — ingest_directory'deki invariant'ın aynısı; ad ayrıştırması her
    # çifti ayıramaz ve sync korumasız kalırsa aynı sessiz kayıp buraya taşınır.
    # (2) Silme aşamasının, az önce başka bir belge için yazılmış bir dosyayı
    # kaldırmasını engellemek: bir kaynak silinip yerine aynı gövde adlı bir
    # başkası eklendiğinde ikisi de aynı processed/ yolunu hedefler.
    written_this_run: dict[Path, str] = {}

    changed_sources = diff.added + diff.modified

    # Guard'ı yalnızca bu çalışmada işlenen belgelerle doldurmak yetmiyor. sync
    # korpusun küçük bir dilimine dokunur; değişmemiş bir belgenin sahip olduğu
    # yol görünmez kalırsa yeni ayrıştırılan bir ad onun üzerine sessizce yazar
    # ve manifest'te iki doc_id tek dosyayı gösterir. Dahası guard çalışmalar
    # arasında kararsız olurdu: reddedilen belge content_hash="" ile kaydedildiği
    # için bir sonraki çalışmanın tek değişeni olur, guard boş kalır ve bu kez
    # kazananı ezerdi — gürültülü hata bir komut sonra sessiz kayba dönüşürdü.
    # Dokunulmayan her belgenin kayıtlı yolunu baştan rezerve ederek guard'ı
    # ingest_directory'ninki gibi korpus kapsamlı ve idempotent hale getiriyoruz.
    touched = {_doc_id(path, ws) for path in changed_sources} | set(diff.deleted)
    for doc_id, entry in manifest.docs.items():
        if doc_id in touched or not entry.processed_path:
            continue
        written_this_run[(ws.root / Path(entry.processed_path)).resolve()] = doc_id

    # Process additions and modifications (embed together for efficiency).
    if changed_sources:
        _process_changed(ws, manifest, changed_sources, diff, report, settings, written_this_run)

    # Process deletions.
    stranded_aliases: list[str] = []
    if diff.deleted:
        stranded_aliases = _process_deletions(ws, manifest, diff.deleted, report, settings, written_this_run)

    # Self-heal stranded aliases in the same run (issue #79):
    # When canonical doc(s) are deleted, their surviving duplicate alias(es) have chunk_count=0.
    # Re-run diff to pick them up via Manifest._is_stale_alias() and re-embed them before resolving duplicates.
    changed_sources2: list[Path] = []
    if stranded_aliases:
        diff2 = manifest.diff(ws)
        changed_sources2 = diff2.added + diff2.modified
        if changed_sources2:
            touched2 = {_doc_id(path, ws) for path in changed_sources2}
            written_this_run = {k: v for k, v in written_this_run.items() if v not in touched2}
            _process_changed(ws, manifest, changed_sources2, diff2, report, settings, written_this_run)

    # Detect content_hash duplicates across doc_ids (issue #18): a doc synced just
    # now may duplicate one embedded in an earlier run, or two changed docs in this
    # same batch may duplicate each other. Runs over the whole manifest, not just
    # this batch's docs, so a late-arriving alias still finds its canonical.
    # A single bad group is isolated inside resolve_duplicates() and surfaces
    # here instead of aborting the run (§1.4 failure isolation).
    from doqqy.dedup import resolve_duplicates
    resolve_duplicates(ws, manifest, settings, failures=report.failed)

    # Guard against loops: check if any stranded aliases still remain unresolved.
    remaining_stranded = [
        alias_id
        for alias_id, entry in manifest.docs.items()
        if entry.alias_of is not None and entry.alias_of not in manifest.docs
    ]
    if remaining_stranded:
        _LOG.error(
            "Sync completed with %d stranded duplicate alias(es) (%s) whose canonical was deleted but could not be recovered.",
            len(remaining_stranded), ", ".join(sorted(remaining_stranded)),
        )

    # Adjust unchanged count: docs that were modified in pass 2 were originally counted
    # in diff.unchanged, so exclude them to reflect the actual untouched document count.
    if changed_sources2:
        reprocessed_doc_ids = {_doc_id(p, ws) for p in changed_sources2}
        report.unchanged = len([d for d in diff.unchanged if d not in reprocessed_doc_ids])

    # Persist the updated manifest atomically.
    manifest.save(ws)
    _LOG.info(
        "Sync complete: +%d ~%d -%d =%d (disambiguated: %d, failed: %d).",
        report.added, report.modified, report.deleted,
        report.unchanged, report.disambiguated, len(report.failed),
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
    written_this_run: dict[Path, str],
) -> None:
    """Ingest, chunk, and embed each changed source file."""
    from doqqy.chunk import Chunk, chunk_file
    from doqqy.infra.vectorstore.base import ChunkRecord
    from doqqy.infra.vectorstore.factory import make_store
    from doqqy.ingest import ingest_file
    from doqqy.ingest.base import IngestError, processed_id
    from doqqy.manifest import read_content_hash

    added_set = set(str(p) for p in diff.added)

    # Collect all chunks that need embedding.
    # (doc_id, content_hash, body_hash, tags, chunks) — body_hash is the
    # frontmatter content_hash (transformed markdown), the join key issue #18
    # dedup groups on; content_hash stays the raw-byte hash used for diffing.
    doc_chunks: list[tuple[str, str, str, list[str], list[Chunk]]] = []
    # Documents that ingested cleanly but produced zero chunks (empty file, blank
    # spreadsheet, …).  They still get a manifest entry with chunk_count=0 —
    # otherwise the diff would classify them as changed on every single run.
    empty_docs: list[tuple[str, str, str, list[str]]] = []  # (doc_id, content_hash, body_hash, tags)
    # doc_id -> bu çalışmada gerçekten yazılan processed/ yolu. Manifest'e ayrı bir
    # sözlükten geçiriliyor; alternatifi yukarıdaki demetleri altı elemana çıkarmaktı.
    processed_paths: dict[str, str] = {}

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
                doc_id = _doc_id(source_path, ws)

                # ingest_directory ile aynı invariant: iki belge tek bir .md
                # dosyasına yazamaz. Ad ayrıştırması çakışmaların büyük çoğunluğunu
                # çözüyor ama hepsini değil, ve sessizce ezmek burada da kabul
                # edilemez — dosya reddedilip rapora hata olarak düşer.
                target = doc.processed_path.resolve()
                clash = written_this_run.get(target)
                if clash is not None and clash != doc_id:
                    raise IngestError(
                        f"çıktı yolu çakıştı: {doc.processed_path} zaten {clash} tarafından yazıldı"
                    )

                doc.write()
                written_this_run[target] = doc_id

                # Çakışma grubu değiştiği için çıktının adı değişmiş olabilir
                # (issue #76). Eski dosya silinmezse öksüz kalır ve chunk/map/inject
                # hepsi processed/*.md taradığı için içerik indekse geri sızar.
                _drop_superseded_processed(ws, manifest.get(doc_id), doc.processed_path, written_this_run)
                processed_paths[doc_id] = processed_id(doc.processed_path, ws)
                if doc.processed_path.stem != source_path.stem:
                    report.disambiguated += 1
                    # ingest ile aynı görünürlük: CLI kullanıcıyı sync.log'a
                    # yönlendiriyor, orada gerçekten bir kayıt bulunmalı.
                    _LOG.warning(
                        "%s adı bir kardeşiyle çakıştı, çıktı %s olarak yazıldı.",
                        source_path, doc.processed_path.name,
                    )
                tags = doc.metadata.get("tags", [])
                content_hash = read_content_hash(source_path) or ""
                body_hash = doc.metadata.get("content_hash", "") or ""

                chunks = chunk_file(doc.processed_path, ws)
                if chunks:
                    doc_chunks.append((doc_id, content_hash, body_hash, tags, chunks))
                else:
                    _LOG.warning("No chunks produced for %s — recording an empty entry.", source_path)
                    empty_docs.append((doc_id, content_hash, body_hash, tags))

                is_new = str(source_path) in added_set
                if is_new:
                    report.added += 1
                else:
                    report.modified += 1

            except Exception as exc:  # noqa: BLE001
                doc_id = _doc_id(source_path, ws)
                _LOG.exception("Failed to process %s: %s", source_path, exc)
                report.failed.append((doc_id, f"{type(exc).__name__}: {exc}"))
                previous = manifest.get(doc_id)
                manifest.update_entry(doc_id, ManifestEntry(
                    source=doc_id,
                    content_hash="",
                    status="failed",
                    # Yol, dosya yazıldıktan SONRA da hata alınabildiği için
                    # bu çalışmada yazılan addan okunuyor; yalnızca hiç
                    # yazılamadıysa önceki ada düşülüyor. Ters sırada olsaydı
                    # manifest artık var olmayan bir adı gösterir ve gerçek
                    # çıktı kimsenin temizleyemeyeceği bir öksüz olurdu.
                    processed_path=processed_paths.get(
                        doc_id, previous.processed_path if previous else ""
                    ),
                ))

    # A document that used to have chunks and no longer does must lose its old
    # chunks from the store, or they would linger as orphans.
    if empty_docs:
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with contextlib.closing(make_store(ws, settings)) as store:
            for doc_id, content_hash, body_hash, tags in empty_docs:
                store.delete_by_doc(doc_id)
                manifest.update_entry(doc_id, ManifestEntry(
                    source=doc_id,
                    content_hash=content_hash,
                    tags=tags,
                    chunk_count=0,
                    status="indexed",
                    indexed_at=now,
                    body_hash=body_hash,
                    processed_path=processed_paths.get(doc_id, ""),
                ))
        _update_chunks_parquet(ws, new_records=[], removed_doc_ids={d[0] for d in empty_docs})

    if not doc_chunks:
        return

    # Embed all chunks in batches.
    all_chunks: list[Chunk] = []
    chunk_doc_map: list[int] = []  # chunk index → doc_chunks index
    for idx, (_, _, _, _, chunks) in enumerate(doc_chunks):
        for c in chunks:
            all_chunks.append(c)
            chunk_doc_map.append(idx)

    texts = [c.content for c in all_chunks]
    model = _load_embed_model()
    dense_vecs, sparse_jsons = _embed_texts(model, texts)

    # Build ChunkRecords and group by doc.
    doc_records: dict[int, list[ChunkRecord]] = {}
    all_new_records: list[ChunkRecord] = []
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
        all_new_records.append(rec)

    # Upsert into the store: delete old chunks, insert new ones.
    modified_or_added_doc_ids: set[str] = set()
    with contextlib.closing(make_store(ws, settings)) as store:
        for idx, (doc_id, content_hash, body_hash, tags, _chunks) in enumerate(doc_chunks):
            records = doc_records.get(idx, [])
            if not records:
                continue
            store.delete_by_doc(doc_id)
            store.upsert(records)
            modified_or_added_doc_ids.add(doc_id)

            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            manifest.update_entry(doc_id, ManifestEntry(
                source=doc_id,
                content_hash=content_hash,
                tags=tags,
                chunk_count=len(records),
                status="indexed",
                indexed_at=now,
                body_hash=body_hash,
                processed_path=processed_paths.get(doc_id, ""),
            ))

    # Keep chunks.parquet synchronized if it exists.
    _update_chunks_parquet(ws, all_new_records, modified_or_added_doc_ids)


def _process_deletions(
    ws: Workspace,
    manifest: Manifest,
    deleted_doc_ids: list[str],
    report: SyncReport,
    settings: Settings | None,
    written_this_run: dict[Path, str],
) -> list[str]:
    """Remove deleted documents from the store, processed files, and manifest."""
    from doqqy.infra.vectorstore.factory import make_store

    all_stranded: list[str] = []

    with contextlib.closing(make_store(ws, settings)) as store:
        for doc_id in deleted_doc_ids:
            try:
                store.delete_by_doc(doc_id)

                processed = _recorded_processed_path(ws, manifest.get(doc_id), doc_id)
                if processed is not None and processed.exists():
                    # Aynı çalışmada başka bir belge bu yola yazdıysa dosya artık
                    # ona ait: silinen kaynağın adını taşıyor olması yeterli değil.
                    # Bir kaynağın silinip yerine aynı gövde adlı bir başkasının
                    # eklendiği durumda bu kontrol olmadan yeni belgenin çıktısı
                    # anında yok edilir ve hiçbir çalışma bunu geri getirmez.
                    # Yol manifest'ten geliyor; processed/ dışına çıkan bir değer
                    # asla silinmemeli.
                    try:
                        processed.resolve().relative_to(ws.processed_dir.resolve())
                    except ValueError:
                        _LOG.warning("%s için kayıtlı yol processed/ dışında (%s), silinmedi.", doc_id, processed)
                        manifest.remove_entry(doc_id)
                        report.deleted += 1
                        continue

                    owner = written_this_run.get(processed.resolve())
                    if owner is not None:
                        _LOG.info(
                            "%s silindi ama %s bu çalışmada aynı çıktıya (%s) yazdı — dosya korunuyor.",
                            doc_id, owner, processed.name,
                        )
                    else:
                        processed.unlink()

                # Deleting a canonical (issue #18) takes the group's only copy
                # of the shared content down with it: its aliases carry
                # chunk_count=0 of their own. Detect stranded aliases so sync()
                # can re-embed them in the same run (issue #79).
                stranded = sorted(
                    alias_id
                    for alias_id, entry in manifest.docs.items()
                    if entry.alias_of == doc_id
                )
                if stranded:
                    _LOG.info(
                        "Deleted %s was the canonical copy for %d duplicate alias(es) (%s) — "
                        "re-indexing in this run.",
                        doc_id, len(stranded), ", ".join(stranded),
                    )
                    all_stranded.extend(stranded)

                manifest.remove_entry(doc_id)
                report.deleted += 1
            except Exception as exc:  # noqa: BLE001
                _LOG.exception("Failed to delete %s: %s", doc_id, exc)
                report.failed.append((doc_id, f"{type(exc).__name__}: {exc}"))

    _update_chunks_parquet(ws, new_records=[], removed_doc_ids=set(deleted_doc_ids))
    return all_stranded


def _recorded_processed_path(ws: Workspace, entry: ManifestEntry | None, doc_id: str) -> Path | None:
    """Resolve the processed/ file a document actually wrote, for a source that is already gone.

    The manifest is the only reliable answer here. Recomputing it with
    processed_path_for() would consult the source's surviving same-stem siblings
    (issue #76) and, with the source itself deleted, name a *different* file —
    leaving the real output orphaned in processed/, where chunk/map/inject would
    keep picking it up and feed deleted content straight back into the index.

    Entries written before the field existed have no recorded path, and there is
    nothing safe to put in its place: recomputing would name a file that may well
    belong to a surviving sibling, and deleting that is worse than leaving an
    orphan. Such a corpus needs the one-time upgrade step in docs/USAGE.md.
    """
    if entry is not None and entry.processed_path:
        return ws.root / Path(entry.processed_path)
    return None


def _drop_superseded_processed(
    ws: Workspace,
    entry: ManifestEntry | None,
    current: Path,
    written_this_run: dict[Path, str],
) -> None:
    """Delete the previous processed/ output when a document has just been rewritten under a new name."""
    if entry is None or not entry.processed_path:
        return

    previous = ws.root / Path(entry.processed_path)
    try:
        resolved_previous = previous.resolve()
        same = resolved_previous == current.resolve()
    except OSError:
        resolved_previous = previous
        same = previous == current
    if same or not previous.exists():
        return

    # Bu belgenin eski adı, bu çalışmada başka bir belgenin yeni adı olmuş
    # olabilir (aynı gövde adını paylaşan iki kaynak yer değiştirdiğinde).
    # O dosya artık ona ait, silinemez.
    owner = written_this_run.get(resolved_previous)
    if owner is not None:
        _LOG.info(
            "Eski çıktı %s bu çalışmada %s tarafından yeniden yazıldı — silinmiyor.",
            entry.processed_path, owner,
        )
        return

    try:
        previous.unlink()
        _LOG.info("Renamed output: %s -> %s.", entry.processed_path, current.name)
    except OSError as exc:
        # Eski çıktı silinemezse yenisi yine de yazıldı; öksüz dosyayı sessizce
        # bırakmak yerine görünür kılıyoruz (§1.4 failure isolation).
        _LOG.warning("Could not remove superseded output %s: %s", previous, exc)


def _update_chunks_parquet(
    ws: Workspace,
    new_records: list[ChunkRecord],
    removed_doc_ids: set[str],
) -> None:
    """Keep ws.chunks_parquet synchronized with vector store changes."""
    if not ws.chunks_parquet.exists():
        return

    try:
        import pandas as pd

        existing_df = pd.read_parquet(ws.chunks_parquet)
        if "doc_id" in existing_df.columns and removed_doc_ids:
            filtered_df = existing_df[~existing_df["doc_id"].isin(removed_doc_ids)].copy()
        else:
            filtered_df = existing_df

        if new_records:
            rows = [
                {
                    "chunk_id": r.chunk_id,
                    "doc_id": r.doc_id,
                    "source": r.source,
                    "doc_type": r.doc_type,
                    "tags": r.tags,
                    "content": r.content,
                    "section_path": r.section_path,
                    "char_count": r.char_count,
                    "prev_chunk": r.prev_chunk,
                    "next_chunk": r.next_chunk,
                }
                for r in new_records
            ]
            new_df = pd.DataFrame(rows)
            combined_df = pd.concat([filtered_df, new_df], ignore_index=True)
        else:
            combined_df = filtered_df

        # Atomic, same as the manifest: a crash mid-write must not be able to
        # leave a truncated parquet behind, because the previous file is the
        # only copy of the chunk table.
        fd, tmp_name = tempfile.mkstemp(
            dir=str(ws.chunks_parquet.parent), prefix=".chunks_", suffix=".tmp"
        )
        os.close(fd)
        tmp_path = Path(tmp_name)
        try:
            combined_df.to_parquet(tmp_path, index=False)
            os.replace(tmp_path, ws.chunks_parquet)
        except BaseException:
            with contextlib.suppress(OSError):
                tmp_path.unlink()
            raise

        _LOG.debug("Updated %s with %d rows.", ws.chunks_parquet, len(combined_df))
    except Exception as exc:  # noqa: BLE001
        _LOG.warning("Failed to update %s: %s", ws.chunks_parquet, exc)


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
