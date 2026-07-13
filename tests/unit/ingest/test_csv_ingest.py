"""CSV veri yükleme parser'ı için birim testleri."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from doqqy.ingest.base import IngestError
from doqqy.ingest.csv_ingest import ingest_csv
from doqqy.workspace import Workspace


@pytest.fixture()
def ws(tmp_path: Path) -> Workspace:
    """Testler workspace'i açıkça alır — cwd veya monkeypatch bağımlılığı yok."""
    workspace = Workspace(tmp_path)
    workspace.ensure_dirs()
    return workspace


def test_csv_ingest_with_different_delimiters(tmp_path: Path, ws: Workspace) -> None:
    """Virgül ve noktalı virgül ayıraçlarının otomatik algılanmasını doğrular."""

    csv_comma = tmp_path / "raw" / "test_comma.csv"
    csv_comma.write_text("id,name\n1,Ahmet\n2,Mehmet", encoding="utf-8")

    doc_comma = ingest_csv(csv_comma, ws)

    assert doc_comma.metadata["delimiter"] == ","
    assert doc_comma.metadata["parser"] == "pandas"
    assert "content_hash" in doc_comma.metadata
    assert "Ahmet" in doc_comma.content

    csv_semi = tmp_path / "raw" / "test_semi.csv"
    csv_semi.write_text("id;name\n3;Ayşe\n4;Fatma", encoding="utf-8")

    doc_semi = ingest_csv(csv_semi, ws)

    assert doc_semi.metadata["delimiter"] == ";"
    assert doc_semi.metadata["parser"] == "pandas"
    assert "content_hash" in doc_semi.metadata
    assert "Ayşe" in doc_semi.content


def test_csv_ingest_row_blocking(tmp_path: Path, ws: Workspace) -> None:
    """40 satırı aşan CSV dosyalarının birden fazla markdown bloğuna bölündüğünü doğrular."""

    csv_large = tmp_path / "raw" / "test_large.csv"

    df = pd.DataFrame({"id": list(range(1, 51)),
                       "val": [f"Row{i}" for i in range(1, 51)]})

    df.to_csv(csv_large, index=False, sep=",")

    doc = ingest_csv(csv_large, ws)

    assert doc.metadata["type"] == "csv"
    assert doc.metadata["parser"] == "pandas"
    assert "content_hash" in doc.metadata

    # H1 başlığı dosya adından üretilmeli
    assert doc.content.startswith("# test_large")

    # 50 satır -> en az 2 markdown tablo bloğu
    assert doc.content.count("|---") >= 2


def test_csv_cp1254_fallback(tmp_path: Path, ws: Workspace) -> None:
    """cp1254 kodlamalı CSV dosyalarının başarıyla okunabildiğini doğrular."""

    csv_cp1254 = tmp_path / "raw" / "cp1254.csv"

    csv_cp1254.write_bytes("id;isim\n1;Çınar\n2;Şule".encode("cp1254"))

    doc = ingest_csv(csv_cp1254, ws)

    assert doc.metadata["encoding"] == "cp1254"
    assert doc.metadata["parser"] == "pandas"
    assert "Çınar" in doc.content
    assert "Şule" in doc.content


def test_csv_invalid_or_empty_raises(tmp_path: Path, ws: Workspace) -> None:
    """Boş CSV dosyalarının IngestError fırlattığını doğrular."""

    csv_empty = tmp_path / "raw" / "empty.csv"
    csv_empty.write_text("", encoding="utf-8")

    with pytest.raises(IngestError):
        ingest_csv(csv_empty, ws)

