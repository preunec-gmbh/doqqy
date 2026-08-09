# Retrieval Eval Fixture

Ground-truth corpus and query set for the doqqy retrieval eval harness (#15). This directory contains no harness code — only the fixture data it consumes:

```
tests/eval/
├── corpus/raw/    # eval-only doqqy input tree (fed to `doqqy ingest`)
└── queries.yaml   # (query, expected doc, expected section) ground truth
```

## Corpus layout

`corpus/raw/` is a self-contained doqqy `raw/` tree, structured exactly like a real one: tags are derived from folder path.

```
corpus/raw/
├── erp/
│   ├── faturalama/   → tags: [erp, faturalama]
│   └── stok/         → tags: [erp, stok]
└── hr/
    └── izin/         → tags: [hr, izin]
```

All content is fictional: a made-up company, "Nova Ticaret A.Ş.", with a fictional UK subsidiary "Nova Trading UK Ltd" used for the English-language documents. Nothing here is copied from a real source, a customer document, or scraped from the web — this repo is public and every file in `corpus/` must stay that way. If you add a document, write it yourself; don't paste in real policy text or documentation, even paraphrased.

The corpus deliberately exercises specific chunker/embedder behavior, not just "some markdown files":

- **Header nesting** — several docs use H1 through H4 (see `erp/faturalama/e-fatura-entegrasyon-tr.md` for H4 subsections under an H3).
- **Atomic blocks** — `erp/faturalama/e-fatura-entegrasyon-tr.md` and `erp/stok/barkod-entegrasyonu-tr.md` each contain a fenced code block; `erp/faturalama/kdv-hesaplama-tr.md`, `erp/stok/minimum-stok-seviyesi-tr.md`, and `hr/izin/yillik-izin-hesaplama-tr.md` each contain a GFM table. These must never be split mid-block by the chunker.
- **Multi-chunk documents** — `erp/faturalama/e-fatura-entegrasyon-tr.md` and `hr/izin/mesai-politikasi-en.md` are long, multi-section documents that split into several chunks.
- **Bilingual coverage** — Turkish and English documents throughout, including two same-topic TR/EN pairs with deliberately different specifics (currency, day thresholds, role names) so a query can only match the correct language variant:
  - invoice cancellation: `erp/faturalama/fatura-iptal-sureci-tr.md` (TRY, Bölge Müdürü/Genel Müdür) vs. `erp/faturalama/invoice-cancellation-en.md` (GBP, Regional Manager/Finance Director)
  - annual leave request: `hr/izin/izin-sureci-tr.md` (3 business days, manager-only approval) vs. `hr/izin/leave-process-en.md` (5 business days, manager + HR approval)

`hr/izin/mesai-politikasi-en.md` (overtime policy, English content despite the Turkish filename) is deliberately filed under `izin` rather than a separate `mesai`/overtime tag folder: it exists specifically as the near-topic distractor for the TOIL-vs-annual-leave-forfeiture `hard_rerank` query in `queries.yaml`, which depends on both documents sharing the `hr`/`izin` tags. Don't take it as the pattern for "which folder does a new HR document go in" — a genuinely new HR topic should get its own tag folder.

## queries.yaml

Each entry is a `(query, expected_doc_id[, expected_section])` pair plus an optional `tag_filter`, a `category`, and a `reason` explaining what retrieval behavior it targets: exact-term (sparse should win), paraphrase (dense should win), hard/rerank-dependent (a near-duplicate-topic doc competes for top-1), tag-filtered, and cross-lingual (TR query → EN doc or vice versa).

**`expected_doc_id` is not a path relative to `raw/`, it's the literal `Chunk.doc_id`.** `chunk.py` sets `doc_id` from the ingested frontmatter `source` field, which keeps the `raw/` prefix (workspace-root-relative), so `tests/eval/corpus/raw/erp/faturalama/x.md` produces `Chunk.doc_id == "raw/erp/faturalama/x.md"` — and that `raw/`-prefixed form is exactly what every `expected_doc_id` in `queries.yaml` uses. #15 should compare against `Chunk.doc_id` with plain string equality; no path rewriting.

**`tag_filter`** is optional and, where present, is an AND constraint over every listed tag (see `TagFilter` in `infra/vectorstore/base.py`) — not an OR. A single-element filter like `["erp"]` is intentional in some entries, testing that the parent tag matches chunks under either child tag folder; it is not a typo for the two-element form.

**Section-matching contract**: `expected_section`, where present, must be the literal text of a Markdown heading in the target document, or a *list* of such headings — but the harness should treat a chunk as matching if any one of the given heading(s) appears *anywhere in that chunk's `section_path`* (an ancestor heading counts), not only as the chunk's own leaf heading. Since `chunk.py` splits on H1–H4, a chunk's own leaf heading can sit one level below the `expected_section` given here (e.g. an H3 `expected_section` matching a chunk whose leaf heading is an H4 beneath it). This is intentional and is spelled out in `queries.yaml`'s header comment — don't "fix" it by making `expected_section` always the leaf. The list form exists for documents that genuinely restate the same fact in two sibling sections (e.g. a step-by-step subsection and a separate summary table) — list every section that would be an equally correct retrieval target, don't just pick one and call the other a miss.

**The ground truth in this file was written by reading the corpus, never by running `doqqy query` and recording its output.** If you ever regenerate or "fix" an entry by looking at what doqqy currently returns, you've destroyed the point of the harness — a regression that exists today would get baked in as the expected answer and the harness would never be able to catch it again.

## Adding a document or query without invalidating the baseline

1. **New document in an existing tag folder**: fine to add freely, as long as it doesn't quietly change what the *existing* queries' correct answer is. Before adding, check `queries.yaml` for any query whose `expected_doc_id` is in the same tag folder — if your new document is a closer match to that query's text than the current expected doc, either reword your document to avoid the overlap or don't add it there.
2. **New tag folder**: safe in isolation, but consider whether it should also gain a cross-lingual pair and at least one hard/rerank query against an existing near-topic doc — a corpus that only grows in one language or one difficulty tier stops being a useful regression signal.
3. **New query**: write the query first by reading the corpus, decide the expected doc/section from the text alone, then add a `category` and a one-line `reason`. Never add a query by running doqqy first and copying its top result.
4. **Editing an existing document's content**: if you change a fact that a query's ground truth depends on (a number, a role name, a section heading used in `expected_section`), update that query entry in the same change. Search `queries.yaml` for the doc's path before editing the doc.
5. **Removing a document**: delete every query in `queries.yaml` that references it as `expected_doc_id`.

Keep the corpus small and dense rather than large — the value of this fixture is that every expected answer was reasoned about by hand, not that it has coverage at scale.
