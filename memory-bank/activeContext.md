# Aktif Bağlam

## Şu Anki Durum
**✅ Faz 5 TAMAM (2026-06-07) — Çoklu Korpus / Tag Filtreleme sistemi eklendi.**

Detaylı implementation notları: [fazlar/faz4.md](fazlar/faz4.md).
Faz 3 notları: [fazlar/faz3.md](fazlar/faz3.md).
Faz 2 notları: [fazlar/faz2.md](fazlar/faz2.md).

**Mevcut hal:**
- Tüm kaynak kod (`src/doqqy/`): ingest (md/txt/pdf/docx), chunk, embed, query, cli — yazıldı ve tam test edildi.
- `.venv/` Python 3.10.11 + tüm bağımlılıklar kurulu (torch 2.12 CPU, docling 2.95, FlagEmbedding 1.4, lancedb 0.30, mammoth, pymupdf4llm vb.).
- `raw/` altında gerçek PDF + DOCX + TXT + MD dosyalarıyla tam smoke test tamamlandı.
- bge-m3 modeli HuggingFace cache'inde (~2 GB, `%USERPROFILE%\.cache\huggingface\`, symlink yok diye duplicate).
- Windows-spesifik fix: `cli.py` UTF-8 stdout + `rich_markup_mode=None`.

**2026-06-02 Günü Yapılan Değişiklikler (Faz 3):**
1. **`map_gen.py` (yeni):** Pass 1 (regex explicit referanslar) + Pass 2 (LanceDB dense vektör cosine komşuluk) → `topics.yaml`. 10 dosya, 213 section, 788 tematik bağlantı üretildi.
2. **`index_gen.py` (yeni):** `topics.yaml` → `processed/INDEX.md`. 📌 explicit + 💡 might_be kategorileri.
3. **`cli.py`:** `doqqy map` (--pass1/--pass2/--threshold/--top-n) + `doqqy index` komutları eklendi.
4. **`config.py`:** `MAP_COSINE_THRESHOLD=0.75`, `MAP_TOP_N_NEIGHBORS=5`, `TOPICS_YAML` sabitleri eklendi.

**2026-05-28 Günü Yapılan Değişiklikler (Faz 2):**
1. **RAM fix:** `max_length` 8192→1024, `EMBEDDING_BATCH_SIZE` 12→4. Embed RAM kullanımı 28 GB→~6 GB. RAG kalitesine etkisi yok.
2. **`embed.py`:** `return_sparse=True`, sparse çıktı JSON string olarak `sparse_vector` kolonuna yazılıyor.
3. **`rerank.py` (yeni):** `transformers.AutoModelForSequenceClassification` ile `bge-reranker-v2-m3`. FlagEmbedding 1.4.0 tokenizer bug'ı nedeniyle bypass edildi.
4. **`query.py`:** Dense top-50 + sparse top-50 → RRF (k=60) → reranker → top-5. `_safe_section_path()` numpy array fix.
5. **`cli.py`:** `--no-rerank` flag, `dense_rank / sparse_rank / rrf / rerank` skor çıktısı.
6. **`config.py`:** `RETRIEVAL_TOP_K=50`, `RERANKER_MODEL`, `RERANKER_BATCH_SIZE=4` eklendi.

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
| Harita LLM | **Kullanılmayacak** (2026-06-01 kararı) | Embedding zaten tematik ilişkiyi biliyor; LLM gereksiz maliyet ve complexity |
| Harita granülaritesi | **Section seviyesi** (her `##` / `###` ayrı işlenir) | Daha kaliteli |
| Harita üretim stratejisi | **Regex + embedding cosine** — API yok, tamamen local | Sıfır maliyet, sıfır dış bağımlılık |
| Harita ilişki kaynağı | **Regex (explicit) + embedding cosine (might_be)** — iki kategori | LLM sentezi yok; orijinal referanslar + semantik komşuluk yeterli |
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

