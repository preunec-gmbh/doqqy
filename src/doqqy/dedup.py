"""Duplicate document detection and alias resolution by body content_hash.

Two documents are duplicates only when their processed markdown bodies hash
identically (the frontmatter ``content_hash`` every ingester already writes —
see ``manifest.read_body_hash``). There is no fuzzy/near matching.

Within a duplicate group, the alphabetically-first doc_id is canonical: it
keeps the group's only chunks in the vector store. Every other member becomes
an alias — its manifest entry points at the canonical doc via ``alias_of`` and
carries no chunks of its own. The canonical's tags become the union of every
member's tags, so ``--tag`` filtering finds the shared content from any of the
duplicate's folders.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from dataclasses import field as dc_field
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from doqqy.config import get_logger
from doqqy.manifest import Manifest

if TYPE_CHECKING:
    from doqqy.infra.settings import Settings
    from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.dedup")


@dataclass
class DuplicateGroup:
    """One set of documents sharing an identical body hash."""

    canonical: str
    aliases: list[str] = dc_field(default_factory=list)
    tags: list[str] = dc_field(default_factory=list)


def find_duplicate_groups(manifest: Manifest) -> list[DuplicateGroup]:
    """Group manifest entries by body_hash. Failed/unhashed entries never participate.

    Grouping is idempotent: it is derived purely from each entry's own body_hash
    and tags, so recomputing it after a previous resolution yields the same groups.
    """
    by_hash: dict[str, list[str]] = {}
    for doc_id, entry in manifest.docs.items():
        if not entry.body_hash or entry.status == "failed":
            continue
        by_hash.setdefault(entry.body_hash, []).append(doc_id)

    groups: list[DuplicateGroup] = []
    for doc_ids in by_hash.values():
        if len(doc_ids) < 2:
            continue
        ordered = sorted(doc_ids)
        canonical, *aliases = ordered
        tags: set[str] = set()
        for doc_id in ordered:
            entry = manifest.get(doc_id)
            if entry is not None:
                tags.update(entry.tags)
        groups.append(DuplicateGroup(canonical=canonical, aliases=aliases, tags=sorted(tags)))
    return groups


def resolve_duplicates(
    ws: "Workspace",
    manifest: Manifest,
    settings: "Settings | None" = None,
    *,
    failures: list[tuple[str, str]] | None = None,
) -> list[DuplicateGroup]:
    """Detect duplicate groups in *manifest* and reconcile manifest + vector store.

    Call this after ingest/chunk/embed have written fresh manifest entries (with
    body_hash populated) for whatever changed, and before ``manifest.save(ws)``.
    Mutates *manifest* entries in place. Only touches the vector store when a
    group's resolution actually differs from the current state (a newly-arrived
    alias needs its own chunks removed, or the canonical's tag union grew).

    Failure isolation: one group failing (e.g. a transient store error) never
    aborts the others or the caller's pipeline run — see CLAUDE.md/
    DEVELOPER-HANDOVER.md §1.4 ("one bad file never aborts a batch"). The store
    side of a group is always applied before its manifest entries are touched,
    so a failed group is left exactly as it was found and gets re-evaluated
    (and retried) on the next sync/embed run. Failures are logged; pass
    *failures* to also collect them as (doc_id, message) pairs, e.g. to fold
    into a SyncReport.
    """
    groups = find_duplicate_groups(manifest)
    # No early return on an empty groups list: a doc can still be carrying a
    # stale tag union from a group that has since fully dissolved (its other
    # member(s) deleted) — the orphaned-carrier pass below needs to run even
    # when there are zero *active* groups left anywhere in the manifest.
    store = None
    parquet_removed: set[str] = set()
    parquet_new_records = []

    try:
        for group in groups:
            try:
                canonical_entry = manifest.get(group.canonical)
                if canonical_entry is None:
                    continue

                tags_changed = sorted(canonical_entry.tags) != group.tags
                was_marked_alias = canonical_entry.alias_of is not None

                newly_aliased: list[str] = []
                for alias_id in group.aliases:
                    alias_entry = manifest.get(alias_id)
                    if alias_entry is None:
                        continue
                    had_own_chunks = alias_entry.chunk_count > 0 and alias_entry.alias_of is None
                    if had_own_chunks:
                        newly_aliased.append(alias_id)

                # A tag union only needs a store write when the canonical actually
                # has chunks sitting there to re-tag; otherwise there's nothing to
                # drift out of sync with, so it's trivially "written".
                canonical_needs_store_write = tags_changed and canonical_entry.chunk_count > 0
                canonical_store_write_ok = not canonical_needs_store_write

                # Store operations first: if any of these raise, the manifest
                # below is never touched, so this group is retried cleanly
                # next run instead of drifting out of sync with the store.
                if tags_changed or newly_aliased:
                    if store is None:
                        from doqqy.infra.vectorstore.factory import make_store
                        store = make_store(ws, settings)

                    for alias_id in newly_aliased:
                        store.delete_by_doc(alias_id)
                        parquet_removed.add(alias_id)

                    if canonical_needs_store_write:
                        records = store.get_by_doc(group.canonical)
                        if records:
                            updated = [replace(r, tags=group.tags) for r in records]
                            store.delete_by_doc(group.canonical)
                            store.upsert(updated)
                            parquet_removed.add(group.canonical)
                            parquet_new_records.extend(updated)
                            canonical_store_write_ok = True
                            _LOG.info(
                                "Duplicate group canonical=%s: tags -> %s (%d alias(es)).",
                                group.canonical, group.tags, len(group.aliases),
                            )
                        else:
                            # get_by_doc came back empty despite chunk_count > 0 —
                            # store drift. Don't claim the tag union in the
                            # manifest; leave it stale so tags_changed stays True
                            # and this group is retried next run instead of the
                            # discrepancy going undetected forever.
                            _LOG.warning(
                                "Duplicate group canonical=%s: expected %d stored chunk(s) "
                                "but found none — leaving manifest tags unchanged, will retry.",
                                group.canonical, canonical_entry.chunk_count,
                            )

                # Only record what the store actually reflects: if the tag union
                # needed a store write and it didn't happen, skip the manifest
                # write entirely (including clearing alias_of) so the whole
                # canonical entry is retried cleanly next run rather than
                # partially applied.
                if canonical_store_write_ok and (tags_changed or was_marked_alias):
                    canonical_entry.tags = group.tags
                    canonical_entry.alias_of = None
                    manifest.update_entry(group.canonical, canonical_entry)

                for alias_id in group.aliases:
                    alias_entry = manifest.get(alias_id)
                    if alias_entry is None:
                        continue
                    if (
                        alias_entry.alias_of != group.canonical
                        or alias_entry.status != "aliased"
                        or alias_entry.chunk_count != 0
                    ):
                        alias_entry.alias_of = group.canonical
                        alias_entry.chunk_count = 0
                        alias_entry.status = "aliased"
                        alias_entry.indexed_at = _now()
                        manifest.update_entry(alias_id, alias_entry)

            except Exception as exc:  # noqa: BLE001 — one bad group must not abort the run
                _LOG.exception(
                    "Duplicate resolution failed for canonical=%s: %s", group.canonical, exc
                )
                if failures is not None:
                    failures.append((group.canonical, f"{type(exc).__name__}: {exc}"))
                continue

        # A group that shrinks to a single survivor (its other member(s) deleted)
        # never gets re-grouped by find_duplicate_groups — but the survivor can
        # still be carrying a tag union from members that are now gone. Shed it
        # back to the doc's own folder-derived tags. Aliases are excluded: a
        # stranded alias is Manifest.diff()'s job (it gets fully reprocessed).
        #
        # This rests on a corpus-wide invariant: a doc's tags come from its
        # folder path and nowhere else (ingest.base_metadata), so any drift
        # away from that can only be a leftover union. md_ingest deliberately
        # namespaces a user's own frontmatter keys as original_*, so a
        # hand-written `tags:` never reaches a manifest entry. If a second tag
        # source is ever introduced (frontmatter tags, manual tagging, a
        # config-level default), this pass would silently reset it on every
        # run — and for every doc in the manifest, not just former duplicate
        # carriers. Narrow the loop to docs known to have carried a union
        # before adding one.
        grouped_doc_ids: set[str] = set()
        for g in groups:
            grouped_doc_ids.add(g.canonical)
            grouped_doc_ids.update(g.aliases)

        for doc_id in list(manifest.docs.keys()):
            entry = manifest.get(doc_id)
            if entry is None or entry.alias_of is not None or doc_id in grouped_doc_ids:
                continue
            if not entry.tags:
                continue

            try:
                own_tags = _own_tags(doc_id, ws)
                if sorted(entry.tags) == sorted(own_tags):
                    continue

                needs_store_write = entry.chunk_count > 0
                store_write_ok = not needs_store_write
                if needs_store_write:
                    if store is None:
                        from doqqy.infra.vectorstore.factory import make_store
                        store = make_store(ws, settings)
                    records = store.get_by_doc(doc_id)
                    if records:
                        updated = [replace(r, tags=own_tags) for r in records]
                        store.delete_by_doc(doc_id)
                        store.upsert(updated)
                        parquet_removed.add(doc_id)
                        parquet_new_records.extend(updated)
                        store_write_ok = True
                        _LOG.info(
                            "Orphaned duplicate carrier %s: tags %s -> %s (other group member(s) gone).",
                            doc_id, entry.tags, own_tags,
                        )
                    else:
                        _LOG.warning(
                            "Orphaned duplicate carrier %s: expected %d stored chunk(s) but "
                            "found none — leaving manifest tags unchanged, will retry.",
                            doc_id, entry.chunk_count,
                        )

                if store_write_ok:
                    entry.tags = own_tags
                    manifest.update_entry(doc_id, entry)

            except Exception as exc:  # noqa: BLE001 — one bad doc must not abort the run
                _LOG.exception("Failed to shed stale tag union for %s: %s", doc_id, exc)
                if failures is not None:
                    failures.append((doc_id, f"{type(exc).__name__}: {exc}"))
                continue
    finally:
        if store is not None:
            store.close()

    if parquet_removed or parquet_new_records:
        # _update_chunks_parquet already catches and logs its own failures
        # (see sync.py) — chunks.parquet is a best-effort mirror of the store.
        from doqqy.sync import _update_chunks_parquet
        _update_chunks_parquet(ws, parquet_new_records, parquet_removed)

    return groups


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _own_tags(doc_id: str, ws: "Workspace") -> list[str]:
    """A document's own folder-derived tags, independent of any union pollution.

    Pure path parsing — base_metadata() derives tags from doc_id's folder
    structure alone, no file I/O — so this is safe to call even for a doc_id
    whose canonical/co-aliases have since been deleted.
    """
    from doqqy.ingest.base import base_metadata
    return base_metadata(Path(doc_id), ws.root, kind="md")["tags"]
