# Developer Handover

Everything a new maintainer needs: how the code fits together, how to extend it (with working code), the sharp edges I'd want to know about, and how to start testing it.

Read [ARCHITECTURE.md](ARCHITECTURE.md) first for the pipeline mental model. This document is about *working on* the code.

## 1. Ground rules (non-negotiable invariants)

1. **No LLM, no network in the query/map path.** This is the product's core promise ("local-first, transparent"). Embedding, reranking, and map generation run on local CPU/GPU only. Never add an API call to `query.py`, `rerank.py`, or `map_gen.py`.
2. **Format-agnostic core.** After ingest, everything is markdown. `chunk.py`, `embed.py`, `query.py` must never learn about source formats.
3. **Idempotency.** Every stage can be re-run safely; overwrite is the default. New stages must follow this.
4. **Failure isolation.** One bad file never aborts a batch. Log it, count it, keep going, report at the end.
5. **`raw/` is read-only.** Only `processed/` and `.doqqy/` are ever written.
6. **`pathlib.Path` everywhere; explicit `encoding="utf-8"` on every file open.** Windows is a first-class platform here.
7. **Heavy imports stay inside functions** (`FlagEmbedding`, `lancedb`, `torch`, `pandas`) so `doqqy --help` stays instant.
8. **Tuning constants live in `config.py`; paths live on `Workspace`.** No magic numbers inline. `EMBEDDING_BATCH_SIZE=4` and `max_length=1024` are deliberate RAM ceilings — don't raise without a reason. Never reintroduce module-level path constants: every pipeline function takes `ws: Workspace` explicitly.
9. **CLI UX**: typer + rich. New commands print rich Panels/Tables and use the shared Progress-bar pattern (see `chunk_directory` / `router.ingest_directory`).
10. Code comments and log messages are in **Turkish**; keep that consistent within a file.

## 2. Codebase tour — where things live and why

```
src/doqqy/
├── workspace.py        ← START HERE. Workspace(root) frozen dataclass — the single source of
│                          per-corpus paths (raw_dir/processed_dir/state_dir/...), ensure_dirs().
│                          Threaded explicitly through every pipeline function; nothing path-
│                          related is resolved at import time.
├── config.py           ← tuning constants (models, thresholds, batch sizes), device detection,
│                          logger factory + file_log() context manager. Legacy path constants
│                          (PROJECT_ROOT, RAW_DIR, ...) are a DeprecationWarning __getattr__ shim.
├── cli.py              ← typer commands; thin wrappers, no logic. Each command builds
│                          ws = Workspace(Path.cwd()). Windows UTF-8 stdout fix at top.
├── ingest/
│   ├── base.py         ← Document (write() serializes frontmatter+body), IngestResult,
│   │                      IngestError, content_hash, base_metadata (TAG DERIVATION lives here)
│   ├── router.py       ← _DISPATCH {ext → callable}; ingest_directory (batch + failure isolation)
│   ├── md_ingest.py    ← .md + .txt; YAML frontmatter auto-repair (_try_fix_yaml_frontmatter)
│   ├── pdf_ingest.py   ← docling → docling-ocr → pymupdf4llm (optional) chain
│   └── docx_ingest.py  ← pandoc (auto-download!) → mammoth fallback chain
├── chunk.py            ← Chunk dataclass; _atomic_blocks / _pack_blocks / _split_section;
│                          bold-heading → ## normalization (_BOLD_HEADING_RE)
├── embed.py            ← build_index(); tags_str + section_path_str derived columns
├── query.py            ← search(ws, ...); _dense_search / _sparse_search / _rrf; SearchHit;
│                          lru_cache singleton _model() (corpus-independent) + per-workspace
│                          table cache _TABLE_CACHE (keyed by root) with invalidate_table_cache()
├── rerank.py           ← rerank(); lru_cache singleton _load_reranker(); sigmoid over logits
├── map_gen.py          ← generate_map(); _pass1 (regex) / _pass2 (centroid cosine);
│                          section id scheme _section_id = STEM_slug
├── index_gen.py        ← generate_index(); pure topics.yaml → markdown rendering
└── wikilink_inject.py  ← inject_links(); marker-block idempotency (_MARKER_BLOCK_RE)
```

**Data contracts between stages** (change these and you must migrate everything downstream):

