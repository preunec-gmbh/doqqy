"""Faz 3 — INDEX.md üretimi: topics.yaml → processed/INDEX.md."""

from __future__ import annotations

from pathlib import Path

import yaml

from docq.config import PROCESSED_DIR, TOPICS_YAML, get_logger

_LOG = get_logger("docq.index_gen")


def generate_index(
    topics_path: Path = TOPICS_YAML,
    output_dir: Path = PROCESSED_DIR,
) -> Path:
    """topics.yaml okuyup INDEX.md yaz. Dönen değer: yazılan dosya yolu."""
    if not topics_path.exists():
        raise FileNotFoundError(f"{topics_path} yok — önce `docq map` çalıştır.")

    data = yaml.safe_load(topics_path.read_text(encoding="utf-8"))
    sections = data.get("sections", [])

    if not sections:
        raise ValueError("topics.yaml içinde section yok.")

    # Dosyaya göre grupla
    by_file: dict[str, list[dict]] = {}
    for sec in sections:
        fname = sec.get("file", "?")
        by_file.setdefault(fname, []).append(sec)

    lines: list[str] = [
        "# Doküman İndeksi",
        "",
        "> Bu dosya `docq index` tarafından otomatik üretilmiştir.",
        "",
    ]

    for fname in sorted(by_file.keys()):
        lines.append(f"## {fname}")
        lines.append("")
        for sec in by_file[fname]:
            heading = sec.get("section", "")
            heading_clean = heading.lstrip("#").strip()
            if heading_clean and heading_clean != "(başlıksız)":
                lines.append(f"### {heading_clean}")
            else:
                lines.append("### (genel)")

            explicit = sec.get("explicit_related", [])
            for ref in explicit:
                tid = ref.get("target_id", "")
                tsec = ref.get("target_section") or ""
                tsec_str = f" → {tsec}" if tsec else ""
                lines.append(f"- 📌 Explicit: `{tid}`{tsec_str}")

            thematic = sec.get("might_be_related", [])
            for ref in thematic:
                tid = ref.get("target_id", "")
                tsec = ref.get("target_section") or ""
                score = ref.get("score", 0.0)
                tsec_str = f" → {tsec}" if tsec else ""
                lines.append(f"- 💡 İlgili olabilir: `{tid}`{tsec_str} ({score:.2f})")

            lines.append("")

    output = output_dir / "INDEX.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    _LOG.info(f"INDEX.md yazıldı: {output}")
    return output
