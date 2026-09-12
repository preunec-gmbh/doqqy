"""Unit coverage for MCP process startup invariants."""

from __future__ import annotations

import builtins
import importlib.util
import logging
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

pytest.importorskip("mcp.server.fastmcp")

from doqqy import config, mcp_server


def test_mcp_quiets_progress_before_model_imports(monkeypatch) -> None:
    """Progress suppression must be active before model modules execute."""
    monkeypatch.setenv("HF_HUB_DISABLE_PROGRESS_BARS", "0")
    monkeypatch.setenv("TQDM_DISABLE", "0")

    disable_progress_bar = Mock()
    fake_transformers = SimpleNamespace(
        utils=SimpleNamespace(
            logging=SimpleNamespace(disable_progress_bar=disable_progress_bar),
        ),
    )
    real_import = builtins.__import__

    def checked_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in {"FlagEmbedding", "transformers"}:
            assert config.os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] == "1"
            assert config.os.environ["TQDM_DISABLE"] == "1"
            return SimpleNamespace() if name == "FlagEmbedding" else fake_transformers
        if name in {"doqqy.query", "doqqy.rerank"}:
            return SimpleNamespace()
        if name == "doqqy.infra.vectorstore":
            return SimpleNamespace(factory=SimpleNamespace())
        return real_import(name, globals, locals, fromlist, level)

    server = SimpleNamespace(run=Mock())
    monkeypatch.setattr(builtins, "__import__", checked_import)
    monkeypatch.setattr(mcp_server, "create_mcp_server", Mock(return_value=server))
    monkeypatch.setattr(config, "set_console_log_level", Mock())

    mcp_server.run_mcp_server(Path("/corpus"))

    config.set_console_log_level.assert_called_once_with(logging.WARNING)
    disable_progress_bar.assert_called_once_with()
    server.run.assert_called_once_with(transport="stdio")


def test_console_level_change_preserves_file_log_detail(tmp_path, capsys) -> None:
    """MCP's console threshold must not discard INFO records from file logs."""
    root = logging.getLogger("doqqy")
    original_handlers = root.handlers[:]
    original_level = root.level
    original_propagate = root.propagate
    root.handlers.clear()
    try:
        config._ensure_console_handler()
        config.set_console_log_level(logging.WARNING)
        logger = config.get_logger("doqqy.mcp-test")
        log_path = tmp_path / "mcp.log"

        with config.file_log("doqqy.mcp-test", log_path):
            logger.info("file detail")
            logger.warning("operator warning")

        captured = capsys.readouterr()
        assert "file detail" not in captured.err
        assert "operator warning" in captured.err
        contents = log_path.read_text(encoding="utf-8")
        assert "file detail" in contents
        assert "operator warning" in contents
    finally:
        root.handlers[:] = original_handlers
        root.setLevel(original_level)
        root.propagate = original_propagate


def test_missing_mcp_extra_fails_before_model_imports(monkeypatch) -> None:
    """The CLI can catch an absent optional extra without loading models."""
    real_import = builtins.__import__

    def import_without_mcp(name, *args, **kwargs):
        if name == "mcp.server.fastmcp":
            raise ModuleNotFoundError("MCP extra is missing", name="mcp")
        assert name not in {"FlagEmbedding", "transformers"}
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", import_without_mcp)
    spec = importlib.util.spec_from_file_location("startup_probe", mcp_server.__file__)
    module = importlib.util.module_from_spec(spec)
    with pytest.raises(ModuleNotFoundError, match="MCP extra is missing"):
        spec.loader.exec_module(module)
