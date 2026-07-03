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
8. **Config lives in `config.py`.** No magic numbers inline. `EMBEDDING_BATCH_SIZE=4` and `max_length=1024` are deliberate RAM ceilings — don't raise without a reason.
9. **CLI UX**: typer + rich. New commands print rich Panels/Tables and use the shared Progress-bar pattern (see `chunk_directory` / `router.ingest_directory`).
10. Code comments and log messages are in **Turkish**; keep that consistent within a file.

## 2. Codebase tour — where things live and why

```
src/doqqy/
├── config.py           ← START HERE. All paths, constants, device detection, logger factory.
│                          PROJECT_ROOT = Path.cwd() — evaluated at import time!
├── cli.py              ← typer commands; thin wrappers, no logic. Windows UTF-8 stdout fix at top.
├── ingest/
│   ├── base.py         ← Document (write() serializes frontmatter+body), IngestResult,
│   │                      IngestError, content_hash, base_metadata (TAG DERIVATION lives here)
│   ├── router.py       ← _DISPATCH {ext → callable}; ingest_directory (batch + failure isolation)
│   ├── md_ingest.py    ← .md + .txt; YAML frontmatter auto-repair (_try_fix_yaml_frontmatter)
│   ├── pdf_ingest.py   ← docling → pymupdf4llm fallback chain
│   └── docx_ingest.py  ← pandoc (auto-download!) → mammoth fallback chain
├── chunk.py            ← Chunk dataclass; _atomic_blocks / _pack_blocks / _split_section;
│                          bold-heading → ## normalization (_BOLD_HEADING_RE)
├── embed.py            ← build_index(); tags_str + section_path_str derived columns
├── query.py            ← search(); _dense_search / _sparse_search / _rrf; SearchHit;
│                          lru_cache singletons _model() and _table()
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

from doqqy.config import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR
from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash


def _processed_path(source: Path) -> Path:
    try:
        rel = source.resolve().relative_to(RAW_DIR.resolve())
    except ValueError:
        rel = Path(source.name)
    return (PROCESSED_DIR / rel).with_suffix(".md")


def ingest_html(source: Path) -> Document:
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

    meta = base_metadata(source, PROJECT_ROOT, kind="html")
    meta["content_hash"] = content_hash(md)
    return Document(source.resolve(), _processed_path(source), md, meta)
```

**2) Register in the router** — `src/doqqy/ingest/router.py`:

```python
from doqqy.ingest.html_ingest import ingest_html

_DISPATCH: dict[str, Callable[[Path], Document]] = {
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
    from doqqy.config import CHUNKS_PARQUET

    if not CHUNKS_PARQUET.exists():
        console.print("[red]chunks.parquet yok — önce `doqqy chunk`.[/red]", err=True)
        raise typer.Exit(1)

    df = pd.read_parquet(CHUNKS_PARQUET)
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
3. **`PROJECT_ROOT = Path.cwd()` is evaluated at import time** (`config.py`). Library consumers must `os.chdir()` *before* importing any doqqy module. This is the single biggest refactor needed for a server/API version (a request can't switch corpora). See ROADMAP §API for the `Workspace` refactor sketch.
4. **Embed is all-or-nothing** — `build_index` drops and recreates the table. `content_hash` is already stored in frontmatter precisely to enable incremental updates (planned, not built). Changing one document currently costs a full re-embed.
5. **The reranker always runs on CPU** — `rerank.py` never calls `model.to(device)` and doesn't use `detect_device()`. Easy win: move model + inputs to CUDA when available.
6. **`map_gen._parse_sections` frontmatter skip is a hack** — it uses `"in_fm" in dir()` to test whether a local variable exists. It works, but it's fragile and unidiomatic; if you touch this function, replace with a proper boolean initialized before the loop. It also only skips frontmatter when the *very first line* is `---`.
7. **Pass 2 section↔chunk matching is heuristic** (`map_gen._pass2`): a chunk belongs to a section if the source filenames match and the heading text appears in `" > ".join(section_path)` — substring containment, so heading "API" also matches "API Keys". Duplicate heading texts across a file collapse into one centroid. Good enough in practice; know it's fuzzy.
8. **`chunk.py` reads tags from frontmatter written by ingest** — if a user hand-writes files into `processed/` without `tags`, they get `[]` (fine), but if they write `tags: "erp12"` (string, not list) it flows through as a string and `tags_str` becomes `",e,r,p,1,2,"` at embed time (`','.join("erp12")`). Validate or coerce in `chunk_file` if this becomes a support issue.
9. **`_normalize_target` in Pass 1 is prefix-tolerant both ways** — `AUTH` matches `AUTHENTICATION.md` *and* `AUTH.md`; first match in set-iteration order wins (nondeterministic across runs). Sort `known_files` before matching if you need determinism.
10. **Unused config**: `CHUNK_OVERLAP`, `CHUNK_MIN_MERGE_TOKENS` are declared but not implemented. Don't assume overlap exists.
11. **Windows specifics**: `cli.py` reconfigures stdout/stderr to UTF-8 (Turkish characters under cp1252); `doc_id` normalizes backslashes to `/`. Keep both behaviors when refactoring.
12. **The repo root contains `pandoc-3.9.0.2-windows-x86_64.msi` (~40 MB)** — an installer artifact that predates the `pypandoc.download_pandoc()` auto-install. It's committed to git; consider removing it from history if repo size matters.
13. **`pyproject.toml` readme field points at the deleted `memory-bank/`** — `readme = { text = "Bkz. memory-bank/", ... }`; harmless but stale, point it at `README.md` when touching packaging. (The README itself was rewritten in English in July 2026 and no longer references memory-bank.)

## 5. Testing (none exists — here's the plan)

There are **no tests today** (MVP). Highest-value order:

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

**Integration tests** (mark `slow`; require model download): tiny fixture corpus in `tests/fixtures/raw/` → run ingest→chunk→embed→query in a `tmp_path` with `monkeypatch.chdir`, assert a known string is retrieved. Note the `PROJECT_ROOT`-at-import-time issue (§4.3): tests must chdir before importing doqqy modules, or you refactor config first (recommended — make tests the forcing function).

```powershell
pip install pytest
pytest tests/ -v -m "not slow"
```

**No linter is configured.** Suggested: `ruff` (the codebase already carries `# noqa: BLE001, PLC0415` markers in ruff's vocabulary — someone ran it locally without committing config). Add `[tool.ruff]` to `pyproject.toml`.

## 6. Release / versioning

- Version lives in `pyproject.toml` (`0.1.6`) and `src/doqqy/__init__.py`. Keep them in sync when bumping.
- No CI, no publishing pipeline — installs are `pip install -e .` from source.
- Dependencies are floor-pinned (`>=`); `docling` is the heaviest and most volatile — pin tighter if a release breaks PDF parsing.
