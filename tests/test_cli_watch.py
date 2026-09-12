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
from typer.testing import CliRunner

import doqqy.cli as cli
from doqqy.manifest import DiffResult
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

    def fake_sync(ws, *, settings=None, dry_run=False, diff=None):
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
            patch("doqqy.manifest.Manifest.load") as load_manifest,
        ):
            load_manifest.return_value.diff.return_value = DiffResult(added=[temp_ws.raw_dir / "x.md"])
            # Must not raise -- KeyboardInterrupt on the third batch is caught
            # internally and the command returns normally.
            cli.watch(backend=None, debounce=0.01, verbose=True)
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


@pytest.mark.parametrize("verbose", [False, True])
def test_watch_skips_noop_batch_without_dropping_later_changes(
    temp_ws: Workspace, capsys, monkeypatch: pytest.MonkeyPatch, verbose: bool
) -> None:
    first_path = temp_ws.raw_dir / "first.md"
    second_path = temp_ws.raw_dir / "second.md"

    def fake_watchfiles_watch(path, debounce=0):
        yield {("added", str(first_path))}
        yield {("modified", str(first_path))}
        yield {("modified", str(first_path))}
        yield {("added", str(second_path))}
        raise KeyboardInterrupt

    fake_watchfiles = types.ModuleType("watchfiles")
    fake_watchfiles.watch = fake_watchfiles_watch  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "watchfiles", fake_watchfiles)

    with (
        patch.object(cli, "_workspace", return_value=temp_ws),
        patch("doqqy.sync.sync", side_effect=[SyncReport(added=1), SyncReport(added=1)]) as run_sync,
        patch("doqqy.manifest.Manifest.load") as load_manifest,
    ):
        load_manifest.return_value.diff.side_effect = [
            DiffResult(added=[first_path]),
            DiffResult(unchanged=["first"]),
            RuntimeError("manifest unavailable"),
            DiffResult(added=[second_path]),
        ]
        cli.watch(backend=None, debounce=0.01, verbose=verbose)

    assert run_sync.call_count == 2
    assert run_sync.call_args_list[0].kwargs["diff"].added == [first_path]
    assert run_sync.call_args_list[1].kwargs["diff"].added == [second_path]
    output = capsys.readouterr().out
    assert output.count("Change detected") == 2
    assert "sync failed: RuntimeError: manifest unavailable" in output

    log_text = (temp_ws.logs_dir / "watch.log").read_text(encoding="utf-8")
    assert (str(first_path) in log_text) is verbose
    assert (str(second_path) in log_text) is verbose
    assert ("Skipping filesystem event batch with no manifest changes" in log_text) is verbose


def test_watch_help_describes_maximum_batch_window() -> None:
    result = CliRunner().invoke(cli.app, ["watch", "--help"])
    normalized_output = " ".join(result.output.split())

    assert result.exit_code == 0
    assert "Maximum seconds to batch changes" in normalized_output
    assert "measured from the first change" in normalized_output
