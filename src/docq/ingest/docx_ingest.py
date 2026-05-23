"""DOCX ingester'ı: pandoc (ana) → mammoth (fallback).

pandoc CLI kurulu değilse (`winget install pandoc`), otomatik olarak mammoth'a düşer.
mammoth saf Python — kurulum gerekmiyor, ama tablo/karmaşık layout'larda pandoc kadar iyi değil.
"""

from __future__ import annotations

from pathlib import Path

from docq.config import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR, get_logger
from docq.ingest.base import Document, IngestError, base_metadata, content_hash

_LOG = get_logger("docq.ingest.docx", log_file="ingest.log")


def _processed_path(source: Path) -> Path:
    rel = source.relative_to(RAW_DIR)
    return (PROCESSED_DIR / rel).with_suffix(".md")


def _parse_with_pandoc(source: Path) -> str:
    """pypandoc → markdown. pandoc binary'si yoksa OSError fırlatır."""
    import pypandoc  # type: ignore

    # pandoc'un GFM çıktısı (tablo, kod blokları, başlıklar için iyi).
    return pypandoc.convert_file(
        str(source),
        to="gfm",
        format="docx",
        extra_args=["--wrap=none", "--standalone=false"],
    )


def _parse_with_mammoth(source: Path) -> str:
    """mammoth → markdown. Saf Python, sistem bağımlılığı yok."""
    import mammoth  # type: ignore

    with source.open("rb") as fh:
        result = mammoth.convert_to_markdown(fh)
    return result.value


def ingest_docx(source: Path) -> Document:
    md: str | None = None
    parser_used: str | None = None
    pandoc_error: Exception | None = None

    try:
        md = _parse_with_pandoc(source)
        parser_used = "pandoc"
    except OSError as exc:
        # pypandoc, pandoc binary'si yoksa OSError("No pandoc was found ...") fırlatır.
        pandoc_error = exc
        _LOG.info("pandoc kurulu değil (%s) — mammoth'a düşülüyor.", source.name)
    except Exception as exc:  # noqa: BLE001
        pandoc_error = exc
        _LOG.warning("pandoc başarısız (%s): %s — mammoth denenecek.", source.name, exc)

    if md is None or not md.strip():
        try:
            md = _parse_with_mammoth(source)
            parser_used = "mammoth"
        except Exception as exc:  # noqa: BLE001
            raise IngestError(
                f"hem pandoc hem mammoth başarısız. pandoc: {pandoc_error}. mammoth: {exc}"
            ) from exc

    if not md.strip():
        raise IngestError("parser boş içerik döndürdü.")

    meta = base_metadata(source, PROJECT_ROOT, kind="docx")
    meta["parser"] = parser_used
    meta["content_hash"] = content_hash(md)

    return Document(
        source_path=source,
        processed_path=_processed_path(source),
        content=md,
        metadata=meta,
    )
