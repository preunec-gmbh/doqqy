# Faz 4 — Obsidian Polish Implementation Notları

Bu belge Faz 4'ün planını, görev listesini ve implementation detaylarını içerir.

## 1. Durum Özeti

**⏳ Faz 4 BEKLEMEDE — Faz 3 tamamlandı (2026-06-02), Faz 4 planlandı (2026-06-06).**

## 2. Amaç

Faz 3 sonunda elimizde `topics.yaml` var: her section için `explicit_related` ve `might_be_related` listeleri. Ama bu veri yalnızca `INDEX.md`'de okunabilir formatta — Obsidian **graph view boş**, çünkü markdown dosyaları içinde hiç `[[wikilink]]` yok.

Faz 4 bu boşluğu dolduruyor:

- `processed/*.md` dosyalarının her biri `topics.yaml`'daki ilişkilerine göre güncellenir.
- Her dosyanın altına (ya da ilgili section'ın altına) `[[wikilink]]` satırları enjekte edilir.
- Obsidian vault'unda graph view otomatik olarak dolar — hiçbir manuel işlem gerekmez.

## 3. Temel Tasarım Kararları

| Karar | Gerekçe |
|---|---|
| Linkler dosya sonuna enjekte edilir (section sonuna değil) | Simpler implementation, Obsidian her dosyadaki tüm `[[...]]`'yi graph'a ekler — nerede olduğu önemli değil |
| Orijinal `processed/*.md` **yerinde güncellenir** (overwrite) | Idempotency: `doqqy inject` her çalıştırmada önceki enjeksiyonu temizleyip yeniden yazar |
| Marker blok kullanılır | `<!-- doqqy:links:start -->` / `<!-- doqqy:links:end -->` arasına yazılır — idempotent silme/yeniden yazma kolaylaşır |
| Üç link kategorisi ayrı gösterilir | `📌` explicit, `🔗` tematik (might_be) — kullanıcı güven seviyesini hemen görür |
| Sadece `processed/` değişir, `raw/` dokunulmaz | raw/ kaynak gerçeği, hiçbir zaman değiştirilmemeli |

## 4. Enjeksiyon Formatı

Her `processed/*.md` dosyasının **sonuna** aşağıdaki blok eklenir:

```markdown
<!-- doqqy:links:start -->
## Bağlantılar

### 📌 Explicit Referanslar
- [[SEQUENCE]] → Ödeme Akışı
- [[AUTH]] → JWT Yenileme

### 🔗 Tematik Bağlantılar
- [[PRISMA]] → Payment Model (0.83)
- [[WEBHOOK]] → Callback Handler (0.79)
- [[ENVIRONMENT]] → JWT Config (0.76)
<!-- doqqy:links:end -->
```

**Kurallar:**
- Bir dosyanın hiçbir section'ı bağlantı içermiyorsa blok eklenmez (dosya temiz kalır).
- Birden fazla section'dan gelen linkler tek blokta birleştirilir, tekrarlar dedupe edilir.
- Link hedefi dosya adından türetilir: `SEQUENCE.md` → `[[SEQUENCE]]`.
- Tematik linkler skora göre azalan sırada listelenir.

## 5. Modül: `wikilink_inject.py`

```
src/doqqy/wikilink_inject.py
```

**Sorumluluklar:**

1. `topics.yaml` oku → tüm section bağlantılarını bir lookup dict'e dönüştür: `{file: {explicit: [...], tematic: [...]}}`
2. `processed/*.md` dosyalarını tara
3. Her dosya için:
   a. Önceki `<!-- doqqy:links:start -->...<!-- doqqy:links:end -->` bloğu varsa sil
   b. Toplanan linkleri dedupe et ve sırala
   c. Link varsa yeni bloğu dosya sonuna yaz
4. Özet bas: kaç dosya güncellendi, kaç link enjekte edildi

**Fonksiyon imzası (taslak):**

```python
def inject_links(
    topics_path: Path = TOPICS_YAML,
    processed_dir: Path = PROCESSED_DIR,
    dry_run: bool = False,
) -> InjectionResult:
    ...
```

`dry_run=True` ile dosyaları değiştirmeden neyin enjekte edileceğini raporlar.

## 6. CLI Komutu

```
doqqy inject          # topics.yaml → processed/*.md içine [[link]] enjekte et
doqqy inject --dry-run  # Neyin enjekte edileceğini göster, dosyaları değiştirme
doqqy inject --topics path/to/topics.yaml  # Farklı topics dosyası
```

## 7. Obsidian Vault Testi

`processed/` klasörü Obsidian'da vault olarak açılır. Doğrulanacaklar:

- [ ] Graph view'da dosyalar arası kenar (edge) görünüyor mu?
- [ ] `INDEX.md`'den dosyalara tıklama navigasyonu çalışıyor mu?
- [ ] Explicit linkler (`📌`) ve tematik linkler (`🔗`) `INDEX.md`'de ayrı görünüyor mu?
- [ ] Hiç `[[...]]` içermeyen dosyalar graph'ta yalnız düğüm olarak mı görünüyor (beklenen)?
- [ ] Çok bağlantılı dosyalar (hub nodes) tespit edilebiliyor mu?

## 8. Dosya Değişiklikleri

| Dosya | Değişiklik |
|---|---|
| `src/doqqy/wikilink_inject.py` | **YENİ** — `topics.yaml` → `processed/*.md` enjeksiyon |
| `src/doqqy/cli.py` | `doqqy inject` komutu eklenir |
| `src/doqqy/config.py` | Gerekirse yeni sabit (marker string) |
| `processed/*.md` | Runtime'da güncellenir (kaynak kodu değil) |

## 9. Görev Listesi

- [ ] `src/doqqy/wikilink_inject.py` oluştur
  - [ ] `topics.yaml` okuma + file→links lookup dict üretimi
  - [ ] Marker blok silme (idempotent temizlik)
  - [ ] Explicit + tematik linkleri dedupe + sırala
  - [ ] Dosya sonuna blok enjeksiyonu
  - [ ] `--dry-run` modu
  - [ ] `InjectionResult` (güncellenen dosya sayısı, toplam link sayısı)
- [ ] `src/doqqy/cli.py` — `doqqy inject` komutu ekle (`--dry-run`, `--topics`)
- [ ] `processed/` klasörünü Obsidian'da vault olarak aç
- [ ] Graph view doğrulaması (edge'ler görünüyor mu)
- [ ] `INDEX.md`'den navigasyon testi
- [ ] Smoke test: `doqqy inject --dry-run` önce, sonra gerçek çalıştır

## 10. Riskler

| Risk | Olasılık | Çözüm |
|---|---|---
| Marker blok silme regex'i frontmatter veya kod bloğuyla çakışır | Düşük | Marker string'i yeterince unique tut (`<!-- doqqy:links:start -->`) |
| Aynı hedef dosyaya birden fazla section'dan link → tekrar | Orta | Set-based dedupe, ilk occurrence'ı koru |
| `topics.yaml`'da section ID → dosya adı eşlemesi bozulur | Düşük | ID formatı `FILENAME_section-slug` — `_` ile split, ilk parça dosya adı |
| Obsidian `[[LINK]]` büyük/küçük harf duyarlıysa | Düşük | Dosya adlarını uppercase olarak sakla (zaten öyle) |
| `doqqy inject` sonrası `doqqy map` tekrar çalışırsa eski enjeksiyonla çakışır | Orta | `doqqy inject` her çalışmada markerlı bloğu önce temizler — idempotent |

## 11. Faz Sonrası (Faz 4+ / Roadmap)

Faz 4 tamamlandıktan sonra sıradaki konular (öncelik sırası belirlenmedi):

- **Eval set:** 15-20 test sorusu + recall@5 metriği — retrieval kalitesini ölçmek için
- **Çoklu korpus / proje filtresi:** `--project paytr` ile sadece belirli alt kümeyi işle (`doqqy map`, `doqqy query`, `doqqy inject`)
- **Inkremental update:** Content hash bazlı diff — sadece değişen dosyaları yeniden işle
- **MCP server:** Claude Code entegrasyonu için doqqy'u MCP sunucusu olarak sun
- **Görsel caption üretimi:** Vision LLM ile PDF görsellerinden açıklama üret
