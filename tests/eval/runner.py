"""Değerlendirme motoru için çalıştırma, regresyon kontrolü ve raporlama mantığı."""

from __future__ import annotations

import datetime
import json
from pathlib import Path

from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table

from doqqy.infra.settings import Settings
from doqqy.query import search
from doqqy.workspace import Workspace

from .metrics import (
    compute_aggregate_metrics,
    compute_category_breakdowns,
    evaluate_query_hits,
)
from .models import EvalQuery, EvalReport, QueryEvalResult

DEFAULT_BASELINE_PATH = Path(__file__).parent / "baseline_lancedb.json"
DEFAULT_QDRANT_BASELINE_PATH = Path(__file__).parent / "baseline_qdrant.json"

# Genel metriklerde izin verilen maksimum düşüş
DEFAULT_TOLERANCE: float = 0.02


def run_eval(
    ws: Workspace,
    queries: list[EvalQuery],
    backend: str = "lancedb",
    settings: Settings | None = None,
    top_k: int = 10,
) -> EvalReport:
    """Değerlendirme sorgularını gerçek search() iş hattı üzerinden Workspace'e karşı çalıştırır."""
    app_settings = settings or Settings(vector_backend=backend)
    results: list[QueryEvalResult] = []

    for q in queries:
        # Rerank açık modda çalıştır
        hits_rerank = search(
            ws,
            q.query,
            k=top_k,
            rerank=True,
            tag_filter=q.tag_filter,
            settings=app_settings,
        )

        # Rerank kapalı (saf dense + sparse RRF) modda çalıştır
        hits_no_rerank = search(
            ws,
            q.query,
            k=top_k,
            rerank=False,
            tag_filter=q.tag_filter,
            settings=app_settings,
        )

        res = evaluate_query_hits(q, hits_rerank, hits_no_rerank)
        results.append(res)

    rerank_on = compute_aggregate_metrics(results, rerank=True)
    rerank_off = compute_aggregate_metrics(results, rerank=False)
    by_category = compute_category_breakdowns(results)

    return EvalReport(
        backend=backend,
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        rerank_on=rerank_on,
        rerank_off=rerank_off,
        by_category=by_category,
        per_query=results,
    )


def check_regression(
    current: EvalReport,
    baseline: EvalReport,
    tolerance: float = DEFAULT_TOLERANCE,
) -> tuple[bool, list[str]]:
    """Mevcut metriklerin belirlenen tolerans sözleşmesini aşıp aşmadığını kontrol eder."""
    violations: list[str] = []

    # Rerank açık için genel metrikleri denetle
    for metric_name in ("recall_at_1", "recall_at_5", "recall_at_10", "mrr"):
        curr_val = getattr(current.rerank_on, metric_name)
        base_val = getattr(baseline.rerank_on, metric_name)
        if curr_val < base_val - tolerance:
            violations.append(
                f"[Rerank AÇIK] {metric_name} geriledi: {base_val:.4f} -> {curr_val:.4f} "
                f"(düşüş {base_val - curr_val:.4f} > tolerans {tolerance:.4f})"
            )

    # Rerank kapalı için genel metrikleri denetle
    for metric_name in ("recall_at_1", "recall_at_5", "recall_at_10", "mrr"):
        curr_val = getattr(current.rerank_off, metric_name)
        base_val = getattr(baseline.rerank_off, metric_name)
        if curr_val < base_val - tolerance:
            violations.append(
                f"[Rerank KAPALI] {metric_name} geriledi: {base_val:.4f} -> {curr_val:.4f} "
                f"(düşüş {base_val - curr_val:.4f} > tolerans {tolerance:.4f})"
            )

    # exact_term sorguları için Rerank açık sıfır tolerans tabanı
    if "exact_term" in current.by_category and "exact_term" in baseline.by_category:
        curr_exact_r5 = current.by_category["exact_term"].rerank_on.recall_at_5
        base_exact_r5 = baseline.by_category["exact_term"].rerank_on.recall_at_5
        if curr_exact_r5 < base_exact_r5:
            violations.append(
                f"[exact_term] Sıfır tolerans kuralı ihlal edildi: "
                f"Recall@5 {base_exact_r5:.4f} seviyesinden {curr_exact_r5:.4f} seviyesine düştü"
            )

    return len(violations) > 0, violations


