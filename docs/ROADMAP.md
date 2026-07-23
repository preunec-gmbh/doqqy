# Roadmap & Future-Feature Analysis

An engineering analysis of where doqqy can go: what the codebase already supports well, what blocks each direction, and a prioritized path — with special focus on **an API layer as the base for a SaaS offering**.

## 0. Current state, honestly assessed

**Strengths to build on**

- Clean stage separation with stable data contracts (parquet, LanceDB schema, topics.yaml) — stages can be lifted into services without rewriting logic.
- The retrieval quality stack is already "production-grade RAG": hybrid dense+sparse, RRF, cross-encoder rerank. Most SaaS competitors ship less.
- Failure isolation and idempotency are already the culture — exactly what job-queue workers need.
- Tag system is a primitive but real **tenancy/partition mechanism** (filter pushed down to the store).
- No LLM dependency = no per-query marginal API cost. A doqqy SaaS's unit economics are compute-only.

**Structural blockers (must fix before any server/SaaS work)**

| # | Blocker | Where | Why it blocks |
|---|---|---|---|
| B1 | ✅ **Fixed (issue #5)** — ~~`PROJECT_ROOT = Path.cwd()` resolved at import time~~ paths now come from an explicit `Workspace(root)` | `workspace.py` | A server process must serve *many* corpora; paths must be per-request, not per-process |
| B2 | ✅ **Fixed (issue #5)** — ~~`lru_cache` singletons for store table (`_table`)~~ table handles are per-workspace (`_TABLE_CACHE` keyed by root) | `query.py` | Caches one corpus's table handle forever — wrong corpus after the first request |
| B3 | ✅ **Fixed (issue #7)** — ~~Unsanitized string interpolation into LanceDB `where()`~~ | `query.py`, `map_gen.py` | Injection surface the moment input comes from a network |
| B4 | Full-table rebuild on embed; full-table scan on sparse search | `embed.py`, `query.py` | Per-upload re-embedding cost and per-query latency both scale with corpus size |
| B5 | No auth, no user model, no quotas | everywhere | Table stakes for multi-tenant |

None of these are deep — B1/B2 are a one-week refactor, B3 is an afternoon.

## 1. Phase 1 — The `Workspace` refactor (enabler for everything)

> **Status: shipped (issue #5, July 2026).** `workspace.py` exists as sketched below, every pipeline function takes `ws: Workspace`, the CLI builds `Workspace(Path.cwd())`, table handles are per-workspace, and legacy `config` path constants survive only as a `DeprecationWarning` shim. The reranker-to-GPU item below is still open.

Replace module-level path constants with an explicit workspace object. This is the single highest-leverage change in the codebase.

```python
# doqqy/workspace.py (new)
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
```

Then thread it through: `ingest_directory(ws)`, `chunk_directory(ws)`, `build_index(ws)`, `search(ws, query, ...)`. The CLI constructs `Workspace(Path.cwd())` — behavior unchanged for users. Models (bge-m3, reranker) stay process-global singletons (they're corpus-independent); **table handles become per-workspace** (an LRU dict keyed by root path).

Also in this phase:
- **B3 fix**: validate tags against `^[\w-]+$` (they're folder names — this is safe) before interpolation.
- ~~**Reranker on GPU**~~ (`model.to(detect_device())`) — **Shipped (issue #8).** Free 5–10× rerank speedup on CUDA boxes; fp32 default, fp16 opt-in via `DOQQY_RERANKER_FP16=1`.
- Tests (the handover doc's plan) — the refactor is the forcing function.

## 2. Phase 2 — Incremental indexing (the most-requested missing feature)

Already planned in the README ("Planlanan: inkremental update"); the groundwork exists: every processed file carries `content_hash`.

Design:

1. **Manifest** `.doqqy/manifest.json`: `{doc_id: {content_hash, chunk_ids, embedded_at}}` written by each stage.
2. `doqqy ingest` skips files whose raw mtime+size are unchanged (fast path) and whose regenerated `content_hash` is unchanged (correct path).
3. `doqqy chunk --changed` re-chunks only docs whose hash changed; parquet becomes append/replace-by-doc.
4. `doqqy embed --changed` uses LanceDB `delete(f"doc_id = '{d}'")` + `add(new_rows)` instead of drop-and-recreate.
5. `doqqy sync` = the whole chain in one command; add `doqqy watch` (watchfiles) for live folders.

Payoff: adding one document to a 10k-chunk corpus goes from ~20 CPU-minutes to seconds. **This matters double for SaaS** — per-upload cost is the dominant compute expense.

## 3. Phase 3 — API layer (the SaaS base)

### 3.1 Shape: FastAPI service over the same core

The CLI stays; the API is a second head on the same body. Read path first (query is stateless and fast once models are warm), write path second (ingest/embed become background jobs).

```python
# doqqy/server/app.py (sketch)
from fastapi import FastAPI, Depends, HTTPException, UploadFile, BackgroundTasks
from pydantic import BaseModel, Field

from doqqy.workspace import Workspace
from doqqy.query import search

app = FastAPI(title="doqqy API", version="0.1")

class QueryRequest(BaseModel):
    q: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(5, ge=1, le=50)
    tag: str | None = Field(None, pattern=r"^[\w-]+$")   # B3: validated at the edge
    rerank: bool = True

class Hit(BaseModel):
    score: float
    doc_id: str
    source: str
    section_path: list[str]
    content: str
    scores: dict   # dense_rank / sparse_rank / rrf_score / rerank_score

def get_workspace(workspace_id: str) -> Workspace:
    ws = registry.lookup(workspace_id)          # tenant → path resolution
    if ws is None:
        raise HTTPException(404, "workspace not found")
    return ws

@app.post("/v1/workspaces/{workspace_id}/query", response_model=list[Hit])
def query(workspace_id: str, req: QueryRequest, ws: Workspace = Depends(get_workspace)):
    hits = search(ws, req.q, k=req.top_k, rerank=req.rerank, tag=req.tag)
    return [Hit(score=h.score, doc_id=h.doc_id, source=h.source,
                section_path=h.section_path, content=h.content, scores=h.extra)
            for h in hits]

@app.post("/v1/workspaces/{workspace_id}/documents", status_code=202)
async def upload(workspace_id: str, file: UploadFile, bg: BackgroundTasks,
                 ws: Workspace = Depends(get_workspace)):
    dest = ws.raw_dir / file.filename            # + path-traversal guard, size limit, ext whitelist
    dest.write_bytes(await file.read())
    job_id = jobs.enqueue("ingest_embed", workspace=ws.root, path=dest)
    return {"job_id": job_id}
```

**Endpoint surface (v1):**

| Method & path | Maps to | Notes |
|---|---|---|
| `POST /v1/workspaces/{id}/query` | `query.search` | sync, warm-model, target p95 < 500 ms |
| `POST /v1/workspaces/{id}/documents` | ingest+chunk+embed | 202 + job id; async pipeline |
| `GET /v1/workspaces/{id}/documents` | manifest | list docs, hashes, status |
| `DELETE /v1/workspaces/{id}/documents/{doc_id}` | incremental delete | needs Phase 2 |
| `GET /v1/workspaces/{id}/tags` | `cli.tags` logic | replace the 100k-row scan with a manifest read |
| `POST /v1/workspaces/{id}/map` | `generate_map` | async job; returns topics.yaml as JSON |
| `GET /v1/jobs/{job_id}` | job store | status/progress/errors (IngestResult maps directly) |
| `GET /v1/healthz`, `/v1/readyz` | — | readiness = models loaded |

**Why the model server matters:** today every CLI invocation pays ~20–60 s of model load. A resident server amortizes it to zero — the API isn't just a SaaS enabler, it's a **10–100× UX improvement for single users** (`doqqy serve` + a thin client mode for the CLI). Ship `doqqy serve` as a local feature first; it de-risks the whole API layer with zero tenancy complexity.

### 3.2 Multi-tenancy model

The corpus-per-directory design maps cleanly onto tenancy — a workspace *is* a directory:

```
/data/tenants/{tenant_id}/{workspace_id}/
├── raw/  processed/  .doqqy/
```

| Concern | v1 (pragmatic) | Later (scale) |
|---|---|---|
| Isolation | Directory per workspace; LanceDB store per workspace (strong isolation for free, no noisy-neighbor index) | Shared vector DB (Qdrant/pgvector/LanceDB Cloud) with tenant column + row-level filters, if per-tenant stores get too numerous |
| Auth | API keys (hashed, per-tenant), `Authorization: Bearer` | OAuth/OIDC, org/member roles |
| Quotas | Per-tenant: max docs, max storage MB, queries/min (slowapi / Redis token bucket) | Metered billing (Stripe usage records on query + embed-seconds) |
| Job queue | One GPU worker consuming `ingest_embed` jobs (arq or RQ on Redis) | Worker pool, priority queues, per-tenant fairness |
| File safety | Extension whitelist, size caps, path-traversal guard, MIME sniff | AV scan hook; sandboxed parser workers (docling/pandoc parse untrusted input — run them in a container with no network, resource-limited) |

**Parser sandboxing deserves emphasis:** in SaaS mode, docling/pymupdf/pandoc process *hostile* files. Run ingest workers in locked-down containers (read-only FS except workdir, no network, memory/CPU caps, timeout per file). doqqy's failure-isolation pattern already treats parser crashes as data, which is exactly right.

### 3.3 Deployment shape

```
                   ┌────────────────────┐
  clients ────────►│  API (FastAPI)     │  stateless, CPU, N replicas
                   │  auth/quota/valid. │
                   └───────┬──────┬─────┘
                           │      │ enqueue
                    query  │      ▼
                           │   ┌──────────────┐     ┌─────────────────┐
                           │   │ Redis (jobs) │◄────┤ ingest workers  │  GPU/CPU,
                           │   └──────────────┘     │ (docling sandbox│  autoscale on
                           ▼                        │  + bge-m3)      │  queue depth
                   ┌────────────────────┐           └─────────────────┘
                   │ query workers      │
                   │ (bge-m3 + reranker │  GPU preferred; models resident
                   │  resident)         │
                   └───────┬────────────┘
                           ▼
                   /data/tenants/... (NFS/EBS)  or  managed vector DB
```

Two model-serving options: (a) keep models **in-process** in query workers (simplest, current code works as-is); (b) split embedding/rerank into a dedicated inference service (HF **Text-Embeddings-Inference** serves both bge-m3 and bge-reranker-v2-m3) — better GPU utilization once there are multiple API replicas. Start with (a).

### 3.4 What SaaS does NOT change

The no-LLM query path stays. That's the differentiator: *"your documents never leave our compute, no third-party AI processes them, answers are verbatim excerpts with sources."* For the privacy-sensitive segment (legal, medical, ERP consultancies — note the existing `erp12` corpora), that's the pitch. An optional LLM answer-synthesis layer can exist later as a clearly-separated, opt-in add-on (the `[llm]` extra already reserves the dependency slot).

## 4. Adjacent feature opportunities (ranked)

| Rank | Feature | Effort | Why |
|---|---|---|---|
| 1 | **Vector-store adapter port + Qdrant backend** | M | **Priority decision (2026-07).** Pluggable `VectorStore` port; LanceDB stays the local default, Qdrant becomes the server/SaaS backend: native sparse vectors + server-side RRF kill the O(N) sparse scan, structured filters kill the injection surface, payload multitenancy replaces shared-FS search. Full design: [VECTOR-STORE-ADAPTERS.md](VECTOR-STORE-ADAPTERS.md) |
| 2 | **`doqqy serve` + thin-client CLI** | S | Kills the per-invocation model-load; prerequisite knowledge for the API anyway |
| 3 | **Incremental indexing / `doqqy sync` / `doqqy watch`** | M | Biggest current UX pain; biggest SaaS cost lever (Phase 2); trivial on Qdrant (`upsert`/`delete_by_doc`) |
| 4 | ✅ **Shipped** — **MCP server** (`doqqy mcp`) | S | Expose `query`/`tags`/`info` as MCP tools → any AI agent (Claude Code, IDEs) can search the corpus locally. Very cheap: wraps the same `search()` — and turns doqqy into "the local RAG backend for agents", a category with real pull right now |
| 5 | **Context expansion at query time** | S | `prev_chunk`/`next_chunk` already stored and unused; `--context 1` flag returns neighbors |
| 6 | **OCR fallback for scanned PDFs** | M | Today scanned PDFs fail; docling has OCR support (EasyOCR/Tesseract) behind options — currently the biggest ingest gap |
| 7 | **Retrieval eval harness** | M | A `tests/eval/` set of (query, expected-doc) pairs + recall@k / MRR script — otherwise threshold/model changes (0.75 cosine, RRF k=60) are vibes-based. Also the backend-parity gate for LanceDB vs Qdrant |
| 8 | **Web UI** | M | Local FastAPI + single-page search UI over the API from Phase 3; also the SaaS front-end seed |
| 9 | **Dedup by `content_hash`** | S | Same doc in two folders currently embeds twice; hash is already computed |
| 10 | **PPTX ingester** | S | Recipe documented in the handover; docling natively handles PPTX; (HTML, XLSX, CSV, and XML ingesters are completed) |
| 11 | **ColBERT reranking leg** | L | bge-m3 can emit ColBERT vectors (`return_colbert_vecs`) — a third retrieval signal; only worth it after the eval harness exists to prove it |

(The former "sparse-search scalability via custom inverted index" item is dropped — the Qdrant adapter solves it properly; the LanceDB backend keeps the current scan, acceptable for local corpus sizes.)

## 5. Suggested sequencing

```
Phase 1   Workspace refactor + VectorStore port + LanceDB adapter (logic move)
          + injection fix + reranker-on-GPU + unit tests                          (~1–2 weeks)
Phase 1.5 Qdrant adapter + `doqqy migrate-store` + backend parity checks          (~1 week)
Phase 2   Incremental indexing (manifest, sync, watch) + dedup                    (~1–2 weeks)
Phase 3a  doqqy serve (local API, single workspace) + thin CLI client + MCP server (~1 week)
Phase 3b  Multi-workspace API + auth + upload jobs + quotas — Qdrant as prod
          backend  ← first SaaS-able cut                                          (~3–4 weeks)
Phase 4   Web UI, billing, parser sandboxing hardening, eval harness, OCR
```

Adapter design, Qdrant schema, and migration tooling: [VECTOR-STORE-ADAPTERS.md](VECTOR-STORE-ADAPTERS.md).

Each phase is independently shippable and none breaks the local-first CLI story — the CLI remains the free, offline core; the API/SaaS is the same engine with tenancy around it.
