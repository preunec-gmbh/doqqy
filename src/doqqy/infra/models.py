"""Process-global ModelManager for bge-m3 embedding & reranking models."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from doqqy.infra.settings import Settings

class ModelManager:
    """Tekil model yöneticisi — modelleri bir kez yükler ve süreç boyu bellekte korur."""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._lock = threading.Lock()
        self._semaphore = threading.Semaphore(1)

        self._embedder: Any = None
        self._reranker_tokenizer: Any = None
        self._reranker_model: Any = None

    def get_embedder(self) -> Any:
        """bge-m3 modelini döndürür (yüklü değilse yükler)."""
        if self._embedder is None:
            with self._lock:
                if self._embedder is None:
                    from FlagEmbedding import BGEM3FlagModel

                    from doqqy.config import detect_device

                    dev = (
                        detect_device()
                        if self._settings.device == "auto"
                        else self._settings.device
                    )
                    use_fp16 = dev == "cuda"
                    self._embedder = BGEM3FlagModel(
                        self._settings.embedding_model,     # BAAI/bge-m3
                        use_fp16=use_fp16,                  # cuda ise True, değilse False
                        device=dev,                         # cuda veya cpu
                    )
        return self._embedder

    def get_reranker(self) -> tuple[Any, Any]:
        """Reranker tokenizer ve modelini döndürür (yüklü değilse yükler)."""
        if self._reranker_model is None:
            with self._lock:
                if self._reranker_model is None:
                    import os

                    from transformers import AutoModelForSequenceClassification, AutoTokenizer

                    from doqqy.config import detect_device

                    dev = (
                        detect_device()
                        if self._settings.device == "auto"
                        else self._settings.device
                    )
                    tokenizer = AutoTokenizer.from_pretrained(self._settings.reranker_model)
                    model = AutoModelForSequenceClassification.from_pretrained(self._settings.reranker_model)
                    model.to(dev)

                    if dev == "cuda" and os.environ.get("DOQQY_RERANKER_FP16", "0") == "1":
                        model.half()

                    model.eval()
                    self._reranker_tokenizer = tokenizer
                    self._reranker_model = model
        return self._reranker_tokenizer, self._reranker_model

    def warmup(self) -> None:
        """Sunucu başlatılırken modelleri belleğe yükler (ısıtır)."""
        self.get_embedder()
        self.get_reranker()

    @property
    def semaphore(self) -> threading.Semaphore:
        """Model hesaplaması yapılırken eşzamanlılığı sınırlamak için kilit semaforu."""
        return self._semaphore
