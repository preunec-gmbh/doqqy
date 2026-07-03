# API Architecture

Implementation blueprint for the doqqy API layer — written for the engineer who will build and operate it (backend + DevOps perspective). This is the concrete companion to [ROADMAP.md](ROADMAP.md) §3: that document says *why*; this one says *how*, module by module.

Design goals, in order: **modular** (core engine untouched and CLI-compatible), **clean** (strict layering, no business logic in routes), **scalable** (stateless API tier, resident-model workers, queue-decoupled writes).

---

## 1. The layer model

The existing pipeline code becomes the innermost layer. Nothing in it may import from the layers above it — enforceable with import-linter later.

```
┌────────────────────────────────────────────────────────────────┐
│  L4  Edge            nginx / traefik: TLS, body limits,        │
│                      rate limits, gzip                         │
├────────────────────────────────────────────────────────────────┤
│  L3  API             FastAPI app: routing, request/response    │
│      doqqy/server/   schemas, auth, validation, quotas.        │
│                      NO business logic. Translates HTTP ↔ L2.  │
├────────────────────────────────────────────────────────────────┤
│  L2  Services        Use-case orchestration: QueryService,     │
│      doqqy/services/ IngestService, WorkspaceService,          │
│                      JobService. Owns transactions/manifests.  │
│                      Knows nothing about HTTP.                 │
├────────────────────────────────────────────────────────────────┤
│  L1  Core engine     Existing modules, refactored to take an   │
│      doqqy/          explicit Workspace: ingest/, chunk.py,    │
│                      embed.py, query.py, rerank.py, map_gen.py │
├────────────────────────────────────────────────────────────────┤
│  L0  Infrastructure  ModelManager (bge-m3 + reranker),         │
│      doqqy/infra/    StoreManager (LanceDB handles),           │
│                      JobQueue (Redis/arq), Settings, logging   │
└────────────────────────────────────────────────────────────────┘
```

**Dependency rule:** L3 → L2 → L1 → L0. The CLI (`cli.py`) becomes a second L3 head calling the same L2 services — one body, two heads. Anything you can do over HTTP you can do offline, forever.

### Target package layout

```
src/doqqy/
├── config.py                  # legacy constants → thin shim over infra/settings.py (deprecation path)
├── workspace.py               # Workspace dataclass (paths only, frozen)
├── cli.py                     # unchanged UX; calls services
│
├── ingest/  chunk.py  embed.py  query.py  rerank.py  map_gen.py
│   index_gen.py  wikilink_inject.py        # L1 — signatures gain `ws: Workspace`
│
├── infra/
│   ├── settings.py            # pydantic-settings; ALL env config, single source
│   ├── models.py              # ModelManager: process-global bge-m3 + reranker singletons
│   ├── store.py               # StoreManager: per-workspace LanceDB handles, LRU + lock
│   ├── jobs.py                # JobQueue protocol + arq implementation + InProcessQueue (dev)
│   └── logging.py             # structlog JSON config, request-id contextvars
│
├── services/
│   ├── workspaces.py          # WorkspaceService: registry, create/list/delete, quotas
│   ├── querying.py            # QueryService: validate → search → shape results
│   ├── ingestion.py           # IngestService: upload → ingest → chunk → embed (job body)
│   ├── mapping.py             # MapService: map/index/inject
│   └── manifest.py            # Manifest read/write (doc_id → hash, chunk_ids, status)
│
└── server/
    ├── app.py                 # create_app() factory; lifespan loads models
    ├── deps.py                # Depends(): settings, auth → Principal, workspace resolution
    ├── errors.py              # exception → RFC 7807 problem+json mapping
    ├── schemas.py             # pydantic request/response models (the wire contract)
    ├── middleware.py          # request-id, timing, access log
    └── routers/
        ├── query.py  documents.py  workspaces.py  maps.py  jobs.py  meta.py
```

Ship it as an extra: `pip install doqqy[server]` → adds `fastapi`, `uvicorn`, `pydantic-settings`, `arq`, `python-multipart`, `structlog`. The core install stays lean.

---

## 2. L0 — Infrastructure

### 2.1 Settings (`infra/settings.py`)

One config object, environment-driven, injected everywhere. Kills the scattered `os.environ` / module-constant pattern for server concerns while leaving `config.py`'s tuning constants (chunk sizes, thresholds) alone.

