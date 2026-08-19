"""Değerlendirme motoru için IR metrikleri (Recall@k, MRR) ve referans eşleştirme mantığı."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.eval.models import AggregateMetrics, CategoryMetrics, EvalQuery, QueryEvalResult

if TYPE_CHECKING:
    from doqqy.query import SearchHit


def is_matching_hit(hit: SearchHit, query: EvalQuery) -> bool:
    """Bir SearchHit'in EvalQuery referans doğrusuyla eşleşip eşleşmediğini kontrol eder."""
    if hit.doc_id != query.expected_doc_id:
        return False

    expected_sec = query.expected_section
    if not expected_sec:
        return True

    section_path = hit.section_path or []

    if isinstance(expected_sec, str):
        return expected_sec in section_path
    elif isinstance(expected_sec, (list, tuple)):
        return any(sec in section_path for sec in expected_sec)

    return False


def find_first_match_rank(hits: list[SearchHit], query: EvalQuery) -> tuple[int | None, SearchHit | None]:
    """Aday listesinde eşleşen ilk sonucun 1-tabanlı sırasını (rank) bulur."""
    for idx, hit in enumerate(hits):
        if is_matching_hit(hit, query):
            return idx + 1, hit
    return None, None


def evaluate_query_hits(
    query: EvalQuery,
    hits_rerank: list[SearchHit],
    hits_no_rerank: list[SearchHit],
) -> QueryEvalResult:
    """Tek bir sorgunun sonuçlarını rerank açık ve kapalı modlar için değerlendirir."""
    rank_rerank, _ = find_first_match_rank(hits_rerank, query)
    rank_no_rerank, _ = find_first_match_rank(hits_no_rerank, query)

    top_doc_rerank = hits_rerank[0].doc_id if hits_rerank else None
    top_sec_rerank = hits_rerank[0].section_path if hits_rerank else []

    top_doc_no_rerank = hits_no_rerank[0].doc_id if hits_no_rerank else None
    top_sec_no_rerank = hits_no_rerank[0].section_path if hits_no_rerank else []

    rr_rerank = 1.0 / rank_rerank if rank_rerank is not None else 0.0
    rr_no_rerank = 1.0 / rank_no_rerank if rank_no_rerank is not None else 0.0

    return QueryEvalResult(
        query=query.query,
        category=query.category,
        expected_doc_id=query.expected_doc_id,
        expected_section=query.expected_section,
        tag_filter=query.tag_filter,
        rank_rerank=rank_rerank,
        rank_no_rerank=rank_no_rerank,
        is_hit_at_1_rerank=(rank_rerank is not None and rank_rerank <= 1),
        is_hit_at_5_rerank=(rank_rerank is not None and rank_rerank <= 5),
        is_hit_at_10_rerank=(rank_rerank is not None and rank_rerank <= 10),
        is_hit_at_1_no_rerank=(rank_no_rerank is not None and rank_no_rerank <= 1),
        is_hit_at_5_no_rerank=(rank_no_rerank is not None and rank_no_rerank <= 5),
        is_hit_at_10_no_rerank=(rank_no_rerank is not None and rank_no_rerank <= 10),
        rr_rerank=rr_rerank,
        rr_no_rerank=rr_no_rerank,
        top_doc_rerank=top_doc_rerank,
        top_section_rerank=top_sec_rerank,
        top_doc_no_rerank=top_doc_no_rerank,
        top_section_no_rerank=top_sec_no_rerank,
    )


def compute_aggregate_metrics(
    results: list[QueryEvalResult],
    *,
    rerank: bool,
) -> AggregateMetrics:
    """Sorgu sonuçları listesi için genel Recall@1, Recall@5, Recall@10 ve MRR metriklerini hesaplar."""
    total = len(results)
    if total == 0:
        return AggregateMetrics(
            recall_at_1=0.0,
            recall_at_5=0.0,
            recall_at_10=0.0,
            mrr=0.0,
            total_queries=0,
        )

    if rerank:
        r1 = sum(1 for r in results if r.is_hit_at_1_rerank) / total
        r5 = sum(1 for r in results if r.is_hit_at_5_rerank) / total
        r10 = sum(1 for r in results if r.is_hit_at_10_rerank) / total
        mrr = sum(r.rr_rerank for r in results) / total
    else:
        r1 = sum(1 for r in results if r.is_hit_at_1_no_rerank) / total
        r5 = sum(1 for r in results if r.is_hit_at_5_no_rerank) / total
        r10 = sum(1 for r in results if r.is_hit_at_10_no_rerank) / total
        mrr = sum(r.rr_no_rerank for r in results) / total

    return AggregateMetrics(
        recall_at_1=round(r1, 4),
        recall_at_5=round(r5, 4),
        recall_at_10=round(r10, 4),
        mrr=round(mrr, 4),
        total_queries=total,
    )


def compute_category_breakdowns(
    results: list[QueryEvalResult],
) -> dict[str, CategoryMetrics]:
    """Kategori bazlı metrik kırılımlarını hesaplar."""
    by_cat: dict[str, list[QueryEvalResult]] = {}
    for r in results:
        by_cat.setdefault(r.category, []).append(r)

    breakdowns: dict[str, CategoryMetrics] = {}
    for cat, cat_results in by_cat.items():
        breakdowns[cat] = CategoryMetrics(
            category=cat,
            total_queries=len(cat_results),
            rerank_on=compute_aggregate_metrics(cat_results, rerank=True),
            rerank_off=compute_aggregate_metrics(cat_results, rerank=False),
        )
    return breakdowns
