"""Container integration tests for QdrantStore.

Requires a reachable Qdrant server (automatically skipped otherwise). See
tests/unit/infra/vectorstore/test_qdrant_store_mocked.py for the mocked
unit tests that need no running dependency.
"""

from __future__ import annotations

import importlib.util
import os
import uuid
from typing import Generator

import numpy as np
import pytest

from doqqy.infra.vectorstore.base import ChunkRecord, TagFilter
from doqqy.infra.vectorstore.qdrant_store import QdrantStore

QDRANT_URL = os.environ.get("DOQQY_QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.environ.get("DOQQY_QDRANT_API_KEY", "")
HAS_QDRANT_CLIENT = importlib.util.find_spec("qdrant_client") is not None


@pytest.fixture(scope="session")
def qdrant_available() -> bool:
    """Check if Qdrant server is reachable and authentication succeeds (cached per session)."""
    if not HAS_QDRANT_CLIENT:
        return False
    try:
        from qdrant_client import QdrantClient  # type: ignore

        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY or None,
            check_compatibility=False,
            timeout=1,
        )
        client.get_collections()
        client.close()
        return True
    except Exception:  # noqa: BLE001
        return False


@pytest.fixture
def qdrant_store(qdrant_available: bool) -> Generator[QdrantStore, None, None]:
    """Fixture providing an isolated QdrantStore instance for integration testing."""
    if not qdrant_available:
        pytest.skip(f"Qdrant server not reachable at {QDRANT_URL}")

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


@pytest.mark.slow
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

    fetched_doc = store.get_by_doc("doc-1")
    assert len(fetched_doc) == 2
    assert {r.chunk_id for r in fetched_doc} == {chunk_id1, chunk_id2}

    iter_batches = list(store.iter_records(batch_size=1))
    assert len(iter_batches) == 2
    iter_records_all = [r for batch in iter_batches for r in batch]
    assert len(iter_records_all) == 2
    assert {r.chunk_id for r in iter_records_all} == {chunk_id1, chunk_id2}
    r1 = next(r for r in iter_records_all if r.chunk_id == chunk_id1)
    assert r1.dense is not None
    assert np.allclose(r1.dense, vec1 / np.linalg.norm(vec1), atol=1e-5)
    assert r1.sparse == {101: 0.5, 102: 1.2}

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


@pytest.mark.slow
def test_qdrant_store_tenant_isolation_integration(qdrant_available: bool) -> None:
    """Integration test verifying two tenants sharing a collection remain fully isolated."""
    if not qdrant_available:
        pytest.skip(f"Qdrant server not reachable at {QDRANT_URL}")

    shared_collection = f"test_shared_{uuid.uuid4().hex[:8]}"
    store_a = QdrantStore(QDRANT_URL, QDRANT_API_KEY, shared_collection, "tenant_alpha")
    store_b = QdrantStore(QDRANT_URL, QDRANT_API_KEY, shared_collection, "tenant_beta")
    dim = 64

    try:
        dense_a = np.zeros(dim, dtype=np.float32)
        dense_a[0] = 1.0
        dense_b = np.zeros(dim, dtype=np.float32)
        dense_b[1] = 1.0

        rec_a = ChunkRecord(
            chunk_id=str(uuid.uuid4()),
            doc_id="doc-a",
            source="alpha.md",
            doc_type="markdown",
            tags=["alpha-tag"],
            content="Alpha content",
            section_path=[],
            char_count=13,
            prev_chunk=None,
            next_chunk=None,
            dense=dense_a,
            sparse={1: 1.0},
        )

        rec_b = ChunkRecord(
            chunk_id=str(uuid.uuid4()),
            doc_id="doc-b",
            source="beta.md",
            doc_type="markdown",
            tags=["beta-tag"],
            content="Beta content",
            section_path=[],
            char_count=12,
            prev_chunk=None,
            next_chunk=None,
            dense=dense_b,
            sparse={2: 1.0},
        )

        store_a.upsert([rec_a])
        store_b.upsert([rec_b])

        # Verify counts are isolated
        assert store_a.count() == 1
        assert store_b.count() == 1

        # Verify list_tags are isolated
        assert store_a.list_tags() == ["alpha-tag"]
        assert store_b.list_tags() == ["beta-tag"]

        assert rec_a.dense is not None
        assert rec_b.dense is not None

        # Verify search is isolated: store_a search returns rec_a and NEVER rec_b
        hits_a = store_a.hybrid_search(rec_a.dense, {1: 1.0}, limit=5)
        assert len(hits_a) == 1
        assert hits_a[0].record.chunk_id == rec_a.chunk_id

        hits_b_on_a = store_a.hybrid_search(rec_b.dense, {2: 1.0}, limit=5)
        for hit in hits_b_on_a:
            assert hit.record.chunk_id != rec_b.chunk_id
            assert hit.record.doc_id != "doc-b"

        hits_b = store_b.hybrid_search(rec_b.dense, {2: 1.0}, limit=5)
        assert len(hits_b) == 1
        assert hits_b[0].record.chunk_id == rec_b.chunk_id

        hits_a_on_b = store_b.hybrid_search(rec_a.dense, {1: 1.0}, limit=5)
        for hit in hits_a_on_b:
            assert hit.record.chunk_id != rec_a.chunk_id
            assert hit.record.doc_id != "doc-a"

        # Verify full_rebuild on tenant A does not delete tenant B
        rec_a2 = ChunkRecord(
            chunk_id=str(uuid.uuid4()),
            doc_id="doc-a2",
            source="alpha2.md",
            doc_type="markdown",
            tags=["alpha-tag"],
            content="Alpha 2 content",
            section_path=[],
            char_count=15,
            prev_chunk=None,
            next_chunk=None,
            dense=np.ones(dim, dtype=np.float32) * 0.3,
            sparse={3: 1.0},
        )

        store_a.full_rebuild([rec_a2], dim=dim)
        assert store_a.count() == 1
        assert store_b.count() == 1

    finally:
        try:
            if store_a._client_instance is not None and store_a._client.collection_exists(shared_collection):
                store_a._client.delete_collection(shared_collection)
        except Exception:  # noqa: BLE001
            pass
        store_a.close()
        store_b.close()
