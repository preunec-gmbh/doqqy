"""Settings manager for the doqqy application."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    """Application settings resolved from environment variables with safe defaults."""

    vector_backend: str = field(
        default_factory=lambda: os.environ.get("DOQQY_VECTOR_BACKEND", "lancedb")
    )
    qdrant_url: str = field(
        default_factory=lambda: os.environ.get("DOQQY_QDRANT_URL", "http://localhost:6333")
    )
    qdrant_api_key: str = field(
        default_factory=lambda: os.environ.get("DOQQY_QDRANT_API_KEY", "")
    )
    qdrant_collection: str = field(
        default_factory=lambda: os.environ.get("DOQQY_QDRANT_COLLECTION", "doqqy_chunks")
    )
