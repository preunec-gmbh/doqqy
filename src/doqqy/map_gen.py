"""Faz 3 — Harita Üretimi: processed/*.md → topics.yaml.

Pass 1: Regex ile explicit referansları yakala (bkz., see section, dosya adı).
Pass 2: LanceDB dense vektörlerinden section centroid cosine benzerliği.
"""

from __future__ import annotations

import contextlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np
import yaml

from doqqy.config import (
    MAP_COSINE_THRESHOLD,
    MAP_TOP_N_NEIGHBORS,
    get_logger,
)
from doqqy.infra.settings import Settings
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.map_gen")


# ---------------------------------------------------------------------------
# Veri yapıları
# ---------------------------------------------------------------------------

@dataclass
class ExplicitRef:
    target_id: str
    target_section: Optional[str]
    source_line: int


@dataclass
class ThematicRef:
    target_id: str
    target_section: str
    score: float


@dataclass
class SectionEntry:
    id: str              # "FILENAME_section-slug"
    file: str            # "FILENAME.md"
    section: str         # "## Başlık"
    explicit_related: list[ExplicitRef] = field(default_factory=list)
    might_be_related: list[ThematicRef] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Yardımcılar
# ---------------------------------------------------------------------------

def _slug(text: str) -> str:
    """Başlık metnini URL-safe slug'a dönüştür."""
    text = text.lstrip("#").strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")[:60]


def _section_id(filename: str, heading: str) -> str:
    stem = Path(filename).stem.upper()
    return f"{stem}_{_slug(heading)}"


def _parse_sections(md_path: Path) -> list[tuple[str, int, list[str]]]:
    """Dosyayı okuyup (heading_text, line_no, body_lines) listesi döndür."""
    lines = md_path.read_text(encoding="utf-8").splitlines()
    sections: list[tuple[str, int, list[str]]] = []
    current_heading = "(başlıksız)"
    current_line = 0
    current_body: list[str] = []

    in_fm = False
    for i, line in enumerate(lines):
        # frontmatter atla
        if i == 0 and line.strip() == "---":
            in_fm = True
            continue
        if in_fm:
            if line.strip() == "---":
                in_fm = False
            continue

        if re.match(r"^#{1,4}\s", line):
            if current_body or sections:
                sections.append((current_heading, current_line, current_body))
            current_heading = line.strip()
            current_line = i + 1
            current_body = []
        else:
            current_body.append(line)

    sections.append((current_heading, current_line, current_body))
    return sections


# ---------------------------------------------------------------------------
# Pass 1 — Regex (Explicit Referanslar)
# ---------------------------------------------------------------------------

# Bilinen referans kalıpları
_KNOWN_FILES: list[str] = []  # Pass 1 başlamadan önce doldurulur

_PATTERNS: list[re.Pattern] = [
    # bkz. FOO veya bkz: FOO (Türkçe)
    re.compile(r"\bbkz[.:]\s*([A-Z][A-Z0-9_\-]{1,40}(?:\.md)?)", re.IGNORECASE),
    # see section / see also FOO
    re.compile(r"\bsee\s+(?:section|also)\s+([A-Z][A-Z0-9_\-]{1,40}(?:\.md)?)", re.IGNORECASE),
    # Parantez içi: (DOSYA.md) veya (bkz. FOO)
    re.compile(r"\((?:bkz[.:]\s*)?([A-Z][A-Z0-9_\-]{1,40}\.md)\)", re.IGNORECASE),
    # [[WikiLink]] tarzı (varsa)
    re.compile(r"\[\[([A-Z][A-Z0-9_\-]{1,40})\]\]", re.IGNORECASE),
]


def _normalize_target(raw: str, known_files: set[str]) -> Optional[str]:
    """Ham referans metnini bilinen dosya adına normalize et. Bulunamazsa None."""
    candidate = raw.upper().removesuffix(".MD")
    sorted_files = sorted(
        known_files,
        key=lambda f: (not (Path(f).stem.upper() == candidate), len(f), f)
    )
    for f in sorted_files:
        stem = Path(f).stem.upper()
        if stem == candidate or stem.startswith(candidate) or candidate.startswith(stem):
            return f
    return None


