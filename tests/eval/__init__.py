"""doqqy arama performansı değerlendirme (retrieval evaluation) modülü."""

from .loader import build_eval_workspace, check_backend_available, load_eval_queries
from .metrics import (
    compute_aggregate_metrics,
    compute_category_breakdowns,
    evaluate_query_hits,
    is_matching_hit,
)
from .models import (
    AggregateMetrics,
    CategoryMetrics,
    EvalQuery,
    EvalReport,
    QueryEvalResult,
)
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

__all__ = [
    "DEFAULT_BASELINE_PATH",
    "DEFAULT_QDRANT_BASELINE_PATH",
    "DEFAULT_TOLERANCE",
    "AggregateMetrics",
    "CategoryMetrics",
    "EvalQuery",
    "EvalReport",
    "QueryEvalResult",
    "build_eval_workspace",
    "check_backend_available",
    "check_regression",
    "compute_aggregate_metrics",
    "compute_category_breakdowns",
    "evaluate_query_hits",
    "is_matching_hit",
    "load_baseline",
    "load_eval_queries",
    "print_parity_report",
    "print_rich_report",
    "run_eval",
    "save_baseline",
]
