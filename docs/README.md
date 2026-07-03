# doqqy — Documentation

English technical documentation for **doqqy**, the local-first document knowledge system.
(Turkish user-facing docs live in [`documentation/`](../documentation/) — `MIMARI.md`, `KULLANIM.md`, `GELISTIRME.md`.)

| Document | Audience | Contents |
|---|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Engineers | Pipeline stages, data models, LanceDB schema, search internals, design decisions |
| [USAGE.md](USAGE.md) | Users / operators | Installation, full CLI reference, typical workflows, Python API, troubleshooting |
| [DEVELOPER-HANDOVER.md](DEVELOPER-HANDOVER.md) | New maintainers | Codebase tour, extension recipes with code, known issues & tech debt, testing strategy |
| [ROADMAP.md](ROADMAP.md) | Product / engineering | Future-feature analysis: REST API layer, SaaS multi-tenancy, incremental indexing, performance improvements |
| [API-ARCHITECTURE.md](API-ARCHITECTURE.md) | Backend / DevOps | Implementation blueprint for the API layer: layering, module layout, FastAPI surface, jobs, deployment, security, build order |

## What doqqy is, in one paragraph

doqqy ingests PDF / Markdown / DOCX / TXT documents into canonical markdown, splits them into header-aware chunks, embeds them **locally** with `BAAI/bge-m3` (dense 1024-dim + sparse lexical weights), and serves **hybrid search**: dense vector search + sparse dot-product search, fused with Reciprocal Rank Fusion (k=60), reranked by the `BAAI/bge-reranker-v2-m3` cross-encoder. It also builds a document relationship map (`.doqqy/topics.yaml`) from explicit textual references (regex) and embedding cosine similarity, rendered as an Obsidian-compatible `INDEX.md` plus injected `[[wikilinks]]`. **No LLM is called anywhere** — queries return raw chunks with sources, and nothing leaves the machine at query time.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .

# put documents under raw/  (subfolders become tags: raw/erp12/... → tag "erp12")
doqqy ingest && doqqy chunk && doqqy embed
doqqy query "how does the JWT refresh flow work?"
```

See [USAGE.md](USAGE.md) for everything else.
