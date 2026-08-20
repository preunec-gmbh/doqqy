"""CLI tests for lossless, backend-agnostic vector-store migration."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import replace
from unittest.mock import patch

import numpy as np
import pytest
from typer.testing import CliRunner

from doqqy.cli import app
from doqqy.infra.vectorstore.base import ChunkRecord

runner = CliRunner()


class MemoryStore:
    """Small port-compatible store used to exercise the CLI migration flow."""

    def __init__(self, records: Sequence[ChunkRecord] = ()) -> None:
        self.records = list(records)
        self.recreated_with: int | None = None
        self.closed = False

    def count(self) -> int:
        return len(self.records)

    def recreate(self, dim: int) -> None:
        self.recreated_with = dim
        self.records.clear()

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        self.records.extend(records)
        return len(records)

    def iter_records(self, batch_size: int = 256) -> Iterator[Sequence[ChunkRecord]]:
        snapshot = list(self.records)
        for offset in range(0, len(snapshot), batch_size):
            yield snapshot[offset : offset + batch_size]

    def close(self) -> None:
        self.closed = True


def _records() -> list[ChunkRecord]:
    return [
        ChunkRecord(
            chunk_id=f"chunk-{i}",
            doc_id=f"doc-{i // 2}",
            source=f"raw/doc-{i // 2}.md",
            doc_type="markdown",
            tags=["docs", f"tag-{i}"],
            content=f"Content {i}",
            section_path=["Root", f"Section {i}"],
            char_count=9,
            prev_chunk=f"chunk-{i - 1}" if i else None,
            next_chunk=f"chunk-{i + 1}" if i < 4 else None,
            dense=np.asarray([i + 0.1, i + 0.2, i + 0.3], dtype=np.float32),
            sparse={100 + i: i + 0.5},
        )
        for i in range(5)
    ]


def _assert_records_equal(actual: Sequence[ChunkRecord], expected: Sequence[ChunkRecord]) -> None:
    assert len(actual) == len(expected)
    for got, want in zip(actual, expected, strict=True):
        assert replace(got, dense=None) == replace(want, dense=None)
        assert np.array_equal(got.dense, want.dense)


def test_migrate_store_round_trip_preserves_every_field(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = _records()
    stores = {"lancedb": MemoryStore(original), "qdrant": MemoryStore()}

    def fake_make_store(_ws, settings):
        return stores[settings.vector_backend]

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DOQQY_VECTOR_BACKEND", "lancedb")
    with patch("doqqy.infra.vectorstore.factory.make_store", side_effect=fake_make_store):
        outward = runner.invoke(app, ["migrate-store", "--to", "qdrant", "--batch", "2"])

    assert outward.exit_code == 0, outward.output
    assert "5 chunk" in outward.output
    _assert_records_equal(stores["qdrant"].records, original)

    # Simulate selecting Qdrant as the current backend for the rollback command.
    stores["lancedb"] = MemoryStore()
    monkeypatch.setenv("DOQQY_VECTOR_BACKEND", "qdrant")
    with patch("doqqy.infra.vectorstore.factory.make_store", side_effect=fake_make_store):
        rollback = runner.invoke(app, ["migrate-store", "--to", "lancedb", "--batch", "3"])

    assert rollback.exit_code == 0, rollback.output
    assert "qdrant → lancedb" in rollback.output
    _assert_records_equal(stores["lancedb"].records, original)


def test_migrate_store_refuses_same_backend(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DOQQY_VECTOR_BACKEND", "lancedb")

    with patch("doqqy.infra.vectorstore.factory.make_store") as make_store:
        result = runner.invoke(app, ["migrate-store", "--to", "lancedb"])

    assert result.exit_code == 1
    assert "Kaynak ve hedef backend aynı" in result.output
    make_store.assert_not_called()


def test_migrate_store_delegates_future_backend_resolution_to_factory(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The CLI must not maintain its own adapter allow-list."""
    source = MemoryStore(_records())
    future = MemoryStore()

    def fake_make_store(_ws, settings):
        return source if settings.vector_backend == "lancedb" else future

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DOQQY_VECTOR_BACKEND", "lancedb")
    with patch("doqqy.infra.vectorstore.factory.make_store", side_effect=fake_make_store):
        result = runner.invoke(app, ["migrate-store", "--to", "future-adapter", "--batch", "2"])

    assert result.exit_code == 0, result.output
    assert "lancedb → future-adapter" in result.output
    _assert_records_equal(future.records, source.records)


def test_migrate_store_failure_reports_partial_destination_and_untouched_source(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = _records()
    source = MemoryStore(original)

    class FailingDestination(MemoryStore):
        def upsert(self, records: Sequence[ChunkRecord]) -> int:
            if self.records:
                raise RuntimeError("Qdrant bağlantısı kesildi")
            return super().upsert(records)

    destination = FailingDestination()
    stores = {"lancedb": source, "qdrant": destination}

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DOQQY_VECTOR_BACKEND", "lancedb")
    with patch(
        "doqqy.infra.vectorstore.factory.make_store",
        side_effect=lambda _ws, settings: stores[settings.vector_backend],
    ):
        result = runner.invoke(app, ["migrate-store", "--to", "qdrant", "--batch", "2"])

    output = " ".join(result.output.split())
    assert result.exit_code == 1
    assert "Migration başarısız" in output
    assert "yalnızca 2 kayıt taşınmış olabilir" in output
    assert "Kaynak lancedb store'una dokunulmadı" in output
    assert "doqqy embed --backend qdrant" in output
    _assert_records_equal(source.records, original)
    assert len(destination.records) == 2
    assert source.closed and destination.closed
