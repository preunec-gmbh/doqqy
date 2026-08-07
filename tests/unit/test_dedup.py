"""Unit tests for doqqy.dedup (issue #18: dedup identical documents by content_hash)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from doqqy.dedup import find_duplicate_groups, resolve_duplicates
from doqqy.infra.vectorstore.base import ChunkRecord, TagFilter
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore
from doqqy.manifest import Manifest, ManifestEntry
from doqqy.workspace import Workspace


@pytest.fixture
def temp_ws(tmp_path: Path) -> Workspace:
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    return ws


def _entry(**overrides) -> ManifestEntry:
    defaults = dict(
        source="raw/x.md",
        content_hash="raw-bytes-hash",
        tags=[],
        chunk_count=1,
        status="indexed",
        body_hash="",
    )
    defaults.update(overrides)
    return ManifestEntry(**defaults)


# ---------------------------------------------------------------------------
# find_duplicate_groups — pure manifest logic, no store involved
# ---------------------------------------------------------------------------


def test_find_duplicate_groups_basic() -> None:
    manifest = Manifest()
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1"))
    manifest.update_entry("raw/b/x.md", _entry(tags=["b"], body_hash="H1"))
    manifest.update_entry("raw/c/y.md", _entry(tags=["c"], body_hash="H2"))

    groups = find_duplicate_groups(manifest)

    assert len(groups) == 1
    group = groups[0]
    assert group.canonical == "raw/a/x.md"
    assert group.aliases == ["raw/b/x.md"]
    assert group.tags == ["a", "b"]


def test_find_duplicate_groups_picks_alphabetically_first_as_canonical() -> None:
    manifest = Manifest()
    manifest.update_entry("raw/z/x.md", _entry(tags=["z"], body_hash="H1"))
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1"))
    manifest.update_entry("raw/m/x.md", _entry(tags=["m"], body_hash="H1"))

    groups = find_duplicate_groups(manifest)

    assert len(groups) == 1
    assert groups[0].canonical == "raw/a/x.md"
    assert groups[0].aliases == ["raw/m/x.md", "raw/z/x.md"]
    assert groups[0].tags == ["a", "m", "z"]


def test_find_duplicate_groups_ignores_blank_and_failed() -> None:
    manifest = Manifest()
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1"))
    manifest.update_entry("raw/b/x.md", _entry(tags=["b"], body_hash="H1", status="failed"))
    manifest.update_entry("raw/c/x.md", _entry(tags=["c"], body_hash=""))

    groups = find_duplicate_groups(manifest)

    assert groups == []


def test_find_duplicate_groups_no_duplicates() -> None:
    manifest = Manifest()
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1"))
    manifest.update_entry("raw/b/y.md", _entry(tags=["b"], body_hash="H2"))

    assert find_duplicate_groups(manifest) == []


# ---------------------------------------------------------------------------
# resolve_duplicates — mutates manifest + reconciles the vector store
# ---------------------------------------------------------------------------


def _dim() -> int:
    return 8


def _record(chunk_id: str, doc_id: str, tags: list[str]) -> ChunkRecord:
    rng = np.random.default_rng(abs(hash(chunk_id)) % (2**32))
    return ChunkRecord(
        chunk_id=chunk_id,
        doc_id=doc_id,
        source=doc_id,
        doc_type="md",
        tags=tags,
        content=f"content for {chunk_id}",
        section_path=[],
        char_count=20,
        prev_chunk=None,
        next_chunk=None,
        dense=rng.random(_dim(), dtype=np.float32),
        sparse={1: 0.5},
    )


def test_resolve_duplicates_aliases_and_unions_tags(temp_ws: Workspace) -> None:
    # Simulate the same-batch scenario: both docs already got embedded under
    # their own doc_id (as sync/embed would before dedup runs), then dedup
    # must fold "raw/b/x.md" into "raw/a/x.md" and union the tags.
    store = LanceDBStore(temp_ws.store_dir)
    store.recreate(dim=_dim())
    store.upsert([_record("c-a", "raw/a/x.md", ["a"]), _record("c-b", "raw/b/x.md", ["b"])])
    store.close()

    manifest = Manifest()
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1", chunk_count=1))
    manifest.update_entry("raw/b/x.md", _entry(tags=["b"], body_hash="H1", chunk_count=1))

    groups = resolve_duplicates(temp_ws, manifest, settings=None)

    assert len(groups) == 1
    canonical = manifest.get("raw/a/x.md")
    alias = manifest.get("raw/b/x.md")

    assert canonical is not None and canonical.tags == ["a", "b"]
    assert canonical.alias_of is None
    assert alias is not None
    assert alias.alias_of == "raw/a/x.md"
    assert alias.chunk_count == 0
    assert alias.status == "aliased"

    # Store must end up with exactly one embedded copy, tagged with the union.
    store = LanceDBStore(temp_ws.store_dir)
    assert store.count() == 1
    remaining = store.get_by_doc("raw/a/x.md")
    assert len(remaining) == 1
    assert remaining[0].tags == ["a", "b"]
    assert store.get_by_doc("raw/b/x.md") == []
    store.close()


def test_resolve_duplicates_idempotent(temp_ws: Workspace) -> None:
    store = LanceDBStore(temp_ws.store_dir)
    store.recreate(dim=_dim())
    store.upsert([_record("c-a", "raw/a/x.md", ["a"]), _record("c-b", "raw/b/x.md", ["b"])])
    store.close()

    manifest = Manifest()
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1", chunk_count=1))
    manifest.update_entry("raw/b/x.md", _entry(tags=["b"], body_hash="H1", chunk_count=1))

    resolve_duplicates(temp_ws, manifest, settings=None)
    first_pass_tags = manifest.get("raw/a/x.md").tags

    # A second pass over the already-resolved manifest must be a no-op.
    resolve_duplicates(temp_ws, manifest, settings=None)

    assert manifest.get("raw/a/x.md").tags == first_pass_tags
    store = LanceDBStore(temp_ws.store_dir)
    assert store.count() == 1
    store.close()


def test_resolve_duplicates_query_hits_by_either_tag(temp_ws: Workspace) -> None:
    """Acceptance criterion: a query filtered by either folder's tag hits the deduped doc."""
    store = LanceDBStore(temp_ws.store_dir)
    store.recreate(dim=_dim())
    store.upsert([_record("c-a", "raw/a/x.md", ["a"]), _record("c-b", "raw/b/x.md", ["b"])])
    store.close()

    manifest = Manifest()
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1", chunk_count=1))
    manifest.update_entry("raw/b/x.md", _entry(tags=["b"], body_hash="H1", chunk_count=1))
    resolve_duplicates(temp_ws, manifest, settings=None)

    store = LanceDBStore(temp_ws.store_dir)
    query_vec = np.zeros(_dim(), dtype=np.float32)
    for tag in ("a", "b"):
        hits = store.hybrid_search(query_vec, {1: 0.5}, limit=5, flt=TagFilter(tags=(tag,)))
        assert len(hits) == 1
        assert hits[0].record.doc_id == "raw/a/x.md"
        assert hits[0].record.tags == ["a", "b"]

    # A tag that was never on either folder must not match.
    no_hits = store.hybrid_search(query_vec, {1: 0.5}, limit=5, flt=TagFilter(tags=("c",)))
    assert no_hits == []
    store.close()


