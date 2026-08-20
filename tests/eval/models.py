"""Değerlendirme motoru için veri modelleri."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class EvalQuery:
    """queries.yaml içindeki referans sorgu modeli."""

    query: str
    expected_doc_id: str
    expected_section: str | list[str] | None = None
    category: str = "general"
    reason: str = ""
    tag_filter: list[str] | None = None


@dataclass
class QueryEvalResult:
    """Tek bir sorgunun rerank açık ve kapalı değerlendirme sonucu."""

    query: str
    category: str
    expected_doc_id: str
    expected_section: str | list[str] | None
    tag_filter: list[str] | None
    rank_rerank: int | None
    rank_no_rerank: int | None
    is_hit_at_1_rerank: bool
    is_hit_at_5_rerank: bool
    is_hit_at_10_rerank: bool
    is_hit_at_1_no_rerank: bool
    is_hit_at_5_no_rerank: bool
    is_hit_at_10_no_rerank: bool
    rr_rerank: float
    rr_no_rerank: float
    top_doc_rerank: str | None = None
    top_section_rerank: list[str] = field(default_factory=list)
    top_doc_no_rerank: str | None = None
    top_section_no_rerank: list[str] = field(default_factory=list)


@dataclass
class AggregateMetrics:
    """Sorgular genelinde toplanan standart IR metrikleri (Recall@k, MRR)."""

    recall_at_1: float
    recall_at_5: float
    recall_at_10: float
    mrr: float
    total_queries: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AggregateMetrics:
        return cls(
            recall_at_1=float(data["recall_at_1"]),
            recall_at_5=float(data["recall_at_5"]),
            recall_at_10=float(data["recall_at_10"]),
            mrr=float(data["mrr"]),
            total_queries=int(data["total_queries"]),
        )


@dataclass
class CategoryMetrics:
    """Belirli bir kategoriye ait metrik kırılımı."""

    category: str
    total_queries: int
    rerank_on: AggregateMetrics
    rerank_off: AggregateMetrics

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "total_queries": self.total_queries,
            "rerank_on": self.rerank_on.to_dict(),
            "rerank_off": self.rerank_off.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CategoryMetrics:
        return cls(
            category=data["category"],
            total_queries=int(data["total_queries"]),
            rerank_on=AggregateMetrics.from_dict(data["rerank_on"]),
            rerank_off=AggregateMetrics.from_dict(data["rerank_off"]),
        )


@dataclass
class EvalReport:
    """Özet, kategori kırılımları ve sorgu detaylarını içeren tam değerlendirme raporu."""

    backend: str
    timestamp: str
    rerank_on: AggregateMetrics
    rerank_off: AggregateMetrics
    by_category: dict[str, CategoryMetrics]
    per_query: list[QueryEvalResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "backend": self.backend,
            "timestamp": self.timestamp,
            "rerank_on": self.rerank_on.to_dict(),
            "rerank_off": self.rerank_off.to_dict(),
            "by_category": {cat: m.to_dict() for cat, m in self.by_category.items()},
            "per_query": [asdict(q) for q in self.per_query],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EvalReport:
        return cls(
            backend=data["backend"],
            timestamp=data.get("timestamp", ""),
            rerank_on=AggregateMetrics.from_dict(data["rerank_on"]),
            rerank_off=AggregateMetrics.from_dict(data["rerank_off"]),
            by_category={
                cat: CategoryMetrics.from_dict(m)
                for cat, m in data.get("by_category", {}).items()
            },
            per_query=[
                QueryEvalResult(**q) for q in data.get("per_query", [])
            ],
        )
