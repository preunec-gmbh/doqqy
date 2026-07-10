# doqqy

Local-first document knowledge system. Ingests PDF, Markdown, DOCX and TXT files, splits them into header-aware chunks, generates local embeddings with **bge-m3** (dense + sparse), and serves instant natural-language search via hybrid retrieval with **bge-reranker-v2-m3** cross-encoder reranking. It also builds an automatic cross-document relationship map (`.doqqy/topics.yaml` + `INDEX.md`) from bge-m3 embedding cosine similarity.

It makes **no LLM calls** — not for queries, not for map generation. Queries return raw chunks + sources; the map is built with pure embedding math. Nothing leaves your machine.

## Quick start

```powershell
# 1. Dependencies
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .

# 2. Put documents under raw/ (PDF, MD, DOCX, TXT, XML, CSV)
#    Folder structure automatically becomes tags: raw/project-a/... → tag: "project-a"

# 3. Pipeline
doqqy ingest        # raw/ → processed/ (canonical markdown)
doqqy chunk         # processed/ → chunks.parquet
doqqy embed         # → .doqqy/store.lance/  (bge-m3 dense + sparse vectors)

# 4. Build the map
doqqy map           # processed/*.md → .doqqy/topics.yaml (regex + embedding cosine)
doqqy index         # .doqqy/topics.yaml → processed/INDEX.md
doqqy inject        # inject [[wikilinks]] into processed/*.md (Obsidian graph view)

# 5. Ask
doqqy query "how does JWT refresh work?"
doqqy query "PayTR refund flow" --top-k 10
doqqy query "refund process" --tag erp12     # search only the erp12 folder
doqqy tags                                   # which tags exist?
doqqy info                                   # pipeline state overview
```

The first `doqqy embed` downloads ~2 GB of models from HuggingFace (one-time; cached afterwards). Everything after that runs fully offline.

## Project structure

```
doqqy/
├── README.md                # this file — start here
├── pyproject.toml           # package + dependencies
├── .env.example             # optional env vars (HF cache dir, reserved LLM keys)
│
├── raw/                     # INPUT — your original files (gitignored, never modified)
├── processed/               # STAGE 1 OUTPUT — canonical markdown (gitignored)
├── .doqqy/                  # STATE (gitignored)
│   ├── chunks/chunks.parquet    # STAGE 2 — chunk records
│   ├── store.lance/             # STAGE 3 — LanceDB vector store
│   ├── topics.yaml              # STAGE 4 — relationship map
│   └── logs/                    # ingest error logs
│
├── src/doqqy/               # SOURCE CODE
│   ├── cli.py               # typer commands
│   ├── config.py            # paths, constants, RAM/model settings
│   ├── chunk.py             # header-aware chunking
│   ├── embed.py             # bge-m3 dense+sparse → LanceDB
│   ├── query.py             # hybrid search (dense + sparse) + RRF fusion
│   ├── rerank.py            # bge-reranker-v2-m3 (cross-encoder)
│   ├── map_gen.py           # Pass 1 (regex) + Pass 2 (cosine) → topics.yaml
│   ├── index_gen.py         # topics.yaml → INDEX.md
│   ├── wikilink_inject.py   # topics.yaml → [[wikilinks]] in processed/*.md
│   └── ingest/              # format-specific parsers
│       ├── base.py          # Document, IngestResult, content_hash, tag derivation
│       ├── router.py        # extension → parser dispatch + batch ingest (failure-isolated)
│       ├── md_ingest.py     # .md (frontmatter + YAML auto-repair) and .txt
│       ├── pdf_ingest.py    # docling → pymupdf4llm fallback
│       ├── docx_ingest.py   # pandoc (auto-download) → mammoth fallback
│       ├── xml_ingest.py    # etree (stdlib)
│       └── csv_ingest.py    # pandas (delimiter detection, encoding fallback, Markdown tables, row-blocking)
│
└── docs/                    # TECHNICAL DOCS
    ├── ARCHITECTURE.md          # pipeline internals, LanceDB schema, design decisions
    ├── USAGE.md                 # full CLI reference, workflows, Python API, FAQ
    ├── DEVELOPER-HANDOVER.md    # codebase tour, extension recipes, known issues, test plan
    ├── ROADMAP.md               # future features: API layer, SaaS path, priorities
    ├── API-ARCHITECTURE.md      # implementation blueprint for the planned API layer
    └── VECTOR-STORE-ADAPTERS.md # PRIORITY: VectorStore port — LanceDB local + Qdrant server backend
```

## Documentation

- **Architecture & data flow:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **CLI reference + workflows + Python API:** [docs/USAGE.md](docs/USAGE.md)
- **Maintainer handover (extension recipes, known issues):** [docs/DEVELOPER-HANDOVER.md](docs/DEVELOPER-HANDOVER.md)
- **Roadmap & SaaS analysis:** [docs/ROADMAP.md](docs/ROADMAP.md)
- **API layer blueprint:** [docs/API-ARCHITECTURE.md](docs/API-ARCHITECTURE.md)
- **Vector store adapters (Qdrant priority):** [docs/VECTOR-STORE-ADAPTERS.md](docs/VECTOR-STORE-ADAPTERS.md)

## Current status

Phases 1–5 complete. Shipped features:

- ✅ Ingest: `.md`, `.txt`, `.pdf` (docling + pymupdf4llm fallback), `.docx` (pandoc + mammoth fallback), `.xml` (etree), `.csv` (pandas with delimiter detection and encoding fallback)
- ✅ Header-aware chunking (code blocks and tables kept atomic; Word bold-heading recovery)
- ✅ bge-m3 dense + sparse embeddings → LanceDB
- ✅ RAM-constrained defaults (embedding batch size 4 / max length 1024)
- ✅ Hybrid search: dense + sparse (Python-side dot product) + RRF fusion (k=60)
- ✅ bge-reranker-v2-m3 cross-encoder reranking (transformers-based)
- ✅ Map generation: Pass 1 (regex explicit references) + Pass 2 (embedding cosine thematic neighbors) → `.doqqy/topics.yaml`
- ✅ `INDEX.md` generation — Obsidian vault entry point
- ✅ Wikilink injection: `topics.yaml` → `[[links]]` in `processed/*.md` (idempotent, `doqqy inject`)
- ✅ Multi-corpus / tag filtering: automatic tags from `raw/` folder structure; isolated search via `doqqy query --tag` and `doqqy map --tag`
- ✅ Typer CLI with Rich UI: `ingest`, `chunk`, `embed`, `map`, `index`, `query`, `inject`, `tags`, `info`

## Roadmap (prioritized)

1. 🎯 **Vector-store adapter port + Qdrant backend** — pluggable `VectorStore` interface; LanceDB stays the zero-daemon local default, Qdrant becomes the server/SaaS backend (native sparse vectors, server-side RRF fusion, payload multitenancy). Design: [docs/VECTOR-STORE-ADAPTERS.md](docs/VECTOR-STORE-ADAPTERS.md)
2. `doqqy serve` — resident-model local API (queries go from ~30 s cold start to <1 s)
3. Incremental indexing (`doqqy sync` / `doqqy watch`) — only reprocess changed files
4. MCP server — expose search to AI agents (Claude Code, IDEs)
5. Multi-tenant REST API — the SaaS-able cut. Blueprint: [docs/API-ARCHITECTURE.md](docs/API-ARCHITECTURE.md)

Full analysis and sequencing: [docs/ROADMAP.md](docs/ROADMAP.md).

## License / Privacy

Local-first: at query time **no** data is sent to the internet. Embedding, reranking, and map generation run entirely on your local CPU/GPU. There are no external API calls.
