"""Değerlendirme motorunun konsol çıktısı için testler."""

from __future__ import annotations

import io

from rich.console import Console

from .__main__ import _configure_utf8_stream


def test_eval_output_stream_is_reconfigured_for_unicode() -> None:
    stream = io.TextIOWrapper(io.BytesIO(), encoding="cp1254")

    _configure_utf8_stream(stream)
    console = Console(file=stream)
    console.print("✓ Tolerans dahilinde hiçbir regresyon tespit edilmedi.")
    stream.flush()

    assert "✓ Tolerans" in stream.detach().getvalue().decode("utf-8")
