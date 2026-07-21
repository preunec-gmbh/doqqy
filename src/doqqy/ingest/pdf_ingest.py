"""PDF ingester'ı: docling (ana) → pymupdf4llm (fallback)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from doqqy.config import get_logger
from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash, processed_path_for
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.ingest.pdf")


@lru_cache(maxsize=1)
def _get_docling_converter():
    """Standart Docling converter'ı tek seferlik belleğe yükler."""
    from docling.document_converter import DocumentConverter  # type: ignore

    return DocumentConverter()


@lru_cache(maxsize=1)
def _get_docling_ocr_converter():
    """OCR özellikli Docling converter'ı tek seferlik belleğe yükler."""
    try:
        from docling.datamodel.base_models import InputFormat  # type: ignore
        from docling.datamodel.pipeline_options import PdfPipelineOptions  # type: ignore
        from docling.document_converter import DocumentConverter, PdfFormatOption  # type: ignore

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True

        return DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)})
    except ImportError as exc:
        raise IngestError("OCR bağımlılıkları eksik. Lütfen 'pip install -e \".[ocr]\"' komutuyla paketleri kurun.") from exc


def _parse_with_docling(source: Path) -> str:
    converter = _get_docling_converter()
    result = converter.convert(str(source))
    return result.document.export_to_markdown()


def _parse_with_docling_ocr(source: Path) -> str:
    converter = _get_docling_ocr_converter()
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
        except IngestError:
            raise
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("docling-ocr başarısız (%s): %s", source.name, exc)

    # 3. Hala sonuç yoksa ve ocr istenmediyse pymupdf4llm dene
    if (md is None or not md.strip()) and not ocr:
        try:
            md = _parse_with_pymupdf4llm(source)
            parser_used = "pymupdf4llm"
        except Exception as exc:  # noqa: BLE001
            raise IngestError(f"Hem docling hem pymupdf4llm başarısız. docling: {docling_error}. pymupdf4llm: {exc}") from exc

    # 4. Çıktı hâlâ boşsa uygun hata mesajını ver
    if md is None or not md.strip():
        if ocr:
            raise IngestError(
                "OCR çalıştırılmasına rağmen içerik çıkarılamadı. "
                "OCR paketlerinin kurulu olduğundan emin olun: 'pip install -e \".[ocr]\"'"
            )
        raise IngestError("Parser boş içerik döndürdü (taranmış PDF olabilir).")

    meta=base_metadata(source, ws.root, kind="pdf")
    meta["parser"]=parser_used
    meta["content_hash"]=content_hash(md)

    return Document(
        source_path=source,
        processed_path=processed_path_for(source, ws),
        content=md,
        metadata=meta,
    )
