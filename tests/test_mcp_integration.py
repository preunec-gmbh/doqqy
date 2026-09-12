"""MCP (Model Context Protocol) stdio sunucusu uçtan uca entegrasyon testi."""

from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

pytest.importorskip("mcp")
pytest.importorskip("pytest_asyncio")

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from doqqy.chunk import chunk_directory
from doqqy.embed import build_index
from doqqy.ingest import ingest_directory
from doqqy.workspace import Workspace

# Test dosyasının konumundan (tests/) bir üst dizine çıkıp src klasörünün mutlak yolunu al
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = str(PROJECT_ROOT / "src")


@pytest.fixture
def fixture_workspace(tmp_path: Path) -> Path:
    """stdio entegrasyon testi için hazırlanmış örnek korpus dizini."""
    ws = Workspace(tmp_path / "mcp_corpus")
    ws.ensure_dirs()

    # Örnek test belgesi oluştur
    (ws.raw_dir / "sample.md").write_text(
        "# Authentication\nJWT refresh tokens enable long-lived sessions safely.",
        encoding="utf-8",
    )

    # Indeksleme pipeline'ını çalıştır
    ingest_directory(ws)
    chunk_directory(ws)
    build_index(ws)

    return ws.root


@pytest.mark.slow
@pytest.mark.asyncio
async def test_mcp_stdio_handshake_and_query_roundtrip(fixture_workspace: Path):
    """'doqqy.mcp_server' sürecini stdio üzerinde çalıştırarak MCP uçtan uca döngüsünü doğrular."""
    # Mevcut PYTHONPATH varsa üzerine ekle yoksa direkt SRC_DIR yaparak ayarla
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{SRC_DIR}{os.pathsep}{existing_pythonpath}" if existing_pythonpath else SRC_DIR

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "doqqy.mcp_server"],
        cwd=str(fixture_workspace),
        env=env,
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            # 1. MCP Protocol Handshake
            init_result = await session.initialize()
            assert init_result is not None
            assert init_result.serverInfo.name == "doqqy"

            # 2. Tool Discovery
            tools_response = await session.list_tools()
            tool_names = [tool.name for tool in tools_response.tools]

            assert "doqqy_query" in tool_names
            assert "doqqy_tags" in tool_names
            assert "doqqy_info" in tool_names

            # 3. Query Tool Call Roundtrip
            query_args = {
                "q": "JWT refresh token",
                "top_k": 2,
                "rerank": True,
            }

            result = await session.call_tool("doqqy_query", arguments=query_args)

            assert result is not None
            assert len(result.content) > 0

            assert result.structuredContent is not None

            hits = result.structuredContent["result"]

            assert isinstance(hits, list)
            assert len(hits) > 0

            assert "content" in hits[0]
            assert "source" in hits[0]
            assert "score" in hits[0]
            assert "JWT refresh" in hits[0]["content"]

            # 4. Info Tool Call Roundtrip
            info_result = await session.call_tool("doqqy_info", arguments={})
            assert info_result is not None
            assert info_result.structuredContent is not None

            # doqqy_info'nun döndürdüğü sözlük içindeki anahtarları ve sayaçları kontrol et
            info_data = info_result.structuredContent.get("result", info_result.structuredContent)
            assert info_data.get("chunks_parquet_exists") is True
            assert info_data.get("vector_store_exists") is True
            assert info_data.get("indexed_documents_count") == 1
            assert info_data.get("indexed_chunks_count") == 1


@pytest.mark.slow
def test_mcp_roundtrip_does_not_require_stderr_reader(fixture_workspace: Path):
    """A real cold-process query must complete without draining its stderr pipe."""
    from mcp.types import LATEST_PROTOCOL_VERSION

    process = subprocess.Popen(
        [sys.executable, "-m", "doqqy.mcp_server"],
        cwd=fixture_workspace,
        env={**os.environ, "PYTHONPATH": SRC_DIR},
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    replies = queue.Queue()

    def read_stdout():
        for line in process.stdout:
            replies.put(json.loads(line))

    threading.Thread(target=read_stdout, daemon=True).start()

    def send(payload):
        process.stdin.write((json.dumps(payload) + "\n").encode())
        process.stdin.flush()

    def response(request_id):
        deadline = time.monotonic() + 120
        while True:
            reply = replies.get(timeout=max(0, deadline - time.monotonic()))
            if reply.get("id") == request_id:
                assert "error" not in reply, reply
                return reply["result"]

    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": LATEST_PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name": "stderr-regression", "version": "1"},
        }})
        assert response(1)["serverInfo"]["name"] == "doqqy"
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
            "name": "doqqy_query", "arguments": {"q": "JWT refresh token", "top_k": 2},
        }})
        result = response(2)
        assert not result.get("isError", False), result
        assert result.get("structuredContent", {}).get("result"), result
    finally:
        process.terminate()
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=15)
    stderr = process.stderr.read()
    assert len(stderr) < 8192, stderr.decode(errors="replace")