def get_default_baseline_path(backend: str = "lancedb") -> Path:
    """Backend için varsayılan referans baseline yolunu döndürür."""
    if backend == "qdrant":
        return DEFAULT_QDRANT_BASELINE_PATH
    return DEFAULT_BASELINE_PATH


def load_baseline(path: Path | None = None, backend: str = "lancedb") -> EvalReport:
    """Referans raporu JSON dosyasından yükler."""
    p = path or get_default_baseline_path(backend)
    if not p.exists():
        raise FileNotFoundError(f"Referans dosyası bulunamadı: {p}")
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return EvalReport.from_dict(data)


def save_baseline(report: EvalReport, path: Path | None = None) -> None:
    """Raporu referans JSON olarak kaydeder."""
    p = path or get_default_baseline_path(report.backend)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)


def _format_rank(rank: int | None) -> str:
    if rank is None:
        return "[bold red]YOK[/bold red]"       # İlk 10’da sonuç yoksa
    elif rank == 1:
        return "[bold green]1[/bold green]"     # 1.sırada ise
    elif rank <= 5:
        return f"[cyan]{rank}[/cyan]"           # 2-5 arası ise
    else:
        return f"[yellow]{rank}[/yellow]"       # 6-10 arası ise


def print_rich_report(
    report: EvalReport,
    baseline: EvalReport | None = None,
    console: Console | None = None,
) -> None:
    """Sorgu bazlı ve özet değerlendirme sonuçlarını Rich tabloları olarak ekrana basar."""
    c = console or Console()

    # 1. Özet metrikler tablosu
    summary_table = Table(
        title=f"\nArama Değerlendirme Özeti (Backend: {report.backend})",
        box=ROUNDED,
        header_style="bold magenta",
    )
    summary_table.add_column("Mod", style="bold")
    summary_table.add_column("Recall@1", justify="right")
    summary_table.add_column("Recall@5", justify="right")
    summary_table.add_column("Recall@10", justify="right")
    summary_table.add_column("MRR", justify="right")
    summary_table.add_column("Toplam Sorgu", justify="right")

    def _diff(curr: float, base: float | None) -> str:
        if base is None:
            return f"{curr:.4f}"
        diff = curr - base
        sign = "+" if diff >= 0 else ""
        color = "green" if diff > 0 else ("red" if diff < -DEFAULT_TOLERANCE else "dim")
        return f"{curr:.4f} ([{color}]{sign}{diff:.4f}[/{color}])"

    b_on = baseline.rerank_on if baseline else None
    b_off = baseline.rerank_off if baseline else None

    summary_table.add_row(
        "Rerank AÇIK",
        _diff(report.rerank_on.recall_at_1, b_on.recall_at_1 if b_on else None),
        _diff(report.rerank_on.recall_at_5, b_on.recall_at_5 if b_on else None),
        _diff(report.rerank_on.recall_at_10, b_on.recall_at_10 if b_on else None),
        _diff(report.rerank_on.mrr, b_on.mrr if b_on else None),
        str(report.rerank_on.total_queries),
    )

    summary_table.add_row(
        "Rerank KAPALI (Saf RRF)",
        _diff(report.rerank_off.recall_at_1, b_off.recall_at_1 if b_off else None),
        _diff(report.rerank_off.recall_at_5, b_off.recall_at_5 if b_off else None),
        _diff(report.rerank_off.recall_at_10, b_off.recall_at_10 if b_off else None),
        _diff(report.rerank_off.mrr, b_off.mrr if b_off else None),
        str(report.rerank_off.total_queries),
    )

    c.print(summary_table)

    # 2. Kategori kırılımları tablosu
    cat_table = Table(
        title="\nKategori Kırılımı (Rerank Açık vs Rerank Kapalı)",
        box=ROUNDED,
        header_style="bold cyan",
    )
    cat_table.add_column("Kategori", style="bold")
    cat_table.add_column("Adet", justify="right")
    cat_table.add_column("Rerank R@1", justify="right")
    cat_table.add_column("Rerank R@5", justify="right")
    cat_table.add_column("Rerank MRR", justify="right")
    cat_table.add_column("Reranksiz R@5", justify="right")
    cat_table.add_column("Reranksiz MRR", justify="right")

    for cat_name, cm in sorted(report.by_category.items()):
        cat_table.add_row(
            cat_name,
            str(cm.total_queries),
            f"{cm.rerank_on.recall_at_1:.4f}",
            f"{cm.rerank_on.recall_at_5:.4f}",
            f"{cm.rerank_on.mrr:.4f}",
            f"{cm.rerank_off.recall_at_5:.4f}",
            f"{cm.rerank_off.mrr:.4f}",
        )

    c.print(cat_table)

    # 3. Sorgu bazlı detay tablosu
    query_table = Table(
        title="\nSorgu Bazlı Değerlendirme Sonuçları",
        box=ROUNDED,
        header_style="bold blue",
    )
    query_table.add_column("#", justify="right", style="dim")
    query_table.add_column("Kategori", style="cyan")
    query_table.add_column("Sorgu", style="white")
    query_table.add_column("Filtre", style="dim")
    query_table.add_column("Rerank Sıra", justify="center")
    query_table.add_column("Reranksiz Sıra", justify="center")
    query_table.add_column("Beklenen Doküman / Başlık", style="dim")

    for i, q in enumerate(report.per_query, start=1):
        filter_str = ",".join(q.tag_filter) if q.tag_filter else "-"
        expected_sec_str = f" > {q.expected_section}" if q.expected_section else ""
        expected_info = f"{q.expected_doc_id}{expected_sec_str}"

        query_table.add_row(
            str(i),
            q.category,
            q.query,
            filter_str,
            _format_rank(q.rank_rerank),
            _format_rank(q.rank_no_rerank),
            expected_info,
        )

    c.print(query_table)


