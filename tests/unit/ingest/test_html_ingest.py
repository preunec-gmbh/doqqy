"""Unit tests for the HTML ingest parser."""

from __future__ import annotations

from pathlib import Path
import pytest

from doqqy.ingest.base import IngestError
from doqqy.ingest.html_ingest import ingest_html


@pytest.fixture(autouse=True)
def setup_mock_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Fixture to mock project root directories.

    This ensures that absolute paths created during testing fall under the
    mocked RAW_DIR and do not cause path resolution errors in base_metadata.
    """
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir = tmp_path / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr("doqqy.ingest.html_ingest.PROJECT_ROOT", tmp_path)
    monkeypatch.setattr("doqqy.ingest.html_ingest.RAW_DIR", raw_dir)
    monkeypatch.setattr("doqqy.ingest.html_ingest.PROCESSED_DIR", processed_dir)


def test_ingest_html_valid(tmp_path: Path) -> None:
    """Test that script/style/nav/header/footer and comments are stripped,
    headings become ATX, and metadata has the correct parser.
    """
    html_content = """
    <html>
        <head>
            <style>body { color: blue; }</style>
        </head>
        <body>
            <header>
                <h1>Site Title</h1>
                <nav><a href="#">Link</a></nav>
            </header>
            <!-- Important Comment -->
            <main>
                <h1>Main Heading</h1>
                <p>This is paragraph text with some <script>console.log("x");</script> script.</p>
                <h2>Sub-heading</h2>
                <p>Paragraph under sub-heading.</p>
            </main>
            <footer>Page footer</footer>
        </body>
    </html>
    """
    html_file = tmp_path / "raw" / "valid.html"
    html_file.write_text(html_content, encoding="utf-8")

    doc = ingest_html(html_file)

    # Check content features
    # Script, style, nav, header, footer, comments should be stripped
    assert "Site Title" not in doc.content
    assert "body {" not in doc.content
    assert "Link" not in doc.content
    assert "Page footer" not in doc.content
    assert "Important Comment" not in doc.content
    assert "console.log" not in doc.content

    # Headings become ATX format
    assert "# Main Heading" in doc.content
    assert "## Sub-heading" in doc.content

    # Metadata checks
    assert doc.metadata["type"] == "html"
    assert doc.metadata["parser"] == "markdownify"
    assert "content_hash" in doc.metadata


def test_ingest_html_empty(tmp_path: Path) -> None:
    """Test that an empty or only-boilerplate HTML page raises an IngestError."""
    html_content = "<html><head><style>body{}</style></head><body><header><nav></nav></header><footer></footer></body></html>"
    html_file = tmp_path / "raw" / "empty.html"
    html_file.write_text(html_content, encoding="utf-8")

    with pytest.raises(IngestError) as exc_info:
        ingest_html(html_file)

    assert "boş içerik" in str(exc_info.value)


def test_ingest_html_encoding_fallback(tmp_path: Path) -> None:
    """Test ingesting an HTML file encoded with latin-1."""
    # Character 'ş' in latin-1 (cp1252) is 0xFE
    html_bytes = b"<html><body><h1>\xfeeker</h1></body></html>"
    html_file = tmp_path / "raw" / "latin1.html"
    html_file.write_bytes(html_bytes)

    doc = ingest_html(html_file)
    assert doc.metadata["type"] == "html"
    # Depending on how read_text decodes latin-1, 0xFE might decode to þ/ş.
    # We verify it doesn't crash and captures the decoded character.
    assert "þeker" in doc.content or "şeker" in doc.content or "þ" in doc.content