def _pass1(processed_dir: Path, known_files: set[str]) -> dict[str, list[ExplicitRef]]:
    """Tüm dosyaları regex ile tara. {section_id: [ExplicitRef]} döndür."""
    results: dict[str, list[ExplicitRef]] = {}

    for md_file in sorted(processed_dir.rglob("*.md")):
        if md_file.name == "INDEX.md":
            continue
        sections = _parse_sections(md_file)
        for heading, start_line, body_lines in sections:
            sec_id = _section_id(md_file.name, heading)
            refs: list[ExplicitRef] = []

            for rel_lineno, line in enumerate(body_lines):
                abs_lineno = start_line + rel_lineno
                for pat in _PATTERNS:
                    for m in pat.finditer(line):
                        raw = m.group(1)
                        target_file = _normalize_target(raw, known_files)
                        if target_file and target_file != md_file.name:
                            target_id = _section_id(target_file, "")
                            refs.append(ExplicitRef(
                                target_id=target_id.rstrip("_"),
                                target_section=None,
                                source_line=abs_lineno,
                            ))

            if refs:
                results[sec_id] = refs

    return results


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def _pass2(
    ws: Workspace,
    sections_meta: list[SectionEntry],
    top_n: int = MAP_TOP_N_NEIGHBORS,
    threshold: float = MAP_COSINE_THRESHOLD,
    filter_tag: str | None = None,
    settings: Settings | None = None,
) -> dict[str, list[ThematicRef]]:
    """Retrieve dense vectors from vector store, find cosine neighbors for each section."""
    from doqqy.infra.vectorstore.base import TagFilter
    from doqqy.infra.vectorstore.factory import make_store

    flt = TagFilter(tags=(filter_tag,)) if filter_tag else None
    with contextlib.closing(make_store(ws, settings)) as store:
        all_vecs, records = store.all_vectors(flt)

    if all_vecs.shape[0] == 0:
        _LOG.warning("No vectors found - Pass 2 skipped.")
        return {}

    # Group chunks for section centroid by matching source filename + heading
    results: dict[str, list[ThematicRef]] = {}


    all_sources = [r.source for r in records]
    all_section_paths = [r.section_path for r in records]

    # Calculate centroid for each section
    sec_centroids: dict[str, tuple[np.ndarray, str]] = {}  # sec_id -> (centroid, source_file)

    for entry in sections_meta:
        mask = []
        for i, src in enumerate(all_sources):
            src_name = Path(str(src)).name if src else ""
            if src_name == entry.file:
                sp_list = all_section_paths[i]
                heading_clean = entry.section.lstrip("#").strip()
                if not sp_list or (sp_list and heading_clean in " > ".join(sp_list)):
                    mask.append(i)

        if not mask:
            continue
        chunk_vecs = all_vecs[mask]
        centroid = chunk_vecs.mean(axis=0)
        centroid = centroid / (np.linalg.norm(centroid) + 1e-9)
        sec_centroids[entry.id] = (centroid, entry.file)

    # Centroidler arası cosine — farklı dosyaları filtrele
    sec_ids = list(sec_centroids.keys())
    for i, src_id in enumerate(sec_ids):
        src_vec, src_file = sec_centroids[src_id]
        neighbors: list[tuple[float, str]] = []

        for j, tgt_id in enumerate(sec_ids):
            if i == j:
                continue
            tgt_vec, tgt_file = sec_centroids[tgt_id]
            if tgt_file == src_file:
                continue  # aynı dosya — atla
            score = _cosine(src_vec, tgt_vec)
            if score >= threshold:
                neighbors.append((score, tgt_id))

        neighbors.sort(reverse=True)
        top = neighbors[:top_n]
        if top:
            results[src_id] = [
                ThematicRef(
                    target_id=tgt_id,
                    target_section=_heading_from_id(tgt_id, sections_meta),
                    score=round(score, 4),
                )
                for score, tgt_id in top
            ]

    return results


