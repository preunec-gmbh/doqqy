"""Doqqy iş hattının uçtan uca çalışmasını doğrulayan entegrasyon testi."""

from __future__ import annotations

from pathlib import Path

import pytest

from doqqy.chunk import chunk_directory
from doqqy.embed import build_index
from doqqy.ingest import ingest_directory
from doqqy.query import search
from doqqy.workspace import Workspace


@pytest.mark.slow
def test_integration_pipeline_flow(tmp_path):
    # 1. pytest'in sağladığı izole geçici dizinde 'raw' klasörü ve mock döküman oluşturulması
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()

    test_document = raw_dir / "test_doc.md"
    test_document.write_text(
        "# Entegrasyon Testi\n"
        "Bu dokümanda çok özel bir gizli kelime geçiyor: MaviEjderha2026.\n"
        "Aradığımızda bu paragrafı bulabilmeliyiz."
    )

    # 2. doqqy Workspace nesnesinin başlatılması ve gerekli alt klasörlerin (.doqqy, processed vb.) kurulması
    ws = Workspace(tmp_path)
    ws.ensure_dirs()

    # 3. Aşama: Ingest (Dökümanları canonical markdown formatına dönüştürme)
    ingest_result = ingest_directory(ws)
    assert len(ingest_result.failed) == 0       # Hiçbir dosya dönüştürmede hata almamalı

    # 4. Aşama: Chunking (Başlık bazlı parçalama)
    chunks = chunk_directory(ws)
    assert len(chunks) > 0      # Chunk'lar başarıyla üretilmiş olmalı

    # 5. Aşama: Embedding & Indeksleme (LanceDB veritabanı oluşturulması)
    embedded_count = build_index(ws)
    assert embedded_count > 0       # En az 1 satır veritabanına yazılmış olmalı

    # 6. Aşama: Hybrid Arama (Sorgu çalıştırma)
    # k=1 parametresi ile en yakın ilk sonucu istiyoruz ve reranker modelini aktif ediyoruz
    search_hits = search(ws, "MaviEjderha2026", k=1, rerank=True)

    # 7. Sonuçların Doğrulanması (Hata almamak için güvenli assertion'lar)
    assert len(search_hits) > 0     # En azından bir eşleşme dönmeli

    hit = search_hits[0]

    # İçeriğin eşleştiğini doğrula
    assert "MaviEjderha2026" in hit.content

    # Kaynak dökümanın adını doğrula
    assert Path(hit.source).name == "test_doc.md"

