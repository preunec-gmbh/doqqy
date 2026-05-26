# Sistem Pattern'leri

## Genel Mimari

```
raw/  →  processed/  →  chunks/  →  [store.lance + topics.yaml]  →  Obsidian / CLI
 │         │             │             │
 │         │             │             └─→ INDEX.md (generate edilir)
 │         │             │
 │         │             └─→ chunk-bazlı arama
 │         │
 │         └─→ Obsidian vault olarak açılabilir (kanonik markdown + wiki-link'ler)
 │
 └─→ Orijinal dosyalar (md, pdf, docx) — dokunulmaz
```

## Pipeline Aşamaları

Her aşama **deterministik ve tekrar çalıştırılabilir**. Sıralama:

1. **Ingest:** `raw/*` → `processed/*.md` (+ metadata frontmatter)
2. **Chunk:** `processed/*.md` → `chunks/chunks.parquet`
3. **Embed:** chunks → `store.lance` (dense + sparse vektör)
4. **Map:** `processed/*` → `topics.yaml` → `INDEX.md` (LLM ile, tek seferlik)
5. **Wiki-link enjeksiyonu:** `topics.yaml` → `processed/*.md` içine `[[link]]` ekle

Aşamalar bağımsız CLI komutu olarak çalıştırılabilir.

## Temel Teknik Kararlar

### Format-Agnostic Core
İngest'ten sonra her şey markdown. Pipeline'ın geri kalanı (chunk, embed, query) format bilmez. Yeni bir format eklemek (HTML, RST vb.) sadece yeni bir ingester yazmak demek.

### Hibrit Retrieval (Dense + Sparse)
bge-m3 modeli aynı anda hem **dense vektör** (semantic similarity) hem **sparse vektör** (lexical / token-level) üretiyor. İkisini birleştirerek:
- **Dense:** "kimlik doğrulama" sorgusu "authentication" chunk'ını bulur (semantic).
- **Sparse:** "JWT_REFRESH_SECRET" sorgusu tam o token'ın geçtiği chunk'ı bulur (lexical).

İkisini **Reciprocal Rank Fusion** ile birleştir. Bu pattern ekstra BM25 motoru kurma ihtiyacını ortadan kaldırır.

### Reranking Mecburi
İlk retrieval (dense + sparse) top-50 getirir. Çoğu noise. `bge-reranker-v2-m3` cross-encoder ile top-50 → top-5 daraltılır. Reranker, sorgu ile chunk'ı **birlikte** görüp gerçek alakayı ölçer (embedding'in göremediği nüansı yakalar).

### Section-Bazlı Harita, Dosya-Bazlı Batch
Harita section seviyesinde tutulur (her `##` / `###` için özet, kavramlar, çapraz referanslar). Ama LLM çağrıları **dosya bazında batch**'lenir: her dosyayı tek seferde LLM'e gönder, "her section için ayrı özet üret" de.

- Granülarite: section (yüksek kalite)
- Maliyet: dosya seviyesi (30 çağrı, ücretsiz tier'a sığar)

### Üç Kaynaklı İlişki Modeli (Seçenek D)
İlişkiler **üç ayrı kanaldan** üretilir ve `topics.yaml`'da ayrı kategoriler olarak tutulur. Tek havuza karıştırılmaz çünkü her birinin güven derecesi ve "neden ilgili" cevabı farklı.

| Kategori | Kaynak | Güven | Anlamı |
|---|---|---|---|
| `explicit_related` | LLM + regex (per-file pass) | Yüksek | Yazıda açık geçiyor ("bkz. Bölüm 3.2") |
| `thematic_related` | LLM (per-file + meta pass) | Orta-Yüksek | LLM "bu iki bölüm konseptik olarak bağlı" diyor |
| `might_be_related` | bge-m3 dense embedding (cosine) | Skorlu | Vektör uzayında yakın, skoru kullanıcı görüyor |

**Agreement sinyali:** Bir section hem LLM tarafından `thematic_related` deniyorsa hem embedding'in top-N'inde varsa → `llm_also_listed: true` flag'iyle işaretlenir. Bu **en güçlü** bağlantı sinyali (iki bağımsız yöntem aynı şeyi söylüyor).

### Wiki-Link Tabanlı İlişkiler
`topics.yaml`'daki üç kategori, `processed/` altındaki markdown dosyalarına `[[link]]` olarak enjekte edilir. Obsidian graph view ilişkileri otomatik gösterir. Render kuralları:

- **`explicit_related`** → kalın edge / 📌 prefix
- **`thematic_related`** → normal edge / 🔗 prefix
- **`might_be_related`** → kesik çizgi edge / 💡 prefix + skor (✓ = LLM ile agreement)

Üç tip görsel olarak ayrılır ki kullanıcı şüpheli olduğunda hangi kanaldan geldiğini bilsin.

## Bileşen İlişkileri

### Ingest Modülleri

```
src/ingest/
├── base.py          # Document dataclass + ortak interface
├── md_ingest.py     # frontmatter merge, içerik koru — _processed_path resolve() fix
├── docx_ingest.py   # pandoc (auto-download) çağrısı, fallback mammoth — _processed_path resolve() fix
├── pdf_ingest.py    # docling çağrısı, fallback pymupdf4llm — _processed_path resolve() fix
└── router.py        # uzantıya göre delegasyon
```

`router.py` uzantıya bakar, doğru ingester'a yönlendirir. Tüm ingester'lar aynı `Document` dataclass'ını döner — bu yüzden pipeline'ın geri kalanı format bilmez.

### Document Dataclass

```python
@dataclass
class Document:
    source_path: Path           # raw/auth/jwt.pdf
    processed_path: Path        # processed/auth/jwt.md
    content: str                # kanonik markdown
    metadata: dict              # {source, type, ingested_at, content_hash, ...}
```

### Chunk Dataclass

```python
@dataclass
class Chunk:
    chunk_id: str               # UUID
    doc_id: str                 # source dosya
    content: str
    section_path: list[str]     # ["Authentication", "3.2 Token Yenileme"]
    page: int | None            # PDF için sayfa numarası
    prev_chunk: str | None
    next_chunk: str | None
```

### topics.yaml Şeması (Seçenek D)

```yaml
sections:
  - id: auth/jwt-flow.pdf#3.2-token-yenileme
    file: auth/jwt-flow.pdf
    heading_path: ["3. Authentication", "3.2 Token Yenileme"]
    page: 23
    summary: "Refresh token rotation mekanizması..."
    concepts: ["refresh token", "rotation", "blacklist"]

    # Kategori 1 — LLM açık referans (regex doğrulamalı)
    explicit_related:
      - { id: auth/jwt-flow.pdf#4.0-blacklist, source: "see-ref" }

    # Kategori 2 — LLM tematik yorum (per-file + meta pass)
    thematic_related:
      - { id: auth/session-storage.md#cache-stratejisi, reason: "Cache mekanizması paylaşılıyor" }
      - { id: security/best-practices.docx#4.1-token-guvenligi, reason: "Token güvenlik prensiplerine atıfta bulunuyor" }

    # Kategori 3 — Embedding cosine (LanceDB top-N)
    might_be_related:
      - { id: auth/session-storage.md#cache-stratejisi, score: 0.84, llm_also_listed: true }
      - { id: api/middleware.md#auth-check, score: 0.78, llm_also_listed: false }
      - { id: security/best-practices.docx#4.1-token-guvenligi, score: 0.76, llm_also_listed: true }
```

`INDEX.md` bu yaml'dan generate edilir, üç kategori farklı render edilir (kalın / normal / kesik çizgi edge'ler).

