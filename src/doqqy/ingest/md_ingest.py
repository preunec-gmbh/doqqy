"""Markdown ve plain-text ingester'ı.

- .md → frontmatter ayrıştırılır, içerik aynen korunur.
- .txt → kanonik markdown olarak işlenir (içerik bir kod bloğuna sarılır).
"""

from __future__ import annotations

import re
from pathlib import Path

import frontmatter

from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash, processed_path_for
from doqqy.workspace import Workspace


def _try_fix_yaml_frontmatter(content: str) -> str:
    """YAML frontmatter içinde tırnaksız colon (:) kullanımından kaynaklı
    mapping values are not allowed in this context hatasını engellemek için
    içerikteki başlık vb gibi alanlardaki verileri tırnak içine alır."""
    if not content.startswith("---"):
        return content

    parts = content.split("---", 2)
    if len(parts) >= 3:
        fm = parts[1]
        # title: SORULAR: -> title: "SORULAR:" (sadece tırnak içinde olmayanlara uygular)
        new_fm = re.sub(
            r'^(title:|project:|team:)\s+(?![\"\'])(.+)(?<![\"\'])$',
            r'\1 "\2"',
            fm,
            flags=re.MULTILINE
        )
        parts[1] = new_fm
        return "---".join(parts)

    return content


def ingest_md(source: Path, ws: Workspace) -> Document:
    # Önce dosyayı string olarak okuyalım ve gerekiyorsa YAML'ı düzeltelim
    try:
        raw_text = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw_text = source.read_text(encoding="latin-1")

    fixed_text = _try_fix_yaml_frontmatter(raw_text)

    try:
        post = frontmatter.loads(fixed_text)
    except Exception as exc:  # noqa: BLE001 — frontmatter farklı hatalar fırlatır
        raise IngestError(f"frontmatter parse hatası: {exc}") from exc

    body = post.content
    meta = base_metadata(source, ws.root, kind="md")
    # Varsa orijinal frontmatter'ı koru ama base metadata'nın üstüne yazma.
    for key, value in post.metadata.items():
        meta.setdefault(f"original_{key}", value)
    meta["content_hash"] = content_hash(body)

    return Document(
        source_path=source,
        processed_path=processed_path_for(source, ws),
        content=body,
        metadata=meta,
    )


def ingest_txt(source: Path, ws: Workspace) -> Document:
    try:
        raw = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Windows kaynaklı dosyalar cp1254/latin1 olabilir.
        raw = source.read_text(encoding="latin-1")

    title = source.stem.replace("_", " ").strip()
    body = f"# {title}\n\n```\n{raw.strip()}\n```\n"

    meta = base_metadata(source, ws.root, kind="txt")
    meta["content_hash"] = content_hash(body)

    return Document(
        source_path=source,
        processed_path=processed_path_for(source, ws),
        content=body,
        metadata=meta,
    )
