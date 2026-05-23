# Faz 1 — MVP Implementation Notları

Bu belge Faz 1'in tamamlanmış halini kayıt altına alır. Implementation sırasında plana göre verilen ek kararları ve "neden böyle yazıldı" gerekçelerini açıklar.

## 1. Durum Özeti

**🟡 Faz 1 kod + kısmi smoke test tamam (2026-05-23). Tam smoke test (PDF/DOCX/TXT) bekliyor.**

- Proje iskeleti (`pyproject.toml`, `.gitignore`, `.env.example`, klasörler).
- `docs/` → `raw/` kopyası (320 dosya, ama içinde docx ve düzgün .txt yok).
- `.venv/` Python 3.10 + tüm bağımlılıklar (torch 2.12 CPU, docling 2.95, FlagEmbedding 1.4, lancedb 0.30, pymupdf4llm, mammoth, pypandoc vb.).
- 4 format için ingest katmanı (md, txt, pdf, docx) — **kodlandı**.
- Header-aware chunking (kod/tablo atomik).
- bge-m3 dense embedding + LanceDB yazımı.
- Cosine dense sorgu.
- Typer CLI: `ingest`, `chunk`, `embed`, `query`, `info`.
- Windows console UTF-8 + rich legacy renderer bypass (`cli.py`).

