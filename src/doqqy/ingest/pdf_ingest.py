"""PDF ingester'ı: docling (ana) → pymupdf4llm (fallback)."""

from __future__ import annotations

from pathlib import Path

from doqqy.config import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR, get_logger
from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash

_LOG = get_logger("doqqy.ingest.pdf", log_file="ingest.log")


def _processed_path(source: Path) -> Path:
    try:
        rel = source.resolve().relative_to(RAW_DIR.resolve())
    except ValueError:
        rel = Path(source.name)
    return (PROCESSED_DIR / rel).with_suffix(".md")


def _parse_with_docling(source: Path) -> str:
    from docling.document_converter import DocumentConverter  # type: ignore

    converter = DocumentConverter()
    result = converter.convert(str(source))
    return result.document.export_to_markdown()


def _parse_with_pymupdf4llm(source: Path) -> str:
    import pymupdf4llm  # type: ignore

    return pymupdf4llm.to_markdown(str(source))


def ingest_pdf(source: Path) -> Document:
    md: str | None = None
    parser_used: str | None = None
    docling_error: Exception | None = None

    try:
        md = _parse_with_docling(source)
        parser_used = "docling"
    except Exception as exc:  # noqa: BLE001
        docling_error = exc
        _LOG.warning("docling başarısız (%s): %s — pymupdf4llm denenecek.", source.name, exc)

    if md is None or not md.strip():
        try:
            md = _parse_with_pymupdf4llm(source)
            parser_used = "pymupdf4llm"
        except Exception as exc:  # noqa: BLE001
            raise IngestError(
                f"hem docling hem pymupdf4llm başarısız. docling: {docling_error}. pymupdf4llm: {exc}"
            ) from exc

    if not md.strip():
        raise IngestError("parser boş içerik döndürdü (taranmış PDF olabilir).")

    meta = base_metadata(source, PROJECT_ROOT, kind="pdf")
    meta["parser"] = parser_used
    meta["content_hash"] = content_hash(md)

    return Document(
        source_path=source,
        processed_path=_processed_path(source),
        content=md,
        metadata=meta,
    )
