# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**doqqy** is a local-first document knowledge system: it ingests PDF/MD/DOCX/TXT into canonical markdown, chunks header-aware, embeds locally with **bge-m3** (dense + sparse), serves hybrid search (dense + sparse → RRF k=60 → **bge-reranker-v2-m3** cross-encoder), and builds a document relationship map via regex + embedding cosine similarity. **It makes no LLM calls** — not for queries, not for map generation. Queries return raw chunks + sources; nothing leaves the machine. Preserve this property: never add network calls or LLM synthesis to the query/map path.

Code comments and log messages are in Turkish; documentation is in English under `docs/` (`ARCHITECTURE.md`, `USAGE.md`, `DEVELOPER-HANDOVER.md` — includes known issues/tech debt, `ROADMAP.md` — API/SaaS analysis, `API-ARCHITECTURE.md` — implementation blueprint for the planned API layer, `VECTOR-STORE-ADAPTERS.md` — priority `VectorStore` port design: LanceDB local default + Qdrant server backend).

## Commands

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .          # installs the `doqqy` CLI (typer app in src/doqqy/cli.py)
```

Pipeline (each stage is an independent, idempotent command — rerun any stage alone):

```powershell
doqqy ingest        # raw/ → processed/ (canonical markdown + YAML frontmatter)
doqqy chunk         # processed/ → .doqqy/chunks/chunks.parquet
doqqy embed         # → .doqqy/store.lance/ (LanceDB, dense + sparse vectors)
doqqy map           # → .doqqy/topics.yaml (Pass 1 regex + Pass 2 cosine; --pass1/--pass2/--threshold/--top-n)
doqqy index         # .doqqy/topics.yaml → processed/INDEX.md (Obsidian entry point)
doqqy inject        # inject [[wikilinks]] into processed/*.md (idempotent marker blocks; --dry-run)
doqqy query "..."   # hybrid search (--top-k, --full, --no-rerank, --tag)
doqqy tags          # list tags in the store
doqqy info          # pipeline state overview
```

There are **no tests and no lint config yet** (MVP). If adding tests, use pytest under `tests/` (see `docs/DEVELOPER-HANDOVER.md` §5 for the expected pattern and ready-made test examples).

**`PROJECT_ROOT` is `Path.cwd()`** (`config.py`) — doqqy operates on whatever directory you run it from. `raw/` is input; `processed/` and all state (`.doqqy/chunks/`, `.doqqy/store.lance/`, `.doqqy/topics.yaml`, `.doqqy/logs/`) live under the cwd and are gitignored. First `doqqy embed` downloads ~2 GB of models from HuggingFace (then cached). `DOQQY_DEVICE` env var overrides CPU/CUDA autodetection.

## Architecture

Pipeline stages map 1:1 to modules in `src/doqqy/`:

- `ingest/` — format-specific parsers dispatched by extension in `router.py`: `.md`/`.txt` → `md_ingest.py`; `.pdf` → docling with pymupdf4llm fallback; `.docx` → pandoc with mammoth fallback. `base.py` defines `Document`, `content_hash`, and `base_metadata` (which derives `tags` from the folder structure under `raw/`: `raw/erp12/faturalama/x.md` → `tags: ["erp12", "faturalama"]`). Output frontmatter records `source`, `type`, `content_hash`, `parser`.
- `chunk.py` — `MarkdownHeaderTextSplitter` on H1–H4, then oversized sections (> ~3200 chars) are split with **atomic blocks**: fenced code and GFM tables are never split; prose is greedy-packed by paragraph. Chunks within a document are linked via `prev_chunk`/`next_chunk` UUIDs.
- `embed.py` — `BAAI/bge-m3` (1024-dim dense + sparse token weights as JSON string), written to LanceDB table `chunks` with `overwrite`. Batch size 4 / max length 1024 are deliberate RAM constraints — don't raise them casually.
- `query.py` — dense LanceDB search + manual Python-side sparse dot product, merged with RRF (k=60), then reranked by `rerank.py` (transformers-based cross-encoder). Returns `SearchHit` list.
- `map_gen.py` — Pass 1 scans `processed/*.md` for explicit references (`bkz.`, `see also`, `[[WikiLink]]`, `(FILE.md)`) → `explicit_related`; Pass 2 computes per-section chunk-vector centroids and cross-file cosine similarity (threshold 0.75, top 5) → `might_be_related`.
- `index_gen.py` / `wikilink_inject.py` — render `.doqqy/topics.yaml` to `INDEX.md` and inject `[[wikilink]]` blocks between `<!-- doqqy:links:start/end -->` markers (previous block is removed on each run; only `processed/` is touched, never `raw/`).
- `config.py` — single source for all paths, model names, thresholds, and tuning constants. Change settings here, not inline.

**Tag filtering:** LanceDB can't run `LIKE`/`IN` on list columns, so tags are also serialized to `tags_str` in `",tag1,tag2,"` form (leading/trailing commas prevent partial matches); `--tag X` filters via `tags_str LIKE '%,X,%'` and applies to dense search, sparse search, and Pass 2 alike. Keep both columns in sync if touching the schema.

## Conventions (see docs/DEVELOPER-HANDOVER.md §1)

- **Format-agnostic core:** after ingest, everything is markdown — chunk/embed/query must never know source formats. Adding a format = new ingester in `ingest/` + entry in `router.py`'s `_DISPATCH` + extension in `config.SUPPORTED_EXTENSIONS` + dependency in `pyproject.toml`; nothing else changes.
- **Idempotency:** every stage must be safely re-runnable (overwrite/rebuild is the default behavior).
- **Failure isolation:** one bad file must not stop a pipeline run — log to `.doqqy/logs/`, continue, report failures in the summary table.
- Use `pathlib.Path` (no `os.path.join`) and always explicit `encoding="utf-8"`.
- CLI commands use typer + rich (panels, progress bars) — match that UX in new commands.
