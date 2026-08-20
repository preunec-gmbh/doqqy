"""Unit tests for doqqy.remote_client: URL/workspace_id construction and error mapping.

Uses a real stdlib http.server instance (no mocking library dependency) so the
urllib-based request path is exercised end to end, matching remote_client.py's
own no-extra-dependency design.
"""

from __future__ import annotations

import contextlib
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from doqqy.remote_client import RemoteQueryError, query_remote
from doqqy.workspace import Workspace


class _EchoHandler(BaseHTTPRequestHandler):
    """Records the requested path/body and returns a canned QueryResponse-shaped payload."""

    response_status = 200
    response_body: dict = {}
    last_path: str | None = None
    last_payload: dict | None = None

    def do_POST(self) -> None:  # noqa: N802 (stdlib method name)
        type(self).last_path = self.path
        length = int(self.headers.get("Content-Length", 0))
        type(self).last_payload = json.loads(self.rfile.read(length))

        body = json.dumps(type(self).response_body).encode("utf-8")
        self.send_response(type(self).response_status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args) -> None:  # keep test output quiet
        pass


@pytest.fixture
def echo_server():
    server = HTTPServer(("127.0.0.1", 0), _EchoHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        thread.join(timeout=5)


def _free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_query_remote_parses_hits_and_encodes_workspace_path(tmp_path, echo_server):
    ws_root = tmp_path / "my corpus"  # a space forces percent-encoding in the URL path
    ws = Workspace(ws_root)
    ws.ensure_dirs()

    _EchoHandler.response_status = 200
    _EchoHandler.response_body = {
        "hits": [
            {
                "score": 0.91,
                "doc_id": "doc-1",
                "source": "raw/fatura.md",
                "section_path": ["Fatura", "İptal"],
                "content": "Fatura iptal süreci...",
                "extra": {"dense_rank": 1, "sparse_rank": None, "rrf_score": 0.03, "rerank_score": 0.87},
            }
        ],
        "took_ms": 17,
        "workspace": str(ws_root),
    }

    port = echo_server.server_address[1]
    hits, took_ms = query_remote(
        f"http://127.0.0.1:{port}", ws, "fatura iptal", k=5, rerank=True, tag=None
    )

    assert took_ms == 17
    assert len(hits) == 1
    hit = hits[0]
    assert hit.doc_id == "doc-1"
    assert hit.source == "raw/fatura.md"
    assert hit.section_path == ["Fatura", "İptal"]
    assert hit.extra == {"dense_rank": 1, "rrf_score": 0.03, "rerank_score": 0.87}  # None dropped

    assert "%20" in _EchoHandler.last_path  # the space in "my corpus" round-trips safely
    assert _EchoHandler.last_payload == {"q": "fatura iptal", "top_k": 5, "tag": None, "rerank": True}


def test_query_remote_http_error_is_wrapped(tmp_path, echo_server):
    ws = Workspace(tmp_path)
    ws.ensure_dirs()

    _EchoHandler.response_status = 404
    _EchoHandler.response_body = {"detail": "Workspace not found"}

    port = echo_server.server_address[1]
    with pytest.raises(RemoteQueryError, match="404"):
        query_remote(f"http://127.0.0.1:{port}", ws, "fatura", k=5, rerank=True, tag=None)


def test_query_remote_connection_refused_raises_clear_error(tmp_path):
    ws = Workspace(tmp_path)
    ws.ensure_dirs()

    dead_port = _free_port()  # nothing is listening here
    with pytest.raises(RemoteQueryError, match="could not reach"):
        query_remote(f"http://127.0.0.1:{dead_port}", ws, "fatura", k=5, rerank=True, tag=None, timeout=2.0)
