# Aktif Bağlam

## Şu Anki Durum
**🟢 Faz 1 MVP TAMAM — PDF, DOCX, TXT smoke testleri tamamlandı (2026-05-26).**

Detaylı implementation notları: [fazlar/faz1.md](fazlar/faz1.md).

**Mevcut hal:**
- Tüm kaynak kod (`src/docq/`): ingest (md/txt/pdf/docx), chunk, embed, query, cli — yazıldı ve tam test edildi.
- `.venv/` Python 3.10.11 + tüm bağımlılıklar kurulu (torch 2.12 CPU, docling 2.95, FlagEmbedding 1.4, lancedb 0.30, mammoth, pymupdf4llm vb.).
- `raw/` altında gerçek PDF + DOCX + TXT + MD dosyalarıyla tam smoke test tamamlandı.
- bge-m3 modeli HuggingFace cache'inde (~2 GB, `%USERPROFILE%\.cache\huggingface\`, symlink yok diye duplicate).
- Windows-spesifik fix: `cli.py` UTF-8 stdout + `rich_markup_mode=None`.

**2026-05-26 Günü Yapılan Düzeltmeler:**
1. **`_processed_path` path hatası** (`md_ingest.py`, `docx_ingest.py`, `pdf_ingest.py`): `source.relative_to(RAW_DIR)` relative/absolute karışımında `ValueError` fırlatıyordu. `source.resolve().relative_to(RAW_DIR.resolve())` + `try/except ValueError → Path(source.name)` ile düzeltildi.
2. **Pandoc auto-download** (`docx_ingest.py`): Pandoc binary yoksa `pypandoc.get_pandoc_version()` → OSError yakalanıp `pypandoc.download_pandoc()` otomatik indirir. Artık `winget install pandoc` ve terminal yeniden başlatma gereksiz.
3. **Bold-heading chunk fix** (`chunk.py`): `_BOLD_HEADING_RE` eklendi. Word'de "Heading" stili yerine bold kullanılmış tek satır başlıklar (`**A124. Başlık**`, `__A224. Başlık__`) artık `## A124. Başlık` şeklinde `##` başlığa çevrilerek `MarkdownHeaderTextSplitter` tarafından kırılım noktası olarak tanınıyor. DOCX dokümanlarında anlamlı chunk bölümlemesi için kritik.

## Son Konuşmada Verilen Tüm Kararlar

| Konu | Karar | Gerekçe |
|---|---|---|
| Format desteği | md, pdf, docx, txt — her biri ayrı pipeline | Format-spesifik problemler farklı |
| PDF parser | `docling` (ana), `pymupdf4llm` (basit fallback) | Layout / başlık hiyerarşisi en iyisi |
| DOCX parser | `pandoc` (ana, auto-download), `mammoth` (fallback) | Olgun, Heading stillerini doğru maple |
| MD/TXT parser | `python-frontmatter` | Frontmatter merge, içeriği koru |
| Chunking | `MarkdownHeaderTextSplitter` + bold-heading normalize + recursive char fallback | Header-aware, kod blokları korunur, Word bold başlıklar da yakalanır |
| Embedding | `BAAI/bge-m3` **local, hybrid mode** | Türkçe iyi, dense + sparse aynı modelden |
| Vector DB | LanceDB | Server'sız, dosya-bazlı, taşınabilir |
| Reranker | `BAAI/bge-reranker-v2-m3` local | Multilingual, ücretsiz, hızlı |
| BM25 | **Kullanılmayacak** | bge-m3 sparse zaten lexical role oynuyor + TR agglutinative dil için BM25 problematik |
| Harita LLM | Gemini 2.5 Pro free (ilk dene), Claude Opus 4.7 (fallback) | Ücretsiz başla, kalite yetmezse yükselt |
| Harita granülaritesi | **Section seviyesi** (her `##` / `###` ayrı işlenir) | Daha kaliteli; per-file batch ile maliyet kontrol altında |
| Harita üretim stratejisi | **Per-file batch** (dosya başına 1 LLM çağrısı) | 300 çağrı yerine 30 çağrı → free tier'a sığar |
| Harita ilişki kaynağı | **Seçenek D — LLM + embedding bonus** (2026-05-23) | LLM tam haritayı kursun (özet, kavram, explicit + thematic ilişki). Embedding ek katman olarak "might_be_related" üretsin. İkisinin agreement'ı en güçlü sinyal. |
| Sorgu cevabı | **Ham chunk + kaynak**, LLM sentezi yok | Şeffaflık, ücretsiz, anlık |
| Görseller | **İşlenmez** — placeholder bırakılır | MVP basit kalsın |
| Inkremental update | **Yok** — her seferinde tam rebuild | MVP basit kalsın |
| Eval set | MVP sonrası | Önce çalıştır, sonra ölç |
| Arayüz | Obsidian (vault) + CLI sorgu | Local, ücretsiz, hazır UX |
| MCP entegrasyonu | İleride, sistem stabilleştiğinde | Önce temel çalışsın |

## Sıradaki Adımlar

