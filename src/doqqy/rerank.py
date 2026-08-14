"""bge-reranker-v2-m3 ile cross-encoder reranking (transformers direkt).

Device placement: detect_device() kullanılır (DOQQY_DEVICE env ile override edilebilir).
fp16: CUDA cihazında DOQQY_RERANKER_FP16=1 veya Settings.reranker_fp16 ile aktif edilir (varsayılan: kapalı).
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import torch

from doqqy.config import RERANKER_BATCH_SIZE, get_logger

if TYPE_CHECKING:
    from doqqy.infra.models import ModelManager
    from doqqy.infra.settings import Settings

_LOG = get_logger("doqqy.rerank")


def _load_reranker(
    models: ModelManager | None = None,
    settings: Settings | None = None,
) -> tuple:
    from doqqy.infra.models import get_default_model_manager

    mgr = models if models is not None else get_default_model_manager(settings)
    return mgr.get_reranker()


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    *,
    models: ModelManager | None = None,
    settings: Settings | None = None,
) -> list[dict]:
    """Cross-encoder reranking with device-aware inference.

    Args:
        query: The search query string.
        candidates: List of dicts each containing at least a "content" key.
        top_k: Number of top results to return.
        models: Optional ModelManager instance to share pre-warmed models.
        settings: Optional Settings instance.

    Returns:
        Top-k candidates sorted by descending rerank_score, each dict extended
        with a "rerank_score" field.
    """
    if not candidates:
        return []

    tokenizer, model, device = _load_reranker(models=models, settings=settings)
    pairs = [(query, c["content"]) for c in candidates]

    all_scores: list[float] = []
    for i in range(0, len(pairs), RERANKER_BATCH_SIZE):
        batch = pairs[i : i + RERANKER_BATCH_SIZE]
        raw_inputs = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )

        inputs = {k: v.to(device) for k, v in raw_inputs.items()}
        with torch.no_grad():
            logits = model(**inputs).logits.squeeze(-1).cpu().float()
        if logits.dim() == 0:
            all_scores.append(_sigmoid(logits.item()))
        else:
            all_scores.extend(_sigmoid(v) for v in logits.tolist())

    ranked = sorted(
        zip(all_scores, candidates, strict=True),
        key=lambda x: x[0],
        reverse=True,
    )
    results = []
    for score, candidate in ranked[:top_k]:
        item = dict(candidate)
        item["rerank_score"] = score
        results.append(item)

    return results
