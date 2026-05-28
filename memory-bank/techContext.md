# Teknoloji Bağlamı

## Geliştirme Ortamı

- **OS:** Windows 10 Pro for Workstations
- **Shell:** PowerShell (Bash da kullanılabilir)
- **Python:** 3.10+ (mevcut: 3.10.11; orijinal plan 3.11+ idi, paket uyumu sebebiyle 3.10'a düşürüldü)
- **Çalışma dizini:** `c:\Users\Emirhan\Desktop\Preunec\puroje`
- **venv:** `.venv/` (proje kökünde, `pip install -e .` ile geliştirme kurulumu)

## Sistem Bağımlılıkları

- **pandoc** *(opsiyonel)* — DOCX → MD dönüşümü için ana parser. Kurulum:
  ```powershell
  winget install pandoc
  ```
  Doğrulama: `pandoc --version`. Kurulu değilse `docq` otomatik olarak `mammoth` (saf Python) fallback'ine geçer; sadece tablo/karmaşık layout'larda kalite farkı olur.
- **Python 3.10+** — `python --version` ile doğrula.

## Python Paketleri

### Core
- `python = ">=3.10"`
- `typer = "*"` — CLI framework
- `python-dotenv = "*"` — `.env` yükleme
- `tqdm = "*"` — progress bar
- `pyyaml = "*"` — `topics.yaml`

### Ingest
- `docling = "*"` — PDF (ana parser, IBM)
- `pymupdf4llm = "*"` — PDF (basit / hızlı fallback)
- `pypandoc = "*"` — pandoc Python wrapper (DOCX)
- `mammoth = "*"` — DOCX fallback
- `python-frontmatter = "*"` — MD frontmatter

### Chunking
- `langchain-text-splitters = "*"` — `MarkdownHeaderTextSplitter`

### Embedding + Vector Store
- `sentence-transformers = "*"` — bge-m3 yükleme/genel kullanım
- `FlagEmbedding = "*"` — bge-m3 **hybrid mode** için (resmi BAAI paketi, dense + sparse aynı anda)
- `lancedb = "*"` — vector store
- `pyarrow = "*"` — parquet / lance backend
- `pandas = "*"` — chunks dataframe

### Reranker
- `transformers` — `AutoModelForSequenceClassification` ile `bge-reranker-v2-m3` direkt. FlagEmbedding 1.4.0 tokenizer bug'ı nedeniyle FlagEmbedding kullanılmıyor.

### LLM (Harita Üretimi)
- `google-genai = "*"` — Gemini 2.5 Pro (ana)
- `anthropic = "*"` — Claude Opus 4.7 (fallback, opsiyonel)

## Modeller

### bge-m3 (Embedding)
- **HuggingFace:** `BAAI/bge-m3`
- **Boyut:** ~2 GB (ilk indirme)
- **Vektör boyutu:** dense 1024, sparse değişken
- **Multilingual:** evet, Türkçe iyi
- **Hybrid mode:** dense + sparse aynı modelden, tek pass'te.

### bge-reranker-v2-m3 (Reranker)
- **HuggingFace:** `BAAI/bge-reranker-v2-m3`
- **Gerçek boyut:** ~2.27 GB (dökümanlarda ~1.1 GB yazıyordu, gerçek daha büyük)
- **Tip:** Cross-encoder, multilingual, XLM-RoBERTa tabanlı.
- **Kullanım:** `transformers.AutoModelForSequenceClassification` ile direkt — FlagEmbedding 1.4.0'da tokenizer bug var.
- **Skor:** Logit → sigmoid → 0-1 normalize.

### Gemini 2.5 Pro (Harita LLM, Ana Seçenek)
- **Context:** 2M token
- **Free tier:** 5 RPM, ~100 req/gün (Google AI Studio)
- **Uyarı:** Free tier verisi Google tarafından model eğitiminde kullanılabilir. Privacy hassasiyeti varsa Vertex AI (ücretli) kullan. Mevcut proje için sorun değil.

### Claude Opus 4.7 (Fallback)
- **Model ID:** `claude-opus-4-7`
- **Context:** 1M token
- **Fiyat:** $15 / 1M input, $75 / 1M output
- **Prompt caching:** Anthropic SDK ile otomatik. 500 sayfalık korpus için cache hit ~%90, harita maliyeti $20-30 civarı.

## Teknik Kısıtlar

### Windows-Spesifik
- Tüm path'lerde `pathlib.Path` kullan. `os.path.join` yerine `Path / "foo"`.
- Subprocess çağrılarında (pandoc) `shell=True`'dan kaçın, list-form kullan: `["pandoc", "input.docx", "-o", "out.md"]`.
- Encoding: dosya okurken explicit `encoding="utf-8"` ver. Varsayılan Windows'ta `cp1254` olabilir, bozar.
- Symlink yok — dosya yolları absolute tut.

### Bellek
- bge-m3 CPU'da çalışabilir ama RAM'i ~3-4 GB tüketir.
- GPU varsa 10x hızlı (CUDA destekli `torch` kurulu olmalı).
- 500 sayfa korpus için embedding süresi: CPU'da ~15-30 dk, GPU'da ~2-3 dk.

### Network
- bge-m3 ve reranker ilk indirme HuggingFace'den (~2.5 GB toplam, tek seferlik).
- Gemini API çağrısı için internet bağlantısı gerekli (sadece harita üretiminde).
- **Sorgu zamanında network YOK** — tamamen local.

## Tool Kullanım Pattern'leri

### .env Dosyası

```
GEMINI_API_KEY=...
ANTHROPIC_API_KEY=...    # opsiyonel, fallback için
```

`.gitignore`'a eklenir, commit edilmez.

### CLI Komutları (Hedef)

```powershell
# Tam pipeline (sırayla)
python -m docq ingest
python -m docq chunk
python -m docq embed
python -m docq map           # LLM çağrısı yapar, dikkat

# Sorgu
python -m docq query "JWT refresh nasıl çalışıyor?"
python -m docq related auth/jwt-flow#3.2

# Vault aç
# Obsidian'da processed/ klasörünü vault olarak aç
```

### Logging

- `logs/ingest.log` — ingest hataları (parse fail, vs.)
- `logs/map.log` — LLM çağrı logları (request / response özetleri, token sayıları, gecikme)
- `tqdm` ile interactive progress; gerçek loglar stderr'e Python `logging` modülü ile.

### Gitignore

```
# Generated artifacts
processed/
chunks/
store.lance/
topics.yaml
logs/

# Secrets
.env

# Python
__pycache__/
*.pyc
.venv/
```

`raw/` ve `src/` commit edilir; `processed/` ve sonrası generated, her makine kendi build'ini yapar.

## Performans Beklentileri

| İşlem | Süre |
|---|---|
| Ingest (500 sayfa, karışık format) | 15-30 dk |
| Chunking | <1 dk |
| Embedding (CPU) | 15-30 dk |
| Embedding (GPU) | 2-3 dk |
| Harita üretimi (Gemini Pro, 30 dosya) | ~1 saat (rate limit ile) |
| Tek sorgu (rerank dahil) | <1 sn |
