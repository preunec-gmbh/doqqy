# Architecture

How doqqy works internally: the pipeline, the data models, the storage schema, and the reasoning behind the design.

## 1. High-level view

```
┌──────────┐  doqqy ingest  ┌─────────────┐  doqqy chunk  ┌──────────────────────┐
│  raw/    │ ─────────────► │ processed/  │ ────────────► │ .doqqy/chunks/       │
│ .pdf .md │ format-specific│ canonical   │  header-aware │ chunks.parquet       │
│ .docx    │ parsers        │ .md + front-│  splitting    │ (pandas DataFrame)   │
│ .txt     │                │ matter      │               │                      │
└──────────┘                └─────────────┘               └──────────┬───────────┘
                                                                     │
                                                              doqqy embed
                                                                     ▼
                                                          ┌──────────────────────┐
                                                          │ .doqqy/store.lance/  │
                                                          │ table "chunks"       │
                                                          │ dense + sparse + meta│
                                                          └──────┬───────────────┘
                              ┌──────────────────────────────────┤
                              │                                  │
                         doqqy map                        doqqy query "..."
                              ▼                                  ▼
                    ┌────────────────────┐             ┌────────────────────┐
                    │ .doqqy/topics.yaml │             │ dense + sparse     │
                    │ explicit_related   │             │ → RRF → reranker   │
                    │ might_be_related   │             │ → top-k SearchHits │
                    └───────┬────────────┘             └────────────────────┘
                            │
                 doqqy index │ doqqy inject
                            ▼
                    ┌────────────────────┐
                    │ processed/INDEX.md │
                    │ processed/*.md     │
                    │ + [[wikilinks]]    │
                    └────────────────────┘
```

**Key idea:** every stage is an independent, deterministic, idempotent command. Re-running `doqqy chunk` after a chunking-config change does not require re-ingesting; a full rebuild is simply the commands in sequence. Every stage writes its output with overwrite semantics.

**Root resolution:** all paths come from an explicit `Workspace(root)` object (`workspace.py`, frozen dataclass) threaded through every pipeline function — there are no module-level path constants and nothing is resolved at import time. The CLI constructs `Workspace(Path.cwd())` per command, so doqqy still behaves as a "per-corpus tool" like git: one working directory = one corpus. All state lives under `<root>/.doqqy/`; inputs in `<root>/raw/`; canonical markdown in `<root>/processed/`. Because the workspace is explicit, one process can serve multiple corpora concurrently (the enabler for `doqqy serve` and the API layer — see ROADMAP §1). The legacy `config.PROJECT_ROOT`/`RAW_DIR`/... names still resolve (from cwd, at access time) via a deprecation shim but warn `DeprecationWarning`.

## 2. Stage-by-stage

### 2.1 Ingest (`doqqy ingest`) — `src/doqqy/ingest/`

Converts every supported file under `raw/` into canonical markdown under `processed/` (same relative path, `.md` extension), with a YAML frontmatter header.

**Dispatch** (`router.py`):

| Extension | Primary parser | Fallback | Notes |
|---|---|---|---|
| `.md`, `.markdown` | `python-frontmatter` | — | Original frontmatter preserved as `original_<key>`; broken YAML (unquoted colons in `title:`/`project:`/`team:`) auto-repaired by `_try_fix_yaml_frontmatter` |
| `.txt` | UTF-8 read, body wrapped in a fenced code block | latin-1 on `UnicodeDecodeError` | Filename becomes the H1 title |
| `.pdf` | **docling** (layout-aware) | **pymupdf4llm** (fast, simple) | Empty output → `IngestError` ("scanned PDF?") |
| `.docx` | **pandoc** via pypandoc (GFM output, `--wrap=none`) | **mammoth** (pure Python) | Missing pandoc binary triggers `pypandoc.download_pandoc()` auto-install; if that fails, mammoth |
| `.xml` | `xml.etree.ElementTree` | — | Pretty-printed XML inside a fenced block, extracts leaf nodes text to a content summary section |
| `.html`, `.htm` | `BeautifulSoup` + `markdownify` | Encoding auto-detected from BOM / `<meta charset>` (UnicodeDammit) | Drops boilerplate (`<script>`, `<style>`, `<nav>`, `<aside>`, `<form>`, `<iframe>`, `<noscript>`, `<svg>`, comments); `<header>`/`<footer>` removed only outside `<article>`/`<section>`/`<main>`; `<title>` → frontmatter `title` and fallback H1 when body has none; ATX headers |
| `.xlsx` | `pandas` + `openpyxl` | – | Reads sheets, renders as GFM tables, and splits sheets into blocks of ≤40 rows with repeated headers |
| `.csv` | `pandas` | Encoding fallback (`cp1254`, `latin-1`) | Supports different delimiters, converts tabular data into GFM tables, and splits rows into blocks with repeated headers |

