"""Ingest katmanı: format-spesifik parser'lar → kanonik markdown."""

from docq.ingest.base import Document, IngestError, IngestResult
from docq.ingest.router import ingest_file, ingest_directory

__all__ = ["Document", "IngestError", "IngestResult", "ingest_file", "ingest_directory"]
