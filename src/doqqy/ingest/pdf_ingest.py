"""PDF ingester'ı: docling (ana) → pymupdf4llm (fallback)."""

from __future__ import annotations

from pathlib import Path

from doqqy.config import get_logger
from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash, processed_path_for
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.ingest.pdf")


def _parse_with_docling(source: Path) -> str:
    from docling.document_converter import DocumentConverter  # type: ignore

    converter = DocumentConverter()
    result = converter.convert(str(source))
    return result.document.export_to_markdown()


def _parse_with_docling_ocr(source: Path) -> str:
    from docling.datamodel.base_models import InputFormat  # type: ignore
    from docling.datamodel.pipeline_options import PdfPipelineOptions  # type: ignore
    from docling.document_converter import DocumentConverter, PdfFormatOption  # type: ignore

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True

    converter = DocumentConverter(
        format_options = {InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )
    result = converter.convert(str(source))
    return result.document.export_to_markdown()


def _parse_with_pymupdf4llm(source: Path) -> str:
    import pymupdf4llm  # type: ignore

    return pymupdf4llm.to_markdown(str(source))


def ingest_pdf(source: Path, ws: Workspace, ocr: bool = False) -> Document:
    md: str | None = None
    parser_used: str | None = None
    docling_error: Exception | None = None

    # 1. Standart Docling denemesi
    try:
        md = _parse_with_docling(source)
        parser_used = "docling"
    except Exception as exc:  # noqa: BLE001
        docling_error = exc
        _LOG.warning("docling başarısız (%s): %s", source.name, exc)

    # 2. Eğer ilk deneme boş veya hatalıysa ve ocr=True ise Docling OCR dene
    if (md is None or not md.strip()) and ocr:
        try:
            _LOG.info("OCR fallback tetikleniyor: %s", source.name)
            md = _parse_with_docling_ocr(source)
            if md and md.strip():
                parser_used = "docling-ocr"
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("docling-ocr başarısız (%s): %s", source.name, exc)

    # 3. Hala sonuç yoksa pymupdf4llm dene
    if md is None or not md.strip():
        try:
            md = _parse_with_pymupdf4llm(source)
            parser_used = "pymupdf4llm"
        except Exception as exc:  # noqa: BLE001
            raise IngestError(
                f"hem docling hem pymupdf4llm başarısız. docling: {docling_error}. pymupdf4llm: {exc}"
            ) from exc

    if not md.strip():
        raise IngestError("Parser returned empty content (possibly a scanned PDF, try --ocr).")

    meta = base_metadata(source, ws.root, kind="pdf")
    meta["parser"] = parser_used
    meta["content_hash"] = content_hash(md)

    return Document(
        source_path=source,
        processed_path=processed_path_for(source, ws),
        content=md,
        metadata=meta,
    )