**Failure isolation:** one bad file never stops the run. `ingest_directory()` catches per-file exceptions, logs to `.doqqy/logs/ingest.log`, collects `(path, error)` pairs in `IngestResult.failed`, and the CLI prints a summary panel.

**Frontmatter written by ingest** (`base.py:base_metadata`):

```yaml
---
source: raw/erp12/faturalama/api.md   # relative original path
type: pdf                             # md / pdf / html / docx / txt / xml / xlsx / csv
tags: [erp12, faturalama]             # derived from folder structure under raw/
ingested_at: "2026-07-03T00:14:00+00:00"
content_hash: a1b2c3d4e5f60718        # first 16 hex of SHA-256(body)
parser: docling                       # pdf/docx only: which parser succeeded
original_title: "..."                 # any original frontmatter, prefixed
---
```

`tags` are **positional**: `raw/<tag1>/<tag2>/file.pdf → ["tag1", "tag2"]`. Files directly under `raw/` get no tags. This is the entire multi-corpus mechanism — there is no separate registry.

### 2.2 Chunk (`doqqy chunk`) — `src/doqqy/chunk.py`

`processed/**/*.md` → `.doqqy/chunks/chunks.parquet`, one row per `Chunk`.

Algorithm per file (`chunk_file`):

1. Split frontmatter from body (`python-frontmatter`).
2. **Bold-heading normalization**: lines that are entirely bold (`**A224. Meeting**` / `__Title__`) are rewritten to `## Title` — Word documents often use bold instead of Heading styles, and this recovers section structure from them.
3. `MarkdownHeaderTextSplitter` (langchain) splits on H1–H4, `strip_headers=False` so heading text stays inside the chunk for embedding context. A headerless document becomes one section.
4. Sections longer than `_MAX_CHARS` (= `CHUNK_MAX_TOKENS * 4` = 3200 chars, ~800 tokens at ~4 chars/token) are sub-split with **atomic blocks**:
   - Fenced code blocks (```` ``` … ``` ````) and GFM tables (regex-detected) are **never split** — a half SQL query is worthless.
   - Remaining prose is split on blank lines (`\n{2,}`).
   - Blocks are **greedy-packed** back together up to `_MAX_CHARS`; an oversized single block (giant code block) becomes its own chunk.
5. Chunks within a document are linked via `prev_chunk` / `next_chunk` UUIDs (context-expansion hook, currently unused by query).

```python
@dataclass
class Chunk:
    chunk_id: str              # UUID4
    doc_id: str                # processed/.../foo.md (relative, forward slashes)
    source: str                # raw/.../foo.pdf (from frontmatter)
    doc_type: str              # md / pdf / docx / txt
    content: str               # chunk text, heading included
    tags: list[str]            # folder-derived tags
    section_path: list[str]    # ["1. Auth", "1.2 JWT"]
    char_count: int
    prev_chunk: str | None
    next_chunk: str | None
```

`CHUNK_OVERLAP` and `CHUNK_MIN_MERGE_TOKENS` exist in config but are **not implemented yet** (no overlap, no short-section merging).

### 2.3 Embed (`doqqy embed`) — `src/doqqy/embed.py`

`chunks.parquet` → pluggable `VectorStore` adapter (defaulting to LanceDB table `chunks` in `.doqqy/store.lance/`).

1. `BAAI/bge-m3` is loaded through `FlagEmbedding.BGEM3FlagModel`. Device auto-detected (`detect_device()`: `DOQQY_DEVICE` env override → `torch.cuda.is_available()` → CPU). fp16 on CUDA.
2. Each batch (`EMBEDDING_BATCH_SIZE = 4`, `max_length=1024` — deliberate RAM constraints for consumer machines) is encoded with `return_dense=True, return_sparse=True`.
3. Dense vectors: `float32[1024]`. Sparse vectors: token-id → weight dicts, normalized to `dict[int, float]` at the port level.
4. Table is dropped and recreated (`store.recreate(dim)`) and records are upserted (`store.upsert(records)`).

Two derived columns are added by the LanceDB adapter at write time:

- `section_path_str` — `"H1 > H2 > H3"` for display.
- `tags_str` — `",tag1,tag2,"` (note leading/trailing commas). LanceDB cannot run SQL `LIKE`/`IN` against `list<string>` columns, so tags are also serialized to a delimited string; the comma-wrapping makes `LIKE '%,erp12,%'` an **exact** tag match (prevents `bulut` matching `bulut-saha`). **If you touch the schema, keep `tags` and `tags_str` in sync.**

**LanceDB schema** (table `chunks`):

