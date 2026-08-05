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
    if not groups:
        return groups

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

                    if tags_changed and canonical_entry.chunk_count > 0:
                        records = store.get_by_doc(group.canonical)
                        if records:
                            updated = [replace(r, tags=group.tags) for r in records]
                            store.delete_by_doc(group.canonical)
                            store.upsert(updated)
                            parquet_removed.add(group.canonical)
                            parquet_new_records.extend(updated)
                            _LOG.info(
                                "Duplicate group canonical=%s: tags -> %s (%d alias(es)).",
                                group.canonical, group.tags, len(group.aliases),
                            )

                if tags_changed or was_marked_alias:
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