def print_parity_report(
    lancedb_report: EvalReport,
    qdrant_report: EvalReport,
    tolerance: float = DEFAULT_TOLERANCE,
    console: Console | None = None,
) -> None:
    """LanceDB ve Qdrant raporlarını yan yana karşılaştıran Rich tablosu oluşturur."""
    c = console or Console()
    parity_table = Table(
        title="\nBackend Eşdeğerlik (Parite) Özeti: LanceDB vs Qdrant",
        box=ROUNDED,
        header_style="bold yellow",
    )
    parity_table.add_column("Metrik", style="bold")
    parity_table.add_column("Rerank Modu", style="cyan")
    parity_table.add_column("LanceDB", justify="right")
    parity_table.add_column("Qdrant", justify="right")
    parity_table.add_column("Fark (Delta)", justify="right")
    parity_table.add_column("Parite Durumu", justify="center")

    metrics_map = [
        ("Recall@1", "rerank_on", lancedb_report.rerank_on.recall_at_1, qdrant_report.rerank_on.recall_at_1),
        ("Recall@5", "rerank_on", lancedb_report.rerank_on.recall_at_5, qdrant_report.rerank_on.recall_at_5),
        ("Recall@10", "rerank_on", lancedb_report.rerank_on.recall_at_10, qdrant_report.rerank_on.recall_at_10),
        ("MRR", "rerank_on", lancedb_report.rerank_on.mrr, qdrant_report.rerank_on.mrr),
        ("Recall@1", "rerank_off", lancedb_report.rerank_off.recall_at_1, qdrant_report.rerank_off.recall_at_1),
        ("Recall@5", "rerank_off", lancedb_report.rerank_off.recall_at_5, qdrant_report.rerank_off.recall_at_5),
        ("Recall@10", "rerank_off", lancedb_report.rerank_off.recall_at_10, qdrant_report.rerank_off.recall_at_10),
        ("MRR", "rerank_off", lancedb_report.rerank_off.mrr, qdrant_report.rerank_off.mrr),
    ]

    for metric_name, mode, l_val, q_val in metrics_map:
        diff = q_val - l_val
        diff_str = f"{diff:+.4f}"
        if abs(diff) <= tolerance:
            status = "[green]✓ Uyumlu[/green]"
        else:
            status = "[red]⚠ Fark Var[/red]"
        parity_table.add_row(
            metric_name,
            "AÇIK" if mode == "rerank_on" else "KAPALI",
            f"{l_val:.4f}",
            f"{q_val:.4f}",
            diff_str,
            status,
        )

    c.print(parity_table)
