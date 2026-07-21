"""XML parser/ingester for the doqqy pipeline."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from typing import Any
from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash, processed_path_for
from doqqy.workspace import Workspace


def _extract_leaf_texts(element: ET.Element) -> list[str]:
    """Recursively extract raw text content from the leaf nodes of an XML element.

    A leaf node is defined as an element with no child elements (len == 0).
    """
    texts = []
    if len(element) > 0:
        for child in element:
            texts.extend(_extract_leaf_texts(child))
    else:
        if element.text:
            text_stripped = element.text.strip()
            if text_stripped:
                texts.append(text_stripped)
    return texts


def ingest_xml(source: Path, ws: Workspace, **_kwargs: Any) -> Document:
    """Ingest an XML file, parse it, and produce a canonical Markdown Document.

    This function is format-agnostic downstream, converting XML structure to formatted markdown.
    It extracts natural language texts from leaf elements for a content summary section ("İçerik Özeti")
    and preserves the full formatted XML in a fenced code block to be picked up by sparse retrieval.
    """
    # Read the file content, falling back to latin-1 on UnicodeDecodeError (e.g. legacy Windows encodings)
    try:
        raw_text = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw_text = source.read_text(encoding="latin-1")

    # Parse the XML content
    try:
        root = ET.fromstring(raw_text)
    except ET.ParseError as exc:
        raise IngestError(f"XML parsing failed: {exc}") from exc

    # Format (pretty-print) the XML tree in-place
    ET.indent(root, space="  ")
    pretty_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")

    # Generate document title from filename
    title = source.stem.replace("_", " ").strip()

    # Extract summary text from leaf nodes
    leaf_texts = _extract_leaf_texts(root)
    summary = " ".join(leaf_texts)

    # Construct the canonical Markdown body
    # Standard header sections are used to keep the structure clear and consistent
    markdown_body = f"# {title}\n\n## İçerik Özeti\n\n{summary}\n\n## XML Kaynağı\n\n```xml\n{pretty_xml.strip()}\n```\n"

    # Derive base metadata and compute content hash
    meta = base_metadata(source, ws.root, kind="xml")
    meta["parser"] = "etree"
    meta["content_hash"] = content_hash(markdown_body)

    return Document(
        source_path=source,
        processed_path=processed_path_for(source, ws),
        content=markdown_body,
        metadata=meta,
    )
