# docq

Yerel doküman bilgi sistemi. PDF, Markdown, DOCX ve TXT dosyalarını ingest eder, header-aware chunk'lara böler, **bge-m3** ile lokal embedding (dense + sparse) üretir, hibrit arama ve **bge-reranker-v2-m3** ile akıllı cross-encoder reranking yaparak anlık doğal-dilli arama imkanı verir.

LLM cevap sentezi **yapmaz** — sorgunun karşılığında ham chunk + kaynak (dosya yolu, başlık hiyerarşisi) döner. Kullanıcı her zaman orijinal metni görür.

## Hızlı başlangıç

```powershell
# 1. Bağımlılıklar
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .

# 2. Dokümanları raw/ altına koy (PDF, MD, DOCX, TXT)

# 3. Pipeline'ı çalıştır
docq ingest        # raw/ → processed/ (markdown)
docq chunk         # processed/ → chunks.parquet
docq embed         # → store.lance/  (bge-m3 dense + sparse vektör)

# 4. Sor
docq query "JWT refresh nasıl çalışıyor?"
docq query "PayTR iade akışı" --top-k 10
docq query "İade süreci" --no-rerank # Reranker'ı devre dışı bırakıp saf hibrit sonuçlara bak
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
│   ├── config.py            # yollar, sabitler, RAM/Model configleri
│   ├── chunk.py             # header-aware chunking
│   ├── embed.py             # bge-m3 dense+sparse LanceDB yazımı
│   ├── query.py             # Hibrit arama (Dense + Sparse) & RRF Birleşimi
│   ├── rerank.py            # bge-reranker-v2-m3 (cross-encoder test)
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

Faz 1 (MVP) ve Faz 2 tamamlandı; Testlerden başarıyla geçti. Mevcut özellikler:

- ✅ Ingest: `.md`, `.txt`, `.pdf` (docling + pymupdf4llm fallback), `.docx` (pandoc + mammoth fallback)
- ✅ Header-aware chunking (kod blokları ve tablolar atomik, Word bold testleri optimize)
- ✅ bge-m3 ile dense ve sparse embedding üretimi + JSON formatında LanceDB uyumu
- ✅ RAM Optimizasyonu (Embedding Batch Size:4 / Max Length: 1024)
- ✅ Hibrit Arama: Dense Arama + Manuel Python-side Sparse Hesaplama 
- ✅ RRF (Reciprocal Rank Fusion) puanı füzyon mekanizması (k=60)
- ✅ bge-reranker-v2-m3 (Transformers tabanlı Cross-encoder entegrasyonu)
- ✅ Typer CLI genişletilmiş parametreleri (`--no-rerank` ve detaylı RRF/Sigmoid skor analizleri)

Sonraki fazlarda gelecek:

- ⏳ **Faz 3:** Statik harita üretimi (Gemini 2.5 Pro ile `topics.yaml` + `INDEX.md`, Explicit/Thematic ilişkilendirme)
- ⏳ **Faz 4:** Obsidian vault polish (`[[wiki-link]]` enjeksiyonu, graph view)

## Lisans / Gizlilik

Local-first: sorgu zamanında **hiçbir** veri internet'e gönderilmez. Embedding ve reranker modelleri **tamamen lokal CPU/GPU gücünüzle çalışır**. Sadece Faz 3 statik harita üretimi external LLM (örn. Gemini 2.5) kullanır (kullanıcı kontrollü, tek seferlik opsiyoneldir).
