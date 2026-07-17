"""bge-reranker-v2-m3 ile cross-encoder reranking (transformers direkt).

Device placement: detect_device() kullanılır (DOQQY_DEVICE env ile override edilebilir).
fp16: CUDA cihazında DOQQY_RERANKER_FP16=1 ile aktif edilir (varsayılan: kapalı).
"""

from __future__ import annotations

import math
import os
from functools import lru_cache

import torch

from doqqy.config import RERANKER_BATCH_SIZE, RERANKER_MODEL, detect_device, get_logger

_LOG = get_logger("doqqy.rerank")


@lru_cache(maxsize=1)
def _load_reranker() -> tuple:
    """Load the reranker model and move it to the detected device.

    Returns:
        (tokenizer, model, device_str) — device_str is needed inside rerank()
        to move input tensors to the same device.

    Notes:
        - fp16 is opt-in via DOQQY_RERANKER_FP16=1 (CUDA only, default off).
        - Results are cached process-globally; clear with _load_reranker.cache_clear().
    """
    from transformers import AutoModelForSequenceClassification, AutoTokenizer  # type: ignore

    device = detect_device()
    _LOG.info("reranker yükleniyor: %s (device=%s)", RERANKER_MODEL, device)

    tokenizer = AutoTokenizer.from_pretrained(RERANKER_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(RERANKER_MODEL)
    model.to(device)

    if device == "cuda" and os.environ.get("DOQQY_RERANKER_FP16", "0") == "1":
        model.half()
        _LOG.info("reranker: fp16 aktif")

    model.eval()
    return tokenizer, model, device


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    """Cross-encoder reranking with device-aware inference.

    Args:
        query: The search query string.
        candidates: List of dicts each containing at least a "content" key.
        top_k: Number of top results to return.

    Returns:
        Top-k candidates sorted by descending rerank_score, each dict extended
        with a "rerank_score" field.

    Notes:
        - Inputs are moved to the same device as the model (CPU or CUDA).
        - Logits are always moved back to CPU before sigmoid conversion.
    """
    if not candidates:
        return []

    tokenizer, model, device = _load_reranker()
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
        # Move tokenized inputs to the same device as the model
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
