<!--
  Fill this in so the PR is easy to review. Keep the scope tight — one change per PR.
-->

## What & why
<!-- One or two sentences: what problem this solves and how. -->

## Type of change
- [ ] 🐛 Bug fix
- [ ] ✨ Feature / new capability
- [ ] ♻️ Refactor / cleanup
- [ ] 📄 New ingester (format support)
- [ ] 📚 Docs
- [ ] 🧰 Tooling / packaging

## Affected pipeline stage(s)
<!-- Check what this touches. -->
- [ ] `ingest`
- [ ] `chunk`
- [ ] `embed`
- [ ] `map`
- [ ] `index` / `inject`
- [ ] `query` / `rerank`
- [ ] CLI / config
- [ ] None (docs/tooling only)

## Local-first invariant
<!-- doqqy makes NO LLM calls and nothing leaves the machine on the query/map path. -->
- [ ] This PR adds **no** network calls or LLM synthesis to the query/map path

## How I tested it
<!-- Commands run and what you observed. Note the model download on first `embed`. -->
- [ ] Ran the affected stage(s) end-to-end on a sample `raw/`
- [ ] `doqqy info` reflects the expected pipeline state
- [ ] Verified idempotency (re-ran the stage; output is stable)

```powershell
# paste the commands you ran, e.g.
# doqqy ingest && doqqy chunk && doqqy embed
# doqqy query "..."
```

## Checklist
- [ ] Config/tuning changes live in `config.py`, not inline
- [ ] `pathlib.Path` used (no `os.path.join`), explicit `encoding="utf-8"` on file I/O
- [ ] Failure isolation preserved (one bad file doesn't stop the run; failures logged + reported)
- [ ] New format? added ingester + `router.py` `_DISPATCH` + `config.SUPPORTED_EXTENSIONS` + `pyproject.toml` dep
- [ ] Docs updated if behavior/architecture changed (`docs/`)
- [ ] No secrets or `.env` values committed