```python
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_config = {"env_prefix": "DOQQY_", "env_file": ".env"}

    # topology
    data_root: Path = Path("./data")          # /data/tenants in prod
    redis_url: str = "redis://localhost:6379/0"
    queue_mode: str = "inprocess"             # "inprocess" (dev/serve) | "arq" (prod)

    # models
    device: str = "auto"                      # auto | cuda | cpu
    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-v2-m3"

    # limits (enforced in L2/L3, tunable without code change)
    max_upload_mb: int = 50
    max_docs_per_workspace: int = 5000
    query_rate_per_min: int = 60
    allowed_extensions: frozenset[str] = frozenset({".md", ".markdown", ".txt", ".pdf", ".docx"})

    # auth
    auth_mode: str = "apikey"                 # "none" (local serve) | "apikey"
    api_key_pepper: str = ""                  # secret for hashing stored keys
```

### 2.2 ModelManager (`infra/models.py`)

Models are corpus-independent → **process-global**, loaded once, thread-guarded. This replaces the `lru_cache` singletons in `query.py`/`rerank.py` (blocker B2 partially — the *table* caches were the bug; the *model* caches were correct and just move here).

```python
import threading

class ModelManager:
    """bge-m3 + reranker; tek yükleme, süreç boyu yaşar."""
    def __init__(self, settings: Settings):
        self._s = settings
        self._lock = threading.Lock()
        self._embedder = None
        self._reranker = None

    def embedder(self):
        if self._embedder is None:
            with self._lock:
                if self._embedder is None:
                    from FlagEmbedding import BGEM3FlagModel
                    dev = detect_device() if self._s.device == "auto" else self._s.device
                    self._embedder = BGEM3FlagModel(
                        self._s.embedding_model, use_fp16=(dev == "cuda"), device=dev
                    )
        return self._embedder

    def reranker(self):  # analogous; and FIX: model.to(device) — today it's CPU-only
        ...

    def warmup(self) -> None:
        """Lifespan'de çağrılır: readiness=yeşil olmadan trafik alma."""
        self.embedder(); self.reranker()
```

Concurrency note: bge-m3 inference is not safely reentrant on one GPU without care. v1: a `threading.Semaphore(1)` around encode/rerank calls per process, scale with **more worker processes** (uvicorn `--workers N` on CPU boxes; on GPU boxes 1–2 processes per GPU). Don't build micro-batching until p95 says you must.

### 2.3 StoreManager (`infra/store.py`)

> **Update (2026-07):** the store is now accessed through a pluggable `VectorStore` port (LanceDB default, **Qdrant priority backend** — see [VECTOR-STORE-ADAPTERS.md](VECTOR-STORE-ADAPTERS.md)). StoreManager remains as the per-workspace cache in front of the adapter factory; the LanceDB-specific sketch below describes the LanceDB adapter's internals.

