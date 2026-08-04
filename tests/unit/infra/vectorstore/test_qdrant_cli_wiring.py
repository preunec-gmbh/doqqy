"""Unit tests for factory resolution and CLI backend option wiring."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from doqqy.cli import app
from doqqy.infra.settings import Settings
from doqqy.infra.vectorstore.factory import make_store
from doqqy.infra.vectorstore.lancedb_store import LanceDBStore
from doqqy.infra.vectorstore.qdrant_store import QdrantStore
from doqqy.workspace import Workspace

runner = CliRunner()


def test_factory_resolves_lancedb(tmp_path: Path):
    """Verify factory returns LanceDBStore when vector_backend is lancedb."""
    ws = Workspace(tmp_path)
    settings = Settings(vector_backend="lancedb")
    store = make_store(ws, settings)
    assert isinstance(store, LanceDBStore)


def test_factory_resolves_qdrant(tmp_path: Path):
    """Verify factory returns QdrantStore with matching tenant key when vector_backend is qdrant."""
    ws = Workspace(tmp_path)
    settings = Settings(
        vector_backend="qdrant",
        qdrant_url="http://localhost:6333",
        qdrant_api_key="test_key",
        qdrant_collection="test_collection",
    )
    store = make_store(ws, settings)
    assert isinstance(store, QdrantStore)
    assert store.url == "http://localhost:6333"
    assert store.api_key == "test_key"
    assert store.collection == "test_collection"
    assert store.tenant_key == str(ws.root)


def test_cli_tags_command_accepts_backend_flag(tmp_path: Path):
    """Verify CLI `tags --backend` passes settings with vector_backend to make_store."""
    with patch("doqqy.infra.vectorstore.factory.make_store") as mock_make_store:
        mock_store = mock_make_store.return_value
        mock_store.list_tags.return_value = ["test-tag"]

        result = runner.invoke(app, ["tags", "--backend", "lancedb"])
        assert result.exit_code == 0
        assert "test-tag" in result.output
        mock_make_store.assert_called_once()
        call_args = mock_make_store.call_args
        passed_settings = call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get("settings")
        assert passed_settings.vector_backend == "lancedb"


def test_cli_embed_command_accepts_backend_flag(tmp_path: Path):
    """Verify CLI `embed --backend` passes settings with vector_backend to build_index."""
    with patch("doqqy.embed.build_index") as mock_build_index:
        mock_build_index.return_value = 5

        result = runner.invoke(app, ["embed", "--backend", "qdrant"])
        assert result.exit_code == 0
        assert "5 chunk" in result.output
        mock_build_index.assert_called_once()
        passed_settings = mock_build_index.call_args[1].get("settings")
        assert passed_settings is not None
        assert passed_settings.vector_backend == "qdrant"
