# İlerleme

## Şu Anki Durum
**✅ Sistem Stabil — Ana pipeline tamamlandı (Faz 1-4).**

Detaylı implementation notları: [fazlar/faz4.md](fazlar/faz4.md).
Faz 3 notları: [fazlar/faz3.md](fazlar/faz3.md).

## Çalışanlar
- Proje iskeleti (`pyproject.toml`, `.gitignore`, `.env.example`).
- Klasör yapısı (`raw/`, `processed/`, `chunks/`, `src/docq/`, `logs/`).
- `docs/` → `raw/` (320 dosya — kullanıcının PayTR + ERP12 + ERIMELEKTRONIK + GENERAL dokümanları).
- `.venv/` Python 3.10.11 ile.
- Kaynak kodun tamamı (`src/docq/`).

## Yapılacaklar

### Faz 1: MVP — **🟢 TAMAM**
- [x] Proje iskeleti
  - [x] `pyproject.toml` (paket bağımlılıkları)
  - [x] Klasör yapısı (`raw/`, `processed/`, `chunks/`, `src/docq/`, `logs/`)
  - [x] `.env.example`
  - [x] `.gitignore`
- [x] Ingest katmanı
  - [x] `src/docq/ingest/base.py` — Document dataclass + IngestResult + helpers
  - [x] `src/docq/ingest/md_ingest.py` — .md + .txt
  - [x] `src/docq/ingest/docx_ingest.py` — pandoc (auto-download) → mammoth fallback
  - [x] `src/docq/ingest/pdf_ingest.py` — docling → pymupdf4llm fallback
  - [x] `src/docq/ingest/router.py`
  - [x] `_processed_path` path hatası düzeltildi (resolve() ile relative/absolute sorun giderildi)
- [x] Chunking
  - [x] `src/docq/chunk.py` — header-aware, kod/tablo atomik
  - [x] Bold-heading normalize: `**Başlık**` / `__Başlık__` → `## Başlık` (Word DOCX uyumluluğu)
- [x] Embedding
  - [x] `src/docq/embed.py` — bge-m3 dense + LanceDB yazımı
- [x] Sorgu
  - [x] `src/docq/query.py` — cosine dense search
- [x] CLI
  - [x] `src/docq/cli.py` — typer ile `ingest`, `chunk`, `embed`, `query`, `info`
- [x] Bağımlılık kurulumu — `pip install -e .`
- [x] **Smoke test — MD path** başarılı
- [x] **Smoke test — PDF path** (docling + pymupdf4llm fallback) başarılı
- [x] **Smoke test — DOCX path** (pandoc auto-download + mammoth fallback) başarılı
- [x] **Smoke test — TXT path** başarılı
- [x] Windows console + Türkçe karakter fix (`cli.py`)

