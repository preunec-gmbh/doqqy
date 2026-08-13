"""Regression test for doqqy.cli.watch's failure-isolation invariant.

A batch-level exception from sync() (model load, store connection, corrupt
manifest, ...) must not crash the watch loop -- it should be logged and the
loop must keep watching, the same way per-file failures inside sync() are
already isolated. Ctrl-C must still exit the loop cleanly.
"""

from __future__ import annotations

import io
import logging
import sys
import types
from pathlib import Path
from unittest.mock import patch

import pytest

import doqqy.cli as cli
from doqqy.sync import SyncReport
from doqqy.workspace import Workspace


@pytest.fixture
def temp_ws(tmp_path: Path) -> Workspace:
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    return ws


def test_watch_survives_batch_failure_and_exits_on_ctrl_c(
    temp_ws: Workspace, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls = {"n": 0}

    def fake_sync(ws, *, settings=None, dry_run=False):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("boom: simulated batch failure")
        if calls["n"] == 2:
            report = SyncReport(added=1)
            report.failed.append(("raw/x.md", "ValueError: bad file"))
            return report
        raise KeyboardInterrupt

    def fake_watchfiles_watch(path, debounce=0):
        for _ in range(3):
            yield {("added", str(path / "x.md"))}

    # `watchfiles` is an optional extra (the `watch` install group) and isn't
    # guaranteed to be present in the environment running this test, so a
    # real `watchfiles.watch` module attribute can't be patched with
    # unittest.mock.patch("watchfiles.watch", ...) -- that requires importing
    # the real module first. Inject a fake module into sys.modules instead;
    # cli.watch()'s `from watchfiles import watch as watchfiles_watch` then
    # resolves against the fake regardless of whether the real package exists.
    fake_watchfiles = types.ModuleType("watchfiles")
    fake_watchfiles.watch = fake_watchfiles_watch  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "watchfiles", fake_watchfiles)

    # Stand-in for the console StreamHandler that config._ensure_console_handler()
    # attaches to the parent "doqqy" logger -- whatever reaches this handler is
    # what the user would see on their terminal. capsys can't be used for that:
    # the real handler binds the stream at import time, so its output never goes
    # through the stream capsys patches.
    console_sink = io.StringIO()
    console_probe = logging.StreamHandler(console_sink)
    logging.getLogger("doqqy").addHandler(console_probe)

    try:
        with (
            patch.object(cli, "_workspace", return_value=temp_ws),
            patch("doqqy.sync.sync", side_effect=fake_sync),
        ):
            # Must not raise -- KeyboardInterrupt on the third batch is caught
            # internally and the command returns normally.
            cli.watch(backend=None, debounce=0.01)
    finally:
        logging.getLogger("doqqy").removeHandler(console_probe)

    # All three batches ran: the loop survived the batch-1 crash instead of
    # dying after the first iteration.
    assert calls["n"] == 3

    out = capsys.readouterr().out
    assert "sync failed" in out
    assert "1 added" in out or "+1" in out

    # The batch-level failure is logged to disk, not just flashed on stdout.
    watch_log = temp_ws.logs_dir / "watch.log"
    assert watch_log.exists()
    assert "Batch sync failed" in watch_log.read_text(encoding="utf-8")

    # The traceback for the batch failure must not also be dumped to the
    # console -- only the concise rich summary line belongs there. This is what
    # cli.watch()'s `log.propagate = False` buys: without it the record reaches
    # the "doqqy" logger's console handler and prints the whole traceback.
    assert "Traceback (most recent call last)" not in console_sink.getvalue()
    assert "Traceback (most recent call last)" not in out
