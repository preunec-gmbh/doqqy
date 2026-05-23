# Kullanım

CLI komutları, tipik akışlar ve sık karşılaşılan sorunlar.

## 1. Kurulum

### Gereksinimler
- **Windows 10/11** (Linux/macOS'ta da çalışmalı ama test edilmedi)
- **Python 3.10+**
- **(Opsiyonel) pandoc CLI** — `.docx` dosyaları için en iyi kalite. Kurulu değilse `mammoth` (saf Python) fallback otomatik devreye girer.
  ```powershell
  winget install pandoc
  ```
- **(Opsiyonel) CUDA destekli NVIDIA GPU** — embedding ~10x hızlanır. CPU'da da çalışır.

### Adım adım

```powershell
# 1. Repo'yu klonla / dosyaları al
cd c:\path\to\puroje

# 2. Virtual env oluştur ve aktifleştir
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Paket + bağımlılıkları kur (editable mode)
pip install --default-timeout=600 -e .
```

İndirme ~500 MB – 1 GB sürer (en büyüğü `torch` ~200 MB). Ağ yavaşsa `--default-timeout=600 --retries=10` ekle.

### Doğrulama

```powershell
docq --help
docq info
```

`docq info` sana mevcut pipeline durumunu söyler (kaç raw dosya, processed var mı, chunks ve store dolu mu).

## 2. Veri hazırlığı

`raw/` klasörüne işlenecek dokümanları koy. Klasör yapısını koruyabilirsin — `processed/`, `chunks/` ve sorgu sonuçları aynı yapıyı yansıtır.

Desteklenen formatlar: `.md`, `.markdown`, `.pdf`, `.docx`, `.txt`.

Diğer her şey (kod örnekleri, `.dll`, `package.json`, görseller) **otomatik olarak atlanır** — pipeline'ı kirletmez.

## 3. Pipeline'ı çalıştır

İlk kurulumda sırayla:

```powershell
docq ingest        # 1. Markdown'a dönüştür
docq chunk         # 2. Header-aware böl
docq embed         # 3. Vektöre dönüştür + indeksle
```

### `docq ingest`

```powershell
docq ingest                       # raw/ tamamı
docq ingest --source path/to/dir  # başka bir klasörden
docq ingest -n 5                  # ilk 5 dosya (smoke test)
```

Çıktı: `processed/<aynı yapı>/<dosya>.md`. Her dosyaya YAML frontmatter eklenir (kaynak, parser, hash vs.).

Hatalı dosyalar atlanır ve `logs/ingest.log`'a yazılır. Sonunda özet basılır:
```
OK: 318 başarılı, 2 başarısız, toplam 320.

Başarısız dosyalar:
  - raw/.../bozuk.pdf: hem docling hem pymupdf4llm başarısız. ...
```

### `docq chunk`

```powershell
docq chunk
docq chunk --processed path/to/processed  # başka bir kaynaktan
```

Çıktı: `chunks/chunks.parquet`. Parquet'i incelemek istersen:
```powershell
python -c "import pandas as pd; print(pd.read_parquet('chunks/chunks.parquet').head())"
```

### `docq embed`

```powershell
docq embed
```

**İlk çalıştırma:** HuggingFace'ten `BAAI/bge-m3` modeli iner (~2 GB, cache: `%USERPROFILE%\.cache\huggingface\`). Sonraki çalıştırmalar cache'ten okur.

Çıktı: `store.lance/chunks/` — LanceDB tablosu. GPU varsa otomatik kullanır (`DOCQ_DEVICE=cpu` ile zorlayabilirsin).

## 4. Sorgu

```powershell
docq query "JWT refresh nasıl çalışıyor?"
docq query "PayTR iade akışı" -k 10                    # top-10
docq query "stored procedure ekle cari kart" --full    # tam chunk göster
```

Örnek çıktı:
```
[1] score=0.847  raw/PAYTR/.../PayTR İade API.pdf
    1. Genel Bilgi > 1.3 Kullanım Şartları
    İade işlemi şu adımlarla gerçekleşir:
    1. POST /odeme/iade endpoint'ine ...
    … (1234 karakter daha)

[2] score=0.792  raw/ERIMELEKTRONIK/SIPARIS_REQUIREMENTS.md
    Sipariş İade Akışı
    Müşteri iade talebi oluşturduğunda ...
```

Flags:
- `-k, --top-k N` — kaç sonuç (varsayılan 5)
- `--full` — chunk'ı kesmeden tam göster (varsayılan ilk 400 karakter)

## 5. Tipik akışlar

### Yeni dokümanlar geldi
Şu an inkremental update yok — tam rebuild:
```powershell
# raw/'a yeni dosyaları kopyala
docq ingest
docq chunk
docq embed   # model yüklü, sadece embedding süresi
```

### Sorgu sonuçları kötü — chunk ayarını değiştir
```powershell
# src/docq/config.py içinde CHUNK_MAX_TOKENS değerini değiştir
docq chunk    # processed/ ve raw/ değişmedi — sadece bunu çalıştır
docq embed    # yeni chunk'lar için vektör üret
```

### Bir dosyada parser sorunu var
```powershell
# logs/ingest.log'a bak
Get-Content logs/ingest.log -Tail 50

# Dosya bazlı dene
python -c "from docq.ingest import ingest_file; from pathlib import Path; print(ingest_file(Path('raw/.../sorunlu.pdf')))"
```

### CPU'ya zorla (GPU sorun çıkarıyorsa)
```powershell
$env:DOCQ_DEVICE = "cpu"
docq embed
```

## 6. Sık karşılaşılan sorunlar

### "ReadTimeoutError" — pip install'da
Ağ yavaş veya dengesiz. Çözüm:
```powershell
pip install --default-timeout=600 --retries=10 -e .
```
Tekrar timeout olursa büyük paketleri tek tek indir:
```powershell
pip install torch
pip install pyarrow docling
pip install -e .
```

### "No pandoc was found"
`.docx` ingest sırasında çıkar. **Hata değil — uyarı.** Otomatik olarak mammoth'a düşer. İstersen `winget install pandoc` ile daha iyi kaliteye geç.

### "store.lance yok — önce `docq embed` çalıştır"
`docq query` sırasında. Açıklayıcı: pipeline'ı sırayla yürütmemişsin. Önce `ingest → chunk → embed`.

### "chunks.parquet yok — önce `docq chunk` çalıştır"
Benzer şekilde. Sırayla yürüt.

### Çok yavaş — embed'de takıldı
GPU yoksa CPU'da bge-m3 yavaştır (500 sayfa ~15-30 dk). Normaldir. `tqdm` progress bar'ı bittiğinde tamamlanır.

### Türkçe karakter sorunu (mojibake)
PowerShell'de çıktı bozuksa:
```powershell
chcp 65001  # UTF-8 code page
```

### "encoding error" .txt ingest'inde
UTF-8 decode başarısız olursa otomatik latin-1 fallback var. Yine de bozuk çıkarsa dosyanın gerçek encoding'ini bul (Notepad++ veya `chardet`) ve `md_ingest.py:ingest_txt`'i geçici olarak güncelle.

## 7. Veri saklama

| Klasör | İçerik | Yedeklenmeli mi? |
|---|---|---|
| `raw/` | Orijinal dosyalar | **EVET** (kaynak gerçeği) |
| `processed/` | Ingest çıktısı | hayır (yeniden üretilebilir) |
| `chunks/` | Parquet | hayır |
| `store.lance/` | Vector store | hayır |
| `logs/` | Hata logları | hayır |

`raw/` ve `src/` versiyon kontrolünde olmalı. Geri kalan `.gitignore`'da.

## 8. Faz 1 sınırlamaları

Bu MVP. Şu özellikler **henüz yok**:

- Inkremental update — değişen dosyaları tespit etme yok, her seferinde tam rebuild
- Hibrit arama — sadece dense vektör (sparse + reranker Faz 2'de gelecek)
- Statik harita — `INDEX.md` ve `topics.yaml` üretimi Faz 3'te
- Wiki-link enjeksiyonu — Obsidian graph view Faz 4'te
- PDF görselleri — yoksayılıyor (caption üretimi ileride)
- MCP server — Claude Code entegrasyonu sistemler stabilleştikten sonra

Tam roadmap için [memory-bank/progress.md](../memory-bank/progress.md).