Fixes blocker B2 properly: LanceDB handles are **per-workspace**, cached in a bounded LRU keyed by workspace root, with a lock (LanceDB handles aren't guaranteed thread-safe across writers).

```python
from collections import OrderedDict
import threading

class StoreManager:
    def __init__(self, max_open: int = 64):
        self._cache: OrderedDict[Path, "lancedb.table.Table"] = OrderedDict()
        self._lock = threading.Lock()
        self._max = max_open

    def table(self, ws: Workspace):
        with self._lock:
            if ws.store_dir in self._cache:
                self._cache.move_to_end(ws.store_dir)
                return self._cache[ws.store_dir]
        import lancedb
        db = lancedb.connect(ws.store_dir)
        tbl = db.open_table("chunks")
        with self._lock:
            self._cache[ws.store_dir] = tbl
            while len(self._cache) > self._max:
                self._cache.popitem(last=False)
        return tbl

    def invalidate(self, ws: Workspace) -> None:
        """Embed sonrası çağrılır — eski handle stale olur."""
        with self._lock:
            self._cache.pop(ws.store_dir, None)
```

**Rule:** after any write (`build_index`, incremental update), the writer calls `invalidate()`. In multi-process deployments, handle staleness across processes by re-opening on version mismatch (LanceDB tables are versioned) — v1: invalidate-on-write within a process + short handle TTL (60 s) across processes.

### 2.4 JobQueue (`infra/jobs.py`)

Protocol first, so dev and prod differ only in wiring:

```python
from typing import Protocol
from dataclasses import dataclass

@dataclass
class Job:
    id: str
    kind: str                  # "ingest_embed" | "map" | "reindex"
    workspace_root: str
    payload: dict
    status: str = "queued"     # queued|running|succeeded|failed
    progress: float = 0.0
    error: str | None = None

class JobQueue(Protocol):
    async def enqueue(self, kind: str, ws: Workspace, payload: dict) -> str: ...
    async def get(self, job_id: str) -> Job | None: ...
```

Two implementations:

- **`InProcessQueue`** — `asyncio.create_task` + in-memory dict. Used by `doqqy serve` (single user, no Redis). Jobs die with the process; acceptable locally.
- **`ArqQueue`** — Redis-backed [arq](https://arq-docs.helpmanual.io/) (async-native, tiny, no Celery weight). Job state stored in Redis hashes with TTL. Workers run `doqqy.services.ingestion.run_ingest_job` — the *same function* the in-process queue calls. Prod default.

Why a queue at all: ingest+embed of one PDF can take minutes (docling + bge-m3). Holding an HTTP connection open for that is how you build a fragile system; 202 + job polling is how you build a boring one.

---

## 3. L1 — Core engine changes (the Workspace refactor)

The only invasive change to existing code, and it's mechanical. `workspace.py`:

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Workspace:
    root: Path

    @property
    def raw_dir(self) -> Path:        return self.root / "raw"
    @property
    def processed_dir(self) -> Path:  return self.root / "processed"
    @property
    def state_dir(self) -> Path:      return self.root / ".doqqy"
    @property
    def chunks_parquet(self) -> Path: return self.state_dir / "chunks" / "chunks.parquet"
    @property
    def store_dir(self) -> Path:      return self.state_dir / "store.lance"
    @property
    def topics_yaml(self) -> Path:    return self.state_dir / "topics.yaml"
    @property
    def logs_dir(self) -> Path:       return self.state_dir / "logs"
    @property
    def manifest_path(self) -> Path:  return self.state_dir / "manifest.json"

    def ensure_dirs(self) -> None:
        for d in (self.raw_dir, self.processed_dir, self.state_dir,
                  self.chunks_parquet.parent, self.logs_dir):
            d.mkdir(parents=True, exist_ok=True)
```

Signature changes (keep old behavior via default `Workspace(Path.cwd())` during migration):

```python
# before                                   # after
ingest_directory(root=None, limit=None)  → ingest_directory(ws: Workspace, *, limit=None)
chunk_directory(processed_dir=None)      → chunk_directory(ws: Workspace)
build_index()                            → build_index(ws: Workspace, *, models: ModelManager, stores: StoreManager)
search(query, k, rerank, tag)            → search(ws: Workspace, query: str, *, k, rerank, tag,
                                                  models: ModelManager, stores: StoreManager)
generate_map(...) / generate_index(...) / inject_links(...)  → same pattern
```

Also in this pass (all flagged in [DEVELOPER-HANDOVER.md](DEVELOPER-HANDOVER.md) §4):

1. **Tag sanitation at the L1 boundary** — `search()` and `generate_map()` reject tags failing `^[\w-]+$` with `ValueError`. Defense in depth: L3 validates too (pydantic pattern), but L1 must not trust its callers.
2. **Reranker to device** — `model.to(detect_device())` + inputs to the same device.
3. `chunk_file`: coerce string `tags` frontmatter to `[tags]` (the `",e,r,p,1,2,"` bug).

The CLI keeps working throughout: each command starts with `ws = Workspace(Path.cwd())`.

---

## 4. L2 — Services

Services are plain classes taking their dependencies in `__init__` (constructor injection — no framework, mirrors the manual-DI pattern you use in mobile-expo). They are the **only** layer that composes L1 calls into use cases, and the only writer of the manifest.

```python
# services/querying.py
class QueryService:
    def __init__(self, models: ModelManager, stores: StoreManager, settings: Settings):
        self._models, self._stores, self._s = models, stores, settings

    def query(self, ws: Workspace, q: str, *, k: int, tag: str | None, rerank: bool) -> list[SearchHit]:
        if not ws.store_dir.exists():
            raise WorkspaceNotIndexed(ws.root.name)          # → 409 at L3
        return search(ws, q, k=k, tag=tag, rerank=rerank,
                      models=self._models, stores=self._stores)
```

```python
# services/ingestion.py — the job body (runs in worker OR in-process task)
class IngestService:
    def __init__(self, models, stores, manifest: ManifestService, settings): ...

    async def run_ingest_job(self, ws: Workspace, job: Job) -> None:
        """upload → ingest → chunk → embed. Aşama başına progress raporlar."""
        job.update(status="running", progress=0.05)
        result = ingest_directory(ws)                        # failure isolation zaten içinde
        job.update(progress=0.40, detail={"failed": [str(p) for p, _ in result.failed]})
        chunk_directory(ws)
        job.update(progress=0.55)
        n = build_index(ws, models=self._models, stores=self._stores)
        self._stores.invalidate(ws)
        self._manifest.rebuild(ws)                           # doc_id → hash/status
        job.update(status="succeeded", progress=1.0, detail={"chunks": n})
```

```python
# services/workspaces.py
class WorkspaceService:
    """tenant_id/workspace_id → dizin çözümü + yaşam döngüsü + kota."""
    def __init__(self, settings: Settings): ...

    def resolve(self, tenant_id: str, workspace_id: str) -> Workspace:
        self._validate_slug(tenant_id); self._validate_slug(workspace_id)   # ^[a-z0-9][a-z0-9-]{1,62}$
        root = self._s.data_root / tenant_id / workspace_id
        if not root.is_dir():
            raise WorkspaceNotFound(workspace_id)
        # path-traversal guard: çözümlenen yol data_root altında kalmalı
        if not root.resolve().is_relative_to(self._s.data_root.resolve()):
            raise WorkspaceNotFound(workspace_id)
        return Workspace(root)

    def create(self, tenant_id: str, workspace_id: str) -> Workspace: ...
    def check_quota(self, ws: Workspace, incoming_bytes: int) -> None:      # raises QuotaExceeded → 429/413
        ...
```

Service-level exceptions (`WorkspaceNotFound`, `WorkspaceNotIndexed`, `QuotaExceeded`, `UnsupportedFileType`, `JobNotFound`) live in `services/errors.py`; L3 maps them to HTTP. Services never import fastapi.

**Manifest** (`services/manifest.py`) — the metadata sidecar that makes list/delete/status O(1) instead of LanceDB scans (kills the `tags` 100k-row scan too):

```json
// .doqqy/manifest.json
{
  "version": 1,
  "docs": {
    "processed/erp12/api.md": {
      "source": "raw/erp12/api.pdf",
      "content_hash": "a1b2c3d4e5f60718",
      "tags": ["erp12"],
      "chunks": 34,
      "status": "indexed",              // ingested | chunked | indexed | failed
      "indexed_at": "2026-07-03T10:00:00Z"
    }
  },
  "tags": ["erp12", "billing"],
  "totals": {"docs": 128, "chunks": 4102, "store_bytes": 91234567}
}
```

Written atomically (`tmp file + os.replace`). This is also the Phase-2 incremental-indexing substrate — the API work and the incremental work share it.

---

## 5. L3 — The HTTP surface

### 5.1 App factory & lifespan

```python
# server/app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        deps = build_container(settings)       # ModelManager, StoreManager, services, queue
        deps.models.warmup()                   # readiness bundan sonra yeşil
        app.state.deps = deps
        yield
        await deps.queue.close()

    app = FastAPI(title="doqqy API", version="1.0", lifespan=lifespan)
    app.include_router(query.router,      prefix="/v1")
    app.include_router(documents.router,  prefix="/v1")
    app.include_router(workspaces.router, prefix="/v1")
    app.include_router(maps.router,       prefix="/v1")
    app.include_router(jobs.router,       prefix="/v1")
    app.include_router(meta.router)                       # /healthz /readyz /metrics
    register_error_handlers(app)                          # errors.py → problem+json
    app.add_middleware(RequestContextMiddleware)          # request-id + timing
    return app
```

`build_container` is ~30 lines of manual wiring in `server/deps.py` — explicit object graph, no DI framework.

### 5.2 Wire contract (v1)

Versioned path prefix `/v1`; breaking changes → `/v2`, never in-place.

| Method | Path | Sync? | Purpose |
|---|---|---|---|
| `POST` | `/v1/workspaces` | sync | create workspace |
| `GET` | `/v1/workspaces` | sync | list (tenant-scoped from auth) |
| `DELETE` | `/v1/workspaces/{wid}` | sync | delete (guarded, see §7) |
| `POST` | `/v1/workspaces/{wid}/query` | **sync** | hybrid search — the hot path |
| `POST` | `/v1/workspaces/{wid}/documents` | **202** | multipart upload → ingest job |
| `GET` | `/v1/workspaces/{wid}/documents` | sync | manifest listing (paginated) |
| `DELETE` | `/v1/workspaces/{wid}/documents/{doc_id}` | 202 | remove + incremental de-index |
| `GET` | `/v1/workspaces/{wid}/tags` | sync | from manifest, not a store scan |
| `POST` | `/v1/workspaces/{wid}/maps` | 202 | generate topics map |
| `GET` | `/v1/workspaces/{wid}/maps/latest` | sync | topics.yaml as JSON |
| `GET` | `/v1/jobs/{job_id}` | sync | job status/progress/errors |
| `GET` | `/healthz` `/readyz` `/metrics` | sync | liveness / models-loaded / Prometheus |

Schemas (`server/schemas.py`) — validation is the contract, mirror L1's rules:

```python
class QueryRequest(BaseModel):
    q: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(5, ge=1, le=50)
    tag: str | None = Field(None, pattern=r"^[\w-]+$")
    rerank: bool = True

class HitOut(BaseModel):
    score: float
    doc_id: str
    source: str
    section_path: list[str]
    content: str
    scores: ScoreBreakdown          # dense_rank/sparse_rank/rrf_score/rerank_score

class QueryResponse(BaseModel):
    hits: list[HitOut]
    took_ms: int
    workspace: str

class JobOut(BaseModel):
    id: str; kind: str; status: str; progress: float
    error: str | None = None
    detail: dict = {}
```

Errors: RFC 7807 `application/problem+json`, one handler per service exception:

```json
{ "type": "https://doqqy.dev/errors/workspace-not-indexed",
  "title": "Workspace not indexed", "status": 409,
  "detail": "Run indexing first: POST /v1/workspaces/erp12/documents",
  "request_id": "01J..." }
```

### 5.3 The hot path, end to end

```python
# server/routers/query.py
router = APIRouter(tags=["query"])

@router.post("/workspaces/{workspace_id}/query", response_model=QueryResponse)
async def query(
    workspace_id: str,
    req: QueryRequest,
    principal: Principal = Depends(require_auth),           # tenant kimliği + scopes
    deps: Container = Depends(get_container),
):
    ws = deps.workspaces.resolve(principal.tenant_id, workspace_id)
    deps.limiter.check(principal, "query")                  # token bucket (Redis)
    t0 = time.perf_counter()
    # CPU/GPU-bound sync çağrı → event loop'u bloke etme:
    hits = await run_in_threadpool(
        deps.querying.query, ws, req.q, k=req.top_k, tag=req.tag, rerank=req.rerank
    )
    return QueryResponse(hits=[to_hit_out(h) for h in hits],
                         took_ms=int((time.perf_counter() - t0) * 1000),
                         workspace=workspace_id)
```

Two things that matter operationally: **(1)** `run_in_threadpool` — search is sync and model-bound; calling it directly would freeze the event loop for every concurrent request. **(2)** the rate limiter sits *after* auth (limits are per-tenant, not per-IP; the edge does coarse per-IP limiting separately).

### 5.4 Auth (`server/deps.py`)

v1 = API keys; design for the OIDC upgrade by resolving everything to a `Principal` early:

```python
@dataclass(frozen=True)
class Principal:
    tenant_id: str
    key_id: str
    scopes: frozenset[str]      # "query", "write", "admin"

async def require_auth(authorization: str = Header(...)) -> Principal:
    # "Bearer dq_live_<keyid>_<secret>" → sha256(secret + pepper) ile store'daki hash karşılaştır
    ...
```

- Keys shown once at creation; only `sha256(secret + pepper)` stored (SQLite/Postgres `api_keys` table: key_id, tenant_id, hash, scopes, created_at, revoked_at).
- `doqqy serve` (local mode) runs with `auth_mode=none` and binds `127.0.0.1` — same app, one settings flag.
- Scope check per route: query needs `query`, uploads need `write`, workspace delete needs `admin`.

---

## 6. Deployment & operations

### 6.1 Process topology

```
                        ┌─────────────┐
        TLS, ≤50MB body │   nginx     │  per-IP rate limit, gzip
      ─────────────────►│  (edge)     │
                        └──────┬──────┘
                               │
                ┌──────────────┴──────────────┐
                │   api  (uvicorn, N replicas)│  CPU pods; models resident;
                │   doqqy.server:create_app   │  readiness = warmup done
                └───────┬──────────────┬──────┘
                 query  │              │ enqueue (Redis)
                (sync)  │              ▼
                        │        ┌───────────┐      ┌──────────────────────┐
                        │        │  redis    │◄─────┤ worker (arq, M pods) │
                        │        │ jobs+rate │      │ docling+pandoc+bge-m3│
                        │        └───────────┘      │ GPU preferred        │
                        ▼                           └──────────┬───────────┘
                ┌────────────────────────────────────────────┐ │
                │  /data/tenants/{t}/{w}/   (RWX volume)     │◄┘
                │  raw/ processed/ .doqqy/store.lance        │
                └────────────────────────────────────────────┘
```

- **api** and **worker** are the *same image*, different entrypoints (`uvicorn doqqy.server.app:create_app` vs `arq doqqy.infra.jobs.WorkerSettings`) — one build, one dependency set, mirrors the Software-1 `ENABLED_FEATURES` pattern you already operate.
- **Storage**: workspaces need a shared filesystem across api+workers (NFS/EFS/CephFS, or single-node bind mount to start). LanceDB is file-based — this is the price of its zero-daemon simplicity. Single-writer-per-workspace is guaranteed by routing all writes through the queue with **per-workspace job serialization** (arq job key = workspace root → no two concurrent embeds on one workspace).
- **Scaling knobs**: api replicas scale on CPU/p95 (each holds its own model copy — RAM ≈ 3–4 GB/replica; that's the trade for in-process inference). Workers scale on queue depth. When model RAM × replicas hurts, *then* split inference out to TEI (Text-Embeddings-Inference serves both bge-m3 and the reranker) and api pods become thin — the ModelManager interface is the seam; swap its internals, nothing else moves.

### 6.2 Compose (first deployable cut)

```yaml
# docker-compose.api.yml
services:
  gateway:
    image: nginx:alpine
    ports: ["8080:80"]
    volumes: ["./nginx/api.conf:/etc/nginx/conf.d/default.conf:ro"]
    depends_on: [api]

  api:
    image: doqqy:latest
    command: uvicorn doqqy.server.app:create_app --factory --host 0.0.0.0 --port 8000 --workers 2
    environment:
      DOQQY_DATA_ROOT: /data/tenants
      DOQQY_REDIS_URL: redis://redis:6379/0
      DOQQY_QUEUE_MODE: arq
      DOQQY_DEVICE: cpu
      HF_HOME: /models
    volumes: ["tenants:/data/tenants", "models:/models"]
    depends_on: [redis]
    healthcheck: { test: ["CMD", "curl", "-sf", "http://localhost:8000/readyz"], interval: 15s, start_period: 120s }

  worker:
    image: doqqy:latest
    command: arq doqqy.infra.jobs.WorkerSettings
    environment: { DOQQY_DATA_ROOT: /data/tenants, DOQQY_REDIS_URL: redis://redis:6379/0, HF_HOME: /models }
    volumes: ["tenants:/data/tenants", "models:/models"]
    depends_on: [redis]
    # gpu: uncomment deploy.resources.reservations.devices for CUDA hosts

  redis:
    image: redis:7-alpine
    volumes: ["redisdata:/data"]

volumes: { tenants: {}, models: {}, redisdata: {} }
```

Dockerfile notes: multi-stage; **bake the HF models into a volume or an init step, not the image** (2 GB models + image registry = pain — an `init-models` one-shot service running `ModelManager.warmup()` populates the `models` volume); non-root user; `PYTHONUNBUFFERED=1`.

### 6.3 Worker hardening (ingest parses hostile files)

docling/pymupdf/pandoc process untrusted input in SaaS mode. The worker container is the sandbox:

- no network egress (compose `internal: true` network for workers; models pre-downloaded),
- read-only rootfs except `/data` and `/tmp`,
- memory limit (4–8 GB) + `pids_limit`, CPU quota,
- per-file timeout inside `IngestService` (`asyncio.wait_for` around the parse, file → failed list on timeout — the existing failure-isolation pattern absorbs this naturally).

### 6.4 Observability

- **Logs**: structlog JSON to stdout; every line carries `request_id`, `tenant_id`, `workspace_id`, `job_id`. The edge injects/forwards `X-Request-ID`.
- **Metrics** (`/metrics`, prometheus-client):
  - `doqqy_query_duration_seconds{stage=embed|dense|sparse|rrf|rerank}` — histogram per stage: this is how you find out sparse-scan is your bottleneck *before* customers do,
  - `doqqy_jobs_total{kind,status}`, `doqqy_job_duration_seconds{kind}`, `doqqy_queue_depth`,
  - `doqqy_workspace_chunks{tenant}`, `doqqy_store_bytes{tenant}` (gauge from manifest, scraped cheaply).
- **Tracing**: optional OTel FastAPI instrumentation behind a settings flag — don't block v1 on it.
- **Alerts** (minimum): readiness flapping, queue depth > N for 10 min, job failure rate > 5%, p95 query > 1.5 s.

### 6.5 SLOs to hold yourself to

| Signal | Target |
|---|---|
| Query p95 (warm, ≤10k chunks, rerank on) | < 800 ms |
| Query p95 (`--no-rerank`) | < 250 ms |
| Upload→searchable (1 typical PDF) | < 3 min |
| Readiness after deploy | < 120 s (model load) |
| Availability (api tier) | 99.5% v1 |

---

## 7. Security checklist (v1 gate — don't ship without)

- [ ] Tag/slug/doc_id validation at L3 (pydantic patterns) **and** L1 (ValueError) — the LanceDB `where()` interpolation is reachable only through validated values.
- [ ] Upload guards: extension whitelist, `max_upload_mb`, filename sanitization (`Path(name).name`, reject `..`), stored under server-generated names with original name in manifest.
- [ ] Workspace resolution proves `resolved.is_relative_to(data_root)` (symlink/traversal).
- [ ] API keys hashed+peppered; constant-time compare; revocation honored without restart.
- [ ] Per-tenant rate limits (query + upload separately); edge per-IP limits as backstop.
- [ ] `DELETE /workspaces/{wid}` requires `admin` scope + `?confirm=<workspace_id>` echo — destructive ops don't ride on one keystroke.
- [ ] Workers: no egress, resource-capped, per-file parse timeout.
- [ ] No document content in logs at INFO (chunk text is customer data); DEBUG only, and DEBUG off in prod.
- [ ] CORS: explicit origin allowlist (empty by default; the API is not a browser API until the web UI exists).
- [ ] Dependency audit in CI (`pip-audit`) — docling's dependency tree is large.

---

## 8. Build order (maps to ROADMAP phases)

| Step | Deliverable | Proves |
|---|---|---|
| 1 | `workspace.py` + L1 signature refactor + tag sanitation + reranker-on-GPU; CLI green, unit tests from handover doc | the seam is real |
| 2 | `infra/`: Settings, ModelManager, StoreManager, InProcessQueue | wiring works without HTTP |
| 3 | `doqqy serve` — create_app, query + meta routers only, auth_mode=none, localhost | hot path + lifespan + threadpool model under load (hit it with `hey`/`k6`) |
| 4 | Manifest service + documents GET/DELETE + tags-from-manifest | metadata layer |
| 5 | Upload endpoint + IngestService job body + ArqQueue + worker entrypoint + compose file | the write path, end to end |
| 6 | Auth (API keys) + WorkspaceService tenancy + quotas + rate limits | multi-tenant |
| 7 | Metrics, problem+json polish, worker sandboxing, security checklist pass | operable |

Each step deploys and demos independently; step 3 already delivers the biggest single-user win (resident models — queries go from ~30 s cold to <1 s warm).

---

## 9. Explicit non-goals for v1

- **No LLM synthesis endpoint** — the product promise is verbatim chunks + sources. If ever added, it's a separate opt-in route with its own pricing, never default.
- ~~No shared multi-tenant vector database~~ — **superseded (2026-07): the Qdrant adapter is now a priority deliverable.** The StoreManager seam becomes a `VectorStore` port with LanceDB (local default) and Qdrant (server/SaaS) backends; Qdrant's server-side hybrid fusion and payload multitenancy replace the sparse-scan and shared-FS-search constraints described above. See [VECTOR-STORE-ADAPTERS.md](VECTOR-STORE-ADAPTERS.md).
- **No websocket/SSE job streaming** — polling `GET /v1/jobs/{id}` is fine; add SSE only when a UI demands it.
- **No Celery, no Kubernetes requirement** — arq + compose runs on one box; the topology scales to k8s later without redesign (stateless api, queue-fed workers, RWX volume → PVC).
