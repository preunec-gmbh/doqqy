"""PDF ingester'ı: docling → docling-ocr (--ocr ile) → pymupdf4llm (opsiyonel: .[pdf-fallback])."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

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
        import easyocr  # noqa: F401        # type: ignore
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


def ingest_pdf(source: Path, ws: Workspace, ocr: bool = False, **_kwargs: Any) -> Document:
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
        # OCR bağımlılıkları eksikse de (IngestError) durmuyoruz: --ocr bir deneme ekler,
        # pymupdf4llm denemesini ortadan kaldırmaz. Hepsi boş dönerse adım 4 doğru mesajı verir.
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("docling-ocr başarısız (%s): %s", source.name, exc)

    # 3. Hala sonuç yoksa pymupdf4llm dene (opsiyonel: pip install -e ".[pdf-fallback]")
    if md is None or not md.strip():
        try:
            md = _parse_with_pymupdf4llm(source)
            parser_used = "pymupdf4llm"
        except ModuleNotFoundError:
            # Paket bilerek opsiyonel (PyMuPDF AGPL-3.0). Kurulu değilse bu bir hata değil,
            # sadece zincirin son halkası eksik — adım 4 doğru mesajı veriyor.
            _LOG.info("pymupdf4llm kurulu değil, fallback atlanıyor: %s", source.name)
        except Exception as exc:  # noqa: BLE001
            raise IngestError(f"Hem docling hem pymupdf4llm başarısız. docling: {docling_error}. pymupdf4llm: {exc}") from exc

    # 4. Çıktı hâlâ boşsa uygun hata mesajını ver
    if md is None or not md.strip():
        if ocr:
            raise IngestError(
                "OCR çalıştırılmasına rağmen içerik çıkarılamadı. "
                "OCR paketlerinin kurulu olduğundan emin olun: 'pip install -e \".[ocr]\"'"
            )
        raise IngestError(
            "Parser boş içerik döndürdü (taranmış PDF olabilir). "
            "'--ocr' ile OCR'ı deneyebilir, ek bir parser için 'pip install -e \".[pdf-fallback]\"' kurabilirsiniz."
        )

    meta = base_metadata(source, ws.root, kind="pdf")
    meta["parser"] = parser_used
    meta["content_hash"] = content_hash(md)

    return Document(
        source_path=source,
        processed_path=processed_path_for(source, ws),
        content=md,
        metadata=meta,
    )
