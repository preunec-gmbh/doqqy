"""Real-adapter round-trip coverage for ``doqqy migrate-store`` CLI."""

from __future__ import annotations

import importlib.util
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
from uuid import UUID

import numpy as np
import pytest
from typer.testing import CliRunner

from doqqy.cli import app
from doqqy.config import EMBEDDING_DIM
from doqqy.infra.vectorstore.base import ChunkRecord
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore
from doqqy.infra.vectorstore.qdrant_store import QdrantStore

HAS_QDRANT_CLIENT = importlib.util.find_spec("qdrant_client") is not None
runner = CliRunner()


def _records() -> list[ChunkRecord]:
    chunk_ids = [str(UUID(int=i + 1)) for i in range(5)]
    return [
        ChunkRecord(
            chunk_id=chunk_id,
            doc_id=f"doc-{i // 2}",
            source=f"raw/topic/doc-{i // 2}.md",
            doc_type="markdown",
            tags=["topic", f"sample-{i}"],
            content=f"Migration sample content {i}",
            section_path=["Root", f"Section {i}"],
            char_count=26,
            prev_chunk=chunk_ids[i - 1] if i else None,
            next_chunk=chunk_ids[i + 1] if i < len(chunk_ids) - 1 else None,
            dense=np.full(EMBEDDING_DIM, i + 0.25, dtype=np.float32),
            sparse={100 + i: i + 0.5, 200 + i: i + 1.5},
        )
        for i, chunk_id in enumerate(chunk_ids)
    ]


def _assert_sampled_records(
    actual: list[ChunkRecord], expected: list[ChunkRecord]
) -> None:
    assert len(actual) == len(expected)
    actual_by_id = {record.chunk_id: record for record in actual}
    for wanted in (expected[0], expected[len(expected) // 2], expected[-1]):
        got = actual_by_id[wanted.chunk_id]
        assert replace(got, dense=None) == replace(wanted, dense=None)
        assert np.array_equal(got.dense, wanted.dense)


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_cli_round_trip_lancedb_qdrant_lancedb_preserves_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Exercise both real adapters without a Qdrant server or embedding model."""
    from qdrant_client import QdrantClient

    lance_path = tmp_path / ".doqqy" / "store.lance"
    qdrant_path = tmp_path / "qdrant-local"
    collection = "migration_round_trip"
    tenant = str(tmp_path)
    expected = _records()

    seed = LanceDBStore(lance_path)
    seed.full_rebuild(expected, dim=EMBEDDING_DIM)
    seed.close()

    def real_store(_ws, settings):
        if settings.vector_backend == "lancedb":
            return LanceDBStore(lance_path)
        store = QdrantStore("http://unused", "", collection, tenant)
        store._client_instance = QdrantClient(path=str(qdrant_path))
        return store

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DOQQY_VECTOR_BACKEND", "lancedb")
    with patch("doqqy.infra.vectorstore.factory.make_store", side_effect=real_store):
        outward = runner.invoke(app, ["migrate-store", "--to", "qdrant", "--batch", "2"])
    assert outward.exit_code == 0, outward.output

    qdrant = real_store(None, type("Settings", (), {"vector_backend": "qdrant"})())
    qdrant_records = [record for batch in qdrant.iter_records(batch_size=2) for record in batch]
    assert qdrant.count() == len(expected)
    _assert_sampled_records(qdrant_records, expected)
    qdrant.close()

    monkeypatch.setenv("DOQQY_VECTOR_BACKEND", "qdrant")
    with patch("doqqy.infra.vectorstore.factory.make_store", side_effect=real_store):
        rollback = runner.invoke(app, ["migrate-store", "--to", "lancedb", "--batch", "3"])
    assert rollback.exit_code == 0, rollback.output

    restored = LanceDBStore(lance_path)
    restored_records = [record for batch in restored.iter_records(batch_size=2) for record in batch]
    assert restored.count() == len(expected)
    _assert_sampled_records(restored_records, expected)
    restored.close()