| Column | Type | Notes |
|---|---|---|
| `chunk_id` | string | UUID, primary key by convention |
| `doc_id`, `source`, `doc_type` | string | |
| `tags` | list\<string\> | original list |
| `tags_str` | string | `",a,b,"` — for SQL LIKE filtering |
| `content` | string | full chunk text |
| `section_path` | list\<string\> | |
| `section_path_str` | string | display form |
| `char_count` | int64 | |
| `prev_chunk`, `next_chunk` | string \| null | |
| `vector` | fixed_size_list\<float32, 1024\> | bge-m3 dense |
| `sparse_vector` | string (JSON) | bge-m3 lexical weights |

### 2.4 Query (`doqqy query`) — `src/doqqy/query.py` + `src/doqqy/rerank.py`

The retrieval pipeline, end to end:

```
query text
   │  _embed_query()  (bge-m3, cached via lru_cache)
   ├──► dense vec (1024) ──► VectorStore hybrid search ────────┐
   └──► sparse weights ───► (client-side or server-side RRF)  ├─► fused list
                                                               │       │
                                                                   top 50 fused
                                                                               │
                                                         bge-reranker-v2-m3 (cross-encoder,
                                                         sigmoid(logit), batch 4, max_len 512)
                                                                               │
                                                                         top-k SearchHits
```

- **Pluggable Vector Store Search**: `query.py` delegates retrieval to `store.hybrid_search(...)` which returns RRF-fused results.
- **LanceDB Adapter Path**:
  - **Dense**: `table.search(qvec).metric("cosine").limit(limit)`; score = `1 - distance`. Tag filter applied as a `where()` clause.
  - **Sparse**: computed client-side by loading the tag-filtered table into pandas and computing `Σ query_weight[tok] * chunk_weight[tok]` per chunk in Python.
  - **RRF**: per chunk_id, `score += 1/(60 + rank)` for each list it appears in; also records `dense_rank` / `sparse_rank` for the UI.
- **Rerank** (`rerank.py`): `AutoModelForSequenceClassification` over `(query, content)` pairs; scores squashed with sigmoid; top-k returned. `--no-rerank` skips this and returns RRF order. The reranker uses `detect_device()` (same as the embedder) and runs on CUDA when available — set `DOQQY_DEVICE=cpu` to force CPU. Optional fp16 on CUDA via `DOQQY_RERANKER_FP16=1` (default off — fp32 is safe across all hardware).
- Result type:

```python
@dataclass
class SearchHit:
    score: float               # rerank_score (or rrf_score with --no-rerank)
    doc_id: str
    source: str
    section_path: list[str]
    content: str
    extra: dict                # chunk_id, doc_type, dense_rank, sparse_rank, rrf_score, rerank_score
```

