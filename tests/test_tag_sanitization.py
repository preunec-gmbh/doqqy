"""Ingest-side tag sanitization tests — bkz. issue #38.

sanitize_tag() klasör adlarını TAG_PATTERN'e uyan tag'lere çevirir (slugify),
böylece --tag ile filtrelenemeyen "dead end" tag'ler üretilmez.
"""

from __future__ import annotations

import re

import pytest

from doqqy.config import TAG_PATTERN, sanitize_tag


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("a b", "a-b"),                # space -> hyphen
        ("smart farming", "smart-farming"),
        ("bulut'lar", "bulutlar"),     # apostrophe stripped
        ('tag"quote', "tagquote"),     # double quote stripped
        ("tag,comma", "tagcomma"),     # comma stripped
        ("  leading-trailing  ", "leading-trailing"),
        ("türkçe", "türkçe"),          # Turkish letters already conform, unchanged
        ("BÜYÜK harf", "BÜYÜK-harf"),
        ("erp12", "erp12"),            # already conforming — unchanged
        ("bulut-saha", "bulut-saha"),
    ],
)
def test_sanitize_tag_produces_conforming_slug(raw: str, expected: str) -> None:
    result = sanitize_tag(raw)
    assert result == expected
    assert re.match(TAG_PATTERN, result)


@pytest.mark.parametrize("raw", ["!!!", "???", "   ", "'\"", ",,,"])
def test_sanitize_tag_drops_symbol_only_names(raw: str) -> None:
    """A folder name with no conforming characters left is dropped entirely."""
    assert sanitize_tag(raw) is None


def test_sanitize_tag_is_idempotent() -> None:
    """Re-sanitizing an already-sanitized tag must be a no-op (stable re-ingest)."""
    once = sanitize_tag("a b")
    twice = sanitize_tag(once)
    assert once == twice == "a-b"


@pytest.mark.parametrize(
    "raw",
    ["erp12", "bulut-saha", "smart_farming2", "türkçe", "BÜYÜK", "İstanbul"],
)
def test_sanitize_tag_leaves_conforming_names_unchanged(raw: str) -> None:
    assert sanitize_tag(raw) == raw
