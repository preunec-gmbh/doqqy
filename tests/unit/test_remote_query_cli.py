"""Tests for `doqqy query --remote` / DOQQY_SERVER_URL: thin-client rendering parity
and the "no silent fallback to in-process search" contract — see issue #20.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
import typer
from typer.testing import CliRunner

import doqqy.cli as cli
from doqqy.query import SearchHit
from doqqy.remote_client import RemoteQueryError
from doqqy.workspace import Workspace

_CANNED_HITS = [
    SearchHit(
        score=0.91,
        doc_id="doc-1",
        source="raw/fatura.md",
        section_path=["Fatura", "İptal Süreci"],
        content="Kurumsal faturalar 7 iş günü içinde iptal edilebilir. " * 5,
        extra={"dense_rank": 1, "sparse_rank": 2, "rrf_score": 0.031, "rerank_score": 0.87},
    ),
    SearchHit(
        score=0.80,
        doc_id="doc-2",
        source="raw/iade.md",
        section_path=["İade Şartları"],
        content="Kargo ve sigorta bedelleri müşteriye aittir.",
        extra={"dense_rank": 3, "sparse_rank": None, "rrf_score": 0.020, "rerank_score": None},
    ),
]


@pytest.fixture
def temp_ws(tmp_path: Path) -> Workspace:
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    return ws


def _run_query(temp_ws: Workspace, *, remote: str | None) -> None:
    with patch.object(cli, "_workspace", return_value=temp_ws):
        cli.query(
            text="fatura iptal ve iade",
            k=5,
            full=False,
            no_rerank=False,
            tag=None,
            context=0,
            backend=None,
            remote=remote,
        )


def test_remote_query_renders_identically_to_inprocess(temp_ws, capsys, monkeypatch):
    """A canned server response must render the same rich output as the equivalent in-process hit list."""
    monkeypatch.delenv("DOQQY_SERVER_URL", raising=False)

    with patch("doqqy.remote_client.query_remote", return_value=(_CANNED_HITS, 42)):
        _run_query(temp_ws, remote="http://127.0.0.1:8000")
    remote_output = capsys.readouterr().out

    with patch("doqqy.query.search", return_value=_CANNED_HITS):
        _run_query(temp_ws, remote=None)
    local_output = capsys.readouterr().out

    assert remote_output == local_output
    assert "raw/fatura.md" in remote_output
    assert "raw/iade.md" in remote_output
    assert "dense=1" in remote_output and "rerank=0.870" in remote_output


def test_remote_connection_failure_is_a_clear_error_not_a_silent_fallback(temp_ws, capsys, monkeypatch):
    """A --remote that can't be reached must raise a clear error and must never fall back to in-process search."""
    monkeypatch.delenv("DOQQY_SERVER_URL", raising=False)

    with (
        patch(
            "doqqy.remote_client.query_remote",
            side_effect=RemoteQueryError("could not reach doqqy serve at http://127.0.0.1:8000: Connection refused"),
        ) as mock_remote,
        patch("doqqy.query.search") as mock_local,
        pytest.raises(typer.Exit) as exc_info,
    ):
        _run_query(temp_ws, remote="http://127.0.0.1:8000")

    assert exc_info.value.exit_code == 1
    mock_remote.assert_called_once()
    mock_local.assert_not_called()
    assert "could not reach" in capsys.readouterr().err


def test_bare_remote_uses_default_url(temp_ws, monkeypatch):
    monkeypatch.delenv("DOQQY_SERVER_URL", raising=False)

    with (
        patch.object(cli, "_workspace", return_value=temp_ws),
        patch("doqqy.remote_client.query_remote", return_value=(_CANNED_HITS, 42)) as mock_remote,
    ):
        result = CliRunner().invoke(cli.app, ["query", "fatura iptal", "--remote"])

    assert result.exit_code == 0, result.output
    assert mock_remote.call_args.args[0] == "http://127.0.0.1:8000"


@pytest.mark.parametrize(
    ("remote_flag", "env_value", "expected"),
    [
        (None, None, None),                                                     # no flag, no env -> in-process
        (None, "http://envhost:7000", "http://envhost:7000"),                   # env alone triggers remote mode
        ("", None, "http://127.0.0.1:8000"),                                    # bare --remote uses default
        ("", "http://envhost:7000", "http://envhost:7000"),                     # bare --remote prefers env
        ("http://cliflag:9000", "http://envhost:7000", "http://cliflag:9000"),  # explicit flag URL wins
    ],
)
def test_resolve_server_url_precedence(monkeypatch, remote_flag, env_value, expected):
    if env_value is None:
        monkeypatch.delenv("DOQQY_SERVER_URL", raising=False)
    else:
        monkeypatch.setenv("DOQQY_SERVER_URL", env_value)
    assert cli._resolve_server_url(remote_flag) == expected
