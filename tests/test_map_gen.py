"""map_gen.py unit tests."""

from __future__ import annotations

from pathlib import Path
from doqqy.map_gen import _parse_sections, _normalize_target


def test_parse_sections_frontmatter_skip(tmp_path):
    # 1. Very first line is ---: skip frontmatter
    doc1 = tmp_path / "doc1.md"
    doc1.write_text(
        "---\ntitle: Doc\ntags: test\n---\n# Heading 1\nBody.",
        encoding="utf-8"
    )
    sections = _parse_sections(doc1)
    assert len(sections) == 1
    assert sections[0][0] == "# Heading 1"
    assert sections[0][2] == ["Body."]
    
    # 2. First line is NOT --- (e.g. empty or text): does not skip frontmatter (treated as body)
    doc2 = tmp_path / "doc2.md"
    doc2.write_text(
        "\n---\ntitle: Doc\n---\n# Heading 1\nBody.",
        encoding="utf-8"
    )
    sections = _parse_sections(doc2)
    # The first section is (başlıksız) and should contain the --- stuff
    assert len(sections) == 2
    assert sections[0][0] == "(başlıksız)"
    assert any("title: Doc" in line for line in sections[0][2])


def test_normalize_target_order():
    known_files = {"AUTHENTICATION.md", "AUTH.md"}
    # candidate AUTH should resolve to AUTH.md because it's an exact match
    res = _normalize_target("AUTH", known_files)
    assert res == "AUTH.md"
    
    known_files = {"AUTHENTICATION.md", "AUTHENTICATE.md"}
    # candidate AUTH (prefix matches both, neither is exact match) should resolve to AUTHENTICATE.md because it is shorter
    res = _normalize_target("AUTH", known_files)
    assert res == "AUTHENTICATE.md"
