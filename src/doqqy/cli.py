"""doqqy CLI — typer ile ingest/chunk/embed/query komutları."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from doqqy.config import (
    DEFAULT_TOP_K,
    MAP_COSINE_THRESHOLD,
    MAP_TOP_N_NEIGHBORS,
    PROCESSED_DIR,
    RAW_DIR,
    TOPICS_YAML,
    ensure_dirs,
)

# Windows'ta varsayılan stdout cp1252; Türkçe karakter mojibake olur.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError):
        pass

console = Console()

app = typer.Typer(
    add_completion=False,
    help="doqqy — yerel dokuman bilgi sistemi.",
    no_args_is_help=True,
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
    from doqqy.ingest import ingest_directory

    ensure_dirs()
    src = source_dir or RAW_DIR
    console.print(f"[bold cyan]ingest[/bold cyan] kaynak: [dim]{src}[/dim]")
    result = ingest_directory(src, limit=limit)

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

    ensure_dirs()
    src = processed_dir or PROCESSED_DIR
    chunks = chunk_directory(src)
    console.print(
        Panel(
            f"[green]✓[/green] {len(chunks)} chunk üretildi.",
            title="[bold green]chunk tamamlandı[/bold green]",
            border_style="green",
        )
    )


@app.command()
def embed() -> None:
    """chunks/chunks.parquet → store.lance (bge-m3 dense)."""
    from doqqy.embed import build_index

    ensure_dirs()
    n = build_index()
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
) -> None:
    """Hibrit arama (dense+sparse → RRF → reranker): top-k chunk + kaynak."""
    from doqqy.query import search

    hits = search(text, k=k, rerank=not no_rerank, tag=tag)
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
) -> None:
    """processed/*.md → topics.yaml (regex referanslar + embedding cosine)."""
    from doqqy.map_gen import generate_map

    ensure_dirs()
    src = processed_dir or PROCESSED_DIR

    do_pass1 = not pass2_only
    do_pass2 = not pass1_only

    out = generate_map(
        processed_dir=src,
        pass1=do_pass1,
        pass2=do_pass2,
        cosine_threshold=threshold,
        top_n=top_n,
        tag=tag,
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

    ensure_dirs()
    out = generate_index(
        topics_path=topics or TOPICS_YAML,
        output_dir=output_dir or PROCESSED_DIR,
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

    ensure_dirs()
    result = inject_links(
        topics_path=topics or TOPICS_YAML,
        processed_dir=processed_dir or PROCESSED_DIR,
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
def tags() -> None:
    """Sistemde kayıtlı olan tag/klasör/proje isimlerini listeler."""
    import numpy as np
    import lancedb  # type: ignore
    from doqqy.config import STORE_DIR, LANCE_TABLE

    if not STORE_DIR.exists():
        console.print("[red]LanceDB bulunamadı. Önce `doqqy embed` çalıştırın.[/red]", err=True)
        raise typer.Exit(1)

    db = lancedb.connect(STORE_DIR)
    if LANCE_TABLE not in db.table_names():
        console.print("[red]LanceDB tablosu boş.[/red]", err=True)
        raise typer.Exit(1)

    table = db.open_table(LANCE_TABLE)
    df = table.search().limit(100000).to_pandas()

    if "tags" not in df.columns:
        console.print("[yellow]Kayıtlı tag bulunamadı (Eski index kullanılıyor olabilir).[/yellow]")
        raise typer.Exit()

    all_tags: set[str] = set()
    for t_list in df["tags"].dropna():
        if isinstance(t_list, (list, tuple, np.ndarray)):
            for t in t_list:
                all_tags.add(t)

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
    from doqqy.config import CHUNKS_PARQUET, STORE_DIR

    table = Table(title="doqqy pipeline durumu", box=box.ROUNDED)
    table.add_column("Aşama", style="bold")
    table.add_column("Durum")

    raw_count = _count_files(RAW_DIR)
    table.add_row("raw/", f"{raw_count} dosya")

    proc_count = _count_files(PROCESSED_DIR, suffix=".md")
    table.add_row("processed/", f"{proc_count} .md dosya")

    if CHUNKS_PARQUET.exists():
        import pandas as pd
        n = len(pd.read_parquet(CHUNKS_PARQUET, columns=["chunk_id"]))
        table.add_row("chunks/", f"[green]{n} chunk[/green] (parquet mevcut)")
    else:
        table.add_row("chunks/", "[yellow](boş — `doqqy chunk` çalıştır)[/yellow]")

    if STORE_DIR.exists():
        table.add_row("store.lance", f"[green]mevcut[/green] ({STORE_DIR})")
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
