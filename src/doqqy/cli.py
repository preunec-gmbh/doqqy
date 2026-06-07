"""doqqy CLI — typer ile ingest/chunk/embed/query komutları."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer

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

app = typer.Typer(
    add_completion=False,
    help="doqqy — yerel dokuman bilgi sistemi.",
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
    from doqqy.ingest import ingest_directory

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
    from doqqy.chunk import chunk_directory

    ensure_dirs()
    src = processed_dir or PROCESSED_DIR
    chunks = chunk_directory(src)
    typer.echo(f"OK: {len(chunks)} chunk üretildi.")


@app.command()
def embed() -> None:
    """chunks/chunks.parquet → store.lance (bge-m3 dense)."""
    from doqqy.embed import build_index

    ensure_dirs()
    n = build_index()
    typer.echo(f"OK: {n} chunk indekslendi.")


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

    hits = search(text, k=k, rerank=not no_rerank)
    if not hits:
        typer.echo("Sonuç yok.")
        raise typer.Exit(code=1)

    for i, hit in enumerate(hits, 1):
        path = " > ".join(hit.section_path) if hit.section_path else "(başlıksız)"
        typer.echo(f"\\n[{i}] {hit.source}")
        typer.echo(f"{path}")

        # Aşama skorlarını göster
        ex = hit.extra
        score_parts = []
        if ex.get("dense_rank") is not None:
            score_parts.append(f"dense_rank={ex['dense_rank']}")
        if ex.get("sparse_rank") is not None:
            score_parts.append(f"sparse_rank={ex['sparse_rank']}")
        if ex.get("rrf_score") is not None:
            score_parts.append(f"rrf={ex['rrf_score']:.4f}")
        if ex.get("rerank_score") is not None:
            score_parts.append(f"rerank={ex['rerank_score']:.3f}")
        if score_parts:
            typer.echo(f"    [{' | '.join(score_parts)}]")

        body = hit.content if full else hit.content[:400].rstrip()
        typer.echo(_indent(body, "    "))
        if not full and len(hit.content) > 400:
            typer.echo(f"    … ({len(hit.content) - 400} karakter daha)")


def _indent(text: str, prefix: str) -> str:
    return "\n".join(prefix + line for line in text.splitlines())


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
        processed_dir=p_dir,
        pass1=p1,
        pass2=p2,
        cosine_threshold=threshold,
        top_n=top_n,
        tag=tag,
    )
    typer.echo(f"OK: {out}")


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
    typer.echo(f"OK: {out}")


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
    typer.echo(
        f"{prefix}OK: {result.updated} dosya güncellendi, "
        f"{result.skipped} atlandı, toplam {result.total_links} link enjekte edildi."
    )


@app.command()

@app.command()
def tags() -> None:
    """Sistemde kayıtlı olan tag/klasör/proje isimlerini listeler."""
    import lancedb # type: ignore
    from doqqy.config import STORE_DIR, LANCE_TABLE
    
    if not STORE_DIR.exists():
        typer.echo("LanceDB bulunamadı. Önce `doqqy embed` çalıştırın.", err=True)
        raise typer.Exit(1)
        
    db = lancedb.connect(STORE_DIR)
    if LANCE_TABLE not in db.table_names():
        typer.echo("LanceDB tablosu boş.", err=True)
        raise typer.Exit(1)
        
    table = db.open_table(LANCE_TABLE)
    df = table.search().limit(100000).to_pandas()
    
    if "tags" not in df.columns:
        typer.echo("Kayıtlı tag bulunamadı (Eski index kullanılıyor olabilir).")
        raise typer.Exit()
        
    all_tags = set()
    for t_list in df["tags"].dropna():
        # pandas array of strings
        if isinstance(t_list, (list, tuple, np.ndarray)):
            for t in t_list:
                all_tags.add(t)
                
    if not all_tags:
        typer.echo("Gösterilecek tag bulunamadı.")
    else:
        typer.echo(f"\nBulunan tag'ler: ({len(all_tags)} adet)")
        typer.echo("-" * 40)
        for t in sorted(all_tags):
            typer.echo(f"- {t}")
        typer.echo("-" * 40)
        typer.echo("Örnek kullanım: doqqy query \"sorgu\" --tag " + list(all_tags)[0])


@app.command()
def info() -> None:
    """Mevcut pipeline durumunu özetle."""
    from doqqy.config import CHUNKS_PARQUET, STORE_DIR

    typer.echo(f"raw/        : {_count_files(RAW_DIR)} dosya")
    typer.echo(f"processed/  : {_count_files(PROCESSED_DIR, suffix='.md')} md dosya")
    if CHUNKS_PARQUET.exists():
        import pandas as pd

        n = len(pd.read_parquet(CHUNKS_PARQUET, columns=["chunk_id"]))
        typer.echo(f"chunks/     : {n} chunk (parquet mevcut)")
    else:
        typer.echo("chunks/     : (boş — `doqqy chunk` çalıştır)")
    if STORE_DIR.exists():
        typer.echo(f"store.lance : mevcut ({STORE_DIR})")
    else:
        typer.echo("store.lance : (boş — `doqqy embed` çalıştır)")


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