def test_resolve_duplicates_isolates_a_failing_group(temp_ws: Workspace) -> None:
    """One group's store error must not abort the others or the whole manifest write.

    Mirrors the project's failure-isolation rule (CLAUDE.md / DEVELOPER-HANDOVER §1.4:
    "one bad file never aborts a batch"). A failing group is left exactly as found
    (retried next run); other groups still resolve.
    """
    manifest = Manifest()
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1", chunk_count=1))
    manifest.update_entry("raw/b/x.md", _entry(tags=["b"], body_hash="H1", chunk_count=1))
    manifest.update_entry("raw/c/y.md", _entry(tags=["c"], body_hash="H2", chunk_count=1))
    manifest.update_entry("raw/d/y.md", _entry(tags=["d"], body_hash="H2", chunk_count=1))

    mock_store = MagicMock()

    def get_by_doc(doc_id: str) -> list[ChunkRecord]:
        # Real record for the group that must succeed (H2's canonical); empty
        # elsewhere so a get_by_doc call never crashes on the failing group.
        if doc_id == "raw/c/y.md":
            return [_record("c1", "raw/c/y.md", ["c"])]
        return []

    mock_store.get_by_doc.side_effect = get_by_doc

    def flaky_delete_by_doc(doc_id: str) -> int:
        if doc_id == "raw/b/x.md":
            raise RuntimeError("simulated store outage")
        return 1

    mock_store.delete_by_doc.side_effect = flaky_delete_by_doc

    failures: list[tuple[str, str]] = []
    with patch("doqqy.infra.vectorstore.factory.make_store", return_value=mock_store):
        groups = resolve_duplicates(temp_ws, manifest, settings=None, failures=failures)

    assert len(groups) == 2  # both groups are still *detected*
    assert len(failures) == 1
    assert failures[0][0] == "raw/a/x.md"

    # Group H1 failed — left untouched, will be retried next run.
    assert manifest.get("raw/a/x.md").tags == ["a"]
    assert manifest.get("raw/a/x.md").alias_of is None
    assert manifest.get("raw/b/x.md").alias_of is None
    assert manifest.get("raw/b/x.md").status != "aliased"

    # Group H2 succeeded despite H1's failure.
    assert manifest.get("raw/c/y.md").tags == ["c", "d"]
    assert manifest.get("raw/d/y.md").alias_of == "raw/c/y.md"
    assert manifest.get("raw/d/y.md").status == "aliased"


