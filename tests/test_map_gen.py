"""map_gen.py modülündeki yardımcı fonksiyonlar için birim testleri."""

from __future__ import annotations

import pytest
from doqqy.map_gen import _slug, _section_id, _normalize_target

def test_slug():
    # Türkçe ve özel karakterler içeren bir başlığı slug formatına dönüştürmeyi test eder
    input_title = "C++ Programlama Dili ve Nesne Yönelimli Programlama!"
    # Fonksiyon '+' karakterini siler ve Türkçe karakterleri (ö) olduğu gibi korur
    expected_output = "c-programlama-dili-ve-nesne-yönelimli-programlama"
    assert _slug(input_title) == expected_output

def test_section_id():
    # Markdown başlık id'lerinin standartlaştırılmasını test eder
    input_filename = "SSS.md"
    input_header = "3. Sıkça Sorulan Sorular"
    # SSS.md -> stem.upper() = SSS
    # "3. Sıkça Sorulan Sorular" -> slug = "3-sıkça-sorulan-sorular"
    expected_output = "SSS_3-sıkça-sorulan-sorular"
    assert _section_id(input_filename, input_header) == expected_output

def test_normalize_target():
    # Link hedeflerinin (target) temizlenmesini ve standartlaştırılmasını test eder
    input_target = "muhasebe_raporu.md"
    
    # map_gen.py içinde known_files, f.name değerlerinden oluşur (yani klasörsüz, sadece dosya adı + uzantı)
    known_files = {
        "muhasebe_raporu.md",
        "baska_dosya.md"
    }
    
    result = _normalize_target(input_target, known_files)
    
    assert result is not None
    assert result == "muhasebe_raporu.md"

