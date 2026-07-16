"""map_gen.py modülündeki yardımcı fonksiyonlar için birim testleri."""

from __future__ import annotations

from doqqy.map_gen import _normalize_target, _parse_sections, _section_id, _slug


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


def test_parse_sections_frontmatter_skip(tmp_path):
    # 1. Very first line is ---: skip frontmatter
    doc1 = tmp_path / "doc1.md"
    doc1.write_text(
        "---\ntitle: Doc\ntags: test\n---\n# Heading 1\nBody.",
        encoding="utf-8"
    )
    sections = _parse_sections(doc1)
    assert len(sections) == 1
    assert sections[0][0] == "# Heading 1"
    assert sections[0][2] == ["Body."]

    # 2. First line is NOT --- (e.g. empty or text): does not skip frontmatter (treated as body)
    doc2 = tmp_path / "doc2.md"
    doc2.write_text(
        "\n---\ntitle: Doc\n---\n# Heading 1\nBody.",
        encoding="utf-8"
    )
    sections = _parse_sections(doc2)
    # The first section is (başlıksız) and should contain the --- stuff
    assert len(sections) == 2
    assert sections[0][0] == "(başlıksız)"
    assert any("title: Doc" in line for line in sections[0][2])


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


def test_normalize_target_order():
    known_files = {"AUTHENTICATION.md", "AUTH.md"}
    # candidate AUTH should resolve to AUTH.md because it's an exact match
    res = _normalize_target("AUTH", known_files)
    assert res == "AUTH.md"

    known_files = {"AUTHENTICATION.md", "AUTHENTICATE.md"}
    # candidate AUTH (prefix matches both, neither is exact match) should resolve to AUTHENTICATE.md because it is shorter
    res = _normalize_target("AUTH", known_files)
    assert res == "AUTHENTICATE.md"
