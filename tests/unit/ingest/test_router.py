"""Unit tests for the ingest router."""

from __future__ import annotations

from pathlib import Path

import pytest

from doqqy.ingest.base import IngestError
from doqqy.ingest.csv_ingest import ingest_csv
from doqqy.ingest.html_ingest import ingest_html
from doqqy.ingest.router import _DISPATCH, ingest_file
from doqqy.ingest.xlsx_ingest import ingest_xlsx
from doqqy.ingest.xml_ingest import ingest_xml
from doqqy.workspace import Workspace


def test_router_html_dispatch_registration() -> None:
    """Test that the .html and .htm extensions are correctly registered in the dispatch map."""
    assert ".html" in _DISPATCH
    assert _DISPATCH[".html"] == ingest_html
    assert ".htm" in _DISPATCH
    assert _DISPATCH[".htm"] == ingest_html


def test_router_dispatch_registration() -> None:
    """Test that the .xml extension is correctly registered in the dispatch map."""
    assert ".xml" in _DISPATCH
    assert _DISPATCH[".xml"] == ingest_xml


def test_router_xlsx_dispatch_registration() -> None:
    """Test that the .xlsx extension is correctly registered in the dispatch map."""
    assert ".xlsx" in _DISPATCH
    assert _DISPATCH[".xlsx"] == ingest_xlsx


def test_router_csv_dispatch_registration() -> None:
    """Test that the .csv extension is correctly registered in the dispatch map."""
    assert ".csv" in _DISPATCH
    assert _DISPATCH[".csv"] == ingest_csv


def test_router_unsupported_raises(tmp_path: Path) -> None:
    """Test that trying to ingest an unsupported file extension raises an IngestError."""
    unsupported_file = Path("dummy.json")
    with pytest.raises(IngestError) as exc_info:
        ingest_file(unsupported_file, Workspace(tmp_path))

    assert "desteklenmeyen uzantı" in str(exc_info.value)