## Kritik Implementation Yolları

### Ingest'te Hata Yönetimi
Bir dosya parse edilemezse:
1. Hatayı `logs/ingest.log`'a yaz (dosya yolu + hata + stack trace).
2. Pipeline'ı **durdurma** — diğer dosyalarla devam et.
3. Başarısız dosyaları sonda raporla (özet tablo).

Bir bozuk PDF tüm korpusu durdurmasın.

### Chunk Sınırları
- Kod blokları (` ``` `) **asla bölünmez**.
- Tablolar **asla bölünmez**.
- Başlık altı çok kısaysa (örn. <100 token), bir sonraki section ile birleştir.
- Çok uzunsa (>1000 token) recursive char splitter ile böl, ama section_path metadata'sını bütün parçalara aynen taşı.

### Cross-Reference Tespiti (Harita Üretiminde — Seçenek D, üç pass)

**Pass 1 — Per-file LLM (~30 çağrı):**
Her dosya tek başına LLM'e gider. Prompt yaklaşık:

> "Bu dosyanın her ## / ### bölümü için şunu üret: (1) 2-3 cümlelik özet, (2) 3-5 anahtar kavram, (3) yazıda açıkça geçen referanslar — 'bkz. Bölüm 3', 'auth_flow.md'de anlatıldığı gibi' gibi (`explicit_related`), (4) sezdiğin tematik bağlantılar — bu bölüm hangi diğer dosya/bölümle aynı konuyu işliyor (`thematic_related`)."

Regex ön-filtre `bkz\.?\s+|see\s+section|→\s*\w` gibi pattern'lerle açık referansları yakalar ve LLM çıktısını doğrular.

**Pass 2 — Meta LLM (1 çağrı):**
Tüm dosyaların özetleri birden LLM'e verilir:

> "Şu section özetlerini incele. Hangi çiftler tematik olarak güçlü bağlı? Pass 1'de kaçırılmış olabilecek çapraz dosya bağlantılarını çıkar."

Çıktı pass 1'in `thematic_related` listesini zenginleştirir.

**Pass 3 — Embedding (LLM yok, anlık):**
Faz 1'de üretilmiş dense vektörler kullanılır. Her section için LanceDB'den top-N cosine neighbor çekilir → `might_be_related` (skorlu).

**Birleştirme:**
- Üç kategori `topics.yaml`'a ayrı yazılır.
- Pass 3 listesinde her item için pass 2 thematic listesinde de varsa `llm_also_listed: true` → **agreement sinyali**.
- Üç kategori farklı render edilir (kalın/normal/kesik çizgi edge'ler, emoji prefix'leri).

### LLM Fallback Stratejisi
1. Önce Gemini 2.5 Pro free tier ile harita üret.
2. Çıktıyı gözle değerlendir.
3. Tatminkâr değilse aynı promptu Claude Opus 4.7 ile çalıştır.
4. Bu adım kullanıcı kararı (otomatik fallback yok).
