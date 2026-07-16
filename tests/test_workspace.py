"""Workspace testleri — yol türetimi + aynı process'te çoklu-korpus izolasyonu (B2 regresyonu).

Dikkat: hiçbir test monkeypatch.chdir kullanmaz — doqqy modülleri import
anında cwd'ye bağımlı olmamalı; Workspace açıkça verilir.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doqqy.workspace import Workspace


def _make_workspace(tmp_path: Path, name: str) -> Workspace:
    ws = Workspace(tmp_path / name)
    ws.ensure_dirs()
    return ws


def test_path_properties_derive_from_root(tmp_path):
    ws = Workspace(tmp_path)
    assert ws.raw_dir == tmp_path / "raw"
    assert ws.processed_dir == tmp_path / "processed"
    assert ws.state_dir == tmp_path / ".doqqy"
    assert ws.chunks_parquet == tmp_path / ".doqqy" / "chunks" / "chunks.parquet"
    assert ws.store_dir == tmp_path / ".doqqy" / "store.lance"
    assert ws.topics_yaml == tmp_path / ".doqqy" / "topics.yaml"
    assert ws.logs_dir == tmp_path / ".doqqy" / "logs"
    assert ws.manifest_path == tmp_path / ".doqqy" / "manifest.json"


def test_ensure_dirs_creates_layout(tmp_path):
    ws = Workspace(tmp_path / "corpus")
    ws.ensure_dirs()
    for d in (ws.raw_dir, ws.processed_dir, ws.state_dir, ws.chunks_parquet.parent, ws.logs_dir):
        assert d.is_dir()


def test_workspace_is_frozen(tmp_path):
    ws = Workspace(tmp_path)
    with pytest.raises(Exception):    # noqa: B017
        ws.root = tmp_path / "other"  # type: ignore[misc]


def test_two_workspaces_ingest_and_chunk_without_crosstalk(tmp_path):
    """B2 regresyonu (pipeline tarafı): aynı process'te iki korpus karışmamalı."""
    import pandas as pd

    from doqqy.chunk import chunk_directory
    from doqqy.ingest import ingest_directory

    ws_a = _make_workspace(tmp_path, "corpus_a")
    ws_b = _make_workspace(tmp_path, "corpus_b")

    (ws_a.raw_dir / "alpha.md").write_text("# Alpha\n\nalpha-only-content\n", encoding="utf-8")
    (ws_b.raw_dir / "beta.md").write_text("# Beta\n\nbeta-only-content\n", encoding="utf-8")

    result_a = ingest_directory(ws_a)
    result_b = ingest_directory(ws_b)
    assert not result_a.failed and not result_b.failed

    assert (ws_a.processed_dir / "alpha.md").exists()
    assert not (ws_a.processed_dir / "beta.md").exists()
    assert (ws_b.processed_dir / "beta.md").exists()
    assert not (ws_b.processed_dir / "alpha.md").exists()

    chunks_a = chunk_directory(ws_a)
    chunks_b = chunk_directory(ws_b)

    assert all("alpha" in c.content for c in chunks_a)
    assert all("beta" in c.content for c in chunks_b)

    df_a = pd.read_parquet(ws_a.chunks_parquet)
    df_b = pd.read_parquet(ws_b.chunks_parquet)
    assert df_a["content"].str.contains("alpha-only-content").any()
    assert not df_a["content"].str.contains("beta-only-content").any()
    assert df_b["content"].str.contains("beta-only-content").any()
    assert not df_b["content"].str.contains("alpha-only-content").any()


def test_table_cache_is_per_workspace(tmp_path):
    """B2 regression (store side): _table cache must isolate handles by store directory."""
    import lancedb

    from doqqy.infra.vectorstore.lancedb_store import LanceDBStore, invalidate_table_cache_by_path

    ws_a = _make_workspace(tmp_path, "corpus_a")
    ws_b = _make_workspace(tmp_path, "corpus_b")

    def _seed(ws: Workspace, rows: int) -> None:
        db = lancedb.connect(ws.store_dir)
        data = [
            {"chunk_id": f"{ws.root.name}-{i}", "content": f"row {i}", "vector": [float(i), 0.0]}
            for i in range(rows)
        ]
        db.create_table("chunks", data=data, mode="overwrite")

    _seed(ws_a, 2)
    _seed(ws_b, 5)

    store_a = LanceDBStore(ws_a.store_dir)
    store_b = LanceDBStore(ws_b.store_dir)

    table_a = store_a._table()
    table_b = store_b._table()

    assert table_a.count_rows() == 2
    assert table_b.count_rows() == 5

    # Repeated calls should return same handle from cache
    assert store_a._table() is table_a
    assert store_b._table() is table_b

    invalidate_table_cache_by_path(ws_a.store_dir)
    assert store_b._table() is table_b
    assert store_a._table() is not table_a
    assert store_a._table().count_rows() == 2