The embedding model is an `@lru_cache(maxsize=1)` process-global singleton (it's corpus-independent) — first query in a process pays the model-load cost, subsequent ones don't. Table handles are cached per workspace and automatically invalidated within the `LanceDBStore` adapter class when updates occur.

### 2.5 Map (`doqqy map`) — `src/doqqy/map_gen.py`

Builds `.doqqy/topics.yaml`, a section-level relationship graph. Two independent passes, **zero LLM calls**:

**Pass 1 — regex, explicit references.** Each `processed/*.md` is parsed into sections (`#`–`####`). Section bodies are scanned for:

- `bkz. FOO` / `bkz: FOO` (Turkish "see")
- `see section FOO` / `see also FOO`
- `(FILE.md)` parenthesized filenames
- `[[WikiLink]]`

Matches are normalized against the set of known processed filenames (case-insensitive, `.md`-suffix tolerant, prefix-tolerant both ways). Output: `explicit_related` with the source line number — these are *certain* links.

**Pass 2 — embedding cosine, thematic neighbors.** All chunk vectors are pulled from LanceDB into memory. For each section, the mean of its chunks' dense vectors (matched by source filename + heading containment against `section_path`) is L2-normalized into a **section centroid**. Cosine similarity is computed between centroids of *different files*; neighbors above `MAP_COSINE_THRESHOLD` (0.75) are kept, top `MAP_TOP_N_NEIGHBORS` (5) per section. Output: `might_be_related` with scores — these are *probabilistic* links. `--tag` restricts Pass 2 to one corpus.

Section IDs are `FILENAME_slug-of-heading` (uppercase stem + slugified heading). Only sections with at least one link are written (noise reduction).

```yaml
# .doqqy/topics.yaml
sections:
  - id: SEQUENCE_odeme-akisi
    file: SEQUENCE.md
    section: "## Ödeme Akışı"
    explicit_related:
      - target_id: PRISMA
        source_line: 42
    might_be_related:
      - target_id: PRISMA_payment-model
        target_section: "## Payment Model"
        score: 0.8312
```

### 2.6 Index (`doqqy index`) — `src/doqqy/index_gen.py`

Renders `.doqqy/topics.yaml` as `processed/INDEX.md`: grouped by file → section, each link shown as 📌 (explicit) or 💡 (thematic, with score). Intended as the entry point of an Obsidian vault opened on `processed/`.

### 2.7 Inject (`doqqy inject`) — `src/doqqy/wikilink_inject.py`

Writes a marker-delimited link block at the end of each `processed/*.md`:

```markdown
<!-- doqqy:links:start -->
## Bağlantılar

### 📌 Explicit Referanslar
- [[SEQUENCE]]

### 🔗 Tematik Bağlantılar
- [[PRISMA]] → Payment Model (0.83)
<!-- doqqy:links:end -->
```

**Idempotent**: each run strips any previous marker block (regex on the marker pair) before appending the fresh one, so repeated runs converge. Only `processed/` is ever modified — `raw/` is read-only by design. Links are file-level (section slugs are collapsed to the filename stem), deduplicated, thematic sorted by score. Obsidian turns the `[[...]]` links into graph-view edges automatically.

## 3. Module map

```
src/doqqy/
├── __init__.py            # version
├── __main__.py            # python -m doqqy → cli.app
├── cli.py                 # typer app: ingest/chunk/embed/query/map/index/inject/tags/info
│                          #   also: Windows stdout→UTF-8 reconfigure (Turkish chars)
├── workspace.py           # Workspace(root): frozen dataclass, SINGLE source of per-corpus paths + ensure_dirs
├── config.py              # tuning constants (models, thresholds, batch sizes), device detect, logger factory
│                          #   legacy path constants live on as a DeprecationWarning __getattr__ shim
├── chunk.py               # header-aware splitting + atomic-block packing
├── embed.py               # bge-m3 encode + LanceDB write (overwrite)
├── query.py               # hybrid search: dense + sparse → RRF → rerank; SearchHit
├── rerank.py              # bge-reranker-v2-m3 cross-encoder (transformers, CPU)
├── map_gen.py             # Pass 1 regex + Pass 2 cosine → topics.yaml
├── index_gen.py           # topics.yaml → INDEX.md
├── wikilink_inject.py     # topics.yaml → [[wikilink]] marker blocks in processed/*.md
└── ingest/
    ├── base.py            # Document, IngestResult, IngestError, content_hash, base_metadata (tags!)
    ├── md_ingest.py       # .md (frontmatter + YAML auto-repair) and .txt (code-block wrap)
    ├── pdf_ingest.py      # docling → pymupdf4llm fallback
    ├── docx_ingest.py     # pandoc (auto-download) → mammoth fallback
    └── router.py          # extension dispatch + batch ingest with failure isolation
```

Heavy imports (`FlagEmbedding`, `lancedb`, `torch`, `pandas`) are done **inside functions**, not at module top — `doqqy --help` stays fast.

## 4. Design decisions

| Decision | Rationale |
|---|---|
| Every stage is an independent command | Re-run one stage after a config change without a full rebuild |
| Format-specific parsers, format-agnostic everything else | New format = one new ingester file + two registrations; chunk/embed/query untouched |
| Header-aware chunking | Section boundaries are semantic boundaries; splitting mid-section destroys context |
| Code blocks & tables atomic | Half a SQL query is two useless halves |
| `prev_chunk`/`next_chunk` links | Ready-made hook for context expansion around a hit |
| No LLM in map generation | Embeddings already encode thematic proximity; an LLM adds cost, latency, and an external dependency for no precision gain |
| No LLM in query answers | Users want to *understand the document*, not a paraphrase; raw chunk + source is transparent, free, instant |
| Local-first embedding + reranking | Zero network dependency at query time; privacy by construction |
| LanceDB (serverless, file-based) | Portable, no daemon, `.doqqy/` can be zipped and moved |
| Two-pass map (regex + cosine) | Certain links and probabilistic links are different animals — kept in separate, separately-inspectable categories |
| `tags_str = ",a,b,"` serialization | LanceDB can't filter list columns; comma-wrapping makes LIKE an exact-match |
| Batch size 4 / max_length 1024 | Deliberate RAM ceiling for consumer laptops — do not raise casually |

## 5. Performance profile

| Operation | Expectation |
|---|---|
| Ingest, 500 mixed pages | 15–30 min (docling dominates) |
| Chunk | < 1 min |
| Embed (CPU) | 15–30 min |
| Embed (CUDA) | 2–3 min |
| Single query, warm process | < 1 s |
| Single query, cold process | model load (tens of seconds) + query |
| First ever `doqqy embed` | one-time ~2 GB HuggingFace model download |

The dominant scaling risk is `_sparse_search` (full-table scan per query) and Pass 2 (all vectors in memory) — fine up to tens of thousands of chunks, a problem beyond that. See ROADMAP §performance.
