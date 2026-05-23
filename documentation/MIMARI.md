# Mimari

Bu belge sistemin **nasıl çalıştığını** açıklar: pipeline akışı, modüller arası bağlantı, veri yapıları ve LanceDB şeması.

## 1. Üst düzey görüntü

```
┌──────────┐   docq ingest   ┌─────────────┐   docq chunk   ┌────────────────┐
│  raw/    │ ──────────────► │ processed/  │ ─────────────► │ chunks/        │
│ .pdf .md │  format-spesifik│ kanonik .md │  header-aware  │ chunks.parquet │
│ .docx    │  parser'lar     │ + frontmtr  │  bölme         │ (pandas df)    │
│ .txt     │                 │             │                │                │
└──────────┘                 └─────────────┘                └────────┬───────┘
                                                                     │
                                                            docq embed
                                                                     ▼
                                                            ┌────────────────┐
                                                            │ store.lance/   │
                                                            │ chunks tablosu │
                                                            │ (vec + meta)   │
                                                            └────────┬───────┘
                                                                     │
                                                            docq query "..."
                                                                     ▼
                                                            ┌────────────────┐
                                                            │ top-k hits     │
                                                            │ ham chunk +    │
                                                            │ kaynak yolu    │
                                                            └────────────────┘
```

**Anahtar fikir:** Her aşama bağımsız çalıştırılabilir ve **deterministik**. `docq ingest`'i baştan çalıştırırsan `processed/`'i baştan yazar. Yeniden chunk'lamak istersen sadece `docq chunk`. Tam rebuild = sırayla 4 komut.

## 2. Aşamalar — detay

### 2.1 Ingest (`docq ingest`)

