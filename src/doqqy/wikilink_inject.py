"""Faz 4 — Obsidian Wikilink Enjeksiyonu: topics.yaml → processed/*.md.

Her processed/*.md dosyasının sonuna <!-- doqqy:links:start/end --> marker bloğu
içinde [[wikilink]] satırları enjekte eder. İdempotent: tekrar çalıştırmak
önceki bloğu temizleyip yeniden yazar.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

from doqqy.config import get_logger
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.wikilink_inject")

MARKER_START = "<!-- doqqy:links:start -->"
MARKER_END = "<!-- doqqy:links:end -->"

_MARKER_BLOCK_RE = re.compile(
    r"\n?" + re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\n?",
    re.DOTALL,
)


# ---------------------------------------------------------------------------
# Veri yapıları
# ---------------------------------------------------------------------------

@dataclass
class FileLinks:
    explicit: list[tuple[str, str]] = field(default_factory=list)  # (target_stem, label)
    thematic: list[tuple[str, str, float]] = field(default_factory=list)  # (target_stem, section, score)


@dataclass
class InjectionResult:
    updated: int = 0
    skipped: int = 0
    total_links: int = 0
    dry_run: bool = False


# ---------------------------------------------------------------------------
# topics.yaml okuyucu
# ---------------------------------------------------------------------------

def _load_file_links(topics_path: Path) -> dict[str, FileLinks]:
    """topics.yaml → {filename: FileLinks} lookup dict."""
    data = yaml.safe_load(topics_path.read_text(encoding="utf-8"))
    sections = data.get("sections", [])

    # {filename → FileLinks}
    file_map: dict[str, FileLinks] = {}

    for sec in sections:
        src_file = sec.get("file", "")
        if not src_file:
            continue

        if src_file not in file_map:
            file_map[src_file] = FileLinks()

        fl = file_map[src_file]

        # Explicit referanslar
        for ref in sec.get("explicit_related", []):
            target_id: str = ref.get("target_id", "")
            if not target_id:
                continue
            # target_id: "FILENAME_section-slug" → stem = ilk "_" öncesi
            target_stem = target_id.split("_")[0]
            label = ref.get("target_section") or target_stem
            pair = (target_stem, label)
            if pair not in fl.explicit:
                fl.explicit.append(pair)

        # Tematik referanslar
        for ref in sec.get("might_be_related", []):
            target_id = ref.get("target_id", "")
            if not target_id:
                continue
            target_stem = target_id.split("_")[0]
            target_section = ref.get("target_section", target_stem)
            score = float(ref.get("score", 0.0))
            entry = (target_stem, target_section, score)
            # Aynı target_stem'i daha önce ekledik mi?
            if not any(e[0] == target_stem for e in fl.thematic):
                fl.thematic.append(entry)

    # Tematik linkleri skora göre azalan sıraya koy
    for fl in file_map.values():
        fl.thematic.sort(key=lambda x: x[2], reverse=True)

    return file_map


# ---------------------------------------------------------------------------
# Blok oluşturucu
# ---------------------------------------------------------------------------

def _build_block(fl: FileLinks) -> Optional[str]:
    """FileLinks → enjekte edilecek markdown bloğu. Link yoksa None."""
    lines: list[str] = [MARKER_START, "## Bağlantılar", ""]

    has_content = False

    if fl.explicit:
        lines.append("### 📌 Explicit Referanslar")
        for stem, _ in fl.explicit:
            lines.append(f"- [[{stem}]]")
        has_content = True

    if fl.thematic:
        if fl.explicit:
            lines.append("")
        lines.append("### 🔗 Tematik Bağlantılar")
        for stem, section, score in fl.thematic:
            heading_clean = section.lstrip("#").strip() if section else stem
            lines.append(f"- [[{stem}]] → {heading_clean} ({score:.2f})")
        has_content = True

    if not has_content:
        return None

    lines.append(MARKER_END)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Dosya güncelleme
# ---------------------------------------------------------------------------

def _strip_marker_block(content: str) -> str:
    """Mevcut doqqy marker bloğunu içerikten temizle."""
    return _MARKER_BLOCK_RE.sub("", content).rstrip()


def _inject_into_file(md_path: Path, block: str, dry_run: bool) -> bool:
    """Dosyaya bloğu enjekte et. Değişiklik olduysa True döner."""
    original = md_path.read_text(encoding="utf-8")
    cleaned = _strip_marker_block(original)
    new_content = cleaned + "\n\n" + block + "\n"

    if new_content == original:
        return False

    if not dry_run:
        md_path.write_text(new_content, encoding="utf-8")

    return True


# ---------------------------------------------------------------------------
# Ana API
# ---------------------------------------------------------------------------

def inject_links(
    ws: Workspace,
    *,
    topics_path: Path | None = None,
    processed_dir: Path | None = None,
    dry_run: bool = False,
) -> InjectionResult:
    """topics.yaml → processed/*.md wikilink enjeksiyonu."""
    topics_path = topics_path or ws.topics_yaml
    processed_dir = processed_dir or ws.processed_dir
    if not topics_path.exists():
        raise FileNotFoundError(f"{topics_path} yok — önce `doqqy map` çalıştır.")

    _LOG.info(f"topics.yaml okunuyor: {topics_path}")
    file_links = _load_file_links(topics_path)

    md_files = [
        f for f in sorted(processed_dir.rglob("*.md"))
        if f.name != "INDEX.md"
    ]

    if not md_files:
        raise FileNotFoundError(f"{processed_dir} içinde .md dosyası yok.")

    result = InjectionResult(dry_run=dry_run)

    for md_path in md_files:
        fl = file_links.get(md_path.name)

        if not fl:
            _LOG.debug(f"  skip (link yok): {md_path.name}")
            result.skipped += 1
            continue

        block = _build_block(fl)
        if not block:
            _LOG.debug(f"  skip (boş blok): {md_path.name}")
            result.skipped += 1
            continue

        link_count = len(fl.explicit) + len(fl.thematic)
        changed = _inject_into_file(md_path, block, dry_run)

        prefix = "[dry-run] " if dry_run else ""
        if changed:
            _LOG.info(f"  {prefix}güncellendi: {md_path.name} ({link_count} link)")
            result.updated += 1
            result.total_links += link_count
        else:
            _LOG.debug(f"  değişmedi: {md_path.name}")
            result.skipped += 1

    return result
