"""Mocked unit tests for QdrantStore verifying serialization, filter construction,
and response mapping (skipped if qdrant-client is not installed).

No network access or running Qdrant server required — see tests/integration/test_qdrant_store.py
for the container-backed tests.
"""

from __future__ import annotations

import importlib.util
import uuid
from unittest.mock import MagicMock

import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord, TagFilter
from doqqy.infra.vectorstore.qdrant_store import QdrantStore

HAS_QDRANT_CLIENT = importlib.util.find_spec("qdrant_client") is not None


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_store_mocked_upsert():
    """Verify upsert constructs PointStruct with correct payload and sparse vector formatting."""
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True

    store = QdrantStore(url="http://localhost:6333", api_key="", collection="test_col", tenant_key="tenant_1")
    store._client_instance = mock_client

    rec = ChunkRecord(
        chunk_id="chunk-abc",
        doc_id="doc-xyz",
        source="doc.md",
        doc_type="markdown",
        tags=["tag1", "tag2"],
        content="Sample content",
        section_path=["Sec1"],
        char_count=14,
        prev_chunk=None,
        next_chunk=None,
        dense=np.ones(4, dtype=np.float32),
        sparse={10: 1.5, 20: 2.5},
    )

    count = store.upsert([rec])
    assert count == 1
    mock_client.upsert.assert_called_once()
    kwargs = mock_client.upsert.call_args[1]
    assert kwargs["collection_name"] == "test_col"
    points = kwargs["points"]
    assert len(points) == 1

    pt = points[0]
    assert pt.id == str(uuid.uuid5(uuid.NAMESPACE_URL, "chunk-abc"))
    assert pt.payload is not None
    assert pt.payload["chunk_id"] == "chunk-abc"
    assert pt.payload["tenant"] == "tenant_1"
    assert pt.payload["tags"] == ["tag1", "tag2"]
    assert pt.payload["doc_id"] == "doc-xyz"
    assert isinstance(pt.vector, dict)
    assert pt.vector["dense"] == [1.0, 1.0, 1.0, 1.0]
    sparse_vec = pt.vector["sparse"]
    assert getattr(sparse_vec, "indices", None) == [10, 20] or sparse_vec.indices == [10, 20]  # type: ignore[union-attr]
    assert getattr(sparse_vec, "values", None) == [1.5, 2.5] or sparse_vec.values == [1.5, 2.5]  # type: ignore[union-attr]


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_store_mocked_hybrid_search():
    """Verify hybrid_search builds dense/sparse Prefetch queries and FusionQuery(RRF)."""
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True

    mock_point = MagicMock()
    mock_point.id = "chunk-100"
    mock_point.score = 0.95
    mock_point.payload = {
        "tenant": "tenant_1",
        "doc_id": "doc-1",
        "source": "file.md",
        "doc_type": "markdown",
        "tags": ["ai"],
        "content": "matched text",
        "section_path": ["Heading"],
        "char_count": 12,
        "prev_chunk": None,
        "next_chunk": None,
    }
    mock_client.query_points.return_value.points = [mock_point]

    store = QdrantStore(url="http://localhost:6333", api_key="", collection="test_col", tenant_key="tenant_1")
    store._client_instance = mock_client

    dense_q = np.array([0.1, 0.2], dtype=np.float32)
    sparse_q = {5: 0.8}
    flt = TagFilter(tags=("ai",))

    hits = store.hybrid_search(dense_q, sparse_q, limit=3, flt=flt)
    assert len(hits) == 1
    assert hits[0].record.chunk_id == "chunk-100"
    assert hits[0].fused_score == 0.95

    mock_client.query_points.assert_called_once()
    q_kwargs = mock_client.query_points.call_args[1]
    assert q_kwargs["collection_name"] == "test_col"
    assert len(q_kwargs["prefetch"]) == 2


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_store_mocked_delete_by_doc():
    """Verify delete_by_doc filters by both tenant and doc_id."""
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True
    mock_client.count.return_value.count = 3

    store = QdrantStore(url="http://localhost:6333", api_key="", collection="test_col", tenant_key="tenant_1")
    store._client_instance = mock_client

    deleted = store.delete_by_doc("doc-99")
    assert deleted == 3
    mock_client.delete.assert_called_once()


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_store_mocked_all_vectors():
    """Verify all_vectors converts scrolled points into numpy matrix and records."""
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True

    p1 = MagicMock()
    p1.id = "c1"
    p1.vector = {"dense": [0.1, 0.2]}
    p1.payload = {"doc_id": "d1", "source": "s1", "doc_type": "md", "tags": []}

    p2 = MagicMock()
    p2.id = "c2"
    p2.vector = {"dense": [0.3, 0.4]}
    p2.payload = {"doc_id": "d1", "source": "s1", "doc_type": "md", "tags": []}

    mock_client.scroll.return_value = ([p1, p2], None)

    store = QdrantStore(url="http://localhost:6333", api_key="", collection="test_col", tenant_key="tenant_1")
    store._client_instance = mock_client

    matrix, records = store.all_vectors()
    assert matrix.shape == (2, 2)
    assert len(records) == 2
    assert records[0].chunk_id == "c1"
    assert records[1].chunk_id == "c2"
