"""chunk.py saf fonksiyon testleri (model/IO yok) — bkz. docs/DEVELOPER-HANDOVER.md §5."""

from __future__ import annotations

from doqqy.chunk import _TABLE_SEP_LINE_RE, _atomic_blocks, _pack_blocks, _split_section, _split_table_block


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


def _make_table(n_rows: int, start: int = 0) -> str:
    header = "| a | b |\n|---|---|\n"
    return header + "".join(f"| {i} | x |\n" for i in range(start, start + n_rows))


def test_adjacent_tables_stay_separate_atomic_blocks():
    """issue #77: bir boş satırla ayrılmış iki tablo tek bloğa birleşmemeli."""
    doc = _make_table(5) + "\n" + _make_table(5, start=5)
    blocks = _atomic_blocks(doc)
    table_blocks = [b for b in blocks if b.startswith("| a | b |")]
    assert len(table_blocks) == 2


def test_large_csv_table_never_exceeds_max_chars():
    """891 satırlık bir CSV'nin tek bir devasa chunk üretmemesi gerekir."""
    big_table = "# ornek-csv\n\n" + _make_table(891)
    chunks = _split_section(big_table)
    assert all(len(c) <= 3200 for c in chunks)


def test_split_table_rows_all_have_separator():
    """Satır bazlı bölünen her parça, veri satırlarının yanında ayraç satırını da taşımalı."""
    table = _make_table(200)
    parts = _split_table_block(table, max_chars=1000)
    assert len(parts) > 1
    for part in parts:
        lines = part.split("\n")
        assert lines[0].startswith("| a | b |")
        assert _TABLE_SEP_LINE_RE.match(lines[1])


def test_split_table_rows_repeat_header():
    """Her parçanın başlık satırı, orijinal tablonun başlık satırıyla aynı olmalı."""
    table = _make_table(200)
    original_header = table.split("\n")[0]
    parts = _split_table_block(table, max_chars=1000)
    for part in parts:
        assert part.split("\n")[0] == original_header


def test_chunk_file_tags_coercion(tmp_path):
    from doqqy.chunk import chunk_file
    from doqqy.workspace import Workspace
    ws = Workspace(tmp_path)
    ws.ensure_dirs()

    # 1. String -> [str]
    md_str_tags = tmp_path / "processed" / "doc1.md"
    md_str_tags.parent.mkdir(parents=True, exist_ok=True)
    md_str_tags.write_text(
        "---\ntags: erp12\n---\nBody text.",
        encoding="utf-8"
    )
    chunks = chunk_file(md_str_tags, ws)
    assert chunks[0].tags == ["erp12"]

    # 2. List of strings stays list of strings
    md_list_tags = tmp_path / "processed" / "doc2.md"
    md_list_tags.write_text(
        "---\ntags:\n  - erp12\n  - billing\n---\nBody text.",
        encoding="utf-8"
    )
    chunks = chunk_file(md_list_tags, ws)
    assert chunks[0].tags == ["erp12", "billing"]

    # 3. Anything else (e.g. dict) -> []
    md_invalid_tags = tmp_path / "processed" / "doc3.md"
    md_invalid_tags.write_text(
        "---\ntags:\n  key: value\n---\nBody text.",
        encoding="utf-8"
    )
    chunks = chunk_file(md_invalid_tags, ws)
    assert chunks[0].tags == []


def test_removed_constants():
    import pytest

    from doqqy import config
    with pytest.raises(AttributeError):
        _ = config.CHUNK_OVERLAP
    with pytest.raises(AttributeError):
        _ = config.CHUNK_MIN_MERGE_TOKENS