**Girdi:** `raw/` altındaki her dosya.
**Çıktı:** `processed/<aynı yapı>/<dosya>.md` (uzantı .md'ye çevrilmiş, kanonik markdown).

Akış:
1. `ingest/router.py` dosya uzantısına bakar, doğru parser'ı çağırır.
2. Parser, formata özgü yöntemle markdown üretir.
3. Sonucu YAML frontmatter (kaynak, tip, ingested_at, content_hash, parser) + body olarak yazar.
4. Bir dosya hata verirse pipeline **durmaz** — `logs/ingest.log`'a yazıp diğer dosyalarla devam eder. Sonuçta bir özet tablo basılır.

Parser eşlemesi:

| Uzantı | Ana parser | Fallback |
|---|---|---|
| `.md`, `.markdown` | python-frontmatter | — |
| `.txt` | UTF-8 decode + code block sarma | latin-1 (encoding hatasında) |
| `.pdf` | **docling** | **pymupdf4llm** |
| `.docx` | **pandoc** (pypandoc) | **mammoth** |

Pandoc CLI kurulu değilse `.docx` otomatik mammoth'a düşer (saf Python). PDF'lerde docling layout-aware çıktı verir; başarısız olursa pymupdf4llm daha hızlı ama basit bir alternatif sağlar.

### 2.2 Chunk (`docq chunk`)

**Girdi:** `processed/**/*.md`.
**Çıktı:** `chunks/chunks.parquet` (her satır bir `Chunk` kaydı).

Akış:
1. Her markdown dosyası açılır, frontmatter ayrılır.
2. `MarkdownHeaderTextSplitter` ile H1–H4 başlıklarına göre bölünür. Header metni içeride bırakılır (bağlam için).
3. Section çok uzunsa (> ~3200 karakter ≈ 800 token):
   - Atomik bloklar çıkarılır: ` ```...``` ` fenced code ve GFM tabloları **asla bölünmez**.
   - Geri kalan prose paragraf bazında bölünür (`\n\n+`).
   - Greedy packing: ardışık bloklar `MAX_CHARS` sınırına kadar toplanır.
   - Tek bir blok zaten büyükse (örn. devasa kod bloğu) kendi başına bir chunk olur.
4. Aynı doküman içindeki chunk'lar `prev_chunk` / `next_chunk` UUID'leriyle bağlanır (Faz 3'te bağlam genişletme için hazır).

### 2.3 Embed (`docq embed`)

**Girdi:** `chunks/chunks.parquet`.
**Çıktı:** `store.lance/chunks/` (LanceDB tablosu, vector + meta).

Akış:
1. `BAAI/bge-m3` modeli yüklenir (ilk çalıştırmada HuggingFace'ten ~2 GB iner, sonra cache'ten).
2. CPU/GPU otomatik tespit edilir (`torch.cuda.is_available()`); GPU'da fp16.
3. Chunk içerikleri batch'ler halinde (batch=12) dense vektöre dönüştürülür (1024 boyut).
4. LanceDB tablosuna `overwrite` ile yazılır.

Faz 2'de sparse vektör de eklenecek; şu an sadece dense.

### 2.4 Query (`docq query "..."`)

**Girdi:** Doğal dilli sorgu metni.
**Çıktı:** Top-k chunk + skor + kaynak yolu + section path.

Akış:
1. Model bir kez yüklenir (lru_cache).
2. Sorgu vektöre dönüştürülür.
3. LanceDB üzerinde cosine arama (`metric="cosine"`).
4. `score = 1.0 - distance` (büyük = daha iyi).
5. Sonuçlar terminal'e yazılır (varsayılan kısa, `--full` ile tam).

## 3. Veri modelleri

### 3.1 `Document` (ingest çıktısı)

```python
@dataclass
class Document:
    source_path: Path        # raw/auth/jwt.pdf
    processed_path: Path     # processed/auth/jwt.md
    content: str             # kanonik markdown body (frontmatter yok)
    metadata: dict           # bkz. aşağı
```

Frontmatter alanları:
- `source` — orijinal dosyanın projeye göre relative yolu
- `type` — `md` / `pdf` / `docx` / `txt`
- `ingested_at` — UTC ISO timestamp
- `content_hash` — body'nin SHA-256'sının ilk 16 hex'i (inkremental update için Faz 5'te kullanılacak)
- `parser` — PDF/DOCX için: hangi parser çalıştı (`docling`/`pymupdf4llm`/`pandoc`/`mammoth`)
- `original_<key>` — kaynak markdown'da varsa orijinal frontmatter alanları

### 3.2 `Chunk` (chunker çıktısı, embedder girdisi)

```python
@dataclass
class Chunk:
    chunk_id: str              # UUID4
    doc_id: str                # processed/.../foo.md (relative)
    source: str                # raw/.../foo.pdf (frontmatter'dan)
    doc_type: str              # md/pdf/docx/txt
    content: str               # chunk metni (header dahil)
    section_path: list[str]    # ["1. Auth", "1.2 JWT"]
    char_count: int
    prev_chunk: str | None     # aynı dokümandaki bir önceki chunk_id
    next_chunk: str | None
```

### 3.3 LanceDB tablo şeması (`store.lance/chunks/`)

Chunk dataclass'ının tüm alanları + iki ek:

| Kolon | Tip | Not |
|---|---|---|
| `chunk_id` | string | birincil anahtar (UUID) |
| `doc_id` | string | |
| `source` | string | orijinal kaynak |
| `doc_type` | string | |
| `content` | string | tam chunk metni |
| `section_path` | list<string> | başlık hiyerarşisi |
| `section_path_str` | string | `"H1 > H2 > H3"` — gösterim için |
| `char_count` | int64 | |
| `prev_chunk` | string \| null | |
| `next_chunk` | string \| null | |
| **`vector`** | **fixed_size_list<float32, 1024>** | bge-m3 dense |

## 4. Dosya organizasyonu

```
src/docq/
├── __init__.py            # version
├── __main__.py            # python -m docq → cli.app
├── cli.py                 # typer komutları (ingest, chunk, embed, query, info)
├── config.py              # yollar, sabitler, GPU detect, logger fabrikası
├── chunk.py               # MarkdownHeaderTextSplitter + atomik blok packing
├── embed.py               # bge-m3 yükleme + LanceDB yazımı
├── query.py               # cosine arama + SearchHit dataclass
└── ingest/
    ├── __init__.py
    ├── base.py            # Document, IngestResult, content_hash, base_metadata
    ├── md_ingest.py       # .md (frontmatter) + .txt (plain wrap)
    ├── docx_ingest.py     # pandoc → mammoth fallback
    ├── pdf_ingest.py      # docling → pymupdf4llm fallback
    └── router.py          # uzantı bazlı dispatch + toplu ingest + IngestResult
```

## 5. Tasarım kararları (özet)

| Karar | Neden |
|---|---|
| Pipeline her aşaması bağımsız komut | Tek bir aşamayı yeniden çalıştırmak (örn. yeni chunking ayarı) tam rebuild gerektirmesin. |
| Format-spesifik parser, sonrası format-agnostic | Yeni format (HTML, RST) eklemek sadece yeni bir ingester yazmak demek. Pipeline'ın geri kalanı dokunulmaz kalır. |
| Header-aware chunking | Section sınırları semantik sınırlardır; ortadan bölmek bağlamı kaybettirir. |
| Kod blokları + tablolar atomik | Bir SQL sorgusunu ortadan bölmek = anlamsız iki yarım. |
| `prev_chunk`/`next_chunk` bağlantısı | Bir chunk bulundu, ama yeterli bağlam vermiyorsa komşuları çekebilirsin. |
| LLM cevap sentezi YOK | Kullanıcı dokümanı **anlamak** istiyor, "özet" değil. Şeffaflık + ücretsiz + anlık. |
| Local-first embedding | Sorgu zamanında internet bağımlılığı yok; gizlilik bonus. |
| LanceDB (server'sız) | Dosya bazlı, taşınabilir, kurulum gerektirmez. |

Daha derin "neden" cevapları için `memory-bank/productContext.md` ve `memory-bank/systemPatterns.md`.

## 6. Performans beklentileri

| İşlem | Süre |
|---|---|
| Ingest (500 sayfa karışık format) | 15–30 dk |
| Chunk | <1 dk |
| Embed (CPU) | 15–30 dk |
| Embed (CUDA) | 2–3 dk |
| Tek sorgu | <1 sn |

İlk `docq embed` ekstra ~2 GB model indirme (tek seferlik, sonra cache'ten).

## 7. Sonraki faz nelerini değiştirir?

- **Faz 2** — sparse vektör eklenecek (`vector_sparse` kolonu), reranker top-50 → top-5 daraltacak. `query.py` Reciprocal Rank Fusion uygulayacak.
- **Faz 3** — Yeni bir `map.py` modülü; LLM çağrısı ile her dosya için section özetleri + cross-reference üretecek → `topics.yaml` + `INDEX.md`.
- **Faz 4** — `topics.yaml`'daki ilişkiler `processed/*.md` içine `[[wiki-link]]` olarak enjekte edilecek → Obsidian graph view.
