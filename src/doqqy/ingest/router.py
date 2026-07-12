"""Uzantıya göre doğru ingester'a delegasyon + toplu ingest."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn, TimeElapsedColumn

from doqqy.config import RAW_DIR, SUPPORTED_EXTENSIONS, get_logger
from doqqy.ingest.base import Document, IngestError, IngestResult
from doqqy.ingest.docx_ingest import ingest_docx
from doqqy.ingest.md_ingest import ingest_md, ingest_txt
from doqqy.ingest.pdf_ingest import ingest_pdf
from doqqy.ingest.xml_ingest import ingest_xml
from doqqy.ingest.xlsx_ingest import ingest_xlsx
from doqqy.ingest.csv_ingest import ingest_csv
from doqqy.ingest.html_ingest import ingest_html


_LOG = get_logger("doqqy.ingest.router", log_file="ingest.log")


_DISPATCH: dict[str, Callable[[Path], Document]] = {
    ".md": ingest_md,
    ".markdown": ingest_md,
    ".txt": ingest_txt,
    ".pdf": ingest_pdf,
    ".docx": ingest_docx,
    ".xml": ingest_xml,
    ".xlsx": ingest_xlsx,
    ".csv": ingest_csv,
    ".html": ingest_html,
    ".htm": ingest_html,
}


def ingest_file(source: Path) -> Document:
    ext = source.suffix.lower()
    parser = _DISPATCH.get(ext)
    if parser is None:
        raise IngestError(f"desteklenmeyen uzantı: {ext}")
    return parser(source)


def _iter_supported(root: Path) -> list[Path]:
    return sorted(
        p
        for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def ingest_directory(root: Path | None = None, *, limit: int | None = None) -> IngestResult:
    """raw/ altındaki tüm desteklenen dosyaları ingest et.

    Bir dosya hata verirse durmaz — log + raporda failed listesine eklenir.
    """
    root = root or RAW_DIR
    if not root.exists():
        raise FileNotFoundError(f"ingest root yok: {root}")

    files = _iter_supported(root)
    if limit:
        files = files[:limit]

    result = IngestResult()
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]ingest[/bold cyan]"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("ingest", total=len(files))
        for path in files:
            progress.update(task, description=f"[dim]{path.name}[/dim]", advance=1)
            try:
                doc = ingest_file(path)
                doc.write()
                result.succeeded.append(path)
            except IngestError as exc:
                _LOG.error("%s: %s", path, exc)
                result.failed.append((path, str(exc)))
            except Exception as exc:  # noqa: BLE001
                _LOG.exception("beklenmedik hata: %s", path)
                result.failed.append((path, f"{type(exc).__name__}: {exc}"))

    _LOG.info(
        "ingest bitti: %d başarılı, %d başarısız, toplam %d.",
        len(result.succeeded),
        len(result.failed),
        result.total,
    )
    return result
