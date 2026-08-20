"""Değerlendirme motoru için CLI giriş noktası: python -m tests.eval"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from rich.console import Console

from doqqy.infra.settings import Settings

from .loader import build_eval_workspace, check_backend_available, load_eval_queries
from .runner import (
    DEFAULT_BASELINE_PATH,
    DEFAULT_QDRANT_BASELINE_PATH,
    DEFAULT_TOLERANCE,
    check_regression,
    load_baseline,
    print_parity_report,
    print_rich_report,
    run_eval,
    save_baseline,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="doqqy arama performansı değerlendirme motoru"
    )
    parser.add_argument(
        "--backend",
        type=str,
        default="lancedb",
        help="Değerlendirilecek vektör deposu backend'i ('lancedb', 'qdrant', vb.)",
    )
    parser.add_argument(
        "--queries",
        type=Path,
        default=None,
        help="Özel queries.yaml dosya yolu",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=None,
        help="Özel korpus raw klasör yolu",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Değerlendirme raporunu JSON olarak belirtilen dosyaya kaydeder",
    )
    parser.add_argument(
        "--record-baseline",
        action="store_true",
        help="Mevcut çalışma sonuçlarını resmi referans JSON (baseline_lancedb.json) üzerine yazar",
    )
    parser.add_argument(
        "--check-baseline",
        action="store_true",
        help="Sonuçlar referans baseline'a göre toleransı aşarsa sıfır dışı çıkış koduyla (exit 1) sonlanır",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=DEFAULT_TOLERANCE,
        help=f"Regresyon tolerans eşiği (varsayılan: {DEFAULT_TOLERANCE})",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=10,
        help="Sorgu başına getirilecek maksimum sonuç sayısı (varsayılan: 10)",
    )

    args = parser.parse_args()
    console = Console()

    settings = Settings(vector_backend=args.backend)
    is_avail, avail_msg = check_backend_available(args.backend, settings=settings)
    if not is_avail:
        console.print(f"[bold yellow]UYARI: '{args.backend}' backend'i kullanılabilir değil:[/bold yellow]")
        console.print(f"  [yellow]{avail_msg}[/yellow]")
        if args.check_baseline:
            console.print(
                "[bold red]HATA: --check-baseline istendi ancak backend sunucusu/bağımlılığı eksik.[/bold red]"
            )
            sys.exit(1)
        console.print("[dim]Değerlendirme testi atlanıyor.[/dim]")
        sys.exit(0)

    if args.backend == "qdrant" and "in-memory" in avail_msg:
        settings = Settings(vector_backend="qdrant", qdrant_url=":memory:")
        console.print("[yellow]Sunucu kapalı olduğu için Qdrant bellek içi (in-memory) modda çalıştırılıyor.[/yellow]")

    console.print("[bold cyan]Değerlendirme sorguları yükleniyor...[/bold cyan]")
    queries = load_eval_queries(args.queries)
    console.print(f"[bold]{len(queries)}[/bold] adet referans sorgu yüklendi.")

    with tempfile.TemporaryDirectory(prefix="doqqy_eval_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        console.print(f"[bold cyan]'{args.backend}' backend'i ile geçici çalışma alanı oluşturuluyor: {tmp_path}...[/bold cyan]")
        ws = build_eval_workspace(
            target_dir=tmp_path,
            corpus_raw_dir=args.corpus,
            backend=args.backend,
            settings=settings,
        )

        console.print("[bold cyan]Arama performansı değerlendirmesi çalıştırılıyor...[/bold cyan]")
        report = run_eval(
            ws,
            queries,
            backend=args.backend,
            settings=settings,
            top_k=args.top_k,
        )

    # Backend'e özel referans (Baseline) karşılaştırması
    target_baseline_path = DEFAULT_QDRANT_BASELINE_PATH if args.backend == "qdrant" else DEFAULT_BASELINE_PATH
    baseline_report = None
    if target_baseline_path.exists():
        try:
            baseline_report = load_baseline(target_baseline_path, backend=args.backend)
        except (OSError, ValueError, KeyError) as exc:
            console.print(f"[yellow]Uyarı: Referans baseline yüklenemedi: {exc}[/yellow]")

    print_rich_report(report, baseline=baseline_report, console=console)

    # Qdrant çalışıyorsa ve LanceDB baseline varsa parite tablosunu bas
    if args.backend == "qdrant" and DEFAULT_BASELINE_PATH.exists():
        try:
            lancedb_base = load_baseline(DEFAULT_BASELINE_PATH, backend="lancedb")
            print_parity_report(lancedb_base, report, tolerance=args.tolerance, console=console)
        except (OSError, ValueError, KeyError) as exc:
            console.print(f"[dim]LanceDB parite karşılaştırması atlandı: {exc}[/dim]")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        save_baseline(report, args.json_out)
        console.print(f"[green]Değerlendirme JSON raporu kaydedildi: {args.json_out}[/green]")

    if args.record_baseline:
        save_baseline(report, target_baseline_path)
        console.print(f"[bold green]Yeni referans baseline kaydedildi: {target_baseline_path}[/bold green]")

    if args.check_baseline:
        if baseline_report is None:
            console.print(
                f"[bold red]HATA: --check-baseline istendi fakat referans baseline "
                f"({target_baseline_path.name}) yüklenemedi.[/bold red]"
            )
            sys.exit(1)

        is_regression, violations = check_regression(report, baseline_report, tolerance=args.tolerance)
        if is_regression:
            console.print("[bold red]PERFORMANS DÜŞÜŞÜ (REGRESYON) TESPİT EDİLDİ:[/bold red]")
            for v in violations:
                console.print(f"  [red]• {v}[/red]")
            sys.exit(1)
        else:
            console.print(f"[bold green]✓ Tolerans ({args.tolerance}) dahilinde hiçbir regresyon tespit edilmedi.[/bold green]")


if __name__ == "__main__":
    main()
