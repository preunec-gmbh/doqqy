"""Unit tests for the HTML ingest parser."""

from __future__ import annotations

from pathlib import Path
import pytest

from doqqy.ingest.base import IngestError
from doqqy.ingest.html_ingest import ingest_html
from doqqy.workspace import Workspace


@pytest.fixture()
def ws(tmp_path: Path) -> Workspace:
    """Testler workspace'i açıkça alır — cwd veya monkeypatch bağımlılığı yok."""
    workspace = Workspace(tmp_path)
    workspace.ensure_dirs()
    return workspace


def test_ingest_html_valid(tmp_path: Path, ws: Workspace) -> None:
    """Test that script/style/nav/site-level header/footer and comments are
    stripped, headings become ATX, and metadata has the correct parser.
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

    doc = ingest_html(html_file, ws)

    # Check content features
    # Script, style, nav, site-level header/footer, comments should be stripped
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


def test_ingest_html_empty(tmp_path: Path, ws: Workspace) -> None:
    """Test that an empty or only-boilerplate HTML page raises an IngestError."""
    html_content = "<html><head><style>body{}</style></head><body><header><nav></nav></header><footer></footer></body></html>"
    html_file = tmp_path / "raw" / "empty.html"
    html_file.write_text(html_content, encoding="utf-8")

    with pytest.raises(IngestError) as exc_info:
        ingest_html(html_file, ws)

    assert "boş içerik" in str(exc_info.value)


def test_ingest_html_article_header_kept(tmp_path: Path, ws: Workspace) -> None:
    """Test that a <header> inside <article> (real content, not site chrome)
    is preserved while the site-level footer is stripped.
    """
    html_content = (
        "<html><body>"
        "<article><header><h1>Makale Başlığı</h1></header>"
        "<p>Makale içeriği.</p></article>"
        "<footer>Site footer</footer>"
        "</body></html>"
    )
    html_file = tmp_path / "raw" / "article.html"
    html_file.write_text(html_content, encoding="utf-8")

    doc = ingest_html(html_file, ws)

    assert "# Makale Başlığı" in doc.content
    assert "Makale içeriği." in doc.content
    assert "Site footer" not in doc.content


def test_ingest_html_title_fallback_when_no_h1(tmp_path: Path, ws: Workspace) -> None:
    """Test that <title> becomes the document H1 when the body has no <h1>,
    and is recorded in metadata.
    """
    html_content = (
        "<html><head><title>Sayfa Başlığı</title></head>"
        "<body><p>Sadece paragraf var.</p></body></html>"
    )
    html_file = tmp_path / "raw" / "no-h1.html"
    html_file.write_text(html_content, encoding="utf-8")

    doc = ingest_html(html_file, ws)

    assert doc.content.startswith("# Sayfa Başlığı")
    assert "Sadece paragraf var." in doc.content
    assert doc.metadata["title"] == "Sayfa Başlığı"


def test_ingest_html_title_not_duplicated_when_h1_exists(tmp_path: Path, ws: Workspace) -> None:
    """Test that <title> does not leak into the content (head is dropped)
    when the body already has an <h1>.
    """
    html_content = (
        "<html><head><title>Tarayıcı Sekmesi Başlığı</title></head>"
        "<body><h1>Gerçek Başlık</h1><p>İçerik.</p></body></html>"
    )
    html_file = tmp_path / "raw" / "with-h1.html"
    html_file.write_text(html_content, encoding="utf-8")

    doc = ingest_html(html_file, ws)

    assert "# Gerçek Başlık" in doc.content
    assert "Tarayıcı Sekmesi Başlığı" not in doc.content
    assert doc.metadata["title"] == "Tarayıcı Sekmesi Başlığı"


def test_ingest_html_meta_charset_detection(tmp_path: Path, ws: Workspace) -> None:
    """Test that a windows-1254 (Turkish) page with a <meta charset> declaration
    is decoded correctly ('ş' is 0xFE in cp1254 — undecodable as utf-8).
    """
    html_content = (
        '<html><head><meta charset="windows-1254"></head>'
        "<body><h1>şeker</h1><p>Türkçe içerik: ğüşıöç</p></body></html>"
    )
    html_file = tmp_path / "raw" / "cp1254.html"
    html_file.write_bytes(html_content.encode("cp1254"))

    doc = ingest_html(html_file, ws)

    assert "# şeker" in doc.content
    assert "ğüşıöç" in doc.content
    assert doc.metadata["type"] == "html"
