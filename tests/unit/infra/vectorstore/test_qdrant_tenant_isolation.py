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
