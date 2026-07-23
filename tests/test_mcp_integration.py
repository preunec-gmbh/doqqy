"""MCP (Model Context Protocol) stdio sunucusu uçtan uca entegrasyon testi."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
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
