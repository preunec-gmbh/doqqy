"""Process-global ModelManager for bge-m3 embedding & reranking models."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from doqqy.infra.settings import Settings

_DEFAULT_MANAGER_LOCK = threading.Lock()
_DEFAULT_MANAGER: ModelManager | None = None


def get_default_model_manager(settings: Settings | None = None) -> ModelManager:
    """CLI ve genel süreçler için varsayılan tekil ModelManager örneğini döndürür."""
    global _DEFAULT_MANAGER
    if _DEFAULT_MANAGER is None:
        with _DEFAULT_MANAGER_LOCK:
            if _DEFAULT_MANAGER is None:
                from doqqy.infra.settings import Settings as DefaultSettings

                _DEFAULT_MANAGER = ModelManager(settings or DefaultSettings())
    return _DEFAULT_MANAGER


class ModelManager:
    """Tekil model yöneticisi — modelleri bir kez yükler ve süreç boyu bellekte korur."""

    @classmethod
    def reset_default(cls) -> None:
        """Varsayılan tekil ModelManager örneğini sıfırlar (testler için)."""
        global _DEFAULT_MANAGER
        with _DEFAULT_MANAGER_LOCK:
            _DEFAULT_MANAGER = None

    def __init__(self, settings: Settings):
        self._settings = settings
        self._lock = threading.Lock()
        self._semaphore = threading.Semaphore(1)

        self._device: str | None = None
        self._embedder: Any = None
        self._reranker_tokenizer: Any = None
        self._reranker_model: Any = None

    def _resolve_device(self) -> str:
        if self._device is None:
            from doqqy.config import detect_device

            self._device = (
                detect_device()
                if self._settings.device == "auto"
                else self._settings.device
            )
        return self._device

    def get_embedder(self) -> Any:
        """bge-m3 modelini döndürür (yüklü değilse yükler)."""
        if self._embedder is None:
            with self._lock:
                if self._embedder is None:
                    from FlagEmbedding import BGEM3FlagModel

                    dev = self._resolve_device()
                    use_fp16 = dev == "cuda"
                    self._embedder = BGEM3FlagModel(
                        self._settings.embedding_model,  # BAAI/bge-m3
                        use_fp16=use_fp16,               # cuda ise True, değilse False
                        device=dev,                      # cuda veya cpu
                    )
        return self._embedder

    def get_reranker(self) -> tuple[Any, Any, str]:
        """Reranker tokenizer, model ve cihaz adını döndürür (yüklü değilse yükler)."""
        if self._reranker_model is None:
            with self._lock:
                if self._reranker_model is None:
                    from transformers import AutoModelForSequenceClassification, AutoTokenizer

                    dev = self._resolve_device()
                    tokenizer = AutoTokenizer.from_pretrained(self._settings.reranker_model)
                    model = AutoModelForSequenceClassification.from_pretrained(self._settings.reranker_model)
                    model.to(dev)

                    if dev == "cuda" and self._settings.reranker_fp16:
                        model.half()

                    model.eval()
                    self._reranker_tokenizer = tokenizer
                    self._reranker_model = model
        dev = self._resolve_device()
        return self._reranker_tokenizer, self._reranker_model, dev

    def warmup(self) -> None:
        """Sunucu başlatılırken modelleri belleğe yükler (ısıtır)."""
        self.get_embedder()
        self.get_reranker()

    @property
    def semaphore(self) -> threading.Semaphore:
        """Model hesaplaması yapılırken eşzamanlılığı sınırlamak için kilit semaforu."""
        return self._semaphore
