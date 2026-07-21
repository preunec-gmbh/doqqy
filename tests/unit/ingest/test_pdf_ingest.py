"""PDF ingest unit testleri (OCR fallback dahil)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from doqqy.ingest.base import IngestError
from doqqy.ingest.pdf_ingest import ingest_pdf
from doqqy.workspace import Workspace


def test_pdf_ingest_standard_docling_success(tmp_path):
    """Standart Docling başarılı olduğunda doğrudan sonucu dönmeli."""
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    fake_pdf = tmp_path / "normal.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake pdf content")

    with patch("doqqy.ingest.pdf_ingest._parse_with_docling", return_value="# Normal Text Content"):
        doc = ingest_pdf(fake_pdf, ws, ocr=False)

        assert doc.content == "# Normal Text Content"
        assert doc.metadata["parser"] == "docling"


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
        with pytest.raises(IngestError, match="taranmış PDF"):
            ingest_pdf(fake_pdf, ws, ocr=False)


def test_pdf_ingest_with_ocr_fallback_success(tmp_path):
    """OCR açıkken (ocr=True) standart parse boş dönse bile OCR fallback devreye girmeli."""
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    fake_pdf = tmp_path / "scanned.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake pdf content")

    # Tüm standart parser'lar (docling ve pymupdf4llm) boş dönüyor yalnızca OCR başarılı dönüyor
    with patch("doqqy.ingest.pdf_ingest._parse_with_docling", return_value=""), patch(
        "doqqy.ingest.pdf_ingest._parse_with_pymupdf4llm", return_value=""
    ), patch(
        "doqqy.ingest.pdf_ingest._parse_with_docling_ocr", return_value="# Scanned Text Content"
    ):
        doc = ingest_pdf(fake_pdf, ws, ocr=True)

        assert doc.content == "# Scanned Text Content"
        assert doc.metadata["parser"] == "docling-ocr"


def test_pdf_ingest_with_ocr_enabled_but_falls_back_to_pymupdf4llm(tmp_path):
    """OCR açık (ocr=True) olmasına rağmen Docling ve Docling-OCR boş dönerse pymupdf4llm devreye girmeli."""
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    fake_pdf = tmp_path / "scanned.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake pdf content")

    with patch("doqqy.ingest.pdf_ingest._parse_with_docling", return_value=""), patch(
        "doqqy.ingest.pdf_ingest._parse_with_docling_ocr", return_value=""
    ), patch(
        "doqqy.ingest.pdf_ingest._parse_with_pymupdf4llm", return_value="# PyMuPDF Fallback Content"
    ):
        doc = ingest_pdf(fake_pdf, ws, ocr=True)

        assert doc.content == "# PyMuPDF Fallback Content"
        assert doc.metadata["parser"] == "pymupdf4llm"


def test_pdf_ingest_missing_ocr_deps_still_falls_back_to_pymupdf4llm(tmp_path):
    """OCR paketleri kurulu değilse bile pymupdf4llm denemesi atlanmamalı — --ocr deneme ekler, kaldırmaz."""
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    fake_pdf = tmp_path / "scanned.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake pdf content")

    with patch("doqqy.ingest.pdf_ingest._parse_with_docling", return_value=""), patch(
        "doqqy.ingest.pdf_ingest._parse_with_docling_ocr",
        side_effect=IngestError("OCR bağımlılıkları eksik."),
    ), patch("doqqy.ingest.pdf_ingest._parse_with_pymupdf4llm", return_value="# PyMuPDF Fallback Content"):
        doc = ingest_pdf(fake_pdf, ws, ocr=True)

        assert doc.content == "# PyMuPDF Fallback Content"
        assert doc.metadata["parser"] == "pymupdf4llm"


def test_pdf_ingest_with_ocr_fails_when_all_parsers_return_empty(tmp_path):
    """OCR açık (ocr=True) iken tüm parser'lar boş dönerse OCR hata mesajı fırlatılmalı."""
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    fake_pdf = tmp_path / "empty.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 fake pdf content")

    with patch("doqqy.ingest.pdf_ingest._parse_with_docling", return_value=""), patch(
        "doqqy.ingest.pdf_ingest._parse_with_docling_ocr", return_value=""
    ), patch("doqqy.ingest.pdf_ingest._parse_with_pymupdf4llm", return_value=""):
        with pytest.raises(IngestError, match="OCR çalıştırılmasına rağmen içerik çıkarılamadı"):
            ingest_pdf(fake_pdf, ws, ocr=True)