**Smoke test sonuçları (5 MD dosyası):**
- Ingest: 5/5 başarılı, <1 sn.
- Chunk: 42 chunk → `chunks/chunks.parquet`.
- Embed: bge-m3 ~2 GB indirme (tek seferlik) + 42 vektör → `store.lance/chunks/` (CPU'da ~66 sn).
- Query: Türkçe sorgular doğru top-k chunk döndürüyor, kaynak + section path düzgün.

**Smoke test eksik kısmı:** PDF/DOCX/TXT ingester'ları kodlandı ama gerçek dosyada **test edilmedi**. raw/'da DOCX yok, kullanılabilir TXT yok (PROCEDURES'taki .txt'ler stored procedure dump'ları — atlanmış sıralamada ilk 5'e girmedi). Kullanıcı internetten örnek dosyalar getirip o üçünü de test edecek.

**Retrieval kalitesi gözlemi:** Sparse vektör + reranker yok → ilk sırada "yakın ama tam isabet değil" sonuçlar olabiliyor (örn. "PayTR odeme akisi" sorgusunda SEQUENCE.md'de tam karşılık var ama PRISMA.md skoru daha yüksek çıktı). Faz 2 ile düzelecek — beklenen davranış.

## 2. Dosya Yapısı

```
puroje/
├── pyproject.toml              # paket metadata + tüm bağımlılıklar
├── .env.example                # GEMINI_API_KEY, ANTHROPIC_API_KEY placeholder
├── .gitignore                  # generated klasörler + .env + .venv
├── raw/                        # docs/'tan kopya, ingest girdisi (gitignore'da)
├── processed/                  # ingest çıktısı, kanonik markdown (gitignore'da)
├── chunks/chunks.parquet       # chunker çıktısı (gitignore'da)
├── store.lance/                # LanceDB tablosu (gitignore'da)
├── logs/                       # ingest.log vb. (gitignore'da)
├── memory-bank/                # bu klasör
└── src/docq/
    ├── __init__.py
    ├── __main__.py             # python -m docq → cli.app
    ├── cli.py                  # typer komutları
    ├── config.py               # yollar, sabitler, GPU detect, logger
    ├── chunk.py                # header-aware chunking
    ├── embed.py                # bge-m3 dense + LanceDB yazımı
    ├── query.py                # cosine arama
    └── ingest/
        ├── __init__.py
        ├── base.py             # Document, IngestResult, helpers
        ├── md_ingest.py        # .md + .txt
        ├── docx_ingest.py      # pandoc → mammoth fallback
        ├── pdf_ingest.py       # docling → pymupdf4llm fallback
        └── router.py           # uzantı bazlı dispatch + toplu ingest
```

## 3. Pipeline Akışı

```
raw/<her şey>
   │
   ▼ docq ingest        (router.py uzantıya göre delegasyon)
processed/<aynı dizin>/<orijinal>.md     (frontmatter + body)
   │
   ▼ docq chunk          (MarkdownHeaderTextSplitter + atomik kod/tablo)
chunks/chunks.parquet                     (Chunk dataclass'ları, prev/next bağlı)
   │
   ▼ docq embed          (bge-m3 dense, batch=12)
store.lance/chunks/                       (LanceDB tablosu, vector + meta)
   │
   ▼ docq query "..."    (cosine, top-k=5)
stdout                                    (score + source + section_path + content)
```

## 4. Modüller — Detay

### 4.1 `config.py`
Tüm yollar buradan türetilir; her modül `from docq.config import ...` ile alır. Önemli sabitler:

| Sabit | Değer | Not |
|---|---|---|
| `SUPPORTED_EXTENSIONS` | `{.md, .markdown, .pdf, .docx, .txt}` | Kod örnekleri (`.py`, `.php`, `.js`, `.cs`, `.aspx`, `.dll`, `.html`, `.ejs`, `package.json`) **dahil edilmez** — memory-bank scope'una uygun. |
| `CHUNK_MAX_TOKENS` | 800 | Yaklaşık; karaktere oranı `*4`. Faz 2'de gerçek tokenizer ile değiştirilebilir. |
| `CHUNK_MIN_MERGE_TOKENS` | 100 | Şu an kullanılmıyor — kısa section merge MVP'ye girmedi. |
| `EMBEDDING_MODEL` | `BAAI/bge-m3` | |
| `EMBEDDING_DIM` | 1024 | bge-m3 dense vektör boyutu |
| `EMBEDDING_BATCH_SIZE` | 12 | Düşük tutuldu — büyük chunk'lar tek batch'te belleği zorlamasın diye |
| `DEFAULT_TOP_K` | 5 | |

`detect_device()` — `DOCQ_DEVICE` env varsa onu, yoksa `torch.cuda.is_available()` sonucuna göre `cuda`/`cpu` döndürür. Torch import maliyetinden kaçınmak için lazy.

`get_logger(name, log_file)` — stream + opsiyonel dosya handler. Çift handler önler.

### 4.2 `ingest/base.py`
Tüm ingester'ların döndürdüğü `Document` dataclass'ı:

```python
@dataclass
class Document:
    source_path: Path        # raw/.../foo.pdf
    processed_path: Path     # processed/.../foo.md
    content: str             # kanonik markdown body
    metadata: dict           # source, type, ingested_at, content_hash, parser?
```

`Document.write()` — `processed_path`'e YAML frontmatter + body yazar. Klasör otomatik oluşur.

`IngestResult` — succeeded/failed/skipped listeleri tutan rapor objesi. CLI bunu yazdırır.

`content_hash(text)` — SHA-256 kısaltması (16 hex). Faz 5 inkremental update için hazır.

### 4.3 `ingest/md_ingest.py`
- **`.md`** — `frontmatter.load(fh)` ile YAML frontmatter ayrıştırılır, body korunur. Orijinal frontmatter alanları `original_<key>` prefix'iyle metadata'ya taşınır (collision'dan kaçınmak için).
- **`.txt`** — Dosya adından `# Title` üretilir, gövde tek bir fenced code block içine sarılır (markdown'da düzgün görünsün diye). UTF-8 decode başarısız olursa latin-1 fallback (Windows'ta yaygın).

### 4.4 `ingest/pdf_ingest.py`
1. **docling** denenir — `DocumentConverter().convert(...).document.export_to_markdown()`.
2. Başarısız olursa veya boş döner → **pymupdf4llm** denenir.
3. İkisi de başarısızsa `IngestError` fırlatılır, router log'a yazıp diğer dosyalarla devam eder.
4. Hangi parser'ın çalıştığı `metadata.parser` alanına yazılır.

Memory-bank planına uygun.

### 4.5 `ingest/docx_ingest.py` *(yeni eklendi)*
1. **pypandoc** (pandoc CLI'yi sarar) ile `gfm` formatına dönüştürmeyi dener.
   - `--wrap=none` — satır sarma yok.
   - `--standalone=false` — sadece body, header/template yok.
2. pandoc CLI kurulu değilse `OSError` fırlatır → otomatik **mammoth** fallback'e geçer.
3. mammoth saf Python, sistem bağımlılığı yok (`pip install mammoth` yeterli).
4. İkisi de başarısızsa `IngestError`.

> Şu anki `raw/`'da `.docx` yok ama format desteklenmek istendi — ileride gelecek dosyalar için hazır.

### 4.6 `ingest/router.py`
- `_DISPATCH` — `{".md": ingest_md, ".pdf": ingest_pdf, ...}` haritası.
- `ingest_file(path)` — tek dosya, uzantıya göre delege eder.
- `ingest_directory(root, limit=None)` — `tqdm` ile ilerleme, **bir dosya hata verirse durmaz**, `IngestResult.failed` listesine ekler ve `logs/ingest.log`'a yazar. `limit` argümanı test için ilk N dosya.

### 4.7 `chunk.py`
İki aşamalı chunking:

1. **Header split** — `MarkdownHeaderTextSplitter` ile H1..H4. Header metni içeride bırakılır (`strip_headers=False`) ki chunk içeriği bağlamı korusun.
2. **Length split** — Section çok uzunsa (> `_MAX_CHARS = 3200`):
   - **Atomik bloklar** çıkarılır: fenced code (` ``` ... ``` `) ve GFM tabloları. Bunlar **asla bölünmez**.
   - Geri kalan prose paragraf bazında bölünür (`\n\n+` regex).
   - `_pack_blocks(...)` greedy şekilde ardışık blokları `_MAX_CHARS` sınırına kadar toplar.
   - Tek bir blok zaten `_MAX_CHARS`'tan büyükse (örn. devasa kod bloğu) kendi başına chunk olur — kayıp yok.

`Chunk` dataclass'ı:

```python
@dataclass
class Chunk:
    chunk_id: str             # UUID4
    doc_id: str               # processed/.../foo.md (relative path)
    source: str               # frontmatter'dan: orijinal raw/.../foo.pdf yolu
    doc_type: str             # md/pdf/txt/docx
    content: str
    section_path: list[str]   # ["1. Auth", "1.2 JWT", ...]
    char_count: int
    prev_chunk: str | None    # aynı dokümandaki bir önceki chunk_id
    next_chunk: str | None    # aynı dokümandaki bir sonraki chunk_id
```

Çıktı: `chunks/chunks.parquet` (pandas → parquet, hızlı + sıkıştırılmış).

**MVP'de yapılmayan**: kısa section merge (memory-bank "<100 token ise birleştir" diyor, atlandı), token bazlı bölme (gerçek tokenizer Faz 2'de).

### 4.8 `embed.py`
1. `chunks/chunks.parquet` okunur.
2. `BGEM3FlagModel(EMBEDDING_MODEL, use_fp16=(device=="cuda"), device=device)` — GPU varsa fp16.
3. Batch'ler halinde dense vektör üretilir (`return_dense=True, return_sparse=False`). Sparse Faz 2.
4. Vektörler `df["vector"]`'a list olarak konur.
5. LanceDB'ye `create_table(..., mode="overwrite")` ile yazılır.
6. Helper: `section_path_str = " > ".join(section_path)` — okunabilir gösterim için ek kolon.

`max_length=8192` — bge-m3'ün max context'i; uzun chunk'larda truncation olur ama 3200 char'lık chunk'lar burada güvenli.

### 4.9 `query.py`
1. `BGEM3FlagModel` `lru_cache(1)` ile bir kez yüklenir (sorgular arasında bellekte kalır).
2. LanceDB tablosu `lru_cache(1)`.
3. Sorgu metni → dense vektör → `table.search(qvec).metric("cosine").limit(k).to_list()`.
4. LanceDB cosine **distance** döndürür → `score = 1.0 - distance` (büyük = daha iyi).
5. `SearchHit` dataclass'ı: score, doc_id, source, section_path, content, extra.

### 4.10 `cli.py`
Typer ile 5 komut:

| Komut | Ne yapar | Önemli flag |
|---|---|---|
| `docq ingest [-s DIR] [-n N]` | raw/ → processed/ | `-n` test için ilk N dosya |
| `docq chunk [-p DIR]` | processed/ → chunks.parquet | |
| `docq embed` | chunks → store.lance | İlk çağrıda model iner (~2 GB) |
| `docq query "..." [-k 5] [--full]` | dense arama, top-k göster | `--full` chunk'ı tam göster |
| `docq info` | pipeline durumu özeti | |

`python -m docq <cmd>` veya `pip install -e .` sonrası `docq <cmd>` çalışır.

## 5. Plana Göre Verilen Ek/Değişen Kararlar

| Konu | Plan | Implementation | Gerekçe |
|---|---|---|---|
| Python sürümü | 3.11+ | 3.10.11 (mevcut) | Kullanılan paketlerin hepsi 3.10'da çalışıyor; sürüm yükseltmeden zaman kazanıldı. |
| `.txt` formatı | Plan dışı | Eklendi (md ingester'da) | `docs/PROCEDURES/*.txt` (SQL stored proc) ve `tablolara_doğru.txt` referans içerik — kullanıcı onayıyla. |
| `.docx` | Plana göre | Saklandı + mammoth fallback eklendi | pandoc CLI kurulu değil; mammoth pure-Python, ilk çağrıda otomatik fallback. |
| Kod örnekleri (`.py`, `.php`, `.js`, `.cs` ...) | — | Atlandı (router uzantı whitelist'i) | Embedding kalitesini kirletmemek için; PDF'lerin yanında zaten örnek olarak yer alıyorlar. |
| Kısa section merge | "<100 token ise birleştir" | Atlandı | MVP basit kalsın; eval set'le ölçüldükten sonra eklenir. |
| Chunk overlap | 100 token | 0 (overlap yok) | MVP'de yok; gerek olursa parametre zaten var. |
| Token bazlı bölme | "MarkdownHeaderTextSplitter + recursive char" | Header split + atomik blok packing | Recursive char yerine code/table'ı koruyan custom packing — daha güvenli. |
| Logging | "tqdm + logging" | `config.get_logger()` (stream + opsiyonel file handler) + tqdm | Çift handler önleyici tek girişli helper. |

## 6. Ortam / Kurulum Durumu

- **OS:** Windows 10 Pro for Workstations, PowerShell 5.1
- **Python:** 3.10.11 (`C:\Users\Emirhan\AppData\Local\Programs\Python\Python310`)
- **venv:** `c:\Users\Emirhan\Desktop\Preunec\puroje\.venv` (oluşturuldu, pip 26.x'e yükseltildi)
- **pandoc CLI:** **kurulu değil** — docx için `winget install pandoc` (opsiyonel; mammoth fallback çalışır)
- **GPU:** otomatik tespit edilecek (`torch.cuda.is_available()`)

### Bağımlılık Kurulumu

İki kez `ReadTimeoutError` (pyarrow 27 MB indirme sırasında) — ağ problemi, kod problemi değil. Kullanıcı tarafından manuel deneme:

```powershell
cd c:\Users\Emirhan\Desktop\Preunec\puroje
.\.venv\Scripts\Activate.ps1
pip install --default-timeout=600 --retries=10 -e .
```

Zaman aşımı tekrarlarsa:
1. Tek tek dene: `pip install torch`, `pip install pyarrow`, `pip install docling`, sonra `pip install -e .`.
2. `--no-cache-dir --use-deprecated=legacy-resolver` ile paralel indirmeyi kapat.
3. Mobil hotspot veya başka ağ.

**Tahmini indirme:** 500 MB – 1 GB (torch CPU ~200 MB, docling deps ~150 MB).
**Bge-m3 modeli:** ilk `docq embed` çağrısında HuggingFace'ten ~2 GB iner (tek seferlik, cache'lenir).

## 7. Kullanım

```powershell
# Aktif venv
.\.venv\Scripts\Activate.ps1

# Durumu gör
docq info

# Önce küçük bir alt küme ile test
docq ingest -n 5
docq chunk
docq embed                       # ilk çağrı yavaş (model indirme)
docq query "JWT refresh nasıl çalışıyor?"

# Tam korpus
docq ingest
docq chunk
docq embed
docq query "PayTR iade akışı"
docq query "Cari kart ekleme stored procedure" --full
```

## 8. Bilinen Sınırlamalar

- **Inkremental update yok** — `docq ingest` her seferinde tam rebuild yapar (memory-bank kararı).
- **Sparse vektör + reranker yok** — Faz 2.
- **Harita üretimi yok** — Faz 3.
- **Wiki-link enjeksiyonu yok** — Faz 4.
- **PDF görselleri yoksayılır** — placeholder bile bırakılmıyor şu an; docling sadece yazı çıkarır. İleride caption pipeline.
- **`chunk_path_str` LanceDB'de tek string** — Obsidian/Markdown UX için path bütün list olarak da saklanıyor; sorgu kodu list'i kullanıyor.

## 9. Implementation Sırasında Karşılaşılan Sorunlar

### pip install — ağ zaman aşımı
İki kez `ReadTimeoutError` (pyarrow 27 MB indirme sırasında). Çözüm: kullanıcı paketleri tek tek indirdi (torch → pyarrow → docling → sonra `pip install -e .`), her komut kaldığı yerden cache ile devam etti.

### Rich + Windows legacy console + Türkçe karakter
Typer help renderer (`rich.legacy_windows_render`) Türkçe karakterleri Windows legacy console'a yazarken çöküyordu. Bash subprocess'ten çalıştırıldığında stdout TTY olmadığı için Rich legacy mode'a düşüyor.

**Çözüm:** `cli.py` başında:
```python
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

app = typer.Typer(
    ...,
    rich_markup_mode=None,           # rich help renderer'ı kapat
    pretty_exceptions_enable=False,
)
```

### HuggingFace symlink uyarısı
Windows Developer Mode kapalı → cache "degraded mode"da (duplicate dosya saklar). Fonksiyon etkilenmedi; disk biraz daha fazla. İstenirse Developer Mode açılabilir veya `HF_HUB_DISABLE_SYMLINKS_WARNING=1`.

## 10. Sonraki Adım (ARA SONRASI — 2026-05-23'te ara verildi)

**Hemen yapılacak:**

1. **Kullanıcı internetten örnek dosyalar indirir** (en az 1 PDF + 1 DOCX + 1 TXT). Türkçe içerikli olması bge-m3 + chunker'ı gerçek koşulda test eder.
2. **Tam smoke test:**
   ```powershell
   mkdir raw-smoke
   # raw-smoke/ klasörüne indirilen örnek dosyaları koy
   docq ingest --source raw-smoke
   docq chunk
   docq embed
   docq query "..."
   ```
   - **PDF:** docling'in çalıştığını gör. Başarısız olursa pymupdf4llm fallback otomatik devreye girer (frontmatter'da `parser: pymupdf4llm` yazar).
   - **DOCX:** pandoc CLI kurulu olmadığı için OSError → mammoth fallback otomatik (frontmatter'da `parser: mammoth` yazar). Eğer kullanıcı `winget install pandoc` ile pandoc kurarsa, `parser: pandoc` görmeli.
   - **TXT:** UTF-8 olarak okunup `# {filename}\n\n```\n{content}\n```` formatında markdown'a sarılmalı. Bozuk encoding'te latin-1 fallback olduğunu da test etmek için bir cp1254 dosyası iyi olur.
3. Üçü de OK → Faz 1 tam kapanır → `progress.md`'deki üç checkbox işaretlenir.

**Sonra:**

4. **Tam korpus ingest** (opsiyonel) — `-n` limitini kaldır, 320 dosyalık tam pipeline. Tahmini süre: ingest ~30-60 dk (PDF docling yavaş), chunk <1 dk, embed CPU'da ~10-20 dk.
5. **Faz 2 — Hibrit arama + reranker:**
   - `embed.py`'de `return_sparse=True` aç.
   - LanceDB schema'ya sparse kolonu ekle (lance v2.4+ destekler).
   - `query.py`'de RRF (Reciprocal Rank Fusion) — dense + sparse skorlarını birleştir.
   - `rerank.py` yeni modül: `bge-reranker-v2-m3` ile top-50 → top-5.
6. **Eval set hazırlığı** — 15-20 test sorusu + recall@5 metriği.
