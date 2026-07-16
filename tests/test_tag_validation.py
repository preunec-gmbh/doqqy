"""Unit tests for tag parameter validation.

All tests call TagFilter directly — no model loading, no filesystem I/O.
CLI integration tests verify exit code and error output via Typer's CliRunner.
"""

from __future__ import annotations

import pytest

from doqqy.infra.vectorstore.base import InvalidTagError, TagFilter


# ---------------------------------------------------------------------------
# Rejected tag values — every one must raise InvalidTagError
# ---------------------------------------------------------------------------

INVALID_TAGS = [
    "x'",                      # SQL single-quote injection
    'tag"',                    # SQL double-quote injection
    "tag\\",                   # backslash escape
    "a b",                     # space (path separator risk)
    "x,y",                     # comma (our delimiter in tags_str)
    "%",                       # SQL LIKE wildcard
    "",                        # empty string — no meaningful tag
    "tag; DROP TABLE chunks;", # classic SQL injection payload
    "tag/",                    # path traversal
    "tag?",                    # glob wildcard
    "tag\n",                   # newline — would bypass $ anchor
    "tag\t",                   # tab character
    "tag*",                    # glob wildcard
    "tag#",                    # URL fragment / comment char
    "tag$",                    # shell variable expansion
    "tag@",                    # email-like injection
    "tag!",                    # shell history expansion
    "tag(1)",                  # parentheses — SQL grouping
    "tag[2]",                  # brackets — SQL / glob
    "tag{3}",                  # braces — shell brace expansion
    " leading-space",          # leading whitespace
    "trailing-space ",         # trailing whitespace
    "a\x00b",                  # null byte
    "../etc/passwd",           # path traversal
    "tag\r",                   # carriage return
]


@pytest.mark.parametrize("invalid_tag", INVALID_TAGS)
def test_tagfilter_rejects_invalid_tag(invalid_tag: str) -> None:
    """TagFilter must raise InvalidTagError for every disallowed value."""
    with pytest.raises(InvalidTagError, match="Tag format must match"):
        TagFilter(tags=(invalid_tag,))


# ---------------------------------------------------------------------------
# Accepted tag values — must construct without raising
# ---------------------------------------------------------------------------

VALID_TAGS = [
    "erp12",                          # typical slug
    "bulut-saha",                     # hyphen allowed
    "smart_farming2",                 # underscore allowed
    "TAG-123_abc",                    # mixed case + digits
    "a",                              # single char
    "1",                              # single digit
    "_",                              # single underscore
    "-",                              # single hyphen
    "TAG_with_UPPERCASE_and_numbers_987",
    "tag--",                          # double hyphen (still valid)
    "türkçe",                         # Turkish Unicode letters — \w covers them
    "BÜYÜK",                          # Turkish uppercase Unicode
    "İstanbul",                       # Turkish İ (U+0130)
]


@pytest.mark.parametrize("valid_tag", VALID_TAGS)
def test_tagfilter_accepts_valid_tag(valid_tag: str) -> None:
    """TagFilter must construct without error for every allowed value."""
    flt = TagFilter(tags=(valid_tag,))
    assert flt.tags == (valid_tag,)


def test_tagfilter_empty_tags_allowed() -> None:
    """An empty tags tuple means 'no filter' — must never raise."""
    flt = TagFilter()
    assert flt.tags == ()


def test_tagfilter_multiple_valid_tags() -> None:
    """Multiple valid tags in one TagFilter must all be validated."""
    flt = TagFilter(tags=("erp12", "bulut-saha", "smart_farming2"))
    assert len(flt.tags) == 3


def test_tagfilter_one_invalid_in_many_raises() -> None:
    """A single bad tag among otherwise valid tags must still raise."""
    with pytest.raises(InvalidTagError):
        TagFilter(tags=("erp12", "bad tag", "bulut"))


# ---------------------------------------------------------------------------
# CLI integration — error output and exit code
# ---------------------------------------------------------------------------

def test_cli_query_invalid_tag_exits_with_code_1() -> None:
    """query command with invalid tag must exit 1 and print a red error."""
    from typer.testing import CliRunner
    from doqqy.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["query", "test query", "--tag", "x'"])
    assert result.exit_code == 1
    # CliRunner captures both stdout and stderr in result.output
    assert "Hata:" in result.output
    assert "Tag format must match" in result.output


def test_cli_map_invalid_tag_exits_with_code_1() -> None:
    """map command with invalid tag must exit 1 and print a red error."""
    from typer.testing import CliRunner
    from doqqy.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["map", "--tag", "a b"])
    assert result.exit_code == 1
    # CliRunner captures both stdout and stderr in result.output
    assert "Hata:" in result.output
    assert "Tag format must match" in result.output