### Faz 1 — MVP — **🟢 TAMAM**
- [x] Proje iskeleti, ingest (4 format), chunk, embed, query, cli.
- [x] `pip install -e .` — tüm bağımlılıklar kurulu.
- [x] Smoke test — MD path başarılı.
- [x] Smoke test — PDF path (docling + pymupdf4llm fallback) başarılı.
- [x] Smoke test — DOCX path (pandoc auto-download + mammoth fallback) başarılı.
- [x] Smoke test — TXT path başarılı.
- [x] Bold-heading chunking fix (`chunk.py`).

### Faz 2 — Hibrit Arama + Rerank (yarım gün)
- [ ] bge-m3 sparse vektörü ekle.
- [ ] LanceDB'de dense + sparse alanları.
- [ ] Reciprocal Rank Fusion.
- [ ] `bge-reranker-v2-m3` entegrasyonu.

### Faz 3 — Harita Üretimi — **Seçenek D (LLM + embedding bonus)**
Üç pass:
- **Pass 1 — Per-file LLM (30 çağrı):** Her section için summary + concepts + explicit_related (regex destekli) + thematic_related (LLM yorumu).
- **Pass 2 — Meta LLM (1 çağrı):** Tüm dosya özetleri birden, "hangi çiftler tematik olarak güçlü bağlı?" — pass 1'deki thematic_related'ı zenginleştir.
- **Pass 3 — Embedding (LLM yok):** Her section için LanceDB'den top-N cosine neighbor → `might_be_related` (skorlu).
- **Birleştirme:** `topics.yaml` yaz. LLM ve embedding aynı section'ı işaret ediyorsa `llm_also_listed: true` flag'i ile "agreement" sinyali. Üç kategori (explicit/thematic/might_be) ayrı tutulur.
- `src/docq/map_gen.py` — Gemini 2.5 Pro client (ana), Claude Opus 4.7 fallback.
- `src/docq/index_gen.py` — `topics.yaml` → `INDEX.md` (üç kategori farklı render edilir).

### Faz 4 — Obsidian Polish (yarım gün)
- `topics.yaml`'dan `[[wiki-link]]` enjeksiyon scripti.
- Obsidian'da vault testi, graph view doğrulaması.

## Aktif Düşünceler / Devam Eden Konular

- **Retrieval kalitesi gözlemi:** Bazı sorgular doğru dosyayı 1. sırada vermedi (örn. "PayTR odeme akisi" → SEQUENCE.md yerine PRISMA.md 1. çıktı). Bu Faz 2 reranker ile düzelmesi beklenen tipik dense-only davranış — kod kusuru değil.
- **HuggingFace symlink uyarısı:** Windows Developer Mode kapalı, cache duplicate dosya saklıyor. Disk biraz daha fazla, fonksiyon etkilenmiyor.
- **Ağ problemi:** PyPI timeout sorunu vardı, pyarrow özellikle. Faz 2'de yeni paket gerekirse `--default-timeout=600 --retries=10` veya tek tek indirme.
- **Eval set:** Faz 2 sonrası, 15-20 test sorusu + recall@5.
- **Proje adı:** Şimdilik `docq`, daha iyi bir isim çıkarsa değişebilir.

## Önemli Pattern'ler ve Tercihler

- **Idempotency:** Her pipeline aşaması yeniden çalıştırılabilir olmalı.
- **Format-agnostic core:** İngest aşamasından sonra her şey kanonik markdown'a indirgenir. Pipeline'ın geri kalanı format bilmiyor.
- **Şeffaflık:** Kullanıcı her zaman orijinal metni görür. Sistem onun yerine yorum yapmaz.
- **Local-first:** Embedding ve reranking local. Sadece harita üretiminde (tek seferlik) external LLM kullanılır.
- **Pragmatik MVP:** Inkremental update, görsel işleme, MCP gibi "iyi olur ama gerekli değil" özellikler ilk versiyonda yok.

## Öğrendiklerimiz

- **Section-bazlı harita per-section çağrı yapsa ücretsiz tier'a sığmaz** (300+ çağrı, gün başına 100 limit). Çözüm: per-file batch — 30 dosya = 30 çağrı.
- **Gemini 2.5 Pro free tier datayı eğitime kullanabilir** — privacy hassasiyeti olan dokümanlar için Vertex AI (ücretli) veya local LLM gerekir.
- **Türkçe için BM25 problemli** (agglutinative dil). bge-m3 hybrid mode bunu doğal olarak çözüyor.
- **Windows `pathlib.relative_to`** relative path verildiğinde absolute `RAW_DIR` ile karışıyor → her zaman `.resolve()` kullan.
- **Pandoc PATH sorunu Windows'ta yaygın** — terminal yeniden başlatmak yerine `pypandoc.download_pandoc()` ile proje içine otomatik indirmek daha sağlam.
- **Word dokümanlarında bold ≠ başlık** — kullanıcılar Heading stili yerine bold kullanırsa chunker atlar. `_BOLD_HEADING_RE` ile tek satır bold'ları `##` başlığa normalize etmek gerekiyor.
- **bge-m3 CPU embedding hızı:** ~160 chunk → birkaç dakika. 320 dosyalık tam korpus için 15-30 dk arası beklenir.
- **Windows + Bash subprocess + Rich uyumsuzluğu:** `rich_markup_mode=None` + `sys.stdout.reconfigure(encoding="utf-8")` ile çözüldü.
