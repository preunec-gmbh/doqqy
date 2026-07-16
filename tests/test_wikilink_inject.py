"""Wikilink marker bloğunun güvenli şekilde kaldırılmasını doğrulayan birim testleri."""

from __future__ import annotations

from doqqy.wikilink_inject import _strip_marker_block


def test_strip_marker_block_idempotency():
    # 1. Ham test metni (içerisinde doqqy link bloğu barındıran bir markdown içeriği)
    original_content = (
        "# Başlık\n"
        "Mevcut döküman içeriği buradadır.\n"
        "<!-- doqqy:links:start -->\n"
        "- [[biyoloji]]\n"
        "- [[kimya]]\n"
        "<!-- doqqy:links:end -->\n"
        "Döküman sonu metni."
    )

    # 2. İlk temizleme işlemi (marker bloğu kaldırılır)
    first_clean = _strip_marker_block(original_content)

    # 3. İkinci temizleme işlemi (marker bloğu zaten kaldırıldığı için bir şey değişmemeli)
    second_clean = _strip_marker_block(first_clean)

    # 4. Doğrulamalar (Assertion)
    # Temizlenmiş içerikte artık marker blokları bulunmamalıdır.
    assert "<!-- doqqy:links:start -->" not in first_clean
    assert "<!-- doqqy:links:end -->" not in first_clean
    assert "[[biyoloji]]" not in first_clean

    # Idempotency doğrulaması: İkinci kez temizlemek çıktıyı değiştirmemelidir (iki çıktı birbirine eşit olmalıdır)
    assert first_clean == second_clean