### Faz 2: Hibrit Arama + Rerank — **🟢 TAMAM (2026-05-28)**
- [x] bge-m3 sparse vektör eklemesi (`return_sparse=True`, JSON string olarak LanceDB'ye)
- [x] LanceDB schema'sına `sparse_vector` kolonu
- [x] Manuel python-side dot product sparse arama (LanceDB FTS uyumsuz)
- [x] Reciprocal Rank Fusion (k=60)
- [x] `bge-reranker-v2-m3` — transformers direkt (FlagEmbedding 1.4.0 bug bypass)
- [x] Top-50 → rerank → top-5, sigmoid normalize skor
- [x] `--no-rerank` flag + aşama skorları çıktısı
- [x] RAM fix: `max_length` 8192→1024, `EMBEDDING_BATCH_SIZE` 12→4
- [x] `_safe_section_path()` — numpy array uyumsuzluk fix
- [x] Test: "PayTR odeme akisi" + "JWT_REFRESH_SECRET" sorguları başarılı

### Faz 3: Harita Üretimi — **🟢 TAMAM (2026-06-02)**

> Orijinal plan (Seçenek D: LLM + embedding) iptal edildi. Embedding zaten tematik ilişkiyi biliyor; LLM gereksiz maliyet ve complexity getiriyordu.

- [x] `src/docq/map_gen.py` — tamamen local, API anahtarı yok
- [x] **Pass 1 — Regex:** `processed/*.md` içinde `bkz.` / `see section` / dosya adı referanslarını yakala → `explicit_related`
- [x] **Pass 2 — Embedding cosine:** LanceDB'den her section için top-N komşu → `might_be_related` (skorlu)
- [x] `topics.yaml` schema + writer (iki kategori: `explicit_related`, `might_be_related`)
- [x] `src/docq/index_gen.py` — `topics.yaml` → `INDEX.md`
- [x] `docq map` + `docq index` CLI komutları (`--pass1`, `--pass2`, `--threshold`, `--top-n`)
- [x] `config.py` sabitleri: `MAP_COSINE_THRESHOLD=0.75`, `MAP_TOP_N_NEIGHBORS=5`
- [x] Test: 10 dosya, 213 section, 788 tematik bağlantı, 172/213 section bağlı

### Faz 4: Obsidian Polish — **🟢 TAMAM (2026-06-06)**

Detaylı plan: [fazlar/faz4.md](fazlar/faz4.md).

- [x] `src/docq/wikilink_inject.py` — `topics.yaml` → `processed/*.md` içine `[[link]]` enjekte (marker blok, idempotent)
- [x] `docq inject` CLI komutu (`--dry-run`, `--topics`, `--processed` flags)
- [x] `processed/` klasörünü Obsidian'da vault olarak aç
- [x] Graph view doğrulaması — edge'ler görünüyor mu (evet)
- [x] `INDEX.md`'den dosyalara navigasyon testi
- [x] Smoke test: `docq inject --dry-run` önce, sonra gerçek çalıştır (6 dosya, 20 link enjekte edildi)

### Faz Sonrası (gelecek, sırasız)
- [ ] Eval set: 15-20 test sorusu + recall@5 metriği
- [ ] Inkremental update (content hash bazlı diff)
- [ ] MCP server (Claude Code entegrasyonu)
- [ ] Görsel caption üretimi (vision LLM)
- [ ] (Belki) Web arayüz
- [ ] **Çoklu korpus / proje filtresi:** Korpus tek bir proje veya konuya ait olmayabilir (örn. PayTR + ERP12 + GENEL karışık). `docq map` ve `docq query` komutlarına `--project` veya `--corpus` parametresi eklenebilir; harita ve arama belirli bir alt kümeye kısıtlanır. Detay için konuşulacak.

## Bilinen Sorunlar / Riskler

**Mevcut:**
- **PDF/DOCX/TXT ingester'ları gerçek dosyada test edilmedi** → kullanıcı örnek dosya getirip test edilecek. Test'te bir şey çıkarsa düzeltilecek.
- **Retrieval kalitesi gözlemi:** 5-dosyalık küçük korpusta dense-only sıralama bazı sorgularda tam isabet etmedi (örn. "PayTR odeme akisi" → SEQUENCE.md tam karşılık olmasına rağmen PRISMA.md 1. çıktı). Beklenen davranış; Faz 2 reranker ile düzelecek.

**Öngörülen (Faz 2+):**
- **Docling PDF'lerde başarısız olabilir** → `pymupdf4llm` fallback hazır, ingest log'una yaz, devam et.
- **Türkçe chunk kalitesi belirsiz** → MVP sonrası eval set ile ölçülecek.
- **Gemini free tier rate limit (5 RPM)** → batch'leme ile aşılıyor, 30 dosya tek günde rahat işlenir.
- **Section-bazlı haritanın LLM tutarlılığı** → 500 sayfa tek pass'te Gemini'de "lost in the middle" olabilir; per-file batch bunu mitigate ediyor.
- **bge-m3 hybrid mode'un LanceDB ile entegrasyonu** → LanceDB sparse vektör desteği yeni, edge case'ler olabilir. Faz 2'de test edilecek.

## Proje Kararlarının Evrimi

### İlk Tartışma: Sistem Yaklaşımı
- "Sadece RAG yetmez, statik harita da lazım" sonucuna varıldı.
- İki katmanlı yaklaşım (harita + arama) seçildi.
- "Hibrit: structured index + semantic search" kararlaştırıldı.

### İkinci Tartışma: Teknoloji Seçimi
- Embedding'de OpenAI yerine **local bge-m3** seçildi (ücretsiz, Türkçe iyi, privacy bonus).
- Vector DB'de Qdrant yerine **LanceDB** seçildi (server'sız, taşınabilir).
- BM25 başlangıçta planlanmıştı, sonra **çıkarıldı** (bge-m3 sparse zaten lexical role oynuyor + Türkçe agglutinative dil için BM25 problematik).
- Harita LLM'i için Claude Opus 4.7 öneriliydi, sonra **Gemini 2.5 Pro free** ana seçenek oldu (ücretsiz, 2M context). Opus fallback olarak kaldı.

### Üçüncü Tartışma: Granülarite ve UX
- **Harita granülaritesi:** dosya seviyesi → **section seviyesi** (kalite için).
- **Maliyet kontrolü:** per-section çağrı yerine **per-file batch** (300 → 30 çağrı).
- **Sorgu cevabı:** LLM sentezi → **ham chunk + kaynak** (şeffaflık, ücretsiz).
- **Görsel işleme:** vision LLM → **işlenmez, placeholder** (MVP basit kalsın).
- **Inkremental update:** baştan tasarlanacaktı → **MVP'den sonra** (basit kalsın).

### Dördüncü Adım: Dokümantasyon
- Memory bank oluşturuldu (Cline pattern, Türkçe).
- Bu, ileride memory reset'lerden sonra projeye yeniden hızlıca uyum sağlamak için.

### Beşinci Tartışma: Harita İlişki Kaynağı (2026-05-23)
- Orijinal plan (A): LLM hem özet hem ilişki üretsin (explicit + thematic, meta pass dahil).
- Alternatif (B): LLM sadece özet/kavram, ilişkileri embedding cosine versin (şeffaf, halüsinasyonsuz).
- Alternatif (C): Harita yok, sadece arama.
- **Seçilen: D (A + embedding bonus)** — LLM tam haritayı kursun (özet + kavram + explicit + thematic), embedding ek katman olarak `might_be_related` üretsin. Üç kategori `topics.yaml`'da ayrı tutulur. LLM ve embedding aynı section'ı işaretliyorsa `llm_also_listed: true` → agreement sinyali (en güçlü bağlantı).
- **Gerekçe:** LLM tematik yorum üretmede güçlü (kullanıcı sezgisi). Embedding zaten Faz 1'de ücretsiz olarak elimizde, eklemek maliyet getirmiyor. İki bağımsız kaynağın agreement'ı manuel halüsinasyon kontrolü işlevi görüyor. Üç kategori ayrı render edilince kullanıcı şüpheli olduğunda kaynağına bakabiliyor.
