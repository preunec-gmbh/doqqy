"""doqqy için MCP (Model Context Protocol) sunucu uygulaması.
Yapay zeka ajanları için stdio taşıyıcısı üzerinden sorgu, etiket ve bilgi araçlarını sunar.
"""

import json
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from doqqy.workspace import Workspace


def create_mcp_server(root_dir: Path | None = None) -> FastMCP:
    """Belirtilen çalışma alanı için FastMCP sunucu örneğini oluşturur ve yapılandırır."""
    ws = Workspace(root_dir or Path.cwd())
    mcp = FastMCP("doqqy")

    @mcp.tool()
    def doqqy_query(
        q: str,
        top_k: int = 5,
        tag: str | None = None,
        rerank: bool = True,
    ) -> list[dict[str, Any]] | dict[str, str]:
        """Search local indexed documents in the workspace using hybrid retrieval.

        NOTE FOR AGENTS:
        - Results returned are verbatim excerpts directly from local source files.
        - `tag` filters results by document tag. Use `doqqy_tags()` first to discover valid tags.

        Args:
            q: Semantic or lexical search query string.
            top_k: Maximum number of search results to return (default: 5).
            tag: Optional tag filter.
            rerank: Whether to apply hybrid reranking (default: True).

        Returns:
            List of search result dictionaries or error message dictionary.
        """
        try:
            from doqqy.query import search

            hits = search(ws, query=q, k=top_k, rerank=rerank, tag=tag)
        except Exception as e: # noqa: BLE001
            return {"error": f"Arama yapılırken hata oluştu: {e}"}

        if not hits:
            return []

        results = []
        for h in hits:
            if isinstance(h, dict):
                content = h.get("content", "")
                source = h.get("source", "Bilinmiyor")
                section = h.get("section_path", "Kök")
                score = h.get("score", "N/A")
            else:
                content = getattr(h, "content", "")
                source = getattr(h, "source", "Bilinmiyor")
                section = getattr(h, "section_path", "Kök")
                score = getattr(h, "score", "N/A")

            results.append(
                {
                    "content": content,
                    "source": str(source),
                    "section_path": section,
                    "score": score,
                }
            )

        return results

    @mcp.tool()
    def doqqy_tags() -> dict[str, Any]:
        """List all document tags and their usage counts in the workspace.

        Returns:
            Dictionary containing tags and their counts, or an error message.
        """
        manifest_path = ws.manifest_path

        if not manifest_path.exists():
            return {"tags": {}, "count": 0}

        try:
            with manifest_path.open(encoding="utf-8") as f:
                data = json.load(f)

            tag_counts: dict[str, int] = {}
            docs = data.get("documents", {})
            for doc_info in docs.values():
                for t in doc_info.get("tags", []):
                    tag_counts[t] = tag_counts.get(t, 0) + 1

            return {"tags": tag_counts, "count": len(tag_counts)}
        except Exception as e: # noqa: BLE001
            return {"error": f"Etiket manifesti okunurken hata oluştu: {e}"}

    @mcp.tool()
    def doqqy_info() -> dict[str, Any]:
        """Get workspace directory structure and status information.

        Returns:
            Dictionary containing workspace directory paths.
        """
        return {
            "root": str(ws.root),
            "processed_dir": str(ws.processed_dir),
            "state_dir": str(ws.state_dir),
            "manifest_path": str(ws.manifest_path),
        }

    return mcp


def run_mcp_server(root_dir: Path | None = None) -> None:
    """MCP sunucusunu standart G/Ç (stdio) taşıyıcısı üzerinden çalıştırır."""
    server = create_mcp_server(root_dir)

    try:
        server.run(transport="stdio")
    except Exception:
        import traceback

        traceback.print_exc()
        raise

if __name__ == "__main__":
    run_mcp_server()
