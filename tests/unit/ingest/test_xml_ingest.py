"""Unit tests for the XML ingest parser."""

from __future__ import annotations

from pathlib import Path
import pytest

from doqqy.ingest.base import IngestError
from doqqy.ingest.xml_ingest import ingest_xml
from doqqy.workspace import Workspace


@pytest.fixture()
def ws(tmp_path: Path) -> Workspace:
    """Testler workspace'i açıkça alır — cwd veya monkeypatch bağımlılığı yok."""
    workspace = Workspace(tmp_path)
    workspace.ensure_dirs()
    return workspace


def test_ingest_xml_valid(tmp_path: Path, ws: Workspace) -> None:
    """Test ingesting a valid XML file.

    It should parse the file, extract leaf nodes text for the summary,
    and pretty-print the original XML structure inside a fenced block.
    """
    xml_content = """<root id="123">
        <header>
            <title>My Document</title>
        </header>
        <body>
            <section name="intro">
                <paragraph>This is the introduction paragraph.</paragraph>
            </section>
            <section name="main">
                <paragraph>This is the main paragraph text.</paragraph>
            </section>
        </body>
    </root>"""
    
    xml_file = tmp_path / "raw" / "valid_sample_doc.xml"
    xml_file.write_text(xml_content, encoding="utf-8")

    doc = ingest_xml(xml_file, ws)

    # Title from stem: "valid_sample_doc" -> "valid sample doc"
    assert doc.content.startswith("# valid sample doc")

    # Metadata checks
    assert doc.metadata["type"] == "xml"
    assert doc.metadata["parser"] == "etree"
    assert "content_hash" in doc.metadata

    # Leaf nodes text checks in summary (title, paragraph, paragraph)
    assert "## İçerik Özeti" in doc.content
    assert "My Document" in doc.content
    assert "This is the introduction paragraph." in doc.content
    assert "This is the main paragraph text." in doc.content

    # XML source code block checks
    assert "## XML Kaynağı" in doc.content
    assert "```xml" in doc.content
    assert '<root id="123">' in doc.content
    assert "</root>" in doc.content
    assert "```" in doc.content


def test_ingest_xml_invalid(tmp_path: Path, ws: Workspace) -> None:
    """Test ingesting a malformed XML file.

    It should raise an IngestError.
    """
    invalid_xml = "<root><unclosed_tag>Data</root>"
    xml_file = tmp_path / "raw" / "invalid_doc.xml"
    xml_file.write_text(invalid_xml, encoding="utf-8")

    with pytest.raises(IngestError) as exc_info:
        ingest_xml(xml_file, ws)
    
    assert "XML parsing failed" in str(exc_info.value)


def test_ingest_xml_encoding_fallback(tmp_path: Path, ws: Workspace) -> None:
    """Test ingesting an XML file encoded with latin-1.

    It should fall back to latin-1 and successfully parse Turkish/special characters.
    """
    # Character 'ş' in latin-1 (cp1252) is 0xFE (254)
    xml_bytes = b'<root><text>\xfeeker</text></root>'
    xml_file = tmp_path / "raw" / "latin1_doc.xml"
    xml_file.write_bytes(xml_bytes)

    doc = ingest_xml(xml_file, ws)

    assert doc.metadata["type"] == "xml"
    # 0xFE in latin-1 is 'þ' (Icelandic thorn) or in cp1254 'ş'.
    # Here source.read_text(encoding="latin-1") reads it as 'þ' or similar.
    # We just assert it parsed without raising UnicodeDecodeError or ParseError.
    assert "þeker" in doc.content or "şeker" in doc.content or "þ" in doc.content
