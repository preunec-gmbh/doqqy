"""XLSX veri yükleme parser'ı için birim testleri."""

from __future__ import annotations

from pathlib import Path
import pytest

from doqqy.ingest.base import IngestError
from doqqy.ingest.xlsx_ingest import ingest_xlsx


@pytest.fixture(autouse=True)
def setup_mock_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Proje kök dizinlerini simüle eden (mock) fixture.

    Bu işlem, testler sırasında oluşturulan mutlak yolların simüle edilmiş
    RAW_DIR altında kalmasını sağlar ve base_metadata içinde yol çözümleme
    hataları oluşmasını engeller.
    """
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir = tmp_path / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr("doqqy.ingest.xlsx_ingest.PROJECT_ROOT", tmp_path)
    monkeypatch.setattr("doqqy.ingest.xlsx_ingest.RAW_DIR", raw_dir)
    monkeypatch.setattr("doqqy.ingest.xlsx_ingest.PROCESSED_DIR", processed_dir)


def test_xlsx_multi_sheet_creates_sections(tmp_path: Path) -> None:
    """Çoklu sayfa -> Her sayfa için bir markdown bölümü (## <sayfa_adi>) oluşmalı."""
    import pandas as pd  

    sheets_data = {
        "Yazilim": pd.DataFrame({"ID": [1, 2], "Isim": ["Ahmet", "Mehmet"]}),
        "Donanim": pd.DataFrame({"ID": [3, 4], "Isim": ["Ayse", "Fatma"]}),
    }
    
    # Dosyayı simüle edilmiş raw klasörüne yazıyoruz.
    xlsx_file = tmp_path / "raw" / "multi_sheet_doc.xlsx"
    with pd.ExcelWriter(xlsx_file, engine="openpyxl") as writer:
        for sheet_name, df in sheets_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    doc = ingest_xlsx(xlsx_file)

    # Biçim Doğrulaması: Her sayfa için '## <sayfa_adi>' bölümü açılmış mı?
    assert "## Yazilim" in doc.content
    assert "## Donanim" in doc.content

    # İçerik Doğrulaması: Her sayfa başlığı yalnızca bir kez bulunmalı
    assert doc.content.count("## Yazilim") == 1
    assert doc.content.count("## Donanim") == 1
    
    # Metadata Doğrulaması
    assert doc.metadata["type"] == "xlsx"
    assert doc.metadata["parser"] == "pandas"
    assert "content_hash" in doc.metadata


def test_xlsx_large_sheet_splits_into_blocks(tmp_path: Path) -> None:
    """200 satırlık sayfa -> Her biri en fazla 40 satırlık, başlık içeren tablo bloklarına bölünmeli."""
    import pandas as pd 

    # 200 satırlık bir veri seti üretiyoruz.
    large_df = pd.DataFrame({
        "SiraNo": list(range(1, 201)),
        "Veri": [f"Satir_{i}" for i in range(1, 201)]
    })
    
    xlsx_file = tmp_path / "raw" / "large_sheet_doc.xlsx"
    with pd.ExcelWriter(xlsx_file, engine="openpyxl") as writer:
        large_df.to_excel(writer, sheet_name="Musteriler", index=False)

    doc = ingest_xlsx(xlsx_file)

    # Biçim doğrulaması
    assert "## Musteriler" in doc.content

    # İçerik doğrulaması
    assert doc.content.count("## Musteriler") == 1

    # Doğrulama: to_markdown() fonksiyonu her alt tablo bloğu için başlık ayracı (|---) üretir.
    # 200 satır / 40 satır = En az 5 adet alt başlık/bölüm tetiklenmeli.
    assert doc.content.count("|---") >= 5


def test_xlsx_non_existent_raises(tmp_path: Path) -> None:
    """Mevcut olmayan dosyaların IngestError fırlattığı doğrulanmalıdır."""
    non_existent = tmp_path / "raw" / "missing.xlsx"
    with pytest.raises(IngestError):
        ingest_xlsx(non_existent)


def test_xlsx_all_empty_sheets_raise(tmp_path: Path) -> None:
    """Tüm çalışma sayfaları boş olduğunda IngestError fırlatılmalıdır."""
    import pandas as pd

    xlsx_file = tmp_path / "raw" / "empty_sheets.xlsx"
    # Yalnızca boş bir çalışma sayfası içeren bir Excel dosyası oluşturuyoruz.
    with pd.ExcelWriter(xlsx_file, engine="openpyxl") as writer:
        pd.DataFrame().to_excel(writer, sheet_name="EmptySheet", index=False)

    with pytest.raises(IngestError):
        ingest_xlsx(xlsx_file)

