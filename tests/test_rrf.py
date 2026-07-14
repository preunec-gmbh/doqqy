"""RRF birleştirme testi — bkz. docs/DEVELOPER-HANDOVER.md §5."""

from __future__ import annotations

from doqqy.infra.vectorstore.lancedb_store import _rrf


def test_rrf_rewards_presence_in_both_lists():
    dense = [{"chunk_id": "a"}, {"chunk_id": "b"}]
    sparse = [{"chunk_id": "b"}, {"chunk_id": "c"}]
    fused = _rrf(dense, sparse)
    assert fused[0]["chunk_id"] == "b"  # iki listede de var → en üstte
    assert {r["chunk_id"] for r in fused} == {"a", "b", "c"}
