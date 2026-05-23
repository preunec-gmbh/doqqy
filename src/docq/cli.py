"""docq CLI — typer ile ingest/chunk/embed/query komutları."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer

from docq.config import (
    DEFAULT_TOP_K,
    PROCESSED_DIR,
    RAW_DIR,
    ensure_dirs,
)

# Windows'ta varsayılan stdout cp1252; Türkçe karakter mojibake olur.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

app = typer.Typer(
    add_completion=False,
    help="docq — yerel dokuman bilgi sistemi.",
    no_args_is_help=True,
    # Rich'in Windows legacy console renderer'ı Türkçe karakterlerde çöküyor;
    # düz click help'i kullan.
    rich_markup_mode=None,
    pretty_exceptions_enable=False,
)


@app.command()
def ingest(
    source_dir: Optional[Path] = typer.Option(
        None, "--source", "-s", help="Kaynak klasör (varsayılan: raw/)."
    ),
    limit: Optional[int] = typer.Option(
        None, "--limit", "-n", help="İlk N dosyayı al (test için)."
    ),
) -> None:
    """raw/ altındaki dosyaları processed/ altına kanonik markdown olarak yaz."""
    from docq.ingest import ingest_directory

    ensure_dirs()
    src = source_dir or RAW_DIR
    typer.echo(f"ingest kaynak: {src}")
    result = ingest_directory(src, limit=limit)
    typer.echo(
        f"OK: {len(result.succeeded)} başarılı, "
        f"{len(result.failed)} başarısız, toplam {result.total}."
    )
    if result.failed:
        typer.echo("\nBaşarısız dosyalar:")
        for path, err in result.failed[:20]:
            typer.echo(f"  - {path}: {err}")
        if len(result.failed) > 20:
            typer.echo(f"  ... ve {len(result.failed) - 20} tane daha (bkz. logs/ingest.log).")


@app.command()
def chunk(
    processed_dir: Optional[Path] = typer.Option(
        None, "--processed", "-p", help="processed/ klasörü (varsayılan: processed/)."
    ),
) -> None:
    """processed/*.md → chunks/chunks.parquet (header-aware bölme)."""
    from docq.chunk import chunk_directory

    ensure_dirs()
    src = processed_dir or PROCESSED_DIR
    chunks = chunk_directory(src)
    typer.echo(f"OK: {len(chunks)} chunk üretildi.")


@app.command()
def embed() -> None:
    """chunks/chunks.parquet → store.lance (bge-m3 dense)."""
    from docq.embed import build_index

    ensure_dirs()
    n = build_index()
    typer.echo(f"OK: {n} chunk indekslendi.")


@app.command()
def query(
    text: str = typer.Argument(..., help="Sorgu metni."),
    k: int = typer.Option(DEFAULT_TOP_K, "--top-k", "-k", help="Kaç sonuç döndürülecek."),
    full: bool = typer.Option(False, "--full", help="Chunk içeriğini tamamen göster."),
) -> None:
    """Dense vektör ile arama: top-k chunk + kaynak."""
    from docq.query import search

    hits = search(text, k=k)
    if not hits:
        typer.echo("Sonuç yok.")
        raise typer.Exit(code=1)

    for i, hit in enumerate(hits, 1):
        path = " > ".join(hit.section_path) if hit.section_path else "(başlıksız)"
        typer.echo(f"\n[{i}] score={hit.score:.3f}  {hit.source}")
        typer.echo(f"    {path}")
        body = hit.content if full else hit.content[:400].rstrip()
        typer.echo(_indent(body, "    "))
        if not full and len(hit.content) > 400:
            typer.echo(f"    … ({len(hit.content) - 400} karakter daha)")


def _indent(text: str, prefix: str) -> str:
    return "\n".join(prefix + line for line in text.splitlines())


@app.command()
def info() -> None:
    """Mevcut pipeline durumunu özetle."""
    from docq.config import CHUNKS_PARQUET, STORE_DIR

    typer.echo(f"raw/        : {_count_files(RAW_DIR)} dosya")
    typer.echo(f"processed/  : {_count_files(PROCESSED_DIR, suffix='.md')} md dosya")
    if CHUNKS_PARQUET.exists():
        import pandas as pd

        n = len(pd.read_parquet(CHUNKS_PARQUET, columns=["chunk_id"]))
        typer.echo(f"chunks/     : {n} chunk (parquet mevcut)")
    else:
        typer.echo("chunks/     : (boş — `docq chunk` çalıştır)")
    if STORE_DIR.exists():
        typer.echo(f"store.lance : mevcut ({STORE_DIR})")
    else:
        typer.echo("store.lance : (boş — `docq embed` çalıştır)")


def _count_files(root: Path, suffix: str | None = None) -> int:
    if not root.exists():
        return 0
    return sum(
        1
        for p in root.rglob("*")
        if p.is_file() and (suffix is None or p.suffix.lower() == suffix)
    )


if __name__ == "__main__":
    app()
