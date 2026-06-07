# Faz 3 — Harita Üretimi Implementation Notları

Bu belge Faz 3'ün planını ve implementation detaylarını içerir.

## 1. Durum Özeti

**⏳ Faz 3 BEKLEMEDE — Faz 2 tamamlandı (2026-05-28), Faz 3 planlandı (2026-06-01).**

**Karar (2026-06-01):** Orijinal Seçenek D (LLM + embedding) iptal edildi.
- LLM çağrısı (Gemini / Claude) → gereksiz maliyet, dış bağımlılık, complexity
- Embedding zaten tematik ilişkiyi biliyor (bge-m3 zaten LanceDB'de)
- Regex explicit referansları zaten dokümanlarda var
- **Yeni plan: tamamen local, sıfır API maliyeti**

## 2. Amaç

Faz 2 sonunda elimizde güçlü bir arama motoru var ama **harita yok**:
- "Neye bakacağımı bilmiyorum" sorusu cevaplanamıyor
- Obsidian graph view boş — dosyalar arası hiç link yok
- `INDEX.md` yok — başlangıç noktası yok

Faz 3 bu boşluğu dolduruyor: `processed/*.md` dosyaları arasındaki ilişkileri iki yöntemle keşfedip `topics.yaml` + `INDEX.md` üretiyor.

## 3. İki Pass, LLM Yok

### Pass 1 — Regex (Explicit Referanslar)

`processed/*.md` dosyalarını tara, açık referansları yakala:

**Yakalanacak pattern'ler:**
- `bkz.` / `bkz:` + bir dosya/bölüm adı
- `see section` / `see also` + hedef
- Dosya adı pattern'leri (büyük harf, `.md` uzantısı, ya da bilinen dosya adları listesi)
- Parantez içi referanslar: `(SEQUENCE.md)`, `(bkz. AUTH)`

**Çıktı:** Her section için `explicit_related` listesi — hedef dosya + hedef section (varsa) + kaynak satır numarası.

**Not:** Bu ilişkiler asimetrik olabilir (A → B ama B → A yok). Her ikisi de `topics.yaml`'a yazılır, `wikilink_inject.py` her iki yönde de link oluşturur.

### Pass 2 — Embedding Cosine (Tematik Komşular)

LanceDB'de zaten her chunk'ın dense vektörü var. Her section için:

1. O section'ın tüm chunk'larının vektörlerini al
2. Ortalama vektörü hesapla (section centroid)
3. LanceDB'den top-N cosine komşu sorgula (farklı dosyadan olanlar)
4. Eşik üstündekiler (örn. cosine > 0.75) → `might_be_related`

**Çıktı:** Her section için `might_be_related` listesi — hedef section + cosine skoru.

**Not:** Aynı dosyadaki chunk'lar filtrelenir (zaten aynı dosyada konuşlandırılmış).

## 4. Çıktı Formatları

### `topics.yaml`

```yaml
sections:
  - id: "SEQUENCE_payment-flow"        # dosyaadi_sectionslug
    file: "SEQUENCE.md"
    section: "## Ödeme Akışı"
    explicit_related:
      - target_id: "PRISMA_payment-model"
        target_section: "## Payment Model"
        source_line: 42
    might_be_related:
      - target_id: "AUTH_jwt-flow"
        target_section: "## JWT Akışı"
        score: 0.81
      - target_id: "WEBHOOK_callback"
        target_section: "## Callback Handler"
        score: 0.77
```

### `INDEX.md`

```markdown
# Doküman İndeksi

## SEQUENCE.md
### Ödeme Akışı
📌 Explicit: [[PRISMA]] → Payment Model
💡 İlgili olabilir: [[AUTH]] → JWT Akışı (0.81), [[WEBHOOK]] → Callback Handler (0.77)
```

## 5. Dosya Değişiklikleri

| Dosya | Açıklama |
|---|---|
| `src/doqqy/map_gen.py` | Pass 1 (regex) + Pass 2 (embedding cosine) → `topics.yaml` |
| `src/doqqy/index_gen.py` | `topics.yaml` → `INDEX.md` |
| `src/doqqy/cli.py` | `doqqy map` ve `doqqy index` komutları eklenir |
| `topics.yaml` | Proje kökünde üretilir (gitignore'a eklenebilir) |
| `processed/INDEX.md` | `processed/` klasörüne yazılır (Obsidian vault'un giriş noktası) |

## 6. CLI Komutları

```
doqqy map          # Pass 1 + Pass 2 → topics.yaml üret
doqqy map --pass1  # Sadece regex pass
doqqy map --pass2  # Sadece embedding pass
doqqy index        # topics.yaml → INDEX.md üret
```

## 7. Görev Listesi

- [ ] `src/doqqy/map_gen.py` oluştur
  - [ ] **Pass 1:** `processed/*.md` okuma + regex pattern'leri
  - [ ] **Pass 1:** Section boundary tespiti (başlık satırları)
  - [ ] **Pass 1:** Pattern eşleştirme + hedef normalizasyonu
  - [ ] **Pass 2:** Her section için chunk vektörlerini LanceDB'den çek
  - [ ] **Pass 2:** Section centroid hesabı (ortalama vektör)
  - [ ] **Pass 2:** Cosine top-N sorgu (farklı dosya filtresi + eşik)
  - [ ] **Birleştirme:** `topics.yaml` schema + yazımı
- [ ] `src/doqqy/index_gen.py` oluştur
  - [ ] `topics.yaml` okuma
  - [ ] `INDEX.md` template + yazımı (📌 explicit, 💡 might_be)
- [ ] `src/doqqy/cli.py` — `doqqy map` + `doqqy index` komutları ekle
- [ ] 5 dosyalık test korpusunda (`test_docs/`) çalıştır, çıktı kalitesini gözden geçir
- [ ] `processed/` klasörüne `INDEX.md` yaz, Obsidian'da aç

## 8. Riskler

| Risk | Olasılık | Çözüm |
|---|---|------|
| Regex pattern'leri Türkçe varyantları kaçırır | Orta | Pattern listesini test sonrası genişlet |
| Section centroid vektörü anlamsız (çok heterojen chunk'lar) | Düşük | Chunk sayısı fazlaysa medoid kullan |
| Cosine eşiği çok düşük — gürültülü ilişkiler | Orta | 0.75 başlangıç, test sonrası ayarla |
| Farklı dosya filtresi bozulur (aynı dosya kendi kendini önerir) | Düşük | `file != source_file` kontrolü yeterli |
| `processed/` klasöründe section boundary yanlış tespit | Orta | `##` / `###` başlıkları yeterli, frontmatter'ı atla |

## 9. Gelecekte Konuşulacak: Çoklu Korpus / Proje Filtresi

> **Not (2026-06-01):** Korpus tek bir proje veya konuya ait olmayabilir. Örneğin `raw/` altında PayTR + ERP12 + ERIMELEKTRONIK + GENEL belgeler karışık duruyor. Bu durumda:
> - `doqqy map --project paytr` → sadece PayTR dokümanlarının haritasını çıkar
> - `doqqy query "..." --project erp12` → sadece ERP12 chunk'larında ara
> - Harita üretirken farklı projeler arası ilişkileri ayrı kategoride göster ya da filtrele
>
> Nasıl yapılacağı (klasör bazlı mı, metadata bazlı mı, prefix bazlı mı) daha sonra konuşulacak ve Faz 3 görev listesine eklenecek.

## 10. Faz 4 ile İlişki

Faz 3 çıktısı (`topics.yaml`) Faz 4'ün tek girdisi:
- `wikilink_inject.py`: Her `processed/*.md` dosyasına ilgili section'lardan `[[link]]` enjekte eder
- Obsidian graph view bu linkleri görsel ağ olarak gösterir
- Faz 3 kaliteli çıktı üretmezse Faz 4'ün değeri düşer — küçük korpusta test zorunlu
