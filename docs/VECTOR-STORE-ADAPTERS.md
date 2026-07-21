# Vector Store Adapters — Qdrant as the priority backend

Design for making the vector store **pluggable**, with **Qdrant as the first-class server backend** and LanceDB remaining the zero-daemon local default. This supersedes the "no shared vector database in v1" non-goal in [API-ARCHITECTURE.md](API-ARCHITECTURE.md) — the adapter seam is now a **priority deliverable**, built during Phase 1 right after the `Workspace` refactor.

## 1. Why Qdrant, and why an adapter (not a swap)

**What Qdrant fixes, concretely:**

| Current pain (LanceDB path) | Qdrant answer |
|---|---|
| `_sparse_search` = full-table pandas scan + Python dot-product loop per query — O(N), the #1 scalability issue | **Native sparse vectors** with an inverted index; bge-m3 lexical weights map 1:1 onto Qdrant's `SparseVector` |
| RRF fusion computed client-side in Python | **Server-side fusion**: Query API `prefetch` (dense + sparse) + `FusionQuery(fusion=RRF)` — one round trip, one result list |
| `tags_str = ",a,b,"` LIKE hack + string interpolation into SQL (injection surface) | Native `tags` keyword payload index; **structured filter objects, nothing interpolated** |
| Store = files on a shared RWX volume; api+workers must mount the same FS | Qdrant is a network service — api/workers need **no shared filesystem for search**, only for raw/processed files |
| Full drop-and-recreate on every embed | First-class `upsert` / `delete(filter=doc_id)` — incremental indexing (ROADMAP Phase 2) becomes trivial |
| Multi-tenant isolation = directory-per-workspace only | Payload-partitioned multitenancy with a dedicated tenant index — one collection, thousands of workspaces |

**Why an adapter and not a migration:** the local-first CLI story (`pip install doqqy`, no daemon, corpus in a folder you can zip) is the product's identity and must keep working with zero infrastructure. LanceDB stays the default for `doqqy` on a laptop; Qdrant is what `doqqy serve` / SaaS runs on. Same engine, one seam, two backends.

## 2. The port: `VectorStore` protocol

Lives in `src/doqqy/infra/vectorstore/base.py`. This is the **only** interface `embed.py`, `query.py`, `map_gen.py`, and the services may talk to — no `lancedb` or `qdrant_client` import outside `infra/vectorstore/`.

```python
"""Vector store portu — embed/query/map yalnızca bu arayüzü bilir."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Sequence

import numpy as np


@dataclass(frozen=True)
class ChunkRecord:
    """Backend-bağımsız chunk kaydı (LanceDB satırı ≈ Qdrant point)."""
    chunk_id: str
    doc_id: str
    source: str
    doc_type: str
    tags: list[str]
    content: str
    section_path: list[str]
    char_count: int
    prev_chunk: str | None
    next_chunk: str | None
    dense: np.ndarray | None = None            # float32[1024]
    sparse: dict[int, float] | None = None     # bge-m3 lexical_weights: token_id → weight


@dataclass(frozen=True)
class ScoredChunk:
    record: ChunkRecord
    dense_rank: int | None = None
    sparse_rank: int | None = None
    fused_score: float = 0.0                   # RRF (backend'de ya da client'ta hesaplanmış)


@dataclass(frozen=True)
class TagFilter:
    """Yapısal filtre — string interpolation YOK. Adapter kendi dialect'ine çevirir."""
    tags: tuple[str, ...] = ()                 # AND semantiği


class VectorStore(Protocol):
    # ---- yazma ----
    def recreate(self, dim: int) -> None: ...
    def upsert(self, records: Sequence[ChunkRecord]) -> int: ...
    def delete_by_doc(self, doc_id: str) -> int: ...

    # ---- okuma ----
    def hybrid_search(
        self, dense: np.ndarray, sparse: dict[int, float],
        *, limit: int, flt: TagFilter | None = None,
    ) -> list[ScoredChunk]:
        """Dense + sparse → RRF-fused tek liste. Fusion'ı backend yapabiliyorsa
        backend yapar (Qdrant); yapamıyorsa adapter client-side RRF uygular (LanceDB)."""
        ...

    def get_by_ids(self, chunk_ids: Sequence[str]) -> list[ChunkRecord]: ...
    def all_vectors(self, flt: TagFilter | None = None) -> tuple[np.ndarray, list[ChunkRecord]]:
        """map_gen Pass 2 için: (N,1024) matris + kayıtlar."""
        ...
    def list_tags(self) -> list[str]: ...
    def count(self) -> int: ...
    def close(self) -> None: ...
```

