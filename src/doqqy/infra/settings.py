"""Settings manager for the doqqy application."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from doqqy.config import SUPPORTED_EXTENSIONS


class Settings(BaseSettings):
    """Application settings resolved from environment variables with safe defaults."""

    model_config = SettingsConfigDict(
        env_prefix="DOQQY_",
        env_file=".env",
        extra="ignore",
        frozen=True,
    )

    # Vector store backend settings
    vector_backend: str = "lancedb"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "doqqy_chunks"

    # Topology and paths
    data_root: Path = Path("./data")
    redis_url: str = "redis://localhost:6379/0"
    queue_mode: str = "inprocess"

    # Machine learning models and device placement
    device: str = "auto"  # "auto", "cpu", or "cuda"
    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-v2-m3"
    reranker_fp16: bool = False  # FP16 precision on CUDA

    # Limits and supported file types
    max_upload_mb: int = 50
    max_docs_per_workspace: int = 5000
    query_rate_per_min: int = 60
    allowed_extensions: frozenset[str] = SUPPORTED_EXTENSIONS

    # Authentication
    auth_mode: str = "apikey"
    api_key_pepper: str = ""