def _heading_from_id(sec_id: str, entries: list[SectionEntry]) -> str:
    for e in entries:
        if e.id == sec_id:
            return e.section
    return sec_id


# ---------------------------------------------------------------------------
# topics.yaml yazıcı
# ---------------------------------------------------------------------------

def _to_dict(entries: list[SectionEntry]) -> dict:
    sections = []
    for e in entries:
        d: dict = {
            "id": e.id,
            "file": e.file,
            "section": e.section,
        }
        if e.explicit_related:
            d["explicit_related"] = [
                {k: v for k, v in {
                    "target_id": r.target_id,
                    "target_section": r.target_section,
                    "source_line": r.source_line,
                }.items() if v is not None}
                for r in e.explicit_related
            ]
        if e.might_be_related:
            d["might_be_related"] = [
                {
                    "target_id": r.target_id,
                    "target_section": r.target_section,
                    "score": r.score,
                }
                for r in e.might_be_related
            ]
        sections.append(d)
    return {"sections": sections}


# ---------------------------------------------------------------------------
# Ana API
# ---------------------------------------------------------------------------

def generate_map(
    ws: Workspace,
    *,
    processed_dir: Path | None = None,
    pass1: bool = True,
    pass2: bool = True,
    cosine_threshold: float = MAP_COSINE_THRESHOLD,
    top_n: int = MAP_TOP_N_NEIGHBORS,
    output: Path | None = None,
    tag: str | None = None,
    settings: Settings | None = None,
) -> Path:
    """processed/*.md → topics.yaml. Returned value: written file path."""
    # Validate tag early — TagFilter.__post_init__ raises InvalidTagError for
    # any value that doesn't match TAG_PATTERN, before any filesystem I/O.
    from doqqy.infra.vectorstore.base import TagFilter as _TagFilter
    if tag is not None:
        _TagFilter(tags=(tag,))  # raises InvalidTagError if format is wrong

    processed_dir = processed_dir or ws.processed_dir
    output = output or ws.topics_yaml
    md_files = sorted(f for f in processed_dir.rglob("*.md") if f.name != "INDEX.md")
    if not md_files:
        raise FileNotFoundError(f"{processed_dir} has no .md files.")

    known_files = {f.name for f in md_files}
    _LOG.info(f"Found {len(md_files)} files.")

    # Extract all section meta first
    all_sections: list[SectionEntry] = []
    for md_file in md_files:
        for heading, _, _ in _parse_sections(md_file):
            sec_id = _section_id(md_file.name, heading)
            all_sections.append(SectionEntry(
                id=sec_id,
                file=md_file.name,
                section=heading,
            ))

    _LOG.info(f"Detected {len(all_sections)} sections.")

    # Pass 1
    explicit_map: dict[str, list[ExplicitRef]] = {}
    if pass1:
        _LOG.info("Pass 1 — regex explicit references...")
        explicit_map = _pass1(processed_dir, known_files)
        total_refs = sum(len(v) for v in explicit_map.values())
        _LOG.info(f"Pass 1 done: found {total_refs} explicit references.")

    # Pass 2
    thematic_map: dict[str, list[ThematicRef]] = {}
    if pass2:
        _LOG.info(f"Pass 2 — embedding cosine similarity... (tag filter: {tag or 'none'})")
        thematic_map = _pass2(
            ws, all_sections, top_n=top_n, threshold=cosine_threshold, filter_tag=tag, settings=settings
        )
        total_th = sum(len(v) for v in thematic_map.values())
        _LOG.info(f"Pass 2 done: found {total_th} thematic links.")

    # Birleştir
    for entry in all_sections:
        entry.explicit_related = explicit_map.get(entry.id, [])
        entry.might_be_related = thematic_map.get(entry.id, [])

    # Sadece bağlantısı olan section'ları yaz (gürültüyü azalt)
    linked = [e for e in all_sections if e.explicit_related or e.might_be_related]
    _LOG.info(f"{len(linked)}/{len(all_sections)} section bağlantılı.")

    data = _to_dict(linked)
    output.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    _LOG.info(f"topics.yaml yazıldı: {output}")
    return output