Design notes:

- **Guaranteed cleanup contract via `contextlib.closing`.** Callers wrap store instantiation in `with contextlib.closing(make_store(ws, settings)) as store:`. This guarantees `close()` is invoked upon exiting the block, even if an exception occurs during `hybrid_search()` or `all_vectors()`, without requiring individual adapters to implement boilerplate context manager methods.
- **Fusion lives behind the port.** `query.py` no longer implements `_rrf` — it calls `hybrid_search` and gets one fused list. The Qdrant adapter delegates fusion to the server; the LanceDB adapter keeps today's client-side RRF (moved into the adapter, byte-for-byte same algorithm so existing behavior is preserved). Reranking (bge-reranker-v2-m3) stays in `query.py` — it's model inference, not storage.
- **`sparse` keys become `int`.** bge-m3's `lexical_weights` keys are token ids serialized as strings today; the port normalizes to `dict[int, float]`, which is exactly Qdrant's `SparseVector(indices, values)` shape. The LanceDB adapter keeps JSON-string serialization internally.
- **`TagFilter` is a value object**, translated per backend: Qdrant → `FieldCondition(key="tags", match=...)`; LanceDB → the validated `tags_str LIKE` clause. The injection surface disappears from core code entirely.

## 3. Factory & configuration

`src/doqqy/infra/vectorstore/factory.py` — selected by settings, resolved per workspace:

```python

def make_store(ws: Workspace, settings: Settings) -> VectorStore:
    match settings.vector_backend:
        case "lancedb":
            from .lancedb_store import LanceDBStore
            return LanceDBStore(ws.store_dir)
        case "qdrant":
            from .qdrant_store import QdrantStore
            return QdrantStore(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                collection=settings.qdrant_collection,      # tek koleksiyon
                tenant_key=str(ws.root),                    # workspace kimliği → payload partition
            )
        case other:
            raise ValueError(f"bilinmeyen vector backend: {other}")
```

```python
# infra/settings.py — eklenen alanlar
vector_backend: str = "lancedb"        # lancedb | qdrant
qdrant_url: str = "http://localhost:6333"
qdrant_api_key: str = ""
qdrant_collection: str = "doqqy_chunks"
```

CLI override for experimentation: `doqqy embed --backend qdrant`, `doqqy query "..." --backend qdrant` (flag > env > default). `StoreManager` from API-ARCHITECTURE becomes the cache in front of this factory — LRU of `VectorStore` instances keyed by `(backend, workspace)`; for Qdrant the "handle" is just a client+tenant pair, so the cache is cheap.

## 4. The Qdrant adapter

`src/doqqy/infra/vectorstore/qdrant_store.py`. Dependency: `qdrant-client>=1.10` (Query API with server-side fusion), shipped as `pip install doqqy[qdrant]`.

### 4.1 Collection schema

