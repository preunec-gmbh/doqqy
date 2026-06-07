# Faz 5 — Çoklu Korpus ve Tag Filtreleme Implementation Notları

Gerçekte ne yapıldı, neden, hangi noktalarda plandan saptık.

## 1. Durum Özeti

**🟢 Faz 5 TAMAM (2026-06-07)**

## 2. Amaç

Faz 4 sonunda elimizde tek bir büyük corpus var: `raw/` altında PayTR, ERP12, Erimelektronik ve genel dokümanlar karışık halde. `doqqy query` her aramada tüm korpusu tarıyor — proje bazlı izolasyon yok.

Faz 5 bu boşluğu dolduruyor:

- `raw/` altındaki klasör kırılımları otomatik olarak **tag** haline gelir.
- `doqqy query --tag <TAG>` ile arama belirli bir proje/konuya kısıtlanır.
- `doqqy map --tag <TAG>` ile harita belirli bir tag alt kümesi üzerinden çıkarılır.
- `doqqy tags` ile sistemdeki tüm kayıtlı tag'ler listelenir.

## 3. Temel Tasarım Kararları

| Karar | Gerekçe |
|---|---|
| Tag'ler `raw/` klasör kırılımından otomatik üretilir | Kullanıcı ek metadata yazmasın; mevcut klasör yapısı zaten semantik bilgi taşıyor |
| LanceDB'ye `tags_str` string olarak serialize edilir | LanceDB `list[str]` üzerinde `LIKE` / `IN` SQL filtresi desteklemez; `",tag1,tag2,"` formatı tam eşleşmeyi garanti eder |
| Virgüllü format (öne+sona) | `"bulut"` ile `"bulut-saha"` eşleşmesini önler — `LIKE '%,bulut,%'` yalnızca tam `bulut` etiketini yakalar |
| Filtreleme LanceDB seviyesinde uygulanır | Python'a çekmeden önce filtrele; büyük korpora'da bellek tasarrufu |
| `doqqy chunk` ve `doqqy embed` yeterli; yeni komut gerekmez | Tag'ler ingest → chunk → embed pipeline'ına seamlessly entegre; kullanıcı ek adım yapmaz |

## 4. Klasör → Tag Eşlemesi

`raw/` altındaki klasör kırılımı tag listesine dönüştürülür; son parça (dosya adı) atılır:

```
raw/bulut-saha/genel/dokuman.pdf          → tags: ["bulut-saha", "genel"]
raw/erp12/faturalama/odeme-api.md         → tags: ["erp12", "faturalama"]
raw/genel/readme.txt                      → tags: ["genel"]
raw/direkt-dosya.pdf                      → tags: []   (alt klasör yok)
```

`raw/` prefix'i atılır. Yalnızca ara klasörler tag olur.

## 5. LanceDB Serialize Formatı

Tags listesi `embed.py`'de LanceDB'ye yazılmadan önce string'e çevrilir:

```python
# ["bulut-saha", "genel"]  →  ",bulut-saha,genel,"
df_out["tags_str"] = df_out["tags"].apply(
    lambda ts: f",{','.join(ts)}," if ts else ""
)
```

Filtreleme SQL'i:
```sql
tags_str LIKE '%,bulut-saha,%'
```

Bu format `"bulut"` ile `"bulut-saha"` arasında yanlış eşleşme olmadığını garantiler.

## 6. Değiştirilen Modüller

### `ingest/base.py` — `base_metadata()`

```python
parts = list(rel.parts)
if parts and parts[0] == "raw":
    parts = parts[1:]
tags = parts[:-1] if len(parts) > 1 else []

return {
    "source": ...,
    "type": kind,
    "tags": tags,
    "ingested_at": ...,
}
```

### `chunk.py` — `Chunk` dataclass

```python
@dataclass
class Chunk:
    ...
    tags: list[str] = field(default_factory=list)
    ...
```

`chunk_file()` içinde frontmatter'dan okunur: `tags = fm.get("tags", [])`.

### `embed.py` — `build_index()`

```python
df_out["tags_str"] = df_out["tags"].apply(
    lambda ts: f",{','.join(ts)}," if ts else ""
)
```

### `query.py` — `search()`, `_dense_search()`, `_sparse_search()`

