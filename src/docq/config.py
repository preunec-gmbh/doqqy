"""Yol ve ayar sabitleri. Proje kökünü pyproject.toml'a göre tespit eder."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv


def _find_project_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "pyproject.toml").exists():
            return parent
    return start


PROJECT_ROOT: Path = _find_project_root(Path(__file__).resolve())

RAW_DIR: Path = PROJECT_ROOT / "raw"
PROCESSED_DIR: Path = PROJECT_ROOT / "processed"
CHUNKS_DIR: Path = PROJECT_ROOT / "chunks"
LOGS_DIR: Path = PROJECT_ROOT / "logs"
STORE_DIR: Path = PROJECT_ROOT / "store.lance"

CHUNKS_PARQUET: Path = CHUNKS_DIR / "chunks.parquet"

# Ingest scope — MVP: sadece dokümantasyon dosyaları, kod örnekleri hariç.
SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".md", ".markdown", ".pdf", ".docx", ".txt"})

# Chunking
CHUNK_MAX_TOKENS: int = 800  # yaklaşık; recursive splitter karakter bazlı çalışır
CHUNK_OVERLAP: int = 100
CHUNK_MIN_MERGE_TOKENS: int = 100

# Embedding
EMBEDDING_MODEL: str = "BAAI/bge-m3"
EMBEDDING_DIM: int = 1024
EMBEDDING_BATCH_SIZE: int = 4
LANCE_TABLE: str = "chunks"

# Query
DEFAULT_TOP_K: int = 5
RETRIEVAL_TOP_K: int = 50  # dense + sparse her biri bu kadar getirir, RRF sonrası reranker'a gider

# Reranker
RERANKER_MODEL: str = "BAAI/bge-reranker-v2-m3"
RERANKER_BATCH_SIZE: int = 4

load_dotenv(PROJECT_ROOT / ".env", override=False)


def ensure_dirs() -> None:
    for d in (RAW_DIR, PROCESSED_DIR, CHUNKS_DIR, LOGS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def get_logger(name: str, log_file: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    if log_file:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(LOGS_DIR / log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger


def detect_device() -> str:
    """CUDA varsa 'cuda', yoksa 'cpu'. torch import maliyetinden kaçınmak için lazy."""
    env_override = os.environ.get("DOCQ_DEVICE")
    if env_override:
        return env_override
    try:
        import torch  # noqa: PLC0415

        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"
