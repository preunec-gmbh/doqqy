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
doqqy --help
doqqy info
```

`doqqy info` sana mevcut pipeline durumunu söyler (kaç raw dosya, processed var mı, chunks ve store dolu mu).

## 2. Veri hazırlığı

`raw/` klasörüne işlenecek dokümanları koy. Klasör yapısını koruyabilirsin — `processed/`, `chunks/` ve sorgu sonuçları aynı yapıyı yansıtır.

Desteklenen formatlar: `.md`, `.markdown`, `.pdf`, `.docx`, `.txt`.

Diğer her şey (kod örnekleri, `.dll`, `package.json`, görseller) **otomatik olarak atlanır** — pipeline'ı kirletmez.

## 3. Pipeline'ı çalıştır

İlk kurulumda sırayla:

```powershell
doqqy ingest        # 1. Markdown'a dönüştür
doqqy chunk         # 2. Header-aware böl
doqqy embed         # 3. Vektöre dönüştür + indeksle
```

### `doqqy ingest`

```powershell
doqqy ingest                       # raw/ tamamı
doqqy ingest --source path/to/dir  # başka bir klasörden
doqqy ingest -n 5                  # ilk 5 dosya (smoke test)
```

Çıktı: `processed/<aynı yapı>/<dosya>.md`. Her dosyaya YAML frontmatter eklenir (kaynak, parser, hash vs.).

Hatalı dosyalar atlanır ve `logs/ingest.log`'a yazılır. Sonunda özet basılır:
```
OK: 318 başarılı, 2 başarısız, toplam 320.

Başarısız dosyalar:
  - raw/.../bozuk.pdf: hem docling hem pymupdf4llm başarısız. ...
```

### `doqqy chunk`

```powershell
doqqy chunk
doqqy chunk --processed path/to/processed  # başka bir kaynaktan
```

Çıktı: `chunks/chunks.parquet`. Parquet'i incelemek istersen:
```powershell
python -c "import pandas as pd; print(pd.read_parquet('chunks/chunks.parquet').head())"
```

### `doqqy embed`

```powershell
doqqy embed
```

**İlk çalıştırma:** HuggingFace'ten `BAAI/bge-m3` modeli iner (~2 GB, cache: `%USERPROFILE%\.cache\huggingface\`). Sonraki çalıştırmalar cache'ten okur.

Çıktı: `store.lance/chunks/` — LanceDB tablosu. GPU varsa otomatik kullanır (`DOQQY_DEVICE=cpu` ile zorlayabilirsin).

## 4. Harita üretimi (Faz 3)

Dokümanlar arasındaki ilişkileri keşfedip `topics.yaml` ve `INDEX.md` üretir. LLM çağrısı yok — tamamen local.

```powershell
doqqy map          # Pass 1 (regex) + Pass 2 (embedding cosine) → topics.yaml
doqqy map --pass1  # Sadece regex explicit referanslar
doqqy map --pass2  # Sadece embedding cosine tematik komşuluk
doqqy index        # topics.yaml → processed/INDEX.md
```

### `doqqy map`

```powershell
doqqy map                        # tüm processed/*.md, varsayılan eşik 0.75
doqqy map --threshold 0.80       # daha az ama daha güvenilir tematik bağlantı
doqqy map --top-n 10             # section başına maksimum 10 komşu (varsayılan 5)
doqqy map --processed path/to/   # farklı klasör
```

**Pass 1 — Regex:** `bkz.`, `bkz:`, `see section`, `see also`, parantez içi `(DOSYA.md)`, `[[WikiLink]]` kalıplarını yakalar. Bulduğu referansı bilinen dosya adlarıyla normalize eder.

**Pass 2 — Embedding cosine:** LanceDB'deki mevcut dense vektörlerden her section için bir centroid hesaplar, farklı dosyalardaki en yakın section'ları bulur. Eşik üstündekiler `might_be_related` olarak kaydedilir.

Çıktı: `topics.yaml` (proje kökünde):
```yaml
sections:
  - id: "PAYTR_REQUIREMENTS_odeme-akisi"
    file: "PAYTR_REQUIREMENTS.md"
    section: "## Ödeme Akışı"
    explicit_related: [...]     # regex ile bulunan
    might_be_related: [...]     # cosine benzerlikle bulunan, skorlu
