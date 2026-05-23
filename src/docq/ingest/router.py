"""Uzantıya göre doğru ingester'a delegasyon + toplu ingest."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from tqdm import tqdm

from docq.config import RAW_DIR, SUPPORTED_EXTENSIONS, get_logger
from docq.ingest.base import Document, IngestError, IngestResult
from docq.ingest.docx_ingest import ingest_docx
from docq.ingest.md_ingest import ingest_md, ingest_txt
from docq.ingest.pdf_ingest import ingest_pdf

_LOG = get_logger("docq.ingest.router", log_file="ingest.log")


_DISPATCH: dict[str, Callable[[Path], Document]] = {
    ".md": ingest_md,
    ".markdown": ingest_md,
    ".txt": ingest_txt,
    ".pdf": ingest_pdf,
    ".docx": ingest_docx,
}


def ingest_file(source: Path) -> Document:
    ext = source.suffix.lower()
    parser = _DISPATCH.get(ext)
    if parser is None:
        raise IngestError(f"desteklenmeyen uzantı: {ext}")
    return parser(source)


def _iter_supported(root: Path) -> list[Path]:
    return sorted(
        p
        for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def ingest_directory(root: Path | None = None, *, limit: int | None = None) -> IngestResult:
    """raw/ altındaki tüm desteklenen dosyaları ingest et.

    Bir dosya hata verirse durmaz — log + raporda failed listesine eklenir.
    """
    root = root or RAW_DIR
    if not root.exists():
        raise FileNotFoundError(f"ingest root yok: {root}")

    files = _iter_supported(root)
    if limit:
        files = files[:limit]

    result = IngestResult()
    for path in tqdm(files, desc="ingest", unit="file"):
        try:
            doc = ingest_file(path)
            doc.write()
            result.succeeded.append(path)
        except IngestError as exc:
            _LOG.error("%s: %s", path, exc)
            result.failed.append((path, str(exc)))
        except Exception as exc:  # noqa: BLE001
            _LOG.exception("beklenmedik hata: %s", path)
            result.failed.append((path, f"{type(exc).__name__}: {exc}"))

    _LOG.info(
        "ingest bitti: %d başarılı, %d başarısız, toplam %d.",
        len(result.succeeded),
        len(result.failed),
        result.total,
    )
    return result