**One collection, payload-partitioned multitenancy** (Qdrant's recommended pattern — scales to thousands of workspaces without per-collection overhead):

```python
from qdrant_client import QdrantClient, models

def ensure_collection(client: QdrantClient, name: str, dim: int) -> None:
    if client.collection_exists(name):
        return
    client.create_collection(
        collection_name=name,
        vectors_config={
            "dense": models.VectorParams(size=dim, distance=models.Distance.COSINE),
        },
        sparse_vectors_config={
            "sparse": models.SparseVectorParams(
                index=models.SparseIndexParams(on_disk=False),
                modifier=models.Modifier.IDF,        # bge-m3 lexical ağırlıklarıyla iyi çalışır
            ),
        },
    )
    # tenant partition anahtarı — Qdrant depolamayı tenant'a göre ko-lokalize eder
    client.create_payload_index(name, "tenant", models.KeywordIndexParams(
        type=models.KeywordIndexType.KEYWORD, is_tenant=True,
    ))
    client.create_payload_index(name, "tags", models.PayloadSchemaType.KEYWORD)
    client.create_payload_index(name, "doc_id", models.PayloadSchemaType.KEYWORD)
```

Point layout — `chunk_id` (UUID) is the point ID directly; everything else is payload:

```python
models.PointStruct(
    id=rec.chunk_id,
    vector={
        "dense": rec.dense.tolist(),
        "sparse": models.SparseVector(
            indices=list(rec.sparse.keys()),      # bge-m3 token id'leri (int)
            values=list(rec.sparse.values()),
        ),
    },
    payload={
        "tenant": self._tenant_key,               # workspace kimliği
        "doc_id": rec.doc_id, "source": rec.source, "doc_type": rec.doc_type,
        "tags": rec.tags,                         # NATIVE list — tags_str hack yok
        "content": rec.content,
        "section_path": rec.section_path,
        "char_count": rec.char_count,
        "prev_chunk": rec.prev_chunk, "next_chunk": rec.next_chunk,
    },
)
```

### 4.2 Hybrid search — the payoff

Dense + sparse retrieval **and** RRF fusion in a single server-side request. This deletes doqqy's Python sparse scan and client fusion in Qdrant mode:

```python
def hybrid_search(self, dense, sparse, *, limit, flt=None):
    conditions = [models.FieldCondition(key="tenant",
                                        match=models.MatchValue(value=self._tenant_key))]
    if flt:
        conditions += [models.FieldCondition(key="tags", match=models.MatchValue(value=t))
                       for t in flt.tags]
    qfilter = models.Filter(must=conditions)

    res = self._client.query_points(
        collection_name=self._collection,
        prefetch=[
            models.Prefetch(query=dense.tolist(), using="dense",
                            filter=qfilter, limit=limit),
            models.Prefetch(
                query=models.SparseVector(indices=list(sparse.keys()),
                                          values=list(sparse.values())),
                using="sparse", filter=qfilter, limit=limit,
            ),
        ],
        query=models.FusionQuery(fusion=models.Fusion.RRF),   # sunucu tarafı RRF
        limit=limit,
        with_payload=True,
    )
    return [self._to_scored(p) for p in res.points]
```

Filter objects all the way down — no string is ever interpolated, so the B3 injection concern is structurally impossible in this backend.

### 4.3 Behavior notes & parity with LanceDB mode

- **RRF constant:** Qdrant's fusion uses its own internal RRF; doqqy's client-side RRF uses k=60. Rankings can differ slightly between backends — acceptable, but the retrieval **eval harness** (ROADMAP #7) should run against both backends in CI to catch real regressions. Per-leg `dense_rank`/`sparse_rank` diagnostics aren't returned by fused queries; expose them behind `--explain` (two extra prefetch-only queries) rather than always paying for them.
- **`all_vectors()` for map Pass 2:** implemented with `scroll` + `with_vectors=["dense"]`, filtered by tenant. Same in-memory centroid math as today. (Later optimization: server-side `query_points` per section centroid — not needed for v1.)
- **Incremental ops:** `delete_by_doc` = `client.delete(filter=doc_id AND tenant)`; `upsert` is idempotent by point ID. The Phase-2 incremental design works unchanged.
- **`list_tags`:** from the workspace **manifest**, not the store (both backends) — no scans.
- **Consistency:** Qdrant upserts are visible near-immediately; no `StoreManager.invalidate()` dance needed — the adapter's `invalidate` is a no-op.

## 5. What changes in existing modules

| Module | Change | Status |
|---|---|---|
| `embed.py` | Stops importing lancedb; builds `ChunkRecord`s (sparse as `dict[int,float]`) and calls `store.recreate(dim)` + `store.upsert(records)`. The `tags_str`/`section_path_str` derived columns move into `LanceDBStore` (its private storage concern) | **Implemented** |
| `query.py` | `_dense_search`, `_sparse_search`, `_rrf` move into `LanceDBStore` (unchanged logic); `search()` becomes: embed query → `store.hybrid_search(...)` → rerank → `SearchHit`s | **Implemented** |
| `map_gen.py` | `_load_table()`/`to_pandas()` replaced by `store.all_vectors(flt)` | **Implemented** |
| `cli.py` | `tags` command uses `store.list_tags()`; `--backend` flag added to `embed`/`query`/`map`/`tags` | **Implemented** |
| `services/`, `server/` | Only construct stores via the factory; no other change — the API blueprint's `StoreManager` seam was designed for exactly this | **Implemented** |

**Phase 1 Status:** Completed. Decoupling port and LanceDB adapter logic relocation is fully implemented, verified via unit and parity testing.

Estimated remaining effort (Phase 1.5): Qdrant adapter + parity tests ~3–4 days; migration tool ~1 day.

## 6. Migration: LanceDB → Qdrant without re-embedding

Vectors already live in the LanceDB store — a corpus can be migrated in minutes, no GPU needed:

```python
# cli.py
@app.command()
def migrate_store(
    to: str = typer.Option(..., "--to", help="Hedef backend (qdrant)."),
    batch: int = typer.Option(256, "--batch"),
) -> None:
    """Mevcut store'daki vektörleri yeniden embed etmeden hedef backend'e taşı."""
    ws = Workspace(Path.cwd())
    src = make_store(ws, settings_with(backend="lancedb"))
    dst = make_store(ws, settings_with(backend=to))
    dst.recreate(dim=EMBEDDING_DIM)
    moved = 0
    for records in src.iter_records(batch_size=batch):     # port'a eklenen iterator
        moved += dst.upsert(records)
    console.print(f"[green]✓[/green] {moved} chunk taşındı → {to}")
```

Rollback is the same command in reverse. Because `doqqy embed` remains fully deterministic from `chunks.parquet`, the worst-case recovery is always "re-run embed against the other backend".

## 7. Deployment addition (compose)

```yaml
# docker-compose.api.yml — eklenen servis
  qdrant:
    image: qdrant/qdrant:latest
    volumes: ["qdrantdata:/qdrant/storage"]
    environment:
      QDRANT__SERVICE__API_KEY: ${QDRANT_API_KEY}
    # prod: 6333 (REST) / 6334 (gRPC) sadece iç ağa açık — edge'den erişilmez

  api:
    environment:
      DOQQY_VECTOR_BACKEND: qdrant
      DOQQY_QDRANT_URL: http://qdrant:6333
      DOQQY_QDRANT_API_KEY: ${QDRANT_API_KEY}
  worker:
    environment: { DOQQY_VECTOR_BACKEND: qdrant, DOQQY_QDRANT_URL: http://qdrant:6333, DOQQY_QDRANT_API_KEY: ${QDRANT_API_KEY} }
```

Operationally this **removes the RWX-volume requirement for search**: api pods no longer need the tenants volume at all for the query path (only workers touch raw/processed files). Snapshot/backup = Qdrant's native snapshot API instead of file-tree copies. Prefer gRPC (`prefer_grpc=True`) between services once things work.

## 8. Revised priority order

This document **changes the ROADMAP sequencing**: the adapter port is pulled into Phase 1 (it's the same refactor motion as `Workspace` — do them together while the code is open), and the Qdrant adapter lands before the multi-tenant API, because the API's scalability story (no sparse scans, no shared-FS search, payload multitenancy) is much stronger on Qdrant.

```
Phase 1   Workspace refactor + VectorStore port + LanceDB adapter (logic move) + tests
Phase 1.5 Qdrant adapter + migrate-store command + backend parity eval        ← NEW, priority
Phase 2   Incremental indexing (manifest; trivial on Qdrant, doable on LanceDB)
Phase 3a  doqqy serve + MCP server
Phase 3b  Multi-tenant API — Qdrant as the default prod backend
```

**Non-goals still hold:** LanceDB remains the default for local CLI use (zero-daemon is the product identity); doqqy does not adopt Qdrant-only features that would break backend parity for core search semantics (dense+sparse+RRF+rerank must mean the same thing on both).
