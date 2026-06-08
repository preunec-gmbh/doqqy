# doqqy

Yerel doküman bilgi sistemi. PDF, Markdown, DOCX ve TXT dosyalarını ingest eder, header-aware chunk'lara böler, **bge-m3** ile lokal embedding (dense + sparse) üretir, hibrit arama ve **bge-reranker-v2-m3** ile akıllı cross-encoder reranking yaparak anlık doğal-dilli arama imkanı verir. **bge-m3 embedding cosine benzerliği** ile dokümanlar arası otomatik harita (`.doqqy/topics.yaml` + `INDEX.md`) üretir.

LLM çağrısı **yapmaz** — ne sorgularda ne de harita üretiminde. Ham chunk + kaynak döner, harita embedding matematiğiyle kurulur.

## Hızlı başlangıç

```powershell
# 1. Bağımlılıklar
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .

# 2. Dokümanları raw/ altına koy (PDF, MD, DOCX, TXT)
#    Klasör yapısı otomatik olarak tag'e dönüşür: raw/proje-a/... → tag: "proje-a"

# 3. Pipeline
doqqy ingest        # raw/ → processed/ (markdown)
doqqy chunk         # processed/ → chunks.parquet
doqqy embed         # → .doqqy/store.lance/  (bge-m3 dense + sparse vektör)

# 4. Harita üret
doqqy map           # processed/*.md → .doqqy/topics.yaml (regex + embedding cosine)
doqqy index         # .doqqy/topics.yaml → processed/INDEX.md
doqqy inject        # .doqqy/topics.yaml → processed/*.md içine [[wikilink]] enjekte et

# 5. Sor
doqqy query "JWT refresh nasıl çalışıyor?"
doqqy query "PayTR iade akışı" --top-k 10
doqqy query "iade süreci" --tag erp12        # sadece erp12 klasöründe ara
doqqy tags                                   # hangi tag'ler var?
```

## Proje yapısı

```
puroje/
├── README.md                # bu dosya — başlangıç noktası
├── pyproject.toml           # paket + bağımlılıklar
├── .env.example             # API anahtarları (sadece Faz 3 harita üretimi için)
│
├── raw/                     # GİRDİ — orijinal dosyalar (gitignore'da)
├── processed/               # AŞAMA 1 ÇIKTI — kanonik markdown (gitignore'da)
├── chunks/                  # AŞAMA 2 ÇIKTI — chunks.parquet (gitignore'da)
├── .doqqy/store.lance/             # AŞAMA 3 ÇIKTI — LanceDB vector store (gitignore'da)
├── .doqqy/topics.yaml              # AŞAMA 4 ÇIKTI — harita verisi (gitignore'da)
├── .doqqy/logs/                    # ingest hata logları (gitignore'da)
│
├── src/doqqy/                # KAYNAK KOD
│   ├── cli.py               # typer komutları
│   ├── config.py            # yollar, sabitler, RAM/Model configleri
│   ├── chunk.py             # header-aware chunking
│   ├── embed.py             # bge-m3 dense+sparse LanceDB yazımı
│   ├── query.py             # Hibrit arama (Dense + Sparse) & RRF Birleşimi
│   ├── rerank.py            # bge-reranker-v2-m3 (cross-encoder)
│   ├── map_gen.py           # Pass 1 (regex) + Pass 2 (cosine) → .doqqy/topics.yaml
│   ├── index_gen.py         # .doqqy/topics.yaml → INDEX.md
│   └── ingest/              # format-spesifik parser'lar
│
├── documentation/           # İNSANLAR İÇİN BELGELER
│   ├── MIMARI.md            # sistem mimarisi, veri akışı, modül-modül açıklama
│   ├── KULLANIM.md          # CLI komut referansı, tipik akışlar, FAQ
│   └── GELISTIRME.md        # yeni format eklemek, ayar değiştirmek
│
└── memory-bank/             # AJANLAR İÇİN NOTLAR
    ├── projectbrief.md      # proje briefi
    ├── productContext.md    # neden var, nasıl çalışmalı
    ├── activeContext.md     # şu anki durum
    ├── progress.md          # ne tamam, ne pending
    ├── systemPatterns.md    # mimari pattern'ler
    ├── techContext.md       # teknoloji stack'i
    └── fazlar/              # her faz için detaylı implementation notu
        ├── faz1.md
        ├── faz2.md
        └── ...
```

## Belgeler

- **Mimari ve veri akışı:** [documentation/MIMARI.md](documentation/MIMARI.md)
- **CLI komut referansı + tipik akışlar:** [documentation/KULLANIM.md](documentation/KULLANIM.md)
- **Yeni format/model eklemek:** [documentation/GELISTIRME.md](documentation/GELISTIRME.md)

## Geçerli durum

Faz 1–5 tamamlandı. Mevcut özellikler:

- ✅ Ingest: `.md`, `.txt`, `.pdf` (docling + pymupdf4llm fallback), `.docx` (pandoc + mammoth fallback)
- ✅ Header-aware chunking (kod blokları ve tablolar atomik, Word bold başlıklar optimize)
- ✅ bge-m3 ile dense ve sparse embedding üretimi + LanceDB
- ✅ RAM Optimizasyonu (Embedding Batch Size:4 / Max Length: 1024)
- ✅ Hibrit Arama: Dense + Sparse (Manuel Python-side dot product) + RRF (k=60)
- ✅ bge-reranker-v2-m3 (Transformers tabanlı Cross-encoder)
- ✅ Harita üretimi: Pass 1 (regex explicit referanslar) + Pass 2 (embedding cosine tematik komşuluk) → `.doqqy/topics.yaml`
- ✅ `INDEX.md` üretimi — Obsidian vault giriş noktası
- ✅ Wikilink enjeksiyonu: `.doqqy/topics.yaml` → `processed/*.md` içine `[[link]]` (idempotent, `doqqy inject`)
- ✅ Çoklu korpus / tag filtreleme: `raw/` klasör yapısından otomatik tag üretimi, `doqqy query --tag` ve `doqqy map --tag` ile izole arama
- ✅ Typer CLI ve Rich UI: `ingest`, `chunk`, `embed`, `map`, `index`, `query`, `inject`, `tags`, `info` (Formatlı paneller, interaktif process barlar)
- 🎯 **Planlanan:** Inkremental update (Sadece değişen dosyaları işleme almak)

## Lisans / Gizlilik

Local-first: sorgu zamanında **hiçbir** veri internet'e gönderilmez. Embedding, reranker ve harita üretimi **tamamen lokal CPU/GPU gücünüzle çalışır**. Dış API çağrısı yoktur.
