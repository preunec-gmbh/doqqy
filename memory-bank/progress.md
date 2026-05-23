# İlerleme

## Şu Anki Durum
**🟡 Faz 1 kod + kısmi smoke test TAMAM, tam smoke test ARA VERİLDİ (2026-05-23).**

Detaylı implementation notları: [fazlar/faz1.md](fazlar/faz1.md).

**Eksik:** Smoke test sadece **MD ingester'ında** çalıştırıldı. PDF/DOCX/TXT path'leri kodlandı ama gerçek dosyayla doğrulanmadı. Kullanıcı internetten örnek dosyalar indirip o üçünü de test edecek. Ondan sonra "Faz 1 tam bitti" → Faz 2'ye geçilecek.

## Çalışanlar
- Proje iskeleti (`pyproject.toml`, `.gitignore`, `.env.example`).
- Klasör yapısı (`raw/`, `processed/`, `chunks/`, `src/docq/`, `logs/`).
- `docs/` → `raw/` (320 dosya — kullanıcının PayTR + ERP12 + ERIMELEKTRONIK + GENERAL dokümanları).
- `.venv/` Python 3.10.11 ile.
- Kaynak kodun tamamı (`src/docq/`).

## Yapılacaklar

### Faz 1: MVP — **🟡 KOD TAMAM, TAM SMOKE TEST ARA VERİLDİ**
- [x] Proje iskeleti
  - [x] `pyproject.toml` (paket bağımlılıkları)
  - [x] Klasör yapısı (`raw/`, `processed/`, `chunks/`, `src/docq/`, `logs/`)
  - [x] `.env.example`
  - [x] `.gitignore`
- [x] Ingest katmanı
  - [x] `src/docq/ingest/base.py` — Document dataclass + IngestResult + helpers
  - [x] `src/docq/ingest/md_ingest.py` — .md + .txt
  - [x] `src/docq/ingest/docx_ingest.py` — pandoc → mammoth fallback
  - [x] `src/docq/ingest/pdf_ingest.py` — docling → pymupdf4llm fallback
  - [x] `src/docq/ingest/router.py`
- [x] Chunking
  - [x] `src/docq/chunk.py` — header-aware, kod/tablo atomik
- [x] Embedding
  - [x] `src/docq/embed.py` — bge-m3 dense + LanceDB yazımı
- [x] Sorgu
  - [x] `src/docq/query.py` — cosine dense search
- [x] CLI
  - [x] `src/docq/cli.py` — typer ile `ingest`, `chunk`, `embed`, `query`, `info`
- [x] Bağımlılık kurulumu — `pip install -e .` (paket paket manuel halledildi)
- [x] **Smoke test — MD path** (5 MD dosyası → 42 chunk → embed → query) başarılı
- [ ] **Smoke test — PDF path** (kullanıcı örnek PDF indirecek; docling + fallback test)
- [ ] **Smoke test — DOCX path** (kullanıcı örnek DOCX indirecek; pandoc yok → mammoth fallback test)
- [ ] **Smoke test — TXT path** (kullanıcı örnek TXT indirecek; code-block sarma + UTF-8/latin-1 fallback test)
- [x] Windows console + Türkçe karakter fix (`cli.py`)

### Faz 2: Hibrit Arama + Rerank (yarım gün)
- [ ] bge-m3 sparse vektör eklemesi (FlagEmbedding hybrid mode)
- [ ] LanceDB schema'sına sparse alan
- [ ] Reciprocal Rank Fusion
- [ ] `bge-reranker-v2-m3` entegrasyonu
- [ ] Top-50 → rerank → top-5

### Faz 3: Harita Üretimi — **Seçenek D** (LLM + embedding bonus)
- [ ] `src/docq/map_gen.py` — Gemini 2.5 Pro client (ana), Claude Opus 4.7 fallback hazır
- [ ] **Pass 1 — Per-file LLM prompt template** (summary + concepts + explicit_related + thematic_related)
- [ ] **Pass 1 yardımcı: explicit_related için regex ön-filtre** (`bkz`, `see section`, dosya adı pattern'leri)
- [ ] **Pass 2 — Meta LLM çağrısı** (tüm özetler birden → thematic_related zenginleştir)
- [ ] **Pass 3 — Embedding cosine top-N** (LanceDB üzerinden, LLM yok) → `might_be_related`
- [ ] **Birleştirme + agreement hesabı** (`llm_also_listed: true` flag'i)
- [ ] `topics.yaml` schema + writer (üç kategori ayrı: explicit_related, thematic_related, might_be_related)
- [ ] `src/docq/index_gen.py` — `topics.yaml` → `INDEX.md` (üç kategori farklı render: 📌 / 🔗 / 💡 + skor)
- [ ] 5 dosyalı küçük korpusta harita kalitesi gözden geçirme (önce LLM'in tematik kalitesi yeterli mi gör)

### Faz 4: Obsidian Polish (yarım gün)
- [ ] `src/docq/wikilink_inject.py` — `topics.yaml` → `processed/*.md` içine `[[link]]` enjekte
- [ ] Üç kategori için ayrı render: `📌 [[X]]` (explicit), `🔗 [[Y]]` (thematic), `💡 [[Z]] (0.84 ✓)` (might_be + agreement)
- [ ] `processed/` klasörünü Obsidian'da vault olarak test
- [ ] Graph view doğrulaması — agreement edge'leri farklı görünüyor mu
- [ ] `INDEX.md`'den dosyalara navigasyon testi

### Faz Sonrası (gelecek, sırasız)
- [ ] Eval set: 15-20 test sorusu + recall@5 metriği
- [ ] Inkremental update (content hash bazlı diff)
- [ ] MCP server (Claude Code entegrasyonu)
- [ ] Görsel caption üretimi (vision LLM)
- [ ] (Belki) Web arayüz

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