- ingest → chunk: frontmatter keys `source`, `type`, `tags` (read in `chunk_file`).
- chunk → embed: `chunks.parquet` columns = `Chunk` dataclass fields.
- embed → query/map: LanceDB schema (see ARCHITECTURE §2.3), especially `vector`, `sparse_vector` (JSON string!), `tags_str` format `",a,b,"`.
- map → index/inject: `topics.yaml` structure `{sections: [{id, file, section, explicit_related?, might_be_related?}]}`; `target_id` is parsed by `wikilink_inject` as `stem = target_id.split("_")[0]` — the `STEM_slug` id scheme is load-bearing.

## 3. Extension recipes

### 3.1 Add a new input format (e.g. HTML)

Three touch points; the rest of the pipeline is untouched by design.

**1) New ingester** — `src/doqqy/ingest/html_ingest.py`:

```python
"""HTML ingester'ı: markdownify ile."""
from __future__ import annotations

from pathlib import Path

from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash, processed_path_for
from doqqy.workspace import Workspace


def ingest_html(source: Path, ws: Workspace) -> Document:
    try:
        from markdownify import markdownify  # noqa: PLC0415 — heavy import inside function
    except ImportError as exc:
        raise IngestError("markdownify gerekli: pip install markdownify") from exc

    try:
        html = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        html = source.read_text(encoding="latin-1")

    md = markdownify(html, heading_style="ATX")
    if not md.strip():
        raise IngestError("boş içerik")

    meta = base_metadata(source, ws.root, kind="html")
    meta["content_hash"] = content_hash(md)
    return Document(source.resolve(), processed_path_for(source, ws), md, meta)
```

Every ingester takes `(source, ws)`; the shared `processed_path_for` helper in `base.py` maps `raw/…` to the mirrored `processed/…` path.

**2) Register in the router** — `src/doqqy/ingest/router.py`:

```python
from doqqy.ingest.html_ingest import ingest_html

_DISPATCH: dict[str, Callable[[Path, Workspace], Document]] = {
    # ... existing ...
    ".html": ingest_html,
    ".htm": ingest_html,
}
```

**3) Whitelist the extension** — `src/doqqy/config.py`:

```python
SUPPORTED_EXTENSIONS: frozenset[str] = frozenset(
    {".md", ".markdown", ".pdf", ".docx", ".txt", ".html", ".htm"}
)
```

Add the dependency to `pyproject.toml`, `pip install -e .`, done. Follow the fallback-chain pattern from `pdf_ingest.py` if there are two viable parsers.

### 3.2 Add a new CLI command

Pattern: thin typer wrapper, heavy import inside, rich output.

```python
@app.command()
def stats() -> None:
    """Chunk istatistikleri."""
    import pandas as pd

    ws = Workspace(Path.cwd())
    if not ws.chunks_parquet.exists():
        console.print("[red]chunks.parquet yok — önce `doqqy chunk`.[/red]", err=True)
        raise typer.Exit(1)

    df = pd.read_parquet(ws.chunks_parquet)
    t = Table(title="Chunk istatistikleri", box=box.ROUNDED)
    t.add_column("Metrik", style="bold"); t.add_column("Değer")
    t.add_row("Toplam chunk", str(len(df)))
    t.add_row("Ortalama karakter", f"{df['char_count'].mean():.0f}")
    t.add_row("Doküman sayısı", str(df["doc_id"].nunique()))
    console.print(t)
```

### 3.3 Context expansion (use the prev/next links that already exist)

`prev_chunk` / `next_chunk` are stored but unused. To return neighboring chunks with each hit:

```python
# in query.py
def expand_context(hit: SearchHit) -> str:
    """Hit'in önceki/sonraki chunk'larını içeriğe ekle."""
    table = _table()
    parts = [hit.content]
    for key, position in (("prev_chunk", 0), ("next_chunk", None)):
        cid = hit.extra.get(key)
        if not cid:
            continue
        rows = table.search().where(f"chunk_id = '{cid}'").limit(1).to_list()
        if rows:
            parts.insert(position, rows[0]["content"]) if position == 0 else parts.append(rows[0]["content"])
    return "\n\n— · —\n\n".join(parts)
```

(You'll need to add `prev_chunk`/`next_chunk` into `SearchHit.extra` in `search()` — they're in the LanceDB row already.)

### 3.4 Swap the embedding model

```python
# config.py
EMBEDDING_MODEL: str = "BAAI/bge-m3"   # change model id
EMBEDDING_DIM: int = 1024              # MUST match the new model's output dim
```

