"""Vector store factory - resolves vector store backends dynamically."""

from __future__ import annotations

from doqqy.infra.settings import Settings
from doqqy.infra.vectorstore.base import VectorStore
from doqqy.workspace import Workspace


def make_store(ws: Workspace, settings: Settings | None = None) -> VectorStore:
    """Create and return a VectorStore instance based on settings configuration."""
    if settings is None:
        settings = Settings()

    match settings.vector_backend:
        case "lancedb":
            from doqqy.infra.vectorstore.lancedb_store import LanceDBStore
            return LanceDBStore(ws.store_dir)
        case "qdrant":
            from doqqy.infra.vectorstore.qdrant_store import QdrantStore
            return QdrantStore(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                collection=settings.qdrant_collection,
                tenant_key=str(ws.root),
            )
        case other:
            raise ValueError(f"Unknown vector backend: {other}")
