"""chunk.py saf fonksiyon testleri (model/IO yok) — bkz. docs/DEVELOPER-HANDOVER.md §5."""

from __future__ import annotations

from doqqy.chunk import _atomic_blocks, _pack_blocks, _split_section


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
