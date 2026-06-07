"""Ingest katmanı ortak tipleri."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Document:
    """Kanonik markdown haline gelmiş bir doküman."""

    source_path: Path                       # raw/auth/jwt.pdf
    processed_path: Path                    # processed/auth/jwt.md
    content: str                            # kanonik markdown
    metadata: dict[str, Any] = field(default_factory=dict)

    def write(self) -> None:
        """processed_path'e frontmatter + content yaz."""
        self.processed_path.parent.mkdir(parents=True, exist_ok=True)
        body = _serialize(self)
        self.processed_path.write_text(body, encoding="utf-8")


def _serialize(doc: Document) -> str:
    """Frontmatter blok + body."""
    import yaml  # type: ignore

    fm = yaml.safe_dump(doc.metadata, allow_unicode=True, sort_keys=True).strip()
    return f"---\n{fm}\n---\n\n{doc.content.strip()}\n"


@dataclass
class IngestResult:
    """Bir ingest çalışmasının özet sonucu."""

    succeeded: list[Path] = field(default_factory=list)
    failed: list[tuple[Path, str]] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.succeeded) + len(self.failed) + len(self.skipped)


class IngestError(Exception):
    """Parser-spesifik hatalar bu tipte sarılır."""


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def base_metadata(source: Path, project_root: Path, kind: str) -> dict[str, Any]:
    rel = source.relative_to(project_root) if source.is_absolute() else source

    # "raw/" veya proje_root altındaki klasör kırılımlarını filtrele
    # Örneğin: raw/bulut-saha/erimelektronik-b2b-sistemi/veri.md
    # -> tags: ["bulut-saha", "erimelektronik-b2b-sistemi"]
    parts = list(rel.parts)
    if parts and parts[0] == "raw":
        parts = parts[1:]

    # Son parça dosya adı, onu atıyoruz. Kalanlar klasör isimleri (tag'ler)
    tags = parts[:-1] if len(parts) > 1 else []

    return {
        "source": str(rel).replace("\\", "/"),
        "type": kind,
        "tags": tags,
        "ingested_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
