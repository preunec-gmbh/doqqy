"""Ayar sabitleri (chunk boyutları, model adları, eşikler) ve logging yardımcıları.

Yol sabitleri artık burada YOK — yollar `doqqy.workspace.Workspace` üzerinden
gelir. Eski isimler (PROJECT_ROOT, RAW_DIR, ...) geçiş süreci için modül
`__getattr__` shim'i ile hâlâ çalışır ama DeprecationWarning verir ve her
erişimde o anki cwd'den hesaplanır.
"""

from __future__ import annotations

import logging
import os
import re
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator

# Ingest scope — MVP: sadece dokümantasyon dosyaları, kod örnekleri hariç.
SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({".md", ".markdown", ".pdf", ".docx", ".txt", ".xml", ".xlsx", ".csv", ".html", ".htm"})
OCR_ENABLED: bool = False       # OCR varsayılan olarak kapalıdır (yavaş çalışır)

# Chunking
CHUNK_MAX_TOKENS: int = 800  # yaklaşık; recursive splitter karakter bazlı çalışır

# Embedding
EMBEDDING_MODEL: str = "BAAI/bge-m3"
EMBEDDING_DIM: int = 1024
EMBEDDING_BATCH_SIZE: int = 4
LANCE_TABLE: str = "chunks"

# Query
DEFAULT_TOP_K: int = 5
RETRIEVAL_TOP_K: int = 50  # dense + sparse her biri bu kadar getirir, RRF sonrası reranker'a gider
RRF_K: int = 60            # Reciprocal Rank Fusion k parametresi

# Tag validation — Unicode \w covers ASCII, Turkish letters, digits, and underscore
TAG_PATTERN: str = r"^[\w-]+\Z"


def sanitize_tag(raw: str) -> str | None:
    """Bir klasör adını TAG_PATTERN'e uyan bir tag'e dönüştürür (ingest-side slugify).

    Boşluklar '-' ile değiştirilir; TAG_PATTERN dışındaki karakterler (tırnak,
    virgül, vb.) tamamen atılır. Sonuç boşsa (örn. klasör adı yalnızca
    sembollerden oluşuyorsa) tag tamamen düşürülür ve None döner.

    Zaten TAG_PATTERN'e uyan bir girdi değişmeden döner — sanitize_tag idempotent'tir,
    yani zaten temizlenmiş bir çıktı üzerinde tekrar çalıştırmak sonucu değiştirmez.
    """
    slug = re.sub(r"\s+", "-", raw.strip())
    slug = re.sub(r"[^\w-]", "", slug)
    slug = slug.strip("-")
    return slug or None

# Reranker
RERANKER_MODEL: str = "BAAI/bge-reranker-v2-m3"
RERANKER_BATCH_SIZE: int = 4

# Map generation (Faz 3)
MAP_COSINE_THRESHOLD: float = 0.75   # Pass 2 minimum cosine benzerliği
MAP_TOP_N_NEIGHBORS: int = 5         # Her section için max komşu sayısı


# ---------------------------------------------------------------------------
# Deprecated yol sabitleri — Workspace'e geçiş shim'i
# ---------------------------------------------------------------------------

def _ws_cwd():
    from doqqy.workspace import Workspace  # noqa: PLC0415 — döngüsel import önlemi

    return Workspace(Path.cwd())


_DEPRECATED_PATHS: dict[str, Callable[[], Path]] = {
    "PROJECT_ROOT": lambda: _ws_cwd().root,
    "DOQQY_STATE_DIR": lambda: _ws_cwd().state_dir,
    "RAW_DIR": lambda: _ws_cwd().raw_dir,
    "PROCESSED_DIR": lambda: _ws_cwd().processed_dir,
    "CHUNKS_DIR": lambda: _ws_cwd().chunks_parquet.parent,
    "LOGS_DIR": lambda: _ws_cwd().logs_dir,
    "STORE_DIR": lambda: _ws_cwd().store_dir,
    "CHUNKS_PARQUET": lambda: _ws_cwd().chunks_parquet,
    "TOPICS_YAML": lambda: _ws_cwd().topics_yaml,
}


def __getattr__(name: str) -> Path:
    if name in _DEPRECATED_PATHS:
        warnings.warn(
            f"doqqy.config.{name} kullanımdan kaldırıldı — doqqy.workspace.Workspace kullanın.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _DEPRECATED_PATHS[name]()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def ensure_dirs() -> None:
    """Deprecated — Workspace(Path.cwd()).ensure_dirs() kullanın."""
    warnings.warn(
        "doqqy.config.ensure_dirs kullanımdan kaldırıldı — Workspace.ensure_dirs kullanın.",
        DeprecationWarning,
        stacklevel=2,
    )
    _ws_cwd().ensure_dirs()


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def _ensure_console_handler() -> None:
    """Tüm doqqy.* logger'ları tek console handler'a propagate eder."""
    root = logging.getLogger("doqqy")
    if root.handlers:
        return
    root.setLevel(logging.INFO)
    stream = logging.StreamHandler()
    stream.setFormatter(_FORMATTER)
    root.addHandler(stream)
    root.propagate = False


def get_logger(name: str) -> logging.Logger:
    _ensure_console_handler()
    return logging.getLogger(name)


@contextmanager
def file_log(scope: str, log_path: Path) -> Iterator[None]:
    """Bir çalışma süresince `scope` logger'ına workspace'e özel dosya handler'ı tak.

    Çıkışta handler sökülür — aynı process'te farklı workspace'lerin logları
    birbirine karışmaz.
    """
    logger = logging.getLogger(scope)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(_FORMATTER)
    logger.addHandler(handler)
    try:
        yield
    finally:
        logger.removeHandler(handler)
        handler.close()


def detect_device() -> str:
    """CUDA varsa 'cuda', yoksa 'cpu'. torch import maliyetinden kaçınmak için lazy."""
    env_override = os.environ.get("DOQQY_DEVICE")
    if env_override:
        return env_override
    try:
        import torch  # noqa: PLC0415

        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"
