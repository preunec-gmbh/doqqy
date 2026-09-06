"""Same-stem sources with different extensions must not overwrite each other (issue #76).

The naming rule is format-agnostic — `router.py` dispatches on the extension and
everything downstream sees markdown — so these use the text-based ingesters
(`.md`, `.txt`, `.csv`, `.html`) rather than binary fixtures. What is under test
is `processed_path_for`, which never looks at the parser.
"""

from __future__ import annotations

from pathlib import Path

from doqqy.chunk import chunk_directory
from doqqy.ingest.base import processed_path_for, reset_stem_group_cache
from doqqy.ingest.router import ingest_directory
from doqqy.workspace import Workspace


def _ws(tmp_path: Path) -> Workspace:
    ws = Workspace(tmp_path)
    ws.ensure_dirs()
    return ws


def _seed(ws: Workspace, folder: str, names: list[str]) -> Path:
    directory = ws.raw_dir / folder
    directory.mkdir(parents=True, exist_ok=True)
    for name in names:
        (directory / name).write_text(f"# Belge {name}\n\n{name} icin govde metni.\n", encoding="utf-8")
    return directory


def _outputs(ws: Workspace) -> list[str]:
    return sorted(
        str(p.relative_to(ws.processed_dir)).replace("\\", "/")
        for p in ws.processed_dir.rglob("*.md")
    )


def test_same_stem_sources_produce_separate_outputs_and_reach_chunks(tmp_path: Path) -> None:
    """Colliding sources each keep their own processed file, and every one reaches the chunk table."""
    ws = _ws(tmp_path)
    _seed(ws, "x", ["a.md", "a.txt"])

    result = ingest_directory(ws)

    assert not result.failed
    assert len(result.succeeded) == 2
    assert _outputs(ws) == ["x/a-md.md", "x/a-txt.md"]
    # Yeniden adlandırma raporlanmalı — sessiz kalırsa kullanıcı processed/ altında
    # beklediği adı bulamadığında nedenini göremez.
    assert sorted(p.name for p in result.disambiguated) == ["a.md", "a.txt"]

    # Asıl kayıp buradaydı: çakışan dosyalardan yalnızca biri chunk'a ulaşıyordu.
    doc_ids = {c.doc_id for c in chunk_directory(ws)}
    assert doc_ids == {"raw/x/a.md", "raw/x/a.txt"}


def test_unique_stem_keeps_todays_output_name(tmp_path: Path) -> None:
    """A stem with no colliding sibling is named exactly as before — existing workspaces are untouched."""
    ws = _ws(tmp_path)
    _seed(ws, "x", ["a.md", "b.md", "c.md"])

    ingest_directory(ws)

    assert _outputs(ws) == ["x/a.md", "x/b.md", "x/c.md"]


def test_output_name_follows_the_current_sibling_set(tmp_path: Path) -> None:
    """The name is a function of the siblings present right now, in both directions."""
    ws = _ws(tmp_path)
    directory = _seed(ws, "x", ["a.md", "a.txt"])

    reset_stem_group_cache()
    assert processed_path_for(directory / "a.md", ws).name == "a-md.md"

    # Kardeş gidince ad geri döner: ingest ile sync'in aynı kümede buluşmasının
    # tek yolu bu — aksi halde tam ingest ile artımlı sync ayrışırdı.
    (directory / "a.txt").unlink()
    reset_stem_group_cache()
    assert processed_path_for(directory / "a.md", ws).name == "a.md"


def test_ingest_fails_the_file_when_two_sources_resolve_to_one_output(tmp_path: Path) -> None:
    """The run-level invariant holds even where the naming rule cannot separate the pair.

    `a.md` and `a.txt` disambiguate to `a-md.md` / `a-txt.md`, which collides with
    the output of a source genuinely named `a-md.md`. Nothing may silently
    overwrite: the second writer is reported as a failure naming the first.
    """
    ws = _ws(tmp_path)
    _seed(ws, "x", ["a.md", "a.txt", "a-md.md"])

    result = ingest_directory(ws)

    assert len(result.failed) == 1, f"tam olarak bir dosya başarısız olmalı: {result.failed}"
    failed_path, message = result.failed[0]
    assert "çıktı yolu çakıştı" in message
    # Mesaj çakışan diğer kaynağı adıyla söylemeli, yoksa kullanıcı neyi
    # yeniden adlandıracağını bilemez.
    assert "a-md.md" in message
    # Kaybeden taraf belirlenmis olmali: _iter_supported sirali gezdigi icin
    # ('-' < '.') gercek `a-md.md` once yazilir ve tekil govde adi olan o dosya
    # kazanir; ayristirma sonucu ayni ada dusen `a.md` reddedilir.
    assert failed_path.name == "a.md"

    # Başarısız dosya yazılmadı; diğer ikisi yerinde.
    assert len(result.succeeded) == 2
    assert _outputs(ws) == ["x/a-md.md", "x/a-txt.md"]


def test_stems_are_grouped_case_insensitively(tmp_path: Path) -> None:
    """`Rapor.md` and `rapor.txt` are one group — on Windows/macOS they name the same file.

    Comparing stems case-sensitively would read these as two unrelated singletons,
    disambiguate neither, and leave exactly the silent overwrite this rule exists
    to remove.
    """
    ws = _ws(tmp_path)
    _seed(ws, "x", ["Rapor.md", "rapor.txt", "tekil.md"])

    result = ingest_directory(ws)

    assert not result.failed
    assert _outputs(ws) == ["x/Rapor-md.md", "x/rapor-txt.md", "x/tekil.md"]
    assert len(result.disambiguated) == 2


def test_rerunning_ingest_removes_the_output_written_under_the_previous_name(tmp_path: Path) -> None:
    """A stale output from an earlier run is cleaned up, not left to be chunked twice.

    `doqqy ingest` is documented as re-runnable. When a colliding sibling appears
    between two runs a document's name moves, and the file written under the old
    name would otherwise stay: `chunk_directory` reads every `processed/**/*.md`,
    so the same document would enter the index twice.
    """
    ws = _ws(tmp_path)
    _seed(ws, "x", ["rapor.md"])
    ingest_directory(ws)
    assert _outputs(ws) == ["x/rapor.md"]

    _seed(ws, "x", ["rapor.txt"])
    result = ingest_directory(ws)

    assert not result.failed
    assert _outputs(ws) == ["x/rapor-md.md", "x/rapor-txt.md"]

    doc_ids = [c.doc_id for c in chunk_directory(ws)]
    assert sorted(doc_ids) == ["raw/x/rapor.md", "raw/x/rapor.txt"]
    assert len(doc_ids) == len(set(doc_ids)), "belge indekste ikilenmis"


def test_removing_the_sibling_cleans_the_disambiguated_output(tmp_path: Path) -> None:
    """The reverse direction: the name reverts and the disambiguated file goes with it."""
    ws = _ws(tmp_path)
    _seed(ws, "x", ["rapor.md", "rapor.txt"])
    ingest_directory(ws)
    assert _outputs(ws) == ["x/rapor-md.md", "x/rapor-txt.md"]

    (ws.raw_dir / "x" / "rapor.txt").unlink()
    ingest_directory(ws)

    # rapor-txt.md kaynagi artik yok; onu ingest temizlemez (silme sync'in isi),
    # ama rapor.md kendi eski adini birakmali.
    assert "x/rapor-md.md" not in _outputs(ws)
    assert "x/rapor.md" in _outputs(ws)
