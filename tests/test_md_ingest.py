"""Markdown ingest aşamasındaki YAML frontmatter düzeltme işlemi için birim testleri."""

from __future__ import annotations

import pytest
from doqqy.ingest.md_ingest import _try_fix_yaml_frontmatter

def test_try_fix_yaml_frontmatter_repairs_unquoted_colons():
    # 1. Hatalı YAML içeren frontmatter bloğu (unquoted colons barındırıyor)
    bad_frontmatter = (
        "---\n"
        "title: Proje Raporu: Bölüm 1\n"
        "project: doqqy: Akıllı Doküman Analiz Sistemi\n"
        "team: Geliştirme Takımı: Ekip A\n"
        "---\n"
        "Normal döküman içeriği buraya geliyor."
    )
    
    # 2. Fonksiyonun hatalı kısımları düzeltmesini bekliyoruz
    fixed_frontmatter = _try_fix_yaml_frontmatter(bad_frontmatter)
    
    # 3. Beklenen düzeltilmiş formatlar (iki noktalardan sonrasının tırnak içine alınması)
    assert 'title: "Proje Raporu: Bölüm 1"' in fixed_frontmatter
    assert 'project: "doqqy: Akıllı Doküman Analiz Sistemi"' in fixed_frontmatter
    assert 'team: "Geliştirme Takımı: Ekip A"' in fixed_frontmatter
    
    # 4. Eğer frontmatter'da sorun yoksa veya hedef alanlar dışındaysa dokunmamalıdır
    good_frontmatter = (
        "---\n"
        "title: \"Zaten Düzgün Bir Başlık\"\n"
        "status: active\n"
        "---\n"
    )
    assert _try_fix_yaml_frontmatter(good_frontmatter) == good_frontmatter

