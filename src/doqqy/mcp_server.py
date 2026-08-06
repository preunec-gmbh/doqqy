"""doqqy için MCP (Model Context Protocol) sunucu uygulaması.
Yapay zeka ajanları için stdio taşıyıcısı üzerinden sorgu, etiket ve bilgi araçlarını sunar.
"""

import contextlib
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from doqqy.workspace import Workspace


def create_mcp_server(root_dir: Path | None = None) -> FastMCP:
    """Belirtilen çalışma alanı için FastMCP sunucu örneğini oluşturur ve yapılandırır."""
    ws = Workspace(root_dir or Path.cwd())

    mcp_instance = FastMCP("doqqy")

    @mcp_instance.tool()
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
        # Backend selection uses the default vector store (no --backend equivalent in MCP tools).

        try:
            from doqqy.query import search

            hits = search(ws, query=q, k=top_k, rerank=rerank, tag=tag)
        except Exception as e:  # noqa: BLE001
            return {"error": f"Arama yapılırken hata oluştu: {e}"}

        if not hits:
            return []

        results = []
        for h in hits:
            results.append(
                {
                    "content": h.content,
                    "source": str(h.source),
                    "section_path": " > ".join(h.section_path) if h.section_path else "Kök",
                    "score": h.score,
                }
            )

        return results


    @mcp_instance.tool()
    def doqqy_tags() -> dict[str, Any]:
        """List all document tags available in the vector store.

        Returns:
            Dictionary containing tags list and count, or an error message.
        """
        try:
            from doqqy.infra.vectorstore.factory import make_store

            with contextlib.closing(make_store(ws)) as store:
                all_tags = store.list_tags()

            return {"tags": sorted(all_tags), "count": len(all_tags)}
        except Exception as e:  # noqa: BLE001
            return {"error": f"Etiketler listelenirken hata oluştu: {e}"}


    @mcp_instance.tool()
    def doqqy_info() -> dict[str, Any]:
        """Get workspace summary status including file counts and store state.

        Returns:
            Dictionary containing workspace status metrics.
        """
        raw_count = (
            sum(1 for p in ws.raw_dir.rglob("*") if p.is_file())
            if ws.raw_dir.exists()
            else 0
        )
        proc_count = (
            sum(1 for p in ws.processed_dir.rglob("*.md") if p.is_file())
            if ws.processed_dir.exists()
            else 0
        )

        chunks_exist = ws.chunks_parquet.exists()
        store_exist = ws.store_dir.exists()

        total_docs = 0
        total_chunks = 0
        try:
            from doqqy.manifest import Manifest
            manifest = Manifest.load(ws)
            totals = manifest.totals()
            total_docs = totals.get("docs", 0)
            total_chunks = totals.get("chunks", 0)
        except Exception:  # noqa: BLE001
            pass

        return {
            "root": str(ws.root),
            "raw_files_count": raw_count,
            "processed_files_count": proc_count,
            "indexed_documents_count": total_docs,
            "indexed_chunks_count": total_chunks,
            "chunks_parquet_exists": chunks_exist,
            "vector_store_exists": store_exist,
        }

    return mcp_instance


def run_mcp_server(root_dir: Path | None = None) -> None:
    """MCP sunucusunu standart G/Ç (stdio) taşıyıcısı üzerinden çalıştırır."""
    import doqqy.query  # noqa: F401
    import doqqy.rerank  # noqa: F401
    from doqqy.infra.vectorstore import factory  # noqa: F401

    server = create_mcp_server(root_dir)

    try:
        server.run(transport="stdio")
    except Exception:
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    run_mcp_server()
