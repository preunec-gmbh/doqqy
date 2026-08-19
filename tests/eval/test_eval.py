"""Değerlendirme motoru için birim ve regresyon testleri."""

from __future__ import annotations

import pytest

from doqqy.query import SearchHit
from tests.eval.loader import build_eval_workspace, load_eval_queries
from tests.eval.metrics import (
    compute_aggregate_metrics,
    is_matching_hit,
)
from tests.eval.models import AggregateMetrics, CategoryMetrics, EvalQuery, EvalReport, QueryEvalResult
from tests.eval.runner import (
    DEFAULT_BASELINE_PATH,
    DEFAULT_TOLERANCE,
    check_regression,
    load_baseline,
    run_eval,
)


def test_load_eval_queries_validates_schema():
    """queries.yaml şemasının ve sorguların geçerliliğini test eder."""
    queries = load_eval_queries()
    assert len(queries) >= 20
    for q in queries:
        assert q.query, "Query metni boş olamaz"
        assert q.expected_doc_id.startswith("raw/"), f"expected_doc_id 'raw/' ile başlamalı: {q.expected_doc_id}"
        assert q.category in {
            "exact_term",
            "paraphrase",
            "hard_rerank",
            "tag_filtered",
            "cross_lingual_tr_to_en",
            "cross_lingual_en_to_tr",
        }


def test_section_matching_contract_ancestor_and_list():
    """Ata başlık (ancestor) ve alternatif başlık listesi eşleşme sözleşmesini test eder."""
    query_single_sec = EvalQuery(
        query="test query",
        expected_doc_id="raw/erp/test.md",
        expected_section="Parent Heading",
    )
    hit_ancestor = SearchHit(
        score=0.9,
        doc_id="raw/erp/test.md",
        source="raw/erp/test.md",
        section_path=["H1 Root", "Parent Heading", "Sub Heading H3"],
        content="some content",
    )
    hit_wrong_doc = SearchHit(
        score=0.9,
        doc_id="raw/other/test.md",
        source="raw/other/test.md",
        section_path=["Parent Heading"],
        content="some content",
    )
    hit_wrong_sec = SearchHit(
        score=0.9,
        doc_id="raw/erp/test.md",
        source="raw/erp/test.md",
        section_path=["Other Heading"],
        content="some content",
    )

    assert is_matching_hit(hit_ancestor, query_single_sec) is True
    assert is_matching_hit(hit_wrong_doc, query_single_sec) is False
    assert is_matching_hit(hit_wrong_sec, query_single_sec) is False

    # İzin verilen başlıklar listesi
    query_list_sec = EvalQuery(
        query="test query",
        expected_doc_id="raw/erp/test.md",
        expected_section=["Alternate Section A", "Alternate Section B"],
    )
    hit_alt_a = SearchHit(
        score=0.9,
        doc_id="raw/erp/test.md",
        source="raw/erp/test.md",
        section_path=["Root", "Alternate Section A"],
        content="content",
    )
    assert is_matching_hit(hit_alt_a, query_list_sec) is True


def test_compute_aggregate_metrics():
    """Recall@k ve MRR metrik hesaplama formüllerini test eder."""
    results = [
        QueryEvalResult(
            query="q1",
            category="exact_term",
            expected_doc_id="raw/doc1.md",
            expected_section=None,
            tag_filter=None,
            rank_rerank=1,
            rank_no_rerank=2,
            is_hit_at_1_rerank=True,
            is_hit_at_5_rerank=True,
            is_hit_at_10_rerank=True,
            is_hit_at_1_no_rerank=False,
            is_hit_at_5_no_rerank=True,
            is_hit_at_10_no_rerank=True,
            rr_rerank=1.0,
            rr_no_rerank=0.5,
        ),
        QueryEvalResult(
            query="q2",
            category="exact_term",
            expected_doc_id="raw/doc2.md",
            expected_section=None,
            tag_filter=None,
            rank_rerank=None,
            rank_no_rerank=None,
            is_hit_at_1_rerank=False,
            is_hit_at_5_rerank=False,
            is_hit_at_10_rerank=False,
            is_hit_at_1_no_rerank=False,
            is_hit_at_5_no_rerank=False,
            is_hit_at_10_no_rerank=False,
            rr_rerank=0.0,
            rr_no_rerank=0.0,
        ),
    ]

    rerank_on = compute_aggregate_metrics(results, rerank=True)
    assert rerank_on.recall_at_1 == 0.5
    assert rerank_on.recall_at_5 == 0.5
    assert rerank_on.recall_at_10 == 0.5
    assert rerank_on.mrr == 0.5
    assert rerank_on.total_queries == 2

    rerank_off = compute_aggregate_metrics(results, rerank=False)
    assert rerank_off.recall_at_1 == 0.0
    assert rerank_off.recall_at_5 == 0.5
    assert rerank_off.mrr == 0.25


