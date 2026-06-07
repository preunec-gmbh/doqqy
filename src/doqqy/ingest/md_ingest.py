"""Markdown ve plain-text ingester'ı.

- .md → frontmatter ayrıştırılır, içerik aynen korunur.
- .txt → kanonik markdown olarak işlenir (içerik bir kod bloğuna sarılır).
"""

from __future__ import annotations

from pathlib import Path

import frontmatter

from doqqy.config import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR
from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash


def _processed_path(source: Path) -> Path:
    try:
        rel = source.resolve().relative_to(RAW_DIR.resolve())
    except ValueError:
        rel = Path(source.name)
    return (PROCESSED_DIR / rel).with_suffix(".md")


def ingest_md(source: Path) -> Document:
    try:
        with source.open("r", encoding="utf-8") as fh:
            post = frontmatter.load(fh)
    except UnicodeDecodeError:
        with source.open("r", encoding="latin-1") as fh:
            post = frontmatter.load(fh)
    except Exception as exc:  # noqa: BLE001 — frontmatter farklı hatalar fırlatır
        raise IngestError(f"frontmatter parse hatası: {exc}") from exc

    body = post.content
    meta = base_metadata(source, PROJECT_ROOT, kind="md")
    # Varsa orijinal frontmatter'ı koru ama base metadata'nın üstüne yazma.
    for key, value in post.metadata.items():
        meta.setdefault(f"original_{key}", value)
    meta["content_hash"] = content_hash(body)

    return Document(
        source_path=source,
        processed_path=_processed_path(source),
        content=body,
        metadata=meta,
    )


def ingest_txt(source: Path) -> Document:
    try:
        raw = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Windows kaynaklı dosyalar cp1254/latin1 olabilir.
        raw = source.read_text(encoding="latin-1")

    title = source.stem.replace("_", " ").strip()
    body = f"# {title}\n\n```\n{raw.strip()}\n```\n"

    meta = base_metadata(source, PROJECT_ROOT, kind="txt")
    meta["content_hash"] = content_hash(body)

    return Document(
        source_path=source,
        processed_path=_processed_path(source),
        content=body,
        metadata=meta,
    )