### Faz 2 — Hibrit Arama + Rerank — **🟢 TAMAM**
- [x] bge-m3 sparse vektör + LanceDB `sparse_vector` kolonu (JSON string)
- [x] Manuel python-side dot product (LanceDB FTS bge-m3 token ID'leriyle uyumsuz)
- [x] RRF (k=60) + `bge-reranker-v2-m3` (transformers direkt, FlagEmbedding bypass)
- [x] `--no-rerank` flag, aşama skorları çıktısı

### Faz 3 — Harita Üretimi — **🟢 TAMAM (2026-06-02)**

> **Karar (2026-06-01):** Orijinal Seçenek D (LLM + embedding) iptal edildi. LLM çağrısı gereksiz maliyet ve complexity getiriyor; embedding zaten tematik ilişkiyi biliyor.

İki pass, LLM yok:
- [x] **Pass 1 — Regex:** Her `processed/*.md` içinde `bkz.` / `see section` / dosya adı referanslarını yakala → `explicit_related`.
- [x] **Pass 2 — Embedding cosine:** LanceDB'den her section için top-N komşu → `might_be_related` (skorlu).
- [x] **Birleştirme:** `topics.yaml` yaz (iki kategori: explicit / might_be).
- [x] `src/doqqy/map_gen.py` — tamamen local, API anahtarı gerektirmez.
- [x] `src/doqqy/index_gen.py` — `topics.yaml` → `INDEX.md`.
- [x] `doqqy map` + `doqqy index` CLI komutları.

**Test sonuçları:** 10 dosya, 213 section, 1 explicit + 788 tematik bağlantı. 172/213 section bağlı.

**2026-06-07 Günü Yapılan Değişiklikler (Faz 5):**
1. **`ingest/base.py`:** `base_metadata()` fonksiyonu `raw/` altındaki klasör kırılımını otomatik olarak `tags: list[str]` haline getiriyor. Örn: `raw/bulut-saha/genel/dosya.pdf` → `tags: ["bulut-saha", "genel"]`.
2. **`chunk.py`:** `Chunk` dataclass'ına `tags: list[str]` alanı eklendi; frontmatter'dan okunuyor.
3. **`embed.py`:** LanceDB'ye yazarken `tags_str` kolonu eklendi — format: `",tag1,tag2,"` (LIKE filtresi için).
4. **`query.py`:** `search()`, `_dense_search()`, `_sparse_search()` fonksiyonlarına `filter_tag` parametresi eklendi; `tags_str LIKE '%,X,%'` SQL filtresi uygulanıyor.
5. **`map_gen.py`:** `_pass2()` ve `generate_map()` fonksiyonlarına `filter_tag` parametresi eklendi; Pass 2 cosine benzerliği sadece filtrelenmiş chunk'larla sınırlı kalıyor.
6. **`cli.py`:** `doqqy query --tag/-t`, `doqqy map --tag/-t`, `doqqy tags` (yeni komut) eklendi.

### Faz 4 — Obsidian Polish — **🟢 TAMAM (2026-06-06)**

Detaylı plan: [fazlar/faz4.md](fazlar/faz4.md).

- [x] `topics.yaml`'dan `[[wiki-link]]` enjeksiyon scripti (`src/doqqy/wikilink_inject.py`).
- [x] `doqqy inject` CLI komutu (`--dry-run`, idempotent).
- [x] Obsidian vault testi, graph view doğrulaması.

### Faz 5 — Çoklu Korpus / Tag Filtreleme — **🟢 TAMAM (2026-06-07)**

- [x] `raw/` klasör kırılımı → `tags: list[str]` otomatik metadata (`ingest/base.py`).
- [x] `Chunk.tags` alanı + LanceDB `tags_str` kolonu (`,tag1,tag2,` serialize formatı).
- [x] `doqqy query --tag <TAG>` — hibrit arama tag filtreli.
- [x] `doqqy map --tag <TAG>` — Pass 2 cosine benzerliği tag filtreli.
- [x] `doqqy tags` — sistemdeki tüm tag'leri listele.

## Aktif Düşünceler / Devam Eden Konular

- **Retrieval kalitesi gözlemi:** Bazı sorgular doğru dosyayı 1. sırada vermedi (örn. "PayTR odeme akisi" → SEQUENCE.md yerine PRISMA.md 1. çıktı). Bu Faz 2 reranker ile düzelmesi beklenen tipik dense-only davranış — kod kusuru değil.
- **HuggingFace symlink uyarısı:** Windows Developer Mode kapalı, cache duplicate dosya saklıyor. Disk biraz daha fazla, fonksiyon etkilenmiyor.
- **Ağ problemi:** PyPI timeout sorunu vardı, pyarrow özellikle. Faz 2'de yeni paket gerekirse `--default-timeout=600 --retries=10` veya tek tek indirme.
- **Eval set:** Faz 2 sonrası, 15-20 test sorusu + recall@5.
- **Proje adı:** Şimdilik `doqqy`, daha iyi bir isim çıkarsa değişebilir.

## Önemli Pattern'ler ve Tercihler

- **Idempotency:** Her pipeline aşaması yeniden çalıştırılabilir olmalı.
- **Format-agnostic core:** İngest aşamasından sonra her şey kanonik markdown'a indirgenir. Pipeline'ın geri kalanı format bilmiyor.
- **Şeffaflık:** Kullanıcı her zaman orijinal metni görür. Sistem onun yerine yorum yapmaz.
- **Local-first:** Embedding ve reranking local. Sadece harita üretiminde (tek seferlik) external LLM kullanılır.
- **Pragmatik MVP:** Inkremental update, görsel işleme, MCP gibi "iyi olur ama gerekli değil" özellikler ilk versiyonda yok.

## Öğrendiklerimiz

### Faz 2 (2026-05-28)
- **FlagEmbedding 1.4.0 + bge-reranker-v2-m3 uyumsuzluğu:** `FlagReranker` ve `FlagLLMReranker` ikisi de `XLMRobertaTokenizer.prepare_for_model` hatası veriyor. Bilinen bug. Çözüm: `transformers` direkt kullan.
- **bge-m3 `max_length=8192` RAM tuzağı:** Model chunk 200 token olsa bile 8192 tokenlik attention matrisi ayırıyor. Her zaman gerçek max chunk boyutuna yakın değer ver (1024).
- **LanceDB FTS + bge-m3 sparse uyumsuzluğu:** bge-m3 sparse çıktısı BM25 terimi değil, model vocab token ID'si. LanceDB FTS bunları index'leyemiyor. Çözüm: JSON string sakla, python-side dot product hesapla.
- **LanceDB `section_path` numpy array döner:** `or []` operatörü numpy array'de `ValueError` fırlatır. `_safe_section_path()` helper zorunlu.
- **bge-reranker-v2-m3 gerçek boyutu:** Dökümanlarda ~1.1 GB, gerçekte 2.27 GB. Windows'ta HuggingFace symlink yok, duplicate saklıyor.
- **`test_docs/` klasörü:** Tam korpus yerine seçilmiş test dokümanlarıyla çalış. `raw/` dokunulmaz kalır.

### Faz 1 (2026-05-26) (300+ çağrı, gün başına 100 limit). Çözüm: per-file batch — 30 dosya = 30 çağrı.
- **Gemini 2.5 Pro free tier datayı eğitime kullanabilir** — privacy hassasiyeti olan dokümanlar için Vertex AI (ücretli) veya local LLM gerekir.
- **Türkçe için BM25 problemli** (agglutinative dil). bge-m3 hybrid mode bunu doğal olarak çözüyor.
- **Windows `pathlib.relative_to`** relative path verildiğinde absolute `RAW_DIR` ile karışıyor → her zaman `.resolve()` kullan.
- **Pandoc PATH sorunu Windows'ta yaygın** — terminal yeniden başlatmak yerine `pypandoc.download_pandoc()` ile proje içine otomatik indirmek daha sağlam.
- **Word dokümanlarında bold ≠ başlık** — kullanıcılar Heading stili yerine bold kullanırsa chunker atlar. `_BOLD_HEADING_RE` ile tek satır bold'ları `##` başlığa normalize etmek gerekiyor.
- **bge-m3 CPU embedding hızı:** ~160 chunk → birkaç dakika. 320 dosyalık tam korpus için 15-30 dk arası beklenir.
- **Windows + Bash subprocess + Rich uyumsuzluğu:** `rich_markup_mode=None` + `sys.stdout.reconfigure(encoding="utf-8")` ile çözüldü.
