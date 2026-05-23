# Aktif Bağlam

## Şu Anki Durum
**Faz 1 MVP kod + smoke test tamam; ARA VERİLDİ (2026-05-23).**

Detaylı implementation notları: [fazlar/faz1.md](fazlar/faz1.md).

**Mevcut hal:**
- Tüm kaynak kod (`src/docq/`): ingest (md/txt/pdf/docx), chunk, embed, query, cli — yazıldı.
- `.venv/` Python 3.10.11 + tüm bağımlılıklar kurulu (torch 2.12 CPU, docling 2.95, FlagEmbedding 1.4, lancedb 0.30, mammoth, pymupdf4llm vb.).
- `docs/` → `raw/` kopyalandı (320 dosya, ama içinde docx ve düzgün .txt yok — kullanıcının ERP/PayTR materyalleri sadece md+pdf).
- bge-m3 modeli HuggingFace cache'inde (~2 GB, `%USERPROFILE%\.cache\huggingface\`, model duplicate olarak saklanıyor symlink desteği yok diye).
- LanceDB tablosu mevcut: **sadece ilk 5 MD dosyasından üretilmiş 42 chunk** indekslenmiş (smoke test için).
- Windows-spesifik fix: `cli.py` UTF-8 stdout + `rich_markup_mode=None`.

**ÖNEMLİ — smoke test eksik kısmı:**
End-to-end test sadece MD ingester'ını kullandı. PDF/DOCX/TXT ingester'ları **kodlandı ama gerçek dosyada test edilmedi.** Kullanıcı internetten örnek .pdf/.docx/.txt dosyaları indirip o üçünü de doğrulayacak. Sonra "Faz 1 tam bitti" diyebileceğiz.

## Kullanıcının Sıradaki Planı (ARA SONRASI)

