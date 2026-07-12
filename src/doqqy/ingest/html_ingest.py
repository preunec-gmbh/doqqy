"""HTML parser/ingester for the doqqy pipeline."""

from __future__ import annotations

from pathlib import Path

from doqqy.config import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR
from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash


def _processed_path(source: Path) -> Path:
    """Derive the target path under processed/ directory for the canonical Markdown file.

    Replace the original extension with '.md'.
    """
    try:
        rel = source.resolve().relative_to(RAW_DIR.resolve())
    except ValueError:
        rel = Path(source.name)
    return (PROCESSED_DIR / rel).with_suffix(".md")


def ingest_html(source: Path) -> Document:
    """Ingest an HTML file, pre-clean elements/comments with BeautifulSoup,
    and convert to canonical Markdown using markdownify.
    """
    try:
        from bs4 import BeautifulSoup, Comment  # noqa: PLC0415
        from markdownify import markdownify  # noqa: PLC0415
    except ImportError as exc:
        raise IngestError(
            "beautifulsoup4 ve markdownify gerekli: pip install beautifulsoup4 markdownify"
        ) from exc

    # Read the file content, falling back to latin-1 on UnicodeDecodeError
    try:
        raw_text = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw_text = source.read_text(encoding="latin-1")

    # Clean boilerplate / script / style / nav / header / footer and comments
    try:
        soup = BeautifulSoup(raw_text, "html.parser")
        
        # Drop boilerplate tags
        for element in soup(["script", "style", "nav", "header", "footer"]):
            element.decompose()
            
        # Drop HTML comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
            
        cleaned_html = str(soup)
    except Exception as exc:  # noqa: BLE001
        raise IngestError(f"HTML ayrıştırma hatası: {exc}") from exc

    # Convert to markdown with ATX heading style
    try:
        md = markdownify(cleaned_html, heading_style="ATX")
    except Exception as exc:  # noqa: BLE001
        raise IngestError(f"Markdown dönüştürme hatası: {exc}") from exc

    if not md.strip():
        raise IngestError("boş içerik")

    meta = base_metadata(source, PROJECT_ROOT, kind="html")
    meta["parser"] = "markdownify"
    meta["content_hash"] = content_hash(md)

    return Document(
        source_path=source,
        processed_path=_processed_path(source),
        content=md,
        metadata=meta,
    )
