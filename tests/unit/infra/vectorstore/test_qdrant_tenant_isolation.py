"""Unit tests for QdrantStore multi-tenant isolation.

Verifies that operations (count, hybrid_search, list_tags, get_by_ids, full_rebuild)
do not leak data between different tenant_key values sharing the same collection.
"""

from __future__ import annotations

import importlib.util
from unittest.mock import MagicMock

import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord
from doqqy.infra.vectorstore.qdrant_store import QdrantStore

HAS_QDRANT_CLIENT = importlib.util.find_spec("qdrant_client") is not None


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_tenant_isolation_filter_construction():
    """Verify tenant_key is strictly enforced in filter building and search queries."""
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True

    store_a = QdrantStore("http://localhost:6333", "", "shared_col", "tenant_A")
    store_a._client_instance = mock_client

    store_b = QdrantStore("http://localhost:6333", "", "shared_col", "tenant_B")
    store_b._client_instance = mock_client

    # 1. _build_filter check
    flt_a = store_a._build_filter()
    flt_b = store_b._build_filter()

    assert flt_a.must[0].key == "tenant"
    assert flt_a.must[0].match.value == "tenant_A"
    assert flt_b.must[0].key == "tenant"
    assert flt_b.must[0].match.value == "tenant_B"

    # 2. count check
    store_a.count()
    kwargs_a = mock_client.count.call_args[1]
    assert kwargs_a["count_filter"].must[0].match.value == "tenant_A"

    store_b.count()
    kwargs_b = mock_client.count.call_args[1]
    assert kwargs_b["count_filter"].must[0].match.value == "tenant_B"


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_tenant_isolation_full_rebuild_does_not_drop_collection():
    """Verify full_rebuild deletes only the points for the target tenant without dropping collection."""
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True

    store_a = QdrantStore("http://localhost:6333", "", "shared_col", "tenant_A")
    store_a._client_instance = mock_client

    rec_a = ChunkRecord(
        chunk_id="chunk-a1",
        doc_id="doc-a",
        source="doc_a.md",
        doc_type="markdown",
        tags=["tag-a"],
        content="Content A",
        section_path=[],
        char_count=9,
        prev_chunk=None,
        next_chunk=None,
        dense=np.ones(4, dtype=np.float32),
        sparse={1: 1.0},
    )

    store_a.full_rebuild([rec_a], dim=4)

    # Must NOT call delete_collection
    mock_client.delete_collection.assert_not_called()

    # Must call client.delete with a FilterSelector matching tenant_A
    mock_client.delete.assert_called_once()
    delete_kwargs = mock_client.delete.call_args[1]
    assert delete_kwargs["collection_name"] == "shared_col"
    selector = delete_kwargs["points_selector"]
    assert selector.filter.must[0].key == "tenant"
    assert selector.filter.must[0].match.value == "tenant_A"


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_tenant_isolation_get_by_ids_filters_other_tenants():
    """Verify get_by_ids filters out records that belong to another tenant."""
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True

    p_a = MagicMock()
    p_a.id = "c1"
    p_a.payload = {"tenant": "tenant_A", "doc_id": "dA", "source": "sA", "doc_type": "md", "tags": []}

    p_b = MagicMock()
    p_b.id = "c2"
    p_b.payload = {"tenant": "tenant_B", "doc_id": "dB", "source": "sB", "doc_type": "md", "tags": []}

    mock_client.retrieve.return_value = [p_a, p_b]

    store_a = QdrantStore("http://localhost:6333", "", "shared_col", "tenant_A")
    store_a._client_instance = mock_client

    records_a = store_a.get_by_ids(["c1", "c2"])
    assert len(records_a) == 1
    assert records_a[0].chunk_id == "c1"


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_tenant_isolation_recreate_does_not_drop_collection():
    """Verify recreate deletes only the points for the target tenant without dropping collection."""
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True

    store_a = QdrantStore("http://localhost:6333", "", "shared_col", "tenant_A")
    store_a._client_instance = mock_client

    store_a.recreate(dim=4)

    # Must NOT call delete_collection
    mock_client.delete_collection.assert_not_called()

    # Must call client.delete with a FilterSelector matching tenant_A
    mock_client.delete.assert_called_once()
    delete_kwargs = mock_client.delete.call_args[1]
    assert delete_kwargs["collection_name"] == "shared_col"
    selector = delete_kwargs["points_selector"]
    assert selector.filter.must[0].key == "tenant"
    assert selector.filter.must[0].match.value == "tenant_A"


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_iter_records_tenant_scoped():
    """Verify iter_records uses tenant-filtered scroll and requests with_vectors=True."""
    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True

    p_a = MagicMock()
    p_a.id = "c1"
    p_a.payload = {"tenant": "tenant_A", "doc_id": "dA", "source": "sA", "doc_type": "md", "tags": ["tag1"]}
    p_a.vector = {
        "dense": [0.1, 0.2, 0.3, 0.4],
        "sparse": MagicMock(indices=[101, 102], values=[0.5, 1.2]),
    }

    mock_client.scroll.return_value = ([p_a], None)

    store_a = QdrantStore("http://localhost:6333", "", "shared_col", "tenant_A")
    store_a._client_instance = mock_client

    batches = list(store_a.iter_records(batch_size=10))
    assert len(batches) == 1
    assert len(batches[0]) == 1
    rec = batches[0][0]
    assert rec.chunk_id == "c1"
    assert rec.sparse == {101: 0.5, 102: 1.2}

    mock_client.scroll.assert_called_once()
    scroll_kwargs = mock_client.scroll.call_args[1]
    assert scroll_kwargs["collection_name"] == "shared_col"
    assert scroll_kwargs["with_payload"] is True
    assert scroll_kwargs["with_vectors"] is True
    assert scroll_kwargs["limit"] == 10
    assert scroll_kwargs["scroll_filter"].must[0].key == "tenant"
    assert scroll_kwargs["scroll_filter"].must[0].match.value == "tenant_A"


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_iter_records_pagination():
    """Verify iter_records iterates across multiple scroll pages using offset tokens losslessly."""
    import numpy as np

    mock_client = MagicMock()
    mock_client.collection_exists.return_value = True

    p1 = MagicMock()
    p1.id = "chunk-1"
    p1.payload = {
        "tenant": "tenant_A",
        "doc_id": "doc-1",
        "source": "raw/doc1.md",
        "doc_type": "markdown",
        "tags": ["python", "backend"],
        "content": "Page 1 content",
        "section_path": ["Root", "Intro"],
        "char_count": 14,
        "prev_chunk": None,
        "next_chunk": "chunk-2",
    }
    p1.vector = {
        "dense": [0.1, 0.2, 0.3, 0.4],
        "sparse": MagicMock(indices=[101, 102], values=[0.5, 1.2]),
    }

    p2 = MagicMock()
    p2.id = "chunk-2"
    p2.payload = {
        "tenant": "tenant_A",
        "doc_id": "doc-1",
        "source": "raw/doc1.md",
        "doc_type": "markdown",
        "tags": ["python"],
        "content": "Page 2 content",
        "section_path": ["Root", "Body"],
        "char_count": 14,
        "prev_chunk": "chunk-1",
        "next_chunk": None,
    }
    p2.vector = {
        "dense": [0.5, 0.6, 0.7, 0.8],
        "sparse": MagicMock(indices=[103], values=[2.0]),
    }

    # Simulate 2-page scroll pagination loop: page 1 returns offset="next_token", page 2 returns offset=None
    mock_client.scroll.side_effect = [
        ([p1], "page_2_offset_token"),
        ([p2], None),
    ]

    store = QdrantStore("http://localhost:6333", "", "shared_col", "tenant_A")
    store._client_instance = mock_client

    batches = list(store.iter_records(batch_size=1))
    assert len(batches) == 2
    assert len(batches[0]) == 1
    assert len(batches[1]) == 1

    # Verify 2 scroll calls made, with correct offset passed in 2nd call
    assert mock_client.scroll.call_count == 2
    call1_kwargs = mock_client.scroll.call_args_list[0][1]
    call2_kwargs = mock_client.scroll.call_args_list[1][1]
    assert call1_kwargs["offset"] is None
    assert call2_kwargs["offset"] == "page_2_offset_token"

    # Lossless field assertions for page 1 (p1)
    rec1 = batches[0][0]
    assert rec1.chunk_id == "chunk-1"
    assert rec1.doc_id == "doc-1"
    assert rec1.source == "raw/doc1.md"
    assert rec1.doc_type == "markdown"
    assert rec1.tags == ["python", "backend"]
    assert rec1.content == "Page 1 content"
    assert rec1.section_path == ["Root", "Intro"]
    assert rec1.char_count == 14
    assert rec1.prev_chunk is None
    assert rec1.next_chunk == "chunk-2"
    assert np.array_equal(rec1.dense, np.asarray([0.1, 0.2, 0.3, 0.4], dtype=np.float32))
    assert rec1.sparse == {101: 0.5, 102: 1.2}

    # Lossless field assertions for page 2 (p2)
    rec2 = batches[1][0]
    assert rec2.chunk_id == "chunk-2"
    assert rec2.prev_chunk == "chunk-1"
    assert rec2.next_chunk is None
    assert rec2.sparse == {103: 2.0}