```python
def _dense_search(qvec, k, filter_tag=None):
    qb = _table().search(qvec).metric("cosine")
    if filter_tag:
        qb = qb.where(f"tags_str LIKE '%,{filter_tag},%'")
    return qb.limit(k).to_list()

def _sparse_search(query_sparse, k, filter_tag=None):
    if filter_tag:
        rows = _table().search().where(f"tags_str LIKE '%,{filter_tag},%'").to_pandas()
    else:
        rows = _table().to_pandas()
    ...

def search(query, k=DEFAULT_TOP_K, rerank=True, tag=None):
    dense_rows = _dense_search(dense_vec, RETRIEVAL_TOP_K, filter_tag=tag)
    sparse_rows = _sparse_search(sparse_vec, RETRIEVAL_TOP_K, filter_tag=tag)
    ...
```

### `map_gen.py` — `_pass2()`, `generate_map()`

```python
def _pass2(processed_dir, sections_meta, top_n, threshold, filter_tag=None):
    if filter_tag:
        df = table.search().where(f"tags_str LIKE '%,{filter_tag},%'").to_pandas()
    else:
        df = table.to_pandas()
    ...

def generate_map(..., tag=None):
    thematic_map = _pass2(..., filter_tag=tag)
    ...
```

### `cli.py` — Yeni komutlar ve parametreler

```python
# doqqy query'ye --tag/-t eklendi
@app.command()
def query(..., tag: Optional[str] = typer.Option(None, "--tag", "-t", ...)):
    hits = search(query_text, k=k, rerank=not no_rerank, tag=tag)

# doqqy map'e --tag/-t eklendi (--threshold'un -t shorthand'i kaldırıldı)
@app.command()
def map(..., tag: Optional[str] = typer.Option(None, "--tag", "-t", ...)):
    generate_map(..., tag=tag)

# YENİ: doqqy tags
@app.command()
def tags():
    """Sistemde kayıtlı olan tag/klasör/proje isimlerini listeler."""
    df = table.search().limit(100000).to_pandas()
    all_tags = set()
    for t_list in df["tags"].dropna():
        for t in t_list:
            all_tags.add(t)
    ...
```

**Not:** `doqqy map`'te `--threshold` için `-t` shorthand'i vardı. `--tag` için de `-t` ekleyince çakışma oluştu. `--threshold`'un shorthand'i kaldırılarak `--tag` için `-t` kullanıldı.

## 7. Dosya Değişiklikleri

| Dosya | Değişiklik |
|---|---|
| `src/doqqy/ingest/base.py` | `base_metadata()` — `tags` alanı eklendi |
| `src/doqqy/chunk.py` | `Chunk.tags: list[str]` alanı + `chunk_file()` frontmatter okuması |
| `src/doqqy/embed.py` | `build_index()` — `tags_str` kolonu LanceDB'ye yazılıyor |
| `src/doqqy/query.py` | `search()`, `_dense_search()`, `_sparse_search()` — `filter_tag` parametresi |
| `src/doqqy/map_gen.py` | `_pass2()`, `generate_map()` — `filter_tag` / `tag` parametresi |
| `src/doqqy/cli.py` | `doqqy query --tag`, `doqqy map --tag`, yeni `doqqy tags` komutu |

## 8. Bilinen Sınırlamalar

- **`doqqy embed` yeniden çalıştırılmalı:** Mevcut LanceDB index'inde `tags_str` kolonu yok. Faz 5 değişikliklerinin etkili olması için `doqqy chunk` + `doqqy embed` baştan çalıştırılmalı.
- **`--threshold`'un `-t` shorthand'i kalktı:** `doqqy map -t 0.80` artık çalışmaz; `doqqy map --threshold 0.80` kullanılmalı.
- **`doqqy tags` tüm tabloyu çeker:** `LIMIT 100000` ile kısıtlı — çok büyük korpuslar için yavaş olabilir. Pratik kullanımda sorun değil.
- **Alt-alt klasör tag'leri ayrı satırlarda:** `raw/a/b/c/dosya.pdf` → `tags: ["a", "b", "c"]`. Kullanıcı `--tag a` yazarsa `a` altındaki her şey gelir (b, c dahil), `--tag b` yazarsa sadece `b` altındakiler. Bu tasarım gereği.

## 9. Faz Sonrası (Faz 6+ / Roadmap)

- **Inkremental update:** Content hash bazlı diff — sadece değişen dosyaları yeniden işle
- **MCP server:** Claude Code entegrasyonu için doqqy'u MCP sunucusu olarak sun
- **Web arayüz:** (Belki) basit bir UI
