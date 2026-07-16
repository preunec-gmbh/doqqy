"""bge-reranker-v2-m3 ile cross-encoder reranking (transformers direkt)."""

from __future__ import annotations

import math
from functools import lru_cache

import torch

from doqqy.config import RERANKER_BATCH_SIZE, RERANKER_MODEL, get_logger

_LOG = get_logger("doqqy.rerank")


@lru_cache(maxsize=1)
def _load_reranker():
    from transformers import AutoModelForSequenceClassification, AutoTokenizer  # type: ignore

    _LOG.info("reranker yükleniyor: %s", RERANKER_MODEL)
    tokenizer = AutoTokenizer.from_pretrained(RERANKER_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(RERANKER_MODEL)
    model.eval()
    return tokenizer, model


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    """
    candidates: [{"content": str, ...arbitrary fields...}]
    Döner: aynı dict'ler, "rerank_score" eklenerek, azalan sırada, top_k adet.
    """
    if not candidates:
        return []

    tokenizer, model = _load_reranker()
    pairs = [(query, c["content"]) for c in candidates]

    all_scores: list[float] = []
    for i in range(0, len(pairs), RERANKER_BATCH_SIZE):
        batch = pairs[i : i + RERANKER_BATCH_SIZE]
        inputs = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )
        with torch.no_grad():
            logits = model(**inputs).logits.squeeze(-1).float()
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
