"""Unit tests for QdrantStore optimizations."""

from __future__ import annotations

import logging
from unittest.mock import MagicMock

import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord
from doqqy.infra.vectorstore.qdrant_store import QdrantStore


def test_hybrid_search_collection_exists_cached() -> None:
    """Verify that two hybrid_search calls issue collection_exists only once when collection exists."""
    store = QdrantStore(url=":memory:", api_key="", collection="test_col", tenant_key="tenant1")
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True
    mock_client.query_points.return_value = MagicMock(points=[])
    store._client_instance = mock_client

    # İlk çağrı - collection_exists kontrol edilir ve True önbelleklenir
    res1 = store.hybrid_search(dense=np.zeros(4, dtype=np.float32), sparse={}, limit=5)
    assert res1 == []
    assert mock_client.collection_exists.call_count == 1

    # İkinci çağrı - collection_exists tekrar sorgulanmadan önbellekteki True dönülür
    res2 = store.hybrid_search(dense=np.zeros(4, dtype=np.float32), sparse={}, limit=5)
    assert res2 == []
    assert mock_client.collection_exists.call_count == 1


def test_collection_ready_negative_cache_guard() -> None:
    """Verify that a False result for collection_exists is NOT cached permanently."""
    store = QdrantStore(url=":memory:", api_key="", collection="test_col", tenant_key="tenant1")
    mock_client = MagicMock()
    mock_client.collection_exists.side_effect = [False, True]
    mock_client.query_points.return_value = MagicMock(points=[])
    store._client_instance = mock_client

    # İlk çağrı - koleksiyon henüz mevcut değil
    res1 = store.hybrid_search(dense=np.zeros(4, dtype=np.float32), sparse={}, limit=5)
    assert res1 == []
    assert mock_client.collection_exists.call_count == 1
    assert not store._collection_verified

    # İkinci çağrı - koleksiyon artık mevcut; doğrulanır ve True önbelleklenir
    res2 = store.hybrid_search(dense=np.zeros(4, dtype=np.float32), sparse={}, limit=5)
    assert res2 == []
    assert mock_client.collection_exists.call_count == 2
    assert store._collection_verified

    # Üçüncü çağrı - önbellekteki True kullanılır, sunucuya 3. çağrı yapılmaz
    res3 = store.hybrid_search(dense=np.zeros(4, dtype=np.float32), sparse={}, limit=5)
    assert res3 == []
    assert mock_client.collection_exists.call_count == 2


def test_upsert_empty_sparse_logs_warning(caplog: pytest.LogCaptureFixture) -> None:
    """Verify that rec.sparse={} logs a warning containing chunk_id and still upserts the point."""
    store = QdrantStore(url=":memory:", api_key="", collection="test_col", tenant_key="tenant1")
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True
    store._client_instance = mock_client

    rec = ChunkRecord(
        chunk_id="chunk_test_999",
        doc_id="doc_1",
        source="doc1.md",
        doc_type="md",
        tags=["tag1"],
        content="hello world",
        section_path=["sec1"],
        char_count=11,
        prev_chunk=None,
        next_chunk=None,
        dense=np.zeros(4, dtype=np.float32),
        sparse={},
    )

    with caplog.at_level(logging.WARNING):
        count = store.upsert([rec])

    assert count == 1
    assert mock_client.upsert.called
    # Uyarı logunun chunk_id içerdiği doğrulanır
    assert "chunk_test_999" in caplog.text
    assert "sparse vektör boş" in caplog.text

    # Nokta sparse vektörünün indeks ve değerlerinin boş olduğu doğrulanır
    upsert_kwargs = mock_client.upsert.call_args.kwargs
    points = upsert_kwargs["points"]
    assert len(points) == 1
    sparse_vec = points[0].vector["sparse"]
    assert sparse_vec.indices == []
    assert sparse_vec.values == []