def test_check_regression_within_and_exceeding_tolerance():
    """Tolerans içi ve toleransı aşan regresyon durumlarını test eder."""
    base_agg = AggregateMetrics(
        recall_at_1=0.80,
        recall_at_5=0.90,
        recall_at_10=0.95,
        mrr=0.85,
        total_queries=10,
    )
    base_report = EvalReport(
        backend="lancedb",
        timestamp="2026-01-01T00:00:00Z",
        rerank_on=base_agg,
        rerank_off=base_agg,
        by_category={
            "paraphrase": CategoryMetrics("paraphrase", 5, base_agg, base_agg)
        },
        per_query=[],
    )

    # 1. Tolerans dahilinde (0.01 düşüş <= 0.02)
    curr_ok_agg = AggregateMetrics(
        recall_at_1=0.79,
        recall_at_5=0.89,
        recall_at_10=0.94,
        mrr=0.84,
        total_queries=10,
    )
    curr_ok_report = EvalReport(
        backend="lancedb",
        timestamp="2026-01-02T00:00:00Z",
        rerank_on=curr_ok_agg,
        rerank_off=curr_ok_agg,
        by_category={
            "paraphrase": CategoryMetrics("paraphrase", 5, curr_ok_agg, curr_ok_agg)
        },
        per_query=[],
    )
    has_reg, violations = check_regression(curr_ok_report, base_report, tolerance=DEFAULT_TOLERANCE)
    assert has_reg is False
    assert len(violations) == 0

    # 2. Toleransı aşan düşüş (0.05 düşüş > 0.02)
    curr_bad_agg = AggregateMetrics(
        recall_at_1=0.70,
        recall_at_5=0.90,
        recall_at_10=0.95,
        mrr=0.85,
        total_queries=10,
    )
    curr_bad_report = EvalReport(
        backend="lancedb",
        timestamp="2026-01-02T00:00:00Z",
        rerank_on=curr_bad_agg,
        rerank_off=curr_bad_agg,
        by_category={
            "paraphrase": CategoryMetrics("paraphrase", 5, curr_bad_agg, curr_bad_agg)
        },
        per_query=[],
    )
    has_reg_bad, violations_bad = check_regression(curr_bad_report, base_report, tolerance=DEFAULT_TOLERANCE)
    assert has_reg_bad is True
    assert any("recall_at_1 geriledi" in v for v in violations_bad)


def test_check_regression_zero_tolerance_exact_term():
    """exact_term kategorisi için sıfır tolerans kuralını test eder."""
    agg = AggregateMetrics(
        recall_at_1=0.80,
        recall_at_5=0.90,
        recall_at_10=0.95,
        mrr=0.85,
        total_queries=10,
    )
    base_report = EvalReport(
        backend="lancedb",
        timestamp="2026-01-01T00:00:00Z",
        rerank_on=agg,
        rerank_off=agg,
        by_category={
            "exact_term": CategoryMetrics("exact_term", 5, agg, agg)
        },
        per_query=[],
    )

    # Genel metrikler eşit olsa bile exact_term kategorisi 0.90'dan 0.80'e düştüğünde hata vermeli
    exact_bad_agg = AggregateMetrics(
        recall_at_1=0.80,
        recall_at_5=0.80,
        recall_at_10=0.95,
        mrr=0.85,
        total_queries=5,
    )
    curr_report = EvalReport(
        backend="lancedb",
        timestamp="2026-01-02T00:00:00Z",
        rerank_on=agg,
        rerank_off=agg,
        by_category={
            "exact_term": CategoryMetrics("exact_term", 5, exact_bad_agg, exact_bad_agg)
        },
        per_query=[],
    )
    has_reg, violations = check_regression(curr_report, base_report, tolerance=DEFAULT_TOLERANCE)
    assert has_reg is True
    assert any("Sıfır tolerans kuralı ihlal edildi" in v for v in violations)


@pytest.mark.slow
def test_lancedb_retrieval_eval(tmp_path):
    """LanceDB arama kalitesini referans baseline'a karşı doğrulayan uçtan uca test."""
    queries = load_eval_queries()
    ws = build_eval_workspace(target_dir=tmp_path, backend="lancedb")
    report = run_eval(ws, queries, backend="lancedb")

    # Temel kalite kontrolleri
    assert report.rerank_on.recall_at_5 >= 0.70
    assert report.rerank_on.mrr >= 0.60
    assert report.rerank_on.total_queries == len(queries)

    # Referans baseline'a karşı regresyon kontrolü
    if DEFAULT_BASELINE_PATH.exists():
        baseline = load_baseline(DEFAULT_BASELINE_PATH)
        has_reg, violations = check_regression(report, baseline, tolerance=DEFAULT_TOLERANCE)
        assert not has_reg, f"Referansa karşı regresyon tespit edildi: {violations}"
