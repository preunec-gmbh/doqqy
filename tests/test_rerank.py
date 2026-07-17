"""Tests for rerank.py — device placement, score correctness, and fp16 mode.

No real GPU required:
- CPU smoke tests run the real model on CPU (marked @pytest.mark.slow —
  they download bge-reranker-v2-m3, so CI's `pytest -m "not slow"` skips them).
- Device placement tests use unittest.mock to verify model.to() and
  input tensor .to() calls without loading a GPU.
- fp16 tests verify model.half() is called when DOQQY_RERANKER_FP16=1.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clear_reranker_cache():
    """Clear the lru_cache singleton so each test gets a fresh load."""
    from doqqy.rerank import _load_reranker
    _load_reranker.cache_clear()


CANDIDATES = [
    {"content": "JWT tokens are signed with a secret key and expire after 1 hour."},
    {"content": "Bicycle chain maintenance: clean with degreaser, re-lube weekly."},
    {"content": "Refresh tokens allow clients to obtain new JWT access tokens silently."},
    {"content": "The weather forecast for tomorrow is partly cloudy."},
]

QUERY = "how does JWT refresh token work?"


# ---------------------------------------------------------------------------
# CPU smoke test — real model, real scores (loads bge-reranker-v2-m3)
# ---------------------------------------------------------------------------

@pytest.mark.slow
class TestRerankScoresOnCPU:
    """Run rerank() on CPU and verify output contract."""

    def setup_method(self):
        _clear_reranker_cache()

    def teardown_method(self):
        _clear_reranker_cache()

    def test_top_result_is_most_relevant(self, monkeypatch):
        """The JWT-related chunk must rank above the bicycle/weather chunks."""
        monkeypatch.setenv("DOQQY_DEVICE", "cpu")
        monkeypatch.delenv("DOQQY_RERANKER_FP16", raising=False)

        from doqqy.rerank import rerank

        results = rerank(QUERY, CANDIDATES, top_k=2)

        assert len(results) == 2
        # Top result must be JWT-related (content keyword check)
        assert "JWT" in results[0]["content"] or "refresh" in results[0]["content"].lower()

    def test_scores_descending(self, monkeypatch):
        """Returned scores must be in descending order."""
        monkeypatch.setenv("DOQQY_DEVICE", "cpu")

        from doqqy.rerank import rerank

        results = rerank(QUERY, CANDIDATES, top_k=4)
        scores = [r["rerank_score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_rerank_score_key_present(self, monkeypatch):
        """Every returned dict must contain a 'rerank_score' float."""
        monkeypatch.setenv("DOQQY_DEVICE", "cpu")

        from doqqy.rerank import rerank

        results = rerank(QUERY, CANDIDATES, top_k=3)
        for r in results:
            assert "rerank_score" in r
            assert isinstance(r["rerank_score"], float)
            assert 0.0 <= r["rerank_score"] <= 1.0

    def test_empty_candidates_returns_empty(self, monkeypatch):
        """rerank() with an empty list must return [] immediately."""
        monkeypatch.setenv("DOQQY_DEVICE", "cpu")

        from doqqy.rerank import rerank

        assert rerank(QUERY, [], top_k=5) == []

    def test_top_k_limits_output(self, monkeypatch):
        """top_k must cap the number of results even if more candidates exist."""
        monkeypatch.setenv("DOQQY_DEVICE", "cpu")

        from doqqy.rerank import rerank

        results = rerank(QUERY, CANDIDATES, top_k=2)
        assert len(results) == 2

    def test_original_fields_preserved(self, monkeypatch):
        """rerank() must not drop existing fields from candidate dicts."""
        monkeypatch.setenv("DOQQY_DEVICE", "cpu")

        from doqqy.rerank import rerank

        candidates_with_extras = [
            {"content": "JWT refresh flow.", "source": "auth.md", "chunk_id": "c1"},
            {"content": "Bicycle guide.", "source": "sports.md", "chunk_id": "c2"},
        ]
        results = rerank(QUERY, candidates_with_extras, top_k=2)
        for r in results:
            assert "source" in r
            assert "chunk_id" in r


# ---------------------------------------------------------------------------
# Device placement tests — mock-based (no GPU required)
# ---------------------------------------------------------------------------

class TestDevicePlacement:
    """Verify model and inputs are moved to the correct device without a GPU."""

    def setup_method(self):
        _clear_reranker_cache()

    def teardown_method(self):
        _clear_reranker_cache()

    def test_model_moved_to_cuda_when_available(self, monkeypatch):
        """_load_reranker() must call model.to('cuda') when detect_device()='cuda'."""
        monkeypatch.setenv("DOQQY_DEVICE", "cuda")
        monkeypatch.delenv("DOQQY_RERANKER_FP16", raising=False)

        mock_model = MagicMock()
        mock_model.to.return_value = mock_model  # .to() returns self
        mock_tokenizer = MagicMock()

        with (
            patch("transformers.AutoModelForSequenceClassification.from_pretrained",
                  return_value=mock_model),
            patch("transformers.AutoTokenizer.from_pretrained",
                  return_value=mock_tokenizer),
        ):
            from doqqy.rerank import _load_reranker
            tokenizer, model, device = _load_reranker()

        assert device == "cuda"
        mock_model.to.assert_called_once_with("cuda")
        mock_model.eval.assert_called_once()

    def test_model_stays_on_cpu_by_default(self, monkeypatch):
        """_load_reranker() must call model.to('cpu') when no CUDA available."""
        monkeypatch.setenv("DOQQY_DEVICE", "cpu")

        mock_model = MagicMock()
        mock_model.to.return_value = mock_model
        mock_tokenizer = MagicMock()

        with (
            patch("transformers.AutoModelForSequenceClassification.from_pretrained",
                  return_value=mock_model),
            patch("transformers.AutoTokenizer.from_pretrained",
                  return_value=mock_tokenizer),
        ):
            from doqqy.rerank import _load_reranker
            _, _, device = _load_reranker()

        assert device == "cpu"
        mock_model.to.assert_called_once_with("cpu")
        # model.half() must NOT be called on CPU
        mock_model.half.assert_not_called()


# ---------------------------------------------------------------------------
# fp16 mode tests — mock-based
# ---------------------------------------------------------------------------

class TestFp16Mode:
    """Verify model.half() is called only when DOQQY_RERANKER_FP16=1 on CUDA."""

    def setup_method(self):
        _clear_reranker_cache()

    def teardown_method(self):
        _clear_reranker_cache()

    def test_fp16_enabled_on_cuda(self, monkeypatch):
        """model.half() must be called when DOQQY_DEVICE=cuda and DOQQY_RERANKER_FP16=1."""
        monkeypatch.setenv("DOQQY_DEVICE", "cuda")
        monkeypatch.setenv("DOQQY_RERANKER_FP16", "1")

        mock_model = MagicMock()
        mock_model.to.return_value = mock_model
        mock_tokenizer = MagicMock()

        with (
            patch("transformers.AutoModelForSequenceClassification.from_pretrained",
                  return_value=mock_model),
            patch("transformers.AutoTokenizer.from_pretrained",
                  return_value=mock_tokenizer),
        ):
            from doqqy.rerank import _load_reranker
            _load_reranker()

        mock_model.half.assert_called_once()

    def test_fp16_not_called_on_cpu(self, monkeypatch):
        """model.half() must NOT be called even if DOQQY_RERANKER_FP16=1 on CPU."""
        monkeypatch.setenv("DOQQY_DEVICE", "cpu")
        monkeypatch.setenv("DOQQY_RERANKER_FP16", "1")

        mock_model = MagicMock()
        mock_model.to.return_value = mock_model
        mock_tokenizer = MagicMock()

        with (
            patch("transformers.AutoModelForSequenceClassification.from_pretrained",
                  return_value=mock_model),
            patch("transformers.AutoTokenizer.from_pretrained",
                  return_value=mock_tokenizer),
        ):
            from doqqy.rerank import _load_reranker
            _load_reranker()

        mock_model.half.assert_not_called()

    def test_fp16_default_off_on_cuda(self, monkeypatch):
        """model.half() must NOT be called when DOQQY_RERANKER_FP16 is not set."""
        monkeypatch.setenv("DOQQY_DEVICE", "cuda")
        monkeypatch.delenv("DOQQY_RERANKER_FP16", raising=False)

        mock_model = MagicMock()
        mock_model.to.return_value = mock_model
        mock_tokenizer = MagicMock()

        with (
            patch("transformers.AutoModelForSequenceClassification.from_pretrained",
                  return_value=mock_model),
            patch("transformers.AutoTokenizer.from_pretrained",
                  return_value=mock_tokenizer),
        ):
            from doqqy.rerank import _load_reranker
            _load_reranker()

        mock_model.half.assert_not_called()
