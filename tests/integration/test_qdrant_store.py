"""Integration and unit tests for QdrantStore.

Includes:
1. Container integration test (automatically skipped if no Qdrant server is reachable).
2. Mocked unit tests verifying serialization, filter construction,
   and response mapping (skipped if qdrant-client is not installed).
"""

from __future__ import annotations

import importlib.util
import os
import urllib.request
import uuid
from typing import Generator
from unittest.mock import MagicMock

import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord, TagFilter
from doqqy.infra.vectorstore.qdrant_store import QdrantStore

QDRANT_URL = os.environ.get("DOQQY_QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.environ.get("DOQQY_QDRANT_API_KEY", "")
HAS_QDRANT_CLIENT = importlib.util.find_spec("qdrant_client") is not None


def _is_qdrant_available() -> bool:
    """Check if Qdrant REST API is reachable."""
    if not HAS_QDRANT_CLIENT:
        return False
    try:
        req = urllib.request.Request(f"{QDRANT_URL}/healthz")
        if QDRANT_API_KEY:
            req.add_header("api-key", QDRANT_API_KEY)
        with urllib.request.urlopen(req, timeout=1.0) as resp:  # noqa: S310
            return resp.status == 200
    except Exception:  # noqa: BLE001
        return False


QDRANT_AVAILABLE = _is_qdrant_available()


@pytest.fixture
def qdrant_store() -> Generator[QdrantStore, None, None]:
    """Fixture providing an isolated QdrantStore instance for integration testing."""
    test_collection = f"test_doqqy_{uuid.uuid4().hex[:8]}"
    tenant_key = f"test_tenant_{uuid.uuid4().hex[:8]}"
    store = QdrantStore(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection=test_collection,
        tenant_key=tenant_key,
    )
    yield store
    # Cleanup collection after test
    try:
        if store._client_instance is not None and store._client.collection_exists(test_collection):
            store._client.delete_collection(test_collection)
    except Exception:  # noqa: BLE001
        pass
    store.close()


@pytest.mark.skipif(not QDRANT_AVAILABLE, reason=f"Qdrant server not reachable at {QDRANT_URL}")
def test_qdrant_store_full_roundtrip(qdrant_store: QdrantStore) -> None:
    """Test full storage lifecycle: ensure_collection, upsert, count, hybrid_search, tags, delete."""
    store = qdrant_store
    dim = 128

    assert store.count() == 0

    vec1 = np.ones(dim, dtype=np.float32) * 0.1
    vec2 = np.ones(dim, dtype=np.float32) * 0.2

    chunk_id1 = str(uuid.uuid4())
    chunk_id2 = str(uuid.uuid4())

    rec1 = ChunkRecord(
        chunk_id=chunk_id1,
        doc_id="doc-1",
        source="raw/doc1.md",
        doc_type="markdown",
        tags=["python", "test"],
        content="Hello Qdrant search world.",
        section_path=["Root", "Intro"],
        char_count=26,
        prev_chunk=None,
        next_chunk=chunk_id2,
        dense=vec1,
        sparse={101: 0.5, 102: 1.2},
    )

    rec2 = ChunkRecord(
        chunk_id=chunk_id2,
        doc_id="doc-1",
        source="raw/doc1.md",
        doc_type="markdown",
        tags=["python"],
        content="Unit testing vector stores.",
        section_path=["Root", "Testing"],
        char_count=27,
        prev_chunk=chunk_id1,
        next_chunk=None,
        dense=vec2,
        sparse={101: 0.8, 103: 0.3},
    )

    upserted = store.upsert([rec1, rec2])
    assert upserted == 2
    assert store.count() == 2

    tags = store.list_tags()
    assert "python" in tags
    assert "test" in tags

    fetched = store.get_by_ids([chunk_id1])
    assert len(fetched) == 1
    assert fetched[0].chunk_id == chunk_id1

    flt_test = TagFilter(tags=("test",))
    hits = store.hybrid_search(
        dense=vec1,
        sparse={102: 1.0},
        limit=5,
        flt=flt_test,
    )
    assert len(hits) == 1
    assert hits[0].record.chunk_id == chunk_id1

    matrix, records = store.all_vectors()
    assert matrix.shape == (2, dim)
    assert len(records) == 2

    deleted = store.delete_by_doc("doc-1")
    assert deleted == 2
    assert store.count() == 0

    rebuilt = store.full_rebuild([rec1], dim=dim)
    assert rebuilt == 1
    assert store.count() == 1


# ---------------------------------------------------------------------------
# Comprehensive Mocked Unit Tests (Gated on HAS_QDRANT_CLIENT)
# ---------------------------------------------------------------------------


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
    assert pt.id == "chunk-abc"
    assert pt.payload["tenant"] == "tenant_1"
    assert pt.payload["tags"] == ["tag1", "tag2"]
    assert pt.payload["doc_id"] == "doc-xyz"
    assert pt.vector["dense"] == [1.0, 1.0, 1.0, 1.0]
    assert pt.vector["sparse"].indices == [10, 20]
    assert pt.vector["sparse"].values == [1.5, 2.5]


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
