"""Değerlendirme motoru için CLI giriş noktası: python -m tests.eval"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from rich.console import Console

from doqqy.infra.settings import Settings

from .loader import build_eval_workspace, load_eval_queries
from .runner import (
    DEFAULT_BASELINE_PATH,
    DEFAULT_TOLERANCE,
    check_regression,
    load_baseline,
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

    console.print("[bold cyan]Değerlendirme sorguları yükleniyor...[/bold cyan]")
    queries = load_eval_queries(args.queries)
    console.print(f"[bold]{len(queries)}[/bold] adet referans sorgu yüklendi.")

    with tempfile.TemporaryDirectory(prefix="doqqy_eval_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        console.print(f"[bold cyan]'{args.backend}' backend'i ile geçici çalışma alanı oluşturuluyor: {tmp_path}...[/bold cyan]")
        settings = Settings(vector_backend=args.backend)
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

    # Referans (Baseline) karşılaştırması
    baseline_report = None
    if DEFAULT_BASELINE_PATH.exists():
        try:
            baseline_report = load_baseline(DEFAULT_BASELINE_PATH)
        except (OSError, ValueError, KeyError) as exc:
            console.print(f"[yellow]Uyarı: Referans baseline yüklenemedi: {exc}[/yellow]")

    print_rich_report(report, baseline=baseline_report, console=console)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        save_baseline(report, args.json_out)
        console.print(f"[green]Değerlendirme JSON raporu kaydedildi: {args.json_out}[/green]")

    if args.record_baseline:
        save_baseline(report, DEFAULT_BASELINE_PATH)
        console.print(f"[bold green]Yeni referans baseline kaydedildi: {DEFAULT_BASELINE_PATH}[/bold green]")

    if args.check_baseline and baseline_report:
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
