# docq

Yerel doküman bilgi sistemi. PDF, Markdown, DOCX ve TXT dosyalarını ingest eder, header-aware chunk'lara böler, **bge-m3** ile lokal embedding üretir ve **LanceDB** üzerinde anlık doğal-dilli arama imkanı verir.

LLM cevap sentezi **yapmaz** — sorgunun karşılığında ham chunk + kaynak (dosya yolu, başlık hiyerarşisi) döner. Kullanıcı her zaman orijinal metni görür.

## Hızlı başlangıç

```powershell
# 1. Bağımlılıklar
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .

# 2. Dokümanları raw/ altına koy (PDF, MD, DOCX, TXT)
#    Var olan docs/'u kopyaladıysan zaten dolu.

# 3. Pipeline'ı çalıştır
docq ingest        # raw/ → processed/ (markdown)
docq chunk         # processed/ → chunks.parquet
docq embed         # → store.lance/  (ilk çalıştırmada bge-m3 ~2 GB iner)

# 4. Sor
docq query "JWT refresh nasıl çalışıyor?"
docq query "PayTR iade akışı" --top-k 10
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
├── store.lance/             # AŞAMA 3 ÇIKTI — LanceDB vector store (gitignore'da)
├── logs/                    # ingest hata logları (gitignore'da)
│
├── src/docq/                # KAYNAK KOD
│   ├── cli.py               # typer komutları
│   ├── config.py            # yollar, sabitler
│   ├── chunk.py             # header-aware chunking
│   ├── embed.py             # bge-m3 + LanceDB yazımı
│   ├── query.py             # cosine arama
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
        └── ...
```

## Belgeler

- **Mimari ve veri akışı:** [documentation/MIMARI.md](documentation/MIMARI.md)
- **CLI komut referansı + tipik akışlar:** [documentation/KULLANIM.md](documentation/KULLANIM.md)
- **Yeni format/model eklemek:** [documentation/GELISTIRME.md](documentation/GELISTIRME.md)

## Geçerli durum

Faz 1 (MVP) kodu yazıldı; smoke test bekliyor. Mevcut özellikler:

- ✅ Ingest: `.md`, `.txt`, `.pdf` (docling + pymupdf4llm fallback), `.docx` (pandoc + mammoth fallback)
- ✅ Header-aware chunking (kod blokları ve tablolar atomik)
- ✅ bge-m3 dense embedding + LanceDB yazımı
- ✅ Cosine dense arama
- ✅ Typer CLI

Sonraki fazlarda gelecek:

- ⏳ **Faz 2:** bge-m3 sparse vektör + Reciprocal Rank Fusion + cross-encoder reranker
- ⏳ **Faz 3:** Statik harita üretimi (Gemini 2.5 Pro ile `topics.yaml` + `INDEX.md`)
- ⏳ **Faz 4:** Obsidian vault polish (`[[wiki-link]]` enjeksiyonu, graph view)

## Lisans / Gizlilik

Local-first: sorgu zamanında **hiçbir** veri internet'e gönderilmez. Embedding ve reranker tamamen lokal çalışır. Sadece Faz 3 harita üretimi external LLM kullanır (tek seferlik, opsiyonel).