def test_resolve_duplicates_does_not_claim_tag_union_when_store_write_fails(temp_ws: Workspace) -> None:
    """Review fix: if get_by_doc comes back empty despite chunk_count > 0 (store
    drift), the manifest must not claim the tag union reached the store — otherwise
    tags_changed goes False and the discrepancy is never retried."""
    manifest = Manifest()
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1", chunk_count=1))
    manifest.update_entry("raw/b/x.md", _entry(tags=["b"], body_hash="H1", chunk_count=0, status="ingested"))

    mock_store = MagicMock()
    mock_store.get_by_doc.return_value = []  # drift: nothing found despite chunk_count=1

    with patch("doqqy.infra.vectorstore.factory.make_store", return_value=mock_store):
        resolve_duplicates(temp_ws, manifest, settings=None)

        # Tags were NOT updated in the manifest — the store never actually got them.
        assert manifest.get("raw/a/x.md").tags == ["a"]
        mock_store.upsert.assert_not_called()

        # A second run must retry (tags_changed is still True), not silently give up.
        mock_store.get_by_doc.return_value = [
            ChunkRecord(
                chunk_id="c1", doc_id="raw/a/x.md", source="raw/a/x.md", doc_type="md",
                tags=["a"], content="x", section_path=[], char_count=1,
                prev_chunk=None, next_chunk=None,
                dense=np.zeros(8, dtype=np.float32), sparse={},
            )
        ]
        resolve_duplicates(temp_ws, manifest, settings=None)

    assert manifest.get("raw/a/x.md").tags == ["a", "b"]
    mock_store.upsert.assert_called_once()


def test_resolve_duplicates_no_groups_leaves_manifest_untouched(temp_ws: Workspace) -> None:
    manifest = Manifest()
    manifest.update_entry("raw/a/x.md", _entry(tags=["a"], body_hash="H1"))
    manifest.update_entry("raw/b/y.md", _entry(tags=["b"], body_hash="H2"))

    groups = resolve_duplicates(temp_ws, manifest, settings=None)

    assert groups == []
    assert manifest.get("raw/a/x.md").alias_of is None
    assert manifest.get("raw/b/y.md").alias_of is None
