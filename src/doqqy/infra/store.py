"""StoreManager — per-workspace VectorStore cache with bounded LRU and invalidation."""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import TYPE_CHECKING

from doqqy.infra.vectorstore.factory import make_store

if TYPE_CHECKING:
    from pathlib import Path

    from doqqy.infra.settings import Settings
    from doqqy.infra.vectorstore.base import VectorStore
    from doqqy.workspace import Workspace


class StoreManager:
    """Çalışma alanı (workspace) bazlı VectorStore tutucularını yöneten LRU önbellek sınıfı."""

    def __init__(self, settings: Settings | None = None, max_open: int = 64):
        self._settings = settings
        self._cache: OrderedDict[Path, VectorStore] = OrderedDict()
        self._lock = threading.Lock()
        self._max = max_open

    def get_store(self, ws: Workspace) -> VectorStore:
        """Çalışma alanı için önbellekteki VectorStore'u döndürür, yoksa oluşturur."""
        key = ws.root.resolve()
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                return self._cache[key]

        store = make_store(ws, self._settings)

        with self._lock:
            self._cache[key] = store
            if len(self._cache) > self._max:
                self._cache.popitem(last=False)
        return store

    def invalidate(self, ws: Workspace) -> None:
        """Yazma işlemi sonrasında çalışma alanının önbellekteki bağlantısını siler."""
        key = ws.root.resolve()
        with self._lock:
            self._cache.pop(key, None)
