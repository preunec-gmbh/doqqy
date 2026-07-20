"""PDF ingest unit testleri (OCR fallback dahil)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from doqqy.ingest.base import IngestError
from doqqy.ingest.pdf_ingest import ingest_pdf
from doqqy.workspace import Workspace


def test_pdf_ingest_without_ocr_fails_on_empty_content(tmp_path):
    """OCR kapalıyken (ocr=False) boş/taranmış PDF'ler IngestError fırlatmalı."""
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    fake_pdf = tmp_path / "scanned.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake pdf content")

    # Hem docling hem pymupdf4llm boş metin dönsün
    with patch("doqqy.ingest.pdf_ingest._parse_with_docling", return_value=""), patch(
        "doqqy.ingest.pdf_ingest._parse_with_pymupdf4llm", return_value=""
    ):
        with pytest.raises(IngestError, match="scanned PDF"):
            ingest_pdf(fake_pdf, ws, ocr=False)


@pytest.mark.slow
def test_pdf_ingest_with_ocr_fallback_success(tmp_path):
    """OCR açıkken (ocr=True) standart parse boş dönse bile OCR fallback devreye girmeli."""
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    fake_pdf = tmp_path / "scanned.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake pdf content")

    with patch("doqqy.ingest.pdf_ingest._parse_with_docling", return_value=""), patch(
        "doqqy.ingest.pdf_ingest._parse_with_docling_ocr", return_value="# Scanned Text Content"
    ):
        doc = ingest_pdf(fake_pdf, ws, ocr=True)

        assert doc.content == "# Scanned Text Content"
        assert doc.metadata["parser"] == "docling-ocr"

