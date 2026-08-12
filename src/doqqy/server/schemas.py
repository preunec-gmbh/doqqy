"""Pydantic request and response contracts for the doqqy API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class QueryRequest(BaseModel):
    """Sorgu isteği için gelen veri şeması ve doğrulama kuralları."""
    q: str = Field(..., min_length=1, max_length=2000, description="Arama sorgusu metni")
    top_k: int = Field(5, ge=1, le=50, description="Getirilecek maksimum sonuç sayısı")
    tag: str | None = Field(None, pattern=r"^[\w-]+$", description="Filtrelenecek etiket (isteğe bağlı)")
    rerank: bool = Field(True, description="Reranker modeli kullanılsın mı?")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "q": "fatura iptal ve iade süreci",
                "top_k": 5,
                "tag": None,
                "rerank": True,
            }
        }
    )


class ScoreBreakdown(BaseModel):
    dense_rank: int | None = None
    sparse_rank: int | None = None
    rrf_score: float | None = None
    rerank_score: float | None = None


class HitOut(BaseModel):
    """Tek bir arama sonucunun dışarıya dönen şeması."""
    score: float
    doc_id: str
    source: str
    section_path: list[str]
    content: str
    scores: ScoreBreakdown | None = None


class QueryResponse(BaseModel):
    """Arama yanıtı şeması."""
    hits: list[HitOut]
    took_ms: int
    workspace: str