```

### `doqqy index`

```powershell
doqqy index                              # topics.yaml → processed/INDEX.md
doqqy index --topics path/topics.yaml    # farklı topics dosyası
doqqy index --output path/to/vault/      # farklı çıktı klasörü
```

`processed/INDEX.md` Obsidian vault'unun giriş noktasıdır. Her dosyanın bağlantılı section'larını 📌 (explicit) ve 💡 (tematik) kategorilerde listeler.

## 5. Wikilink Enjeksiyonu (Faz 4)

`topics.yaml`'daki bağlantıları `processed/*.md` dosyalarına `[[wikilink]]` olarak enjekte eder. Obsidian graph view bu linklerle otomatik dolar.

```powershell
doqqy inject                              # topics.yaml → processed/*.md enjekte et
doqqy inject --dry-run                    # Neyin enjekte edileceğini göster, dosyaları değiştirme
doqqy inject --topics path/topics.yaml   # Farklı topics dosyası
```

**Önce `doqqy map` çalıştırılmış olmalı** — `topics.yaml` yoksa inject çalışmaz.

`inject` idempotent çalışır: her çalıştırmada önceki enjeksiyonu temizleyip yeniden yazar. `raw/` dosyaları asla değişmez.

Enjeksiyondan sonra `processed/` klasörünü Obsidian'da vault olarak aç — graph view dosyalar arası bağlantıları gösterir.

## 6. Çoklu Korpus ve Tag Filtreleme (Faz 5)

`raw/` altındaki klasör yapısı otomatik olarak etiket (tag) haline gelir. Örneğin:

```
raw/
  bulut-saha/
    genel/      ← tag: bulut-saha, genel
      ...
  erp12/        ← tag: erp12
    ...
```

```powershell
# Sistemde kayıtlı tüm tag'leri listele
doqqy tags

# Sadece belirli bir proje/klasörde ara
doqqy query "sipariş iade akışı" --tag erp12
doqqy query "ödeme entegrasyonu" -t bulut-saha

# Sadece belirli bir tag'in haritasını çıkar
doqqy map --tag erp12
doqqy map --tag bulut-saha --threshold 0.80
```

Tag filtreleme LanceDB seviyesinde SQL (`LIKE '%,tag,%'`) ile uygulanır — embedding araması ve harita üretimi yalnızca ilgili belge alt kümesiyle sınırlı kalır.

## 7. Sorgu

```powershell
doqqy query "JWT refresh nasıl çalışıyor?"
doqqy query "PayTR iade akışı" -k 10                    # top-10
doqqy query "stored procedure ekle cari kart" --full    # tam chunk göster
doqqy query "ödeme akışı" --tag paytr                   # sadece paytr klasöründe ara
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
- `-t, --tag TAG` — sadece bu tag/klasördeki dokümanlarda ara

## 7. Tipik akışlar

### Yeni dokümanlar geldi
Şu an inkremental update yok — tam rebuild:
```powershell
# raw/'a yeni dosyaları kopyala
doqqy ingest
doqqy chunk
doqqy embed   # model yüklü, sadece embedding süresi
```

### Sorgu sonuçları kötü — chunk ayarını değiştir
```powershell
# src/doqqy/config.py içinde CHUNK_MAX_TOKENS değerini değiştir
doqqy chunk    # processed/ ve raw/ değişmedi — sadece bunu çalıştır
doqqy embed    # yeni chunk'lar için vektör üret
```

### Bir dosyada parser sorunu var
```powershell
# logs/ingest.log'a bak
Get-Content logs/ingest.log -Tail 50

# Dosya bazlı dene
python -c "from doqqy.ingest import ingest_file; from pathlib import Path; print(ingest_file(Path('raw/.../sorunlu.pdf')))"
```

### CPU'ya zorla (GPU sorun çıkarıyorsa)
```powershell
$env:DOQQY_DEVICE = "cpu"
doqqy embed
```

## 8. Tam pipeline (ilk kurulum)

```powershell
doqqy ingest        # 1. Markdown'a dönüştür
doqqy chunk         # 2. Header-aware böl
doqqy embed         # 3. Vektöre dönüştür + indeksle
doqqy map           # 4. Harita üret → topics.yaml
doqqy index         # 5. topics.yaml → INDEX.md
doqqy inject        # 6. [[wikilink]] enjekte et → Obsidian graph view dolar
doqqy tags          # 7. Hangi tag'ler (klasör/proje) var? listele
doqqy query "..."   # Sor (opsiyonel: --tag ile filtrele)
```

## 9. Sık karşılaşılan sorunlar

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

### "store.lance yok — önce `doqqy embed` çalıştır"
`doqqy query` sırasında. Açıklayıcı: pipeline'ı sırayla yürütmemişsin. Önce `ingest → chunk → embed`.

### "chunks.parquet yok — önce `doqqy chunk` çalıştır"
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

## 9. Veri saklama

| Klasör | İçerik | Yedeklenmeli mi? |
|---|---|---|
| `raw/` | Orijinal dosyalar | **EVET** (kaynak gerçeği) |
| `processed/` | Ingest çıktısı | hayır (yeniden üretilebilir) |
| `chunks/` | Parquet | hayır |
| `store.lance/` | Vector store | hayır |
| `topics.yaml` | Harita verisi | hayır (yeniden üretilebilir) |
| `logs/` | Hata logları | hayır |

`raw/` ve `src/` versiyon kontrolünde olmalı. Geri kalan `.gitignore`'da.

## 10. Mevcut sınırlamalar

Şu özellikler **henüz yok**:

- Inkremental update — değişen dosyaları tespit etme yok, her seferinde tam rebuild
- PDF görselleri — yoksayılıyor (caption üretimi ileride)
- MCP server — Claude Code entegrasyonu sistemler stabilleştikten sonra

Tam roadmap için [memory-bank/progress.md](../memory-bank/progress.md).
