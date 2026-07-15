"""Unit tests for tag parameter validation in search and map generation."""

from __future__ import annotations

from pathlib import Path
import pytest

from doqqy.workspace import Workspace
from doqqy.query import search
from doqqy.map_gen import generate_map


@pytest.mark.parametrize(
    "invalid_tag",
    [
        "x'",
        "a b",
        "x,y",
        "%",
        "",
        "tag; DROP TABLE chunks;",
        "tag\"",
        "tag\\",
        "tag/",
        "tag?",
        "tag\n",
        "tag\t",
        "tag*",
        "tag#",
        "tag$",
        "tag@",
        "tag!",
        "tag(1)",
        "tag[2]",
        "tag{3}",
    ],
)
def test_search_and_map_reject_invalid_tags(tmp_path: Path, invalid_tag: str):
    """Verify that invalid tag values raise a ValueError."""
    ws = Workspace(tmp_path)

    # 1. Test search() rejects the invalid tag before executing further
    with pytest.raises(ValueError) as exc_info:
        search(ws, "test query", tag=invalid_tag)
    assert "Tag format must match" in str(exc_info.value)

    # 2. Test generate_map() rejects the invalid tag before executing further
    with pytest.raises(ValueError) as exc_info:
        generate_map(ws, tag=invalid_tag)
    assert "Tag format must match" in str(exc_info.value)


@pytest.mark.parametrize(
    "valid_tag",
    [
        "erp12",
        "bulut-saha",
        "smart_farming2",
        "TAG-123_abc",
        "a",
        "1",
        "_",
        "-",
        "TAG_with_UPPERCASE_and_numbers_987",
        "tag--",
    ],
)
def test_search_and_map_accept_valid_tags(tmp_path: Path, valid_tag: str):
    """Verify that valid tag formats do not raise a tag-validation ValueError."""
    ws = Workspace(tmp_path)

    # Valid tags shouldn't fail validation. If search() runs past validation,
    # it tries to load FlagEmbedding (which is mocked or might trigger on first load),
    # but to isolate validation we can catch other errors or let it run.
    # Note: search() calls _embed_query, which might download/load models.
    # Let's verify it doesn't raise ValueError due to tag validation.
    try:
        search(ws, "test query", tag=valid_tag)
    except ValueError as e:
        # If it raises a ValueError, verify it is not the tag format validation error
        assert "Tag format must match" not in str(e)
    except Exception:
        # Any other exception (like FileNotFoundError, model loading, etc.) is fine
        pass

    try:
        generate_map(ws, tag=valid_tag)
    except ValueError as e:
        assert "Tag format must match" not in str(e)
    except Exception:
        # generate_map expects processed/ files or a store, so FileNotFoundError or other errors are fine
        pass


def test_cli_query_invalid_tag_exits_red():
    """Verify that query command with invalid tag exits with code 1 and prints a red error message."""
    from typer.testing import CliRunner
    from doqqy.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["query", "test query", "--tag", "x'"])
    assert result.exit_code == 1
    assert "Hata: Tag format must match" in result.stdout


def test_cli_map_invalid_tag_exits_red():
    """Verify that map command with invalid tag exits with code 1 and prints a red error message."""
    from typer.testing import CliRunner
    from doqqy.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["map", "--tag", "a b"])
    assert result.exit_code == 1
    assert "Hata: Tag format must match" in result.stdout
