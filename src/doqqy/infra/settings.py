"""Settings manager for the doqqy application."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings resolved from environment variables with safe defaults."""

    model_config = SettingsConfigDict(
        env_prefix="DOQQY_",
        env_file=".env",
        extra="ignore",
    )

    # Vektör Veritabanı Ayarları
    vector_backend: str = "lancedb"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "doqqy_chunks"

    # Topoloji ve Yollar
    data_root: Path = Path("./data")
    redis_url: str = "redis://localhost:6379/0"
    queue_mode: str = "inprocess"

    # Yapay Zeka Modelleri ve Cihaz Seçimi
    device: str = "auto"  # "auto", "cpu", veya "cuda"
    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-v2-m3"

    # Limitler ve Dosya Türleri
    max_upload_mb: int = 50
    max_docs_per_workspace: int = 5000
    query_rate_per_min: int = 60
    allowed_extensions: frozenset[str] = frozenset({".md", ".markdown", ".txt", ".pdf", ".docx"})

    # Kimlik Doğrulama
    auth_mode: str = "apikey"
    api_key_pepper: str = ""
