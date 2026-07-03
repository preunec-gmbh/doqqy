# TODO — Ingest support for HTML, XLSX, CSV, XML

Small feature: four new input formats for `doqqy ingest`. The pipeline after ingest (chunk/embed/query/map) is format-agnostic and needs **zero changes** — each format is just a new parser. Follow the recipe in [docs/DEVELOPER-HANDOVER.md](docs/DEVELOPER-HANDOVER.md) §3.1; match the existing patterns (failure isolation via `IngestError`, `base_metadata` + `content_hash`, heavy imports inside functions, `encoding="utf-8"` with latin-1 fallback).

## 1. HTML (`.html`, `.htm`) — `src/doqqy/ingest/html_ingest.py`

- [ ] Create `html_ingest.py` with `ingest_html(source: Path) -> Document`
- [ ] Pre-clean with BeautifulSoup: drop `<script>`, `<style>`, `<nav>`, `<header>`, `<footer>`, comments (boilerplate poisons embeddings)
- [ ] Convert with `markdownify` (`heading_style="ATX"`) so H1–H4 survive → header-aware chunking works
- [ ] Encoding: try `utf-8`, fall back to `latin-1` (same pattern as `md_ingest.py`)
- [ ] Raise `IngestError("boş içerik")` when conversion yields nothing
- [ ] `meta = base_metadata(..., kind="html")`; set `parser` field (`markdownify`)

## 2. XLSX (`.xlsx`) — `src/doqqy/ingest/xlsx_ingest.py`

- [ ] Create `xlsx_ingest.py` with `ingest_xlsx(source: Path) -> Document`
- [ ] Read with `pandas.read_excel(sheet_name=None)` (openpyxl engine) → one `## <sheet name>` section per sheet
- [ ] Render sheets as GFM tables (`df.to_markdown(index=False)` — needs `tabulate`)
- [ ] **Split big sheets into table blocks of ≤ ~40 rows, repeating the header row per block.** Chunking treats tables as atomic and never splits them — a 10k-row sheet would otherwise become one giant chunk that exceeds the embedder's 1024-token window
- [ ] Skip empty sheets; stringify NaN as empty; guard against merged-cell weirdness (openpyxl returns None)
- [ ] `kind="xlsx"`, `parser="pandas"`; `IngestError` if all sheets empty

## 3. CSV (`.csv`) — `src/doqqy/ingest/csv_ingest.py`

- [ ] Create `csv_ingest.py` with `ingest_csv(source: Path) -> Document`
- [ ] Sniff delimiter with `csv.Sniffer` (Turkish exports are often `;`-separated); fall back to `,`
- [ ] Encoding: `utf-8` → `latin-1` fallback (cp1254 exports)
- [ ] `pandas.read_csv` → H1 from filename (like `ingest_txt`) + GFM table
- [ ] Same ≤ ~40-row table-block splitting as XLSX (share a `_df_to_md_blocks()` helper between the two modules — put it in `xlsx_ingest.py` or a small `tabular.py`)
- [ ] `kind="csv"`, `parser="pandas"`

## 4. XML (`.xml`) — `src/doqqy/ingest/xml_ingest.py`

- [ ] Create `xml_ingest.py` with `ingest_xml(source: Path) -> Document`
- [ ] Parse with stdlib `xml.etree.ElementTree` (no new dependency); `IngestError` on parse failure
- [ ] v1 approach (keep it simple, mirrors `.txt`): H1 from filename + pretty-printed XML inside a fenced ```` ```xml ```` block — the fence keeps it atomic in chunking, and bge-m3's sparse leg still matches tag/attribute/text tokens
- [ ] Extract and prepend plain-text content of leaf nodes as a "İçerik özeti" section so dense embeddings get natural language, not just markup *(optional — decide during implementation)*
- [ ] `kind="xml"`, `parser="etree"`

## 5. Wiring (one edit each — see DEVELOPER-HANDOVER §3.1)

- [ ] `src/doqqy/ingest/router.py`: add `.html`, `.htm`, `.xlsx`, `.csv`, `.xml` → parser entries to `_DISPATCH`
- [ ] `src/doqqy/config.py`: add the five extensions to `SUPPORTED_EXTENSIONS`
- [ ] `pyproject.toml`: add `markdownify`, `beautifulsoup4`, `openpyxl`, `tabulate` (pandas is already a dependency); bump version `0.1.6 → 0.2.0`; run `pip install -e .`

## 6. Tests (`tests/unit/ingest/`)

- [ ] `test_html_ingest.py`: script/style stripped; headings become `#`; empty page → `IngestError`
- [ ] `test_xlsx_ingest.py`: multi-sheet → one section per sheet; 200-row sheet → multiple ≤40-row table blocks each with header row
- [ ] `test_csv_ingest.py`: `;`-delimited + `,`-delimited both parse; latin-1 file doesn't crash
- [ ] `test_xml_ingest.py`: valid XML → fenced block; malformed XML → `IngestError`
- [ ] `test_router.py`: each new extension dispatches to the right parser; unsupported extension still raises

## 7. Docs & bookkeeping

- [ ] `README.md`: supported-format mentions (intro sentence, quick start comment, status list) + project-tree entries for the new ingest files
- [ ] `docs/ARCHITECTURE.md`: parser table in §2.1 + module map
- [ ] `docs/USAGE.md`: §1 requirements + `doqqy ingest` section
- [ ] `CLAUDE.md`: ingest bullet in the Architecture section
- [ ] `docs/ROADMAP.md`: update ranked item #10 (HTML/PPTX/XLSX ingesters) — mark HTML/XLSX/CSV/XML done, leave PPTX

## 8. Acceptance

- [ ] `doqqy ingest` on a folder mixing all 9 formats: zero crashes, failures (if any) isolated in the summary table
- [ ] `doqqy chunk && doqqy embed && doqqy query "<something from the xlsx>"` returns the table chunk with correct source path
- [ ] A `raw/<tag>/file.csv` gets its folder tag and is filterable via `doqqy query --tag <tag>`
- [ ] Re-running ingest is idempotent (same `content_hash` → identical output files)
