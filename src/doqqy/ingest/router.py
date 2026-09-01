"""Uzantıya göre doğru ingester'a delegasyon + toplu ingest."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from doqqy.config import SUPPORTED_EXTENSIONS, file_log, get_logger
from doqqy.ingest.base import (
    Document,
    IngestError,
    IngestResult,
    drop_superseded_output,
    reset_stem_group_cache,
    reset_tag_log_state,
)
from doqqy.ingest.csv_ingest import ingest_csv
from doqqy.ingest.docx_ingest import ingest_docx
from doqqy.ingest.html_ingest import ingest_html
from doqqy.ingest.md_ingest import ingest_md, ingest_txt
from doqqy.ingest.pdf_ingest import ingest_pdf
from doqqy.ingest.pptx_ingest import ingest_pptx
from doqqy.ingest.xlsx_ingest import ingest_xlsx
from doqqy.ingest.xml_ingest import ingest_xml
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.ingest.router")


_DISPATCH: dict[str, Callable[..., Document]] = {
    ".md": ingest_md,
    ".markdown": ingest_md,
    ".txt": ingest_txt,
    ".pdf": ingest_pdf,
    ".docx": ingest_docx,
    ".pptx": ingest_pptx,
    ".xml": ingest_xml,
    ".xlsx": ingest_xlsx,
    ".csv": ingest_csv,
    ".html": ingest_html,
    ".htm": ingest_html,
}


def ingest_file(source: Path, ws: Workspace, **kwargs: Any) -> Document:
    ext = source.suffix.lower()
    parser = _DISPATCH.get(ext)
    if parser is None:
        raise IngestError(f"desteklenmeyen uzantı: {ext}")

    return parser(source, ws, **kwargs)


def _iter_supported(root: Path) -> list[Path]:
    return sorted(
        p
        for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def ingest_directory(ws: Workspace, *, source_dir: Path | None = None, limit: int | None = None, ocr: bool = False) -> IngestResult:
    """Kaynak klasördeki (varsayılan: ws.raw_dir) tüm desteklenen dosyaları ingest et.

    Bir dosya hata verirse durmaz — log + raporda failed listesine eklenir.
    """
    root = source_dir or ws.raw_dir
    if not root.exists():
        raise FileNotFoundError(f"ingest root yok: {root}")

    files = _iter_supported(root)
    if limit:
        files = files[:limit]

    result = IngestResult()
    # Tag temizleme logları klasör başına tek satır — her çalışma kendi state'iyle başlar.
    reset_tag_log_state()
    # Kardeş taraması önbelleği de çalışmaya özel: iki ingest arasında raw/ değişebilir.
    reset_stem_group_cache()

    # Bu çalışmada yazılan hedefler. processed_path_for() çakışmaları zaten
    # ayrıştırıyor, ama bu invariant ondan bağımsız duruyor: yardımcıyı atlayan
    # ya da ayrıştırma kuralını bozan gelecekteki bir ingester sessizce dosya
    # ezmek yerine gürültüyle başarısız olsun. İki kaynağın aynı .md dosyasına
    # yazması hiçbir koşulda doğru değil.
    written: dict[Path, Path] = {}
    with file_log("doqqy.ingest", ws.logs_dir / "ingest.log"), Progress(
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
                doc = ingest_file(path, ws, ocr=ocr)

                target = doc.processed_path.resolve()
                clash = written.get(target)
                if clash is not None:
                    raise IngestError(
                        f"çıktı yolu çakıştı: {doc.processed_path} zaten {clash} tarafından yazıldı"
                    )

                doc.write()
                written[target] = path

                # Kardeş kümesi bir önceki çalışmadan beri değiştiyse bu belgenin
                # diğer ad biçiminde bir çıktısı duruyor olabilir. Kalırsa chunk/
                # map/inject onu ayrı bir belge sanar ve içerik indekste ikilenir —
                # ingest tekrar çalıştırılabilir olduğu için bu her rerun'da olur.
                removed = drop_superseded_output(
                    ws, path, doc.processed_path, str(doc.metadata.get("source", ""))
                )
                if removed is not None:
                    _LOG.info("bayat çıktı silindi: %s (yeni ad: %s).", removed.name, doc.processed_path.name)

                if doc.processed_path.stem != path.stem:
                    result.disambiguated.append(path)
                    _LOG.warning(
                        "%s adı bir kardeşiyle çakıştı, çıktı %s olarak yazıldı.",
                        path, doc.processed_path.name,
                    )

                result.succeeded.append(path)
            except IngestError as exc:
                _LOG.error("%s: %s", path, exc)
                result.failed.append((path, str(exc)))
            except Exception as exc:  # noqa: BLE001
                _LOG.exception("beklenmedik hata: %s", path)
                result.failed.append((path, f"{type(exc).__name__}: {exc}"))

        _LOG.info(
            "ingest bitti: %d başarılı, %d başarısız, %d ad ayrıştırıldı, toplam %d.",
            len(result.succeeded),
            len(result.failed),
            len(result.disambiguated),
            result.total,
        )
    return result
