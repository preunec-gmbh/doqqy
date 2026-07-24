"""Manifest — per-document metadata sidecar for incremental indexing.

Tracks content hashes, chunk counts, tags, and pipeline status for every
ingested document.  Written atomically (tmp file + os.replace) so a crash
mid-write never leaves a half-written manifest.

Schema (.doqqy/manifest.json):
    {
      "version": 1,
      "docs": {
        "<doc_id>": {
          "source":       "raw/erp12/api.pdf",
          "content_hash": "a1b2c3d4e5f60718",
          "tags":         ["erp12"],
          "chunk_count":  34,
          "status":       "indexed",
          "indexed_at":   "2026-07-03T10:00:00Z"
        }
      },
      "totals": {"docs": 128, "chunks": 4102}
    }
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal

from doqqy.config import SUPPORTED_EXTENSIONS, get_logger
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.manifest")

_MANIFEST_VERSION = 1

# `doqqy sync` only ever persists "indexed" or "failed": the manifest is saved
# once, after the store writes have landed, which is what makes an interrupted
# run self-healing. "ingested" and "chunked" are reserved for the staged
# `ingest --changed` / `chunk --changed` commands still open on #16 — until
# those exist nothing emits them, and `doqqy status` simply won't show them.
Status = Literal["ingested", "chunked", "indexed", "failed"]


@dataclass
class ManifestEntry:
    """Per-document metadata stored in the manifest."""

    source: str
    content_hash: str
    tags: list[str] = field(default_factory=list)
    chunk_count: int = 0
    status: Status = "ingested"
    indexed_at: str | None = None


@dataclass
class DiffResult:
    """Result of comparing the current workspace against the manifest.

    Each field contains doc_ids (str) or raw source paths (Path):
    - added:     source Paths present on disk but absent from the manifest.
    - modified:  source Paths whose content_hash differs from the manifest.
    - deleted:   doc_ids in the manifest whose source file is gone.
    - unchanged: doc_ids with matching hashes — no work needed.
    """

    added: list[Path] = field(default_factory=list)
    modified: list[Path] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.added or self.modified or self.deleted)


class Manifest:
    """In-memory representation of .doqqy/manifest.json."""

    def __init__(self) -> None:
        self._docs: dict[str, ManifestEntry] = {}

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    @property
    def docs(self) -> dict[str, ManifestEntry]:
        return self._docs

    def get(self, doc_id: str) -> ManifestEntry | None:
        return self._docs.get(doc_id)

    def update_entry(self, doc_id: str, entry: ManifestEntry) -> None:
        self._docs[doc_id] = entry

    def remove_entry(self, doc_id: str) -> bool:
        """Remove *doc_id* from the manifest. Returns True if it existed."""
        return self._docs.pop(doc_id, None) is not None

    # ------------------------------------------------------------------
    # Totals
    # ------------------------------------------------------------------

    def totals(self) -> dict[str, int]:
        doc_count = len(self._docs)
        chunk_count = sum(e.chunk_count for e in self._docs.values())
        return {"docs": doc_count, "chunks": chunk_count}

    # ------------------------------------------------------------------
    # Persistence — atomic load / save
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, ws: Workspace) -> Manifest:
        """Load the manifest from *ws.manifest_path*.  Missing file → empty manifest."""
        manifest = cls()
        path = ws.manifest_path
        if not path.exists():
            _LOG.debug("Manifest not found at %s — starting fresh.", path)
            return manifest

        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            _LOG.warning("Corrupt manifest at %s — starting fresh: %s", path, exc)
            return manifest

        for doc_id, entry_dict in raw.get("docs", {}).items():
            manifest._docs[doc_id] = ManifestEntry(
                source=entry_dict.get("source", ""),
                content_hash=entry_dict.get("content_hash", ""),
                tags=entry_dict.get("tags", []),
                chunk_count=entry_dict.get("chunk_count", 0),
                status=entry_dict.get("status", "ingested"),
                indexed_at=entry_dict.get("indexed_at"),
            )

        _LOG.debug("Manifest loaded: %d docs from %s", len(manifest._docs), path)
        return manifest

    def save(self, ws: Workspace) -> Path:
        """Atomically write the manifest to *ws.manifest_path* (tmp + os.replace)."""
        path = ws.manifest_path
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "version": _MANIFEST_VERSION,
            "docs": {doc_id: asdict(entry) for doc_id, entry in self._docs.items()},
            "totals": self.totals(),
        }

        # Write to a temp file in the same directory, then atomically replace.
        fd, tmp_path = tempfile.mkstemp(
            dir=str(path.parent), prefix=".manifest_", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
                fh.write("\n")
            os.replace(tmp_path, str(path))
        except BaseException:
            # Clean up the temp file on any error (including KeyboardInterrupt).
            with contextlib.suppress(OSError):
                os.unlink(tmp_path)
            raise

        _LOG.debug("Manifest saved: %d docs → %s", len(self._docs), path)
        return path

    # ------------------------------------------------------------------
    # Diff — detect added / modified / deleted documents
    # ------------------------------------------------------------------

    def diff(self, ws: Workspace) -> DiffResult:
        """Compare on-disk state against this manifest to find what changed.

        Change detection hashes the **raw source bytes** (see read_content_hash)
        and compares against the hash the manifest recorded on the last run.
        Deliberately not the frontmatter ``content_hash``: that one covers the
        *transformed* markdown, which sync only rewrites after it has already
        decided a document changed — so reading it here could never detect an
        edit.  The trade-off is that an ingester upgrade which changes the
        processed output for identical raw bytes is invisible to the diff.
        """
        result = DiffResult()

        # Build a mapping: doc_id → raw source Path for all supported files on disk.
        on_disk: dict[str, Path] = {}
        if ws.raw_dir.exists():
            for source_path in sorted(ws.raw_dir.rglob("*")):
                if source_path.is_file() and source_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    doc_id = _doc_id_from_source(source_path, ws)
                    on_disk[doc_id] = source_path

        # Classify each on-disk file.
        for doc_id, source_path in on_disk.items():
            existing = self._docs.get(doc_id)
            if existing is None:
                result.added.append(source_path)
                continue

            current_hash = read_content_hash(source_path)
            if current_hash is None or current_hash != existing.content_hash:
                result.modified.append(source_path)
            else:
                result.unchanged.append(doc_id)

        # Detect deletions: doc_ids in manifest but no longer on disk.
        for doc_id in self._docs:
            if doc_id not in on_disk:
                result.deleted.append(doc_id)

        return result


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _doc_id_from_source(source_path: Path, ws: Workspace) -> str:
    """Derive a stable doc_id from a raw source path (relative to workspace root)."""
    try:
        return str(source_path.relative_to(ws.root)).replace("\\", "/")
    except ValueError:
        return source_path.name


def read_content_hash(source_path: Path) -> str | None:
    """Hash the raw source file's bytes. None if it cannot be read.

    Note this is a *different* value from the ``content_hash`` in processed
    frontmatter, which hashes the transformed markdown body — see Manifest.diff.
    """
    try:
        data = source_path.read_bytes()
    except OSError:
        return None
    return hashlib.sha256(data).hexdigest()[:16]
