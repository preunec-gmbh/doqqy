"""DOCX ingester'ı: pandoc (ana) → mammoth (fallback).

pandoc CLI kurulu değilse (`winget install pandoc`), otomatik olarak mammoth'a düşer.
mammoth saf Python — kurulum gerekmiyor, ama tablo/karmaşık layout'larda pandoc kadar iyi değil.
"""

from __future__ import annotations

from pathlib import Path

from doqqy.config import get_logger
from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash, processed_path_for
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.ingest.docx")


def _parse_with_pandoc(source: Path) -> str:
    """pypandoc → markdown. Sistemde yoksa otomatik olarak pandoc'u pypandoc içine indirir."""
    import pypandoc  # type: ignore

    try:
        pypandoc.get_pandoc_version()
    except OSError:
        _LOG.info("pandoc binary bulunamadı, pypandoc.download_pandoc() ile otomatik indiriliyor...")
        # Auto-download pandoc to the specific location pypandoc checks
        pypandoc.download_pandoc()
        _LOG.info("pandoc başarıyla indirildi.")

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


def ingest_docx(source: Path, ws: Workspace) -> Document:
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

    meta = base_metadata(source, ws.root, kind="docx")
    meta["parser"] = parser_used
    meta["content_hash"] = content_hash(md)

    return Document(
        source_path=source,
        processed_path=processed_path_for(source, ws),
        content=md,
        metadata=meta,
    )
