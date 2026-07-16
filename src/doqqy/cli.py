"""doqqy CLI — typer ile ingest/chunk/embed/query komutları.

Her komut, çalıştırıldığı dizini kök kabul eden bir Workspace kurar
(`Workspace(Path.cwd())`) — kullanıcıya görünen davranış eskisiyle aynı.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from doqqy.config import (
    DEFAULT_TOP_K,
    MAP_COSINE_THRESHOLD,
    MAP_TOP_N_NEIGHBORS,
)
from doqqy.workspace import Workspace

# Windows'ta varsayılan stdout cp1252; Türkçe karakter mojibake olur.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

load_dotenv(Path.cwd() / ".env", override=False)

console = Console()

app = typer.Typer(
    add_completion=False,
    help="doqqy — yerel dokuman bilgi sistemi.",
    no_args_is_help=True,
    rich_markup_mode=None,
    pretty_exceptions_enable=False,
)


def _workspace() -> Workspace:
    return Workspace(Path.cwd())


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
    from doqqy.ingest import ingest_directory

    ws = _workspace()
    ws.ensure_dirs()
    src = source_dir or ws.raw_dir
    console.print(f"[bold cyan]ingest[/bold cyan] kaynak: [dim]{src}[/dim]")
    result = ingest_directory(ws, source_dir=source_dir, limit=limit)

    if result.failed:
        console.print(
            Panel(
                f"[green]Başarılı:[/green] {len(result.succeeded)}  "
                f"[red]Başarısız:[/red] {len(result.failed)}  "
                f"Toplam: {result.total}",
                title="[bold]ingest tamamlandı[/bold]",
                border_style="yellow",
            )
        )
        console.print("[red]Başarısız dosyalar:[/red]")
        for path, err in result.failed[:20]:
            console.print(f"  [red]✗[/red] {path}: [dim]{err}[/dim]")
        if len(result.failed) > 20:
            console.print(f"  [dim]... ve {len(result.failed) - 20} tane daha (bkz. logs/ingest.log).[/dim]")
    else:
        console.print(
            Panel(
                f"[green]✓[/green] {len(result.succeeded)} dosya başarıyla işlendi.",
                title="[bold green]ingest tamamlandı[/bold green]",
                border_style="green",
            )
        )


@app.command()
def chunk(
    processed_dir: Optional[Path] = typer.Option(
        None, "--processed", "-p", help="processed/ klasörü (varsayılan: processed/)."
    ),
) -> None:
    """processed/*.md → chunks/chunks.parquet (header-aware bölme)."""
    from doqqy.chunk import chunk_directory

    ws = _workspace()
    ws.ensure_dirs()
    chunks = chunk_directory(ws, processed_dir=processed_dir)
    console.print(
        Panel(
            f"[green]✓[/green] {len(chunks)} chunk üretildi.",
            title="[bold green]chunk tamamlandı[/bold green]",
            border_style="green",
        )
    )


@app.command()
def embed(
    backend: Optional[str] = typer.Option(
        None, "--backend", help="Vector store backend to use (lancedb | qdrant)."
    ),
) -> None:
    """chunks/chunks.parquet → store.lance (bge-m3 dense)."""
    from doqqy.embed import build_index
    from doqqy.infra.settings import Settings

    ws = _workspace()
    ws.ensure_dirs()
    settings = Settings(vector_backend=backend) if backend else None
    n = build_index(ws, settings=settings)
    console.print(
        Panel(
            f"[green]✓[/green] {n} chunk indekslendi.",
            title="[bold green]embed tamamlandı[/bold green]",
            border_style="green",
        )
    )


@app.command()
def query(
    text: str = typer.Argument(..., help="Sorgu metni."),
    k: int = typer.Option(DEFAULT_TOP_K, "--top-k", "-k", help="Kaç sonuç döndürülecek."),
    full: bool = typer.Option(False, "--full", help="Chunk içeriğini tamamen göster."),
    no_rerank: bool = typer.Option(False, "--no-rerank", help="Reranker'ı atla, RRF sonrası döndür."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Sadece bu tag/klasördeki dokümanları ara."),
    backend: Optional[str] = typer.Option(None, "--backend", help="Vector store backend to use (lancedb | qdrant)."),
) -> None:
    """Hibrit arama (dense+sparse → RRF → reranker): top-k chunk + kaynak."""
    from doqqy.infra.settings import Settings
    from doqqy.query import search

    ws = _workspace()
    settings = Settings(vector_backend=backend) if backend else None
    hits = search(ws, text, k=k, rerank=not no_rerank, tag=tag, settings=settings)
    if not hits:
        console.print(Panel("[yellow]Sonuç bulunamadı.[/yellow]", border_style="yellow"))
        raise typer.Exit(code=1)

    console.print(Panel(f'[bold]"{text}"[/bold] için {len(hits)} sonuç', border_style="cyan"))

    for i, hit in enumerate(hits, 1):
        path = " > ".join(hit.section_path) if hit.section_path else "(başlıksız)"
        ex = hit.extra
        score_parts = []
        if ex.get("dense_rank") is not None:
            score_parts.append(f"dense={ex['dense_rank']}")
        if ex.get("sparse_rank") is not None:
            score_parts.append(f"sparse={ex['sparse_rank']}")
        if ex.get("rrf_score") is not None:
            score_parts.append(f"rrf={ex['rrf_score']:.4f}")
        if ex.get("rerank_score") is not None:
            score_parts.append(f"rerank={ex['rerank_score']:.3f}")
        scores = "  [dim]" + " | ".join(score_parts) + "[/dim]" if score_parts else ""

        body = hit.content if full else hit.content[:400].rstrip()
        ellipsis = f"\n[dim]… ({len(hit.content) - 400} karakter daha)[/dim]" if not full and len(hit.content) > 400 else ""

        console.print(
            Panel(
                f"[dim]{path}[/dim]{scores}\n\n{body}{ellipsis}",
                title=f"[bold cyan][{i}][/bold cyan] {hit.source}",
                border_style="dim",
                box=box.ROUNDED,
            )
        )


@app.command()
def map(
    processed_dir: Optional[Path] = typer.Option(
        None, "--processed", "-p", help="processed/ klasörü (varsayılan: processed/)."
    ),
    pass1_only: bool = typer.Option(False, "--pass1", help="Sadece regex pass çalıştır."),
    pass2_only: bool = typer.Option(False, "--pass2", help="Sadece embedding cosine pass çalıştır."),
    threshold: float = typer.Option(MAP_COSINE_THRESHOLD, "--threshold", help="Cosine benzerlik alt limiti."),
    top_n: int = typer.Option(MAP_TOP_N_NEIGHBORS, "--top-n", help="Her section için max komşu sayısı."),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Sadece bu tag'e sahip sectionlar arasında ilişki kur."),
    backend: Optional[str] = typer.Option(None, "--backend", help="Vector store backend to use (lancedb | qdrant)."),
) -> None:
    """processed/*.md → topics.yaml (regex referanslar + embedding cosine)."""
    from doqqy.infra.settings import Settings
    from doqqy.map_gen import generate_map

    ws = _workspace()
    ws.ensure_dirs()

    do_pass1 = not pass2_only
    do_pass2 = not pass1_only

    settings = Settings(vector_backend=backend) if backend else None
    out = generate_map(
        ws,
        processed_dir=processed_dir,
        pass1=do_pass1,
        pass2=do_pass2,
        cosine_threshold=threshold,
        top_n=top_n,
        tag=tag,
        settings=settings,
    )
    console.print(
        Panel(
            f"[green]✓[/green] Harita oluşturuldu: [dim]{out}[/dim]",
            title="[bold green]map tamamlandı[/bold green]",
            border_style="green",
        )
    )


@app.command()
def index(
    topics: Optional[Path] = typer.Option(
        None, "--topics", help="topics.yaml yolu (varsayılan: proje kökü)."
    ),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o", help="INDEX.md yazılacak klasör (varsayılan: processed/)."
    ),
) -> None:
    """topics.yaml → processed/INDEX.md (Obsidian giriş noktası)."""
    from doqqy.index_gen import generate_index

    ws = _workspace()
    ws.ensure_dirs()
    out = generate_index(
        ws,
        topics_path=topics,
        output_dir=output_dir,
    )
    console.print(
        Panel(
            f"[green]✓[/green] Index oluşturuldu: [dim]{out}[/dim]",
            title="[bold green]index tamamlandı[/bold green]",
            border_style="green",
        )
    )


@app.command()
def inject(
    topics: Optional[Path] = typer.Option(
        None, "--topics", help="topics.yaml yolu (varsayılan: proje kökü)."
    ),
    processed_dir: Optional[Path] = typer.Option(
        None, "--processed", "-p", help="processed/ klasörü (varsayılan: processed/)."
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Dosyaları değiştirmeden neyin enjekte edileceğini göster."),
) -> None:
    """topics.yaml → processed/*.md içine [[wikilink]] enjekte et (Obsidian graph view)."""
    from doqqy.wikilink_inject import inject_links

    ws = _workspace()
    ws.ensure_dirs()
    result = inject_links(
        ws,
        topics_path=topics,
        processed_dir=processed_dir,
        dry_run=dry_run,
    )
    prefix = "[dry-run] " if result.dry_run else ""
    console.print(
        Panel(
            f"[green]✓[/green] {prefix}{result.updated} dosya güncellendi, "
            f"{result.skipped} atlandı, toplam {result.total_links} link enjekte edildi.",
            title="[bold green]inject tamamlandı[/bold green]",
            border_style="green" if not result.dry_run else "yellow",
        )
    )


@app.command()
def tags(
    backend: Optional[str] = typer.Option(
        None, "--backend", help="Vector store backend to use (lancedb | qdrant)."
    ),
) -> None:
    """Sistemde kayıtlı olan tag/klasör/proje isimlerini listeler."""
    from doqqy.infra.settings import Settings
    from doqqy.infra.vectorstore.factory import make_store

    ws = _workspace()
    settings = Settings(vector_backend=backend) if backend else None
    store = make_store(ws, settings)

    try:
        all_tags = store.list_tags()
    except Exception as e:      # noqa: BLE001
        console.print(f"[red]Gömülü tag'ler listelenemedi: {e}[/red]", err=True)
        raise typer.Exit(1) from e
    finally:
        store.close()

    if not all_tags:
        console.print("[yellow]Gösterilecek tag bulunamadı.[/yellow]")
    else:
        table_view = Table(title=f"Bulunan Tag'ler ({len(all_tags)} adet)", box=box.ROUNDED)
        table_view.add_column("Tag", style="cyan")
        for t in sorted(all_tags):
            table_view.add_row(t)
        console.print(table_view)
        console.print(f"\n[dim]Örnek: doqqy query \"sorgu\" --tag {sorted(all_tags)[0]}[/dim]")


@app.command()
def info() -> None:
    """Mevcut pipeline durumunu özetle."""
    ws = _workspace()

    table = Table(title="doqqy pipeline durumu", box=box.ROUNDED)
    table.add_column("Aşama", style="bold")
    table.add_column("Durum")

    raw_count = _count_files(ws.raw_dir)
    table.add_row("raw/", f"{raw_count} dosya")

    proc_count = _count_files(ws.processed_dir, suffix=".md")
    table.add_row("processed/", f"{proc_count} .md dosya")

    if ws.chunks_parquet.exists():
        import pandas as pd
        n = len(pd.read_parquet(ws.chunks_parquet, columns=["chunk_id"]))
        table.add_row("chunks/", f"[green]{n} chunk[/green] (parquet mevcut)")
    else:
        table.add_row("chunks/", "[yellow](boş — `doqqy chunk` çalıştır)[/yellow]")

    if ws.store_dir.exists():
        table.add_row("store.lance", f"[green]mevcut[/green] ({ws.store_dir})")
    else:
        table.add_row("store.lance", "[yellow](boş — `doqqy embed` çalıştır)[/yellow]")

    console.print(table)


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
