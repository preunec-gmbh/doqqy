"""Klasör yapısı → tag türetimi testleri — bkz. docs/DEVELOPER-HANDOVER.md §5."""

from __future__ import annotations

from pathlib import Path

from doqqy.ingest.base import base_metadata


def test_folder_structure_becomes_tags(tmp_path):
    meta = base_metadata(Path("raw/erp12/billing/api.md"), tmp_path, kind="md")
    assert meta["tags"] == ["erp12", "billing"]


def test_root_file_has_no_tags(tmp_path):
    meta = base_metadata(Path("raw/readme.md"), tmp_path, kind="md")
    assert meta["tags"] == []