If the replacement is not a bge-m3-family model, `embed.py:_load_model` and `query.py:_model` both construct `BGEM3FlagModel` — replace with e.g. sentence-transformers **in both places**, and decide what to do about sparse vectors (bge-m3's lexical weights are what powers the sparse leg; a dense-only model degrades hybrid search to dense+RRF-of-one-list). Then `doqqy embed` to rebuild.

### 3.5 True token-based chunk sizing

Current sizing is `chars / 4 ≈ tokens`. For exact budgets:

```python
# chunk.py
from functools import lru_cache

@lru_cache(maxsize=1)
def _tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained("BAAI/bge-m3")

def _tok_len(text: str) -> int:
    return len(_tokenizer().encode(text, add_special_tokens=False))
```

Then use `_tok_len` instead of `len` in `_split_section` / `_pack_blocks` (and pass max tokens, not max chars). Costs one tokenizer load + slower chunking; only worth it if you see truncation at embed time.

## 4. Known issues, gotchas, and tech debt

Ordered roughly by how likely they are to bite you.

1. **`_sparse_search` is a full-table scan per query** (`query.py`). It pulls every (tag-filtered) row into pandas and computes dot products in a Python loop with `iterrows()`. Fine at ~10k chunks; painful at 100k. Fix directions: precompute a token→chunk inverted index at embed time; or vectorize with scipy sparse matrices; or move to a store with native sparse support. Same pattern in `cli.py:tags` (`.limit(100000).to_pandas()`).
2. **Tag values are interpolated into LanceDB SQL unescaped** — `where(f"tags_str LIKE '%,{filter_tag},%'")` in `query.py` and `map_gen.py`. Harmless for a local CLI where the user owns the data, but **must be sanitized/parameterized before any API/SaaS exposure** (a tag like `x',` breaks the query; folder names become filter payloads).
3. ~~**`PROJECT_ROOT = Path.cwd()` is evaluated at import time** (`config.py`).~~ **Fixed (issue #5, July 2026)** by the `Workspace` refactor: paths are now an explicit `Workspace(root)` object threaded through the pipeline, nothing is resolved at import time, and one process can serve multiple corpora (the `_table` lru_cache singleton is gone too — table handles are per-workspace). Library consumers construct `Workspace(some_path)` directly; the old `config.PROJECT_ROOT`-style names still work from cwd via a `DeprecationWarning` shim and will be removed once nothing imports them.
4. **Embed is all-or-nothing** — `build_index` drops and recreates the table. `content_hash` is already stored in frontmatter precisely to enable incremental updates (planned, not built). Changing one document currently costs a full re-embed.
5. ~~**The reranker always runs on CPU**~~ — **Fixed (issue #8).** `rerank.py` now calls `detect_device()` and moves both model and input tensors to the detected device. Optional fp16 via `DOQQY_RERANKER_FP16=1` (default off). CPU path is unchanged on machines without CUDA.
6. ~~**`map_gen._parse_sections` frontmatter skip is a hack**~~ **Fixed (July 2026)** by replacing the `"in_fm" in dir()` check with a proper boolean `in_fm = False` initialized before the loop. It also only skips frontmatter when the *very first line* is `---`.
7. **Pass 2 section↔chunk matching is heuristic** (`map_gen._pass2`): a chunk belongs to a section if the source filenames match and the heading text appears in `" > ".join(section_path)` — substring containment, so heading "API" also matches "API Keys". Duplicate heading texts across a file collapse into one centroid. Good enough in practice; know it's fuzzy.
8. ~~**`chunk.py` reads tags from frontmatter written by ingest**~~ **Fixed (July 2026)** by validating/coercing string tags in `chunk_file` to a single-element list, checking that lists contain only strings, and warning + falling back to `[]` for other types.
9. ~~**`_normalize_target` in Pass 1 is prefix-tolerant both ways**~~ **Fixed (July 2026)** by sorting `known_files` before matching (prioritizing exact matches, then shortest filename, then alphabetical order) to ensure reference matching is deterministic.
10. ~~**Unused config**~~ **Fixed (July 2026)** by removing `CHUNK_OVERLAP` and `CHUNK_MIN_MERGE_TOKENS` from `config.py` and `chunk.py`.
11. **Windows specifics**: `cli.py` reconfigures stdout/stderr to UTF-8 (Turkish characters under cp1252); `doc_id` normalizes backslashes to `/`. Keep both behaviors when refactoring.
12. ~~**The repo root contains `pandoc-3.9.0.2-windows-x86_64.msi` (~40 MB)**~~ **Fixed (#12)** by removing the binary from the working tree. Note: Existing Git history was kept intact to avoid breaking active clones/branches, so the ~40 MB blob remains in historical pack files (git clone size is unchanged).
13. ~~**`pyproject.toml` readme field points at the deleted `memory-bank/`**~~ **Fixed (#12)** by pointing `readme` directly to `README.md`.

## 5. Testing [IMPLEMENTED]

Tests live under `tests/` (pytest; install with `pip install -e ".[dev]"`). Current coverage: `tests/test_workspace.py` (Workspace paths + the multi-corpus/B2 isolation regression tests), `tests/test_chunk.py`, `tests/test_rrf.py`, `tests/test_tags.py`, and per-format ingester tests under `tests/unit/ingest/`. Ingester tests take a `ws` fixture (`Workspace(tmp_path)`) — no `monkeypatch` of config paths, no `chdir`. The examples below are the original plan and now exist in the suite:

**Unit tests, pure functions first** (no models, no I/O — fast):

```python
# tests/test_chunk.py
from doqqy.chunk import _atomic_blocks, _pack_blocks, _split_section

def test_code_block_never_split():
    md = "Para 1.\n\n```python\nfor x in range(10):\n    print(x)\n```\n\nPara 2."
    blocks = _atomic_blocks(md)
    code = next(b for b in blocks if b.startswith("```"))
    assert "for x in range(10)" in code and "print(x)" in code

def test_table_never_split():
    md = "| a | b |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |\n"
    assert any(b.count("|") >= 8 for b in _atomic_blocks(md))

def test_long_section_splits_within_budget():
    long = "Paragraf.\n\n" * 500
    chunks = _split_section(long)
    assert len(chunks) > 1
    assert all(len(c) <= 3200 + 100 for c in chunks)

def test_oversized_single_block_is_own_chunk():
    giant = "```\n" + "x = 1\n" * 2000 + "```"
    chunks = _pack_blocks([giant, "small"], max_chars=3200)
    assert chunks[0].startswith("```")
```

```python
# tests/test_rrf.py
from doqqy.query import _rrf

def test_rrf_rewards_presence_in_both_lists():
    dense = [{"chunk_id": "a"}, {"chunk_id": "b"}]
    sparse = [{"chunk_id": "b"}, {"chunk_id": "c"}]
    fused = _rrf(dense, sparse)
    assert fused[0]["chunk_id"] == "b"          # in both lists → top
    assert {r["chunk_id"] for r in fused} == {"a", "b", "c"}
```

```python
# tests/test_tags.py
from pathlib import Path
from doqqy.ingest.base import base_metadata

def test_folder_structure_becomes_tags(tmp_path):
    meta = base_metadata(Path("raw/erp12/billing/api.md"), tmp_path, kind="md")
    assert meta["tags"] == ["erp12", "billing"]

def test_root_file_has_no_tags(tmp_path):
    meta = base_metadata(Path("raw/readme.md"), tmp_path, kind="md")
    assert meta["tags"] == []
```

Also easily unit-testable: `wikilink_inject._strip_marker_block` (idempotency!), `map_gen._slug` / `_section_id` / `_normalize_target`, `md_ingest._try_fix_yaml_frontmatter`.

**Integration tests** (mark `slow`; require model download): tiny fixture corpus in `tests/fixtures/raw/` → run ingest→chunk→embed→query against `Workspace(tmp_path)`, assert a known string is retrieved. No `chdir` needed anywhere — the `Workspace` refactor (§4.3) removed the import-time cwd dependency, so tests just construct a workspace and pass it in.

```powershell
pip install -e ".[dev]"
pytest tests/ -v -m "not slow"
```

**Linter and Formatting**: We use **Ruff** as our official linter and formatter, with the ruleset configured in `pyproject.toml`. The standard line length is set to 140 characters to prevent unwanted code wraps during markdown data processing, inline queries, and dense data structures.

Before committing, make sure to run the check locally to keep the codebase clean:
```bash
ruff check .
```

To automatically fix safe violations (such as import sorting errors): 
```bash
ruff check . --fix
```

## 6. Release / versioning

- Version lives only in src/doqqy/__init__.py. pyproject.toml reads it via [tool.setuptools.dynamic] version = { attr = "doqqy.__version__" }, so bump the one place.
- **Continuous Integration (CI):** We have a fully automated CI workflow configured in GitHub Actions (`.github/workflows/ci.yml`). 
  - Every `push` and `pull_request` on target branches triggers the pipeline.
  - Tests are run against a matrix of both **Ubuntu** (`ubuntu-latest`) and **Windows** (`windows-latest`) to ensure absolute cross-platform compatibility (supporting pathing differences).
  - The pipeline runs `ruff check .` and unit tests (`pytest -m "not slow"`) to avoid downloading heavy ML embedding models (~2GB) inside the runner.
- Dependencies are floor-pinned (`>=`); `docling` is the heaviest and most volatile — pin tighter if a release breaks PDF parsing.