@pytest.mark.skipif(not HAS_QDRANT_CLIENT, reason="qdrant-client package is not installed")
def test_qdrant_iter_records_edge_cases():
    """Verify edge cases: non-existent collection, empty first page, batch_size larger than point count."""
    mock_client = MagicMock()

    store = QdrantStore("http://localhost:6333", "", "shared_col", "tenant_A")
    store._client_instance = mock_client

    # Edge Case 1: Collection does not exist -> yields [] immediately
    mock_client.collection_exists.return_value = False
    assert list(store.iter_records(batch_size=10)) == []

    # Edge Case 2: Collection exists but first scroll returns empty list -> yields []
    mock_client.collection_exists.return_value = True
    mock_client.scroll.return_value = ([], None)
    assert list(store.iter_records(batch_size=10)) == []

    # Edge Case 3: batch_size larger than point count (N=2 points, batch_size=100) -> single batch yielded
    p1 = MagicMock()
    p1.id = "c1"
    p1.payload = {"tenant": "tenant_A", "doc_id": "d1"}
    p1.vector = {"dense": [0.1, 0.2], "sparse": {"indices": [1], "values": [0.5]}}

    p2 = MagicMock()
    p2.id = "c2"
    p2.payload = {"tenant": "tenant_A", "doc_id": "d1"}
    p2.vector = {"dense": [0.3, 0.4], "sparse": {"indices": [2], "values": [0.8]}}

    mock_client.scroll.return_value = ([p1, p2], None)
    batches = list(store.iter_records(batch_size=100))
    assert len(batches) == 1
    assert len(batches[0]) == 2
    assert [r.chunk_id for r in batches[0]] == ["c1", "c2"]