1. **İnternetten örnek dosyalar indir** → `raw-smoke/` veya benzeri ayrı klasör — en az 1 PDF + 1 DOCX + 1 TXT.
2. **Üç ingester'ı da test et:**
   ```powershell
   docq ingest --source raw-smoke
   docq chunk
   docq embed
   docq query "..."
   ```
   - PDF'te docling'in çalıştığını gör (başarısız olursa pymupdf4llm fallback'i doğrula).
   - DOCX'te pandoc YOKKEN mammoth fallback'inin devreye girdiğini gör.
   - TXT'in code-block sarmalı ile düzgün indekslendiğini gör.
3. Üçü de OK olursa → Faz 1 tam kapanır.
4. **Faz 2'ye geç:** hibrit arama + RRF + bge-reranker-v2-m3.

## Son Konuşmada Verilen Tüm Kararlar

| Konu | Karar | Gerekçe |
|---|---|---|
| Format desteği | md, pdf, docx — her biri ayrı pipeline | Format-spesifik problemler farklı |
| PDF parser | `docling` (ana), `pymupdf4llm` (basit fallback) | Layout / başlık hiyerarşisi en iyisi |
| DOCX parser | `pandoc` (ana), `mammoth` (fallback) | Olgun, Heading stillerini doğru maple |
| MD parser | `python-frontmatter` | Frontmatter merge, içeriği koru |
| Chunking | `MarkdownHeaderTextSplitter` + recursive char fallback | Header-aware, kod blokları korunur |
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

### Faz 1 — MVP — **🟡 KOD + KISMI TEST TAMAM**
- [x] Proje iskeleti, ingest (4 format), chunk, embed, query, cli.
- [x] `pip install -e .` — manuel paket paket indirme ile tamamlandı.
- [x] Smoke test — MD path (5 dosya → 42 chunk → embed → query) başarılı.
- [ ] **Smoke test — PDF/DOCX/TXT path'leri (kullanıcı örnek dosya getirecek).**

### Sıradaki adımlar
1. **Kullanıcı:** internetten 1 PDF + 1 DOCX + 1 TXT örneği indirir (`raw-smoke/` klasörü önerildi).
2. **Test:** üç ingester'ı gerçek dosyada doğrula.
3. (Opsiyonel) tam 320-dosya korpus ingest.
4. **Faz 2'ye geç** — sparse + RRF + reranker.

### Faz 2 — Hibrit Arama + Rerank (yarım gün)
- bge-m3 sparse vektörü ekle.
- LanceDB'de dense + sparse alanları.
- Reciprocal Rank Fusion.
- `bge-reranker-v2-m3` entegrasyonu.

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

- **Smoke test'in MD-only oluşu:** Yukarıdaki gibi, PDF/DOCX/TXT path'leri kod olarak yazıldı ama gerçek dosyada hiç çalıştırılmadı. Risk: docling bazı PDF'lerde fail edebilir (fallback hazır), mammoth Türkçe karakterlerde garip davranabilir. Kullanıcı örnek dosyalar getirince anlaşılacak.
- **Pandoc CLI kurulu değil:** Kullanıcı kurmadı. DOCX testi mammoth fallback üzerinden gidecek. İstenirse `winget install pandoc` ile pandoc-ana akış da test edilebilir.
- **Retrieval kalitesi gözlemi (5-dosyalık küçük korpus):** Bazı sorgular doğru dosyayı 1. sırada vermedi (örn. "PayTR odeme akisi" → SEQUENCE.md'de tam akış olmasına rağmen PRISMA.md 1. çıktı). Bu Faz 2 reranker ile düzelmesi beklenen tipik dense-only davranış — kod kusuru değil.
- **HuggingFace symlink uyarısı:** Windows Developer Mode kapalı, cache duplicate dosya saklıyor. Disk biraz daha fazla, fonksiyon etkilenmiyor.
- **Ağ problemi:** PyPI timeout sorunu vardı, pyarrow özellikle. Faz 2'de yeni paket gerekirse `--default-timeout=600 --retries=10` veya tek tek indirme.
- **Kod örnekleri (.py/.php/.js vb.):** `SUPPORTED_EXTENSIONS` whitelist'inden çıkarıldı — embedding kalitesini kirletmesin.
- **Eval set:** Faz 2 sonrası, 15-20 test sorusu + recall@5.
- **Proje adı:** Şimdilik `docq`, daha iyi bir isim çıkarsa değişebilir.

## Önemli Pattern'ler ve Tercihler

- **Idempotency:** Her pipeline aşaması yeniden çalıştırılabilir olmalı. (Faz 1'de tam rebuild, sonra inkremental.)
- **Format-agnostic core:** İngest aşamasından sonra her şey kanonik markdown'a indirgenir. Pipeline'ın geri kalanı format bilmiyor.
- **Şeffaflık:** Kullanıcı her zaman orijinal metni görür. Sistem onun yerine yorum yapmaz.
- **Local-first:** Embedding ve reranking local. Sadece harita üretiminde (tek seferlik) external LLM kullanılır.
- **Pragmatik MVP:** Inkremental update, görsel işleme, MCP gibi "iyi olur ama gerekli değil" özellikler ilk versiyonda yok.

## Bu Oturumda Öğrendiklerimiz (2026-05-23)

- **Section-bazlı harita per-section çağrı yapsa ücretsiz tier'a sığmaz** (300+ çağrı, gün başına 100 limit). Çözüm: per-file batch — her dosyayı LLM'e tek seferde verip "her section için ayrı özet üret" demek. 30 dosya = 30 çağrı, 1 saatte biter.
- **Gemini 2.5 Pro free tier datayı eğitime kullanabilir** — privacy hassasiyeti olan dokümanlar için Vertex AI (ücretli) veya local LLM gerekir. Mevcut proje için sorun değil.
- **Türkçe için BM25 problemli** (agglutinative dil — "token", "tokenı", "tokenlar" hepsi farklı kelime sanılır). bge-m3 hybrid mode bunu doğal olarak çözüyor.
- **Üç farklı LLM rolü var:** embedding (küçük, lokal), reranker (orta, lokal), generation (büyük, API). Bunları karıştırmamak gerek.
- **Windows + Bash subprocess + Rich uyumsuzluğu:** Typer'ın help renderer'ı (`rich.legacy_windows_render`) TTY olmayan subprocess'lerde Türkçe karakterde çöküyor. Çözüm: `app = typer.Typer(rich_markup_mode=None, pretty_exceptions_enable=False)` + `sys.stdout.reconfigure(encoding="utf-8")`. Gerçek interactive terminal'de zaten çalışıyordu; bu sadece subprocess senaryoları için.
- **PyPI indirme timeout'ları Windows'ta sık:** Büyük paketler (pyarrow, torch, docling) için `--default-timeout=600 --retries=10` veya tek tek indirme şart. `pip install -e .` atomic olduğu için tek paket fail edince hepsi tekrar dener; sırayla `pip install torch && pip install pyarrow && pip install -e .` daha güvenli.
- **bge-m3 CPU embedding hızı:** 42 chunk için ~66 sn (4 batch × 16 sn). 500 sayfa korpus için linear extrapolasyon ~15-30 dk doğru çıkıyor.
