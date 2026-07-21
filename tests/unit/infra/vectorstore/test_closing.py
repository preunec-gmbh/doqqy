"""Unit tests verifying contextlib.closing usage and call-site store cleanup.

Guarantees that store.close() is unconditionally invoked upon exiting a `with contextlib.closing(store)` block,
both on normal completion and when exceptions occur across all production call sites:
- query.search()
- map_gen._pass2()
- embed.build_index()
- cli.tags()
"""

from __future__ import annotations

import contextlib
from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import typer

from doqqy.cli import tags as cli_tags
from doqqy.embed import build_index
from doqqy.infra.vectorstore.base import ChunkRecord, ScoredChunk, TagFilter
from doqqy.map_gen import _pass2
from doqqy.query import search
from doqqy.workspace import Workspace

# ---------------------------------------------------------------------------
# Duck-Typed Spy VectorStore Implementation (No nominal Protocol inheritance)
# ---------------------------------------------------------------------------

class SpyVectorStore:
    """Duck-typed spy implementation of VectorStore (no Protocol inheritance).

    Verifies that the port contract relies on structural typing and that close()
    is called unconditionally by contextlib.closing.
    """

    def __init__(self) -> None:
        self.close_called = False

    def recreate(self, dim: int) -> None:
        pass

    def upsert(self, records: Sequence[ChunkRecord]) -> int:
        return len(records)

    def full_rebuild(self, records: Sequence[ChunkRecord], dim: int) -> int:
        return len(records)

    def delete_by_doc(self, doc_id: str) -> int:
        return 0

    def hybrid_search(
        self,
        dense: np.ndarray,
        sparse: dict[int, float],
        *,
        limit: int,
        flt: TagFilter | None = None,
    ) -> list[ScoredChunk]:
        return []

    def get_by_ids(self, chunk_ids: Sequence[str]) -> list[ChunkRecord]:
        return []

    def all_vectors(self, flt: TagFilter | None = None) -> tuple[np.ndarray, list[ChunkRecord]]:
        return np.zeros((0, 1024), dtype=np.float32), []

    def list_tags(self) -> list[str]:
        return []

    def count(self) -> int:
        return 0

    def close(self) -> None:
        self.close_called = True


# ---------------------------------------------------------------------------
# Test Suites
# ---------------------------------------------------------------------------

class TestClosingVectorStoreContract:
    """Verify contextlib.closing behavior on duck-typed VectorStore objects."""

    def test_spy_store_normal_exit_calls_close(self) -> None:
        """Exiting a contextlib.closing block normally must call close()."""
        store = SpyVectorStore()
        assert not store.close_called

        with contextlib.closing(store) as s:
            assert s is store
            assert not store.close_called

        assert store.close_called

    def test_spy_store_exception_exit_calls_close(self) -> None:
        """An exception raised inside contextlib.closing must still trigger close()."""
        store = SpyVectorStore()

        with pytest.raises(RuntimeError, match="Operation failed"):
            with contextlib.closing(store):
                raise RuntimeError("Operation failed")

        assert store.close_called


class TestProductionCallSitesCleanupOnException:
    """Verify that all production call sites invoke store.close() when an exception occurs."""

    def test_query_search_closes_store_when_hybrid_search_raises(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """query.search() must close the store if store.hybrid_search raises an exception."""
        ws = Workspace(tmp_path)
        spy = SpyVectorStore()

        def raise_on_search(*_args, **_kwargs):
            raise RuntimeError("hybrid_search database failure")

        monkeypatch.setattr(spy, "hybrid_search", raise_on_search)
        monkeypatch.setattr("doqqy.query._embed_query", lambda _q: (np.zeros(1024, dtype=np.float32), {1: 0.5}))
        monkeypatch.setattr("doqqy.infra.vectorstore.factory.make_store", lambda _ws, _s=None: spy)

        assert not spy.close_called
        with pytest.raises(RuntimeError, match="hybrid_search database failure"):
            search(ws, "test query", rerank=False)

        assert spy.close_called

    def test_map_gen_pass2_closes_store_when_all_vectors_raises(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """map_gen._pass2() must close the store if store.all_vectors raises an exception."""
        ws = Workspace(tmp_path)
        spy = SpyVectorStore()

        def raise_on_all_vectors(*_args, **_kwargs):
            raise RuntimeError("all_vectors database failure")

        monkeypatch.setattr(spy, "all_vectors", raise_on_all_vectors)
        monkeypatch.setattr("doqqy.infra.vectorstore.factory.make_store", lambda _ws, _s=None: spy)

        assert not spy.close_called
        sec_centroids = {"sec1": (np.zeros(1024, dtype=np.float32), "file.md")}
        with pytest.raises(RuntimeError, match="all_vectors database failure"):
            _pass2(ws, sec_centroids)

        assert spy.close_called

    def test_embed_build_index_closes_store_when_full_rebuild_raises(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """embed.build_index() must close the store if store.full_rebuild raises an exception."""
        ws = Workspace(tmp_path)
        spy = SpyVectorStore()

        def raise_on_rebuild(*_args, **_kwargs):
            raise RuntimeError("full_rebuild database failure")

        df_chunks = pd.DataFrame([{
            "chunk_id": "c1",
            "doc_id": "d1",
            "source": "source.md",
            "doc_type": "md",
            "tags": ["tag1"],
            "content": "sample chunk content",
            "section_path": ["header"],
            "char_count": 20,
            "prev_chunk": None,
            "next_chunk": None,
        }])

        monkeypatch.setattr(spy, "full_rebuild", raise_on_rebuild)
        monkeypatch.setattr("doqqy.embed._load_chunks", lambda _ws: df_chunks)
        monkeypatch.setattr("doqqy.embed._load_model", lambda: "dummy_model")
        monkeypatch.setattr("doqqy.embed._embed_texts", lambda _m, _t: (
            np.zeros((1, 1024), dtype=np.float32),
            ['{"1": 0.5}'],
        ))
        monkeypatch.setattr("doqqy.infra.vectorstore.factory.make_store", lambda _ws, _s=None: spy)

        assert not spy.close_called
        with pytest.raises(RuntimeError, match="full_rebuild database failure"):
            build_index(ws)

        assert spy.close_called

    def test_cli_tags_closes_store_when_list_tags_raises(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """cli.tags() must close the store and catch errors clean if store.list_tags raises an exception."""
        ws = Workspace(tmp_path)
        spy = SpyVectorStore()

        def raise_on_list_tags(*_args, **_kwargs):
            raise RuntimeError("list_tags database failure")

        monkeypatch.setattr(spy, "list_tags", raise_on_list_tags)
        monkeypatch.setattr("doqqy.cli._workspace", lambda: ws)
        monkeypatch.setattr("doqqy.infra.vectorstore.factory.make_store", lambda _ws, _s=None: spy)

        assert not spy.close_called
        with pytest.raises(typer.Exit):
            cli_tags(backend=None)

        assert spy.close_called
