# Geliştirme

Sistemi genişletmek veya değiştirmek istersen başvuru rehberi.

## 1. Yeni bir format eklemek

Örnek: HTML desteği eklemek.

**Adım 1.** Yeni bir ingester yaz: `src/docq/ingest/html_ingest.py`

```python
from pathlib import Path
from docq.config import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR
from docq.ingest.base import Document, IngestError, base_metadata, content_hash


def _processed_path(source: Path) -> Path:
    rel = source.relative_to(RAW_DIR)
    return (PROCESSED_DIR / rel).with_suffix(".md")


def ingest_html(source: Path) -> Document:
    try:
        from markdownify import markdownify
    except ImportError as exc:
        raise IngestError("markdownify gerekli: pip install markdownify") from exc

    html = source.read_text(encoding="utf-8")
    md = markdownify(html, heading_style="ATX")
    if not md.strip():
        raise IngestError("boş içerik")

    meta = base_metadata(source, PROJECT_ROOT, kind="html")
    meta["content_hash"] = content_hash(md)
    return Document(source.resolve(), _processed_path(source), md, meta)
```

**Adım 2.** Router'a kaydet: `src/docq/ingest/router.py`

```python
from docq.ingest.html_ingest import ingest_html

_DISPATCH: dict[str, Callable[[Path], Document]] = {
    ...
    ".html": ingest_html,
    ".htm": ingest_html,
}
```

**Adım 3.** Config'e ekle: `src/docq/config.py`

```python
SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({
    ".md", ".markdown", ".pdf", ".docx", ".txt", ".html", ".htm"
})
```

**Adım 4.** `pyproject.toml`'a bağımlılık ekle ve `pip install -e .` ile güncelle.

Pipeline'ın geri kalanı (chunk, embed, query) hiç değişmez — format-agnostic olarak tasarlanmıştı.

## 2. Chunking ayarlarını değiştirmek

`src/docq/config.py`:

```python
CHUNK_MAX_TOKENS: int = 800        # daha büyük chunk için artır
CHUNK_OVERLAP: int = 100           # şu an kullanılmıyor (Faz 2)
CHUNK_MIN_MERGE_TOKENS: int = 100  # şu an kullanılmıyor (kısa section merge)
```

Değişiklik sonrası:
```powershell
docq chunk    # processed/ değişmedi, sadece bunu yeniden çalıştır
docq embed    # yeni chunk'lar için vektör
```

### Kısa section merge eklemek
`src/docq/chunk.py` → `chunk_file()` içinde header split sonrası, length split öncesi bir merge pass'i ekle. Aynı parent header altındaki ardışık kısa section'ları birleştir. Section path'leri için "OR" mantığı veya en yakın ortak ata.

### Token bazlı bölme
Şu an karakter bazlı (`~4 char ≈ 1 token`). Gerçek tokenizer için:

```python
from transformers import AutoTokenizer
TOKENIZER = AutoTokenizer.from_pretrained("BAAI/bge-m3")

def _len(text: str) -> int:
    return len(TOKENIZER.encode(text, add_special_tokens=False))
```

`_split_section` ve `_pack_blocks` içinde `len(text)` yerine `_len(text)` kullan.

## 3. Farklı embedding modeli

`src/docq/config.py`:

```python
EMBEDDING_MODEL: str = "BAAI/bge-m3"   # değiştir
EMBEDDING_DIM: int = 1024              # yeni modelin boyutu
```

Model bge-m3 dışındaysa `src/docq/embed.py` içindeki `BGEM3FlagModel` çağrısını ilgili sınıfla değiştir. `sentence-transformers` modelleri için:

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer(EMBEDDING_MODEL, device=detect_device())
vectors = model.encode(texts, batch_size=EMBEDDING_BATCH_SIZE, normalize_embeddings=True)
```

Sonrasında `docq embed` ile yeniden indeksle.

## 4. Sorgu cevabını zenginleştirmek

`src/docq/query.py` → `SearchHit` dataclass'ına alan ekle, `search()` içinde LanceDB'den o kolonu çek, `cli.py` → `query()` içinde göster.

Örnek: önceki ve sonraki chunk'ı bağlam olarak ekle:

```python
def search_with_context(query: str, k: int = 5):
    hits = search(query, k=k)
    table = _table()
    for hit in hits:
        prev_id = hit.extra.get("prev_chunk")
        if prev_id:
            prev = table.search().where(f"chunk_id = '{prev_id}'").to_list()
            if prev:
                hit.content = prev[0]["content"] + "\n\n---\n\n" + hit.content
        # next için aynı
    return hits
```

## 5. Yeni CLI komutu

`src/docq/cli.py`:

```python
@app.command()
def stats() -> None:
    """Chunk istatistikleri (uzunluk dağılımı, top dokümanlar, vs.)."""
    import pandas as pd
    from docq.config import CHUNKS_PARQUET
    df = pd.read_parquet(CHUNKS_PARQUET)
    typer.echo(f"toplam chunk: {len(df)}")
    typer.echo(f"ortalama karakter: {df['char_count'].mean():.0f}")
    typer.echo(f"medyan karakter: {df['char_count'].median():.0f}")
    typer.echo("\nEn çok chunk üretilen dokümanlar:")
    typer.echo(df['source'].value_counts().head(10).to_string())
```

## 6. Test yazmak

Şu an test yok (MVP). Test eklemek için:

```powershell
pip install pytest
mkdir tests
```

Örnek `tests/test_chunk.py`:

```python
from docq.chunk import _atomic_blocks, _split_section

def test_atomic_blocks_korunur():
    md = "Paragraf 1.\n\n```python\nfor x in range(10):\n    print(x)\n```\n\nParagraf 2."
    blocks = _atomic_blocks(md)
    code = next(b for b in blocks if b.startswith("```"))
    assert "for x in range(10)" in code
    assert "print(x)" in code

def test_uzun_section_bolunur():
    long = "Paragraf.\n\n" * 500
    chunks = _split_section(long)
    assert len(chunks) > 1
    assert all(len(c) <= 3200 + 100 for c in chunks)  # ~MAX_CHARS toleranslı
```

Çalıştır:
```powershell
pytest tests/ -v
```

## 7. Logging seviyesi

`src/docq/config.py` → `get_logger()` içinde varsayılan `logging.INFO`. Daha verbose için:

```python
import os
LEVEL = os.environ.get("DOCQ_LOG_LEVEL", "INFO")
logger.setLevel(LEVEL)
```

Sonra:
```powershell
$env:DOCQ_LOG_LEVEL = "DEBUG"
docq ingest
```

## 8. Kod kuralları

- **Format-agnostic core:** Ingest'ten sonra her şey markdown. Chunk/embed/query format bilmemeli.
- **Idempotency:** Her aşama yeniden çalıştırılabilir olmalı. `overwrite` veya rebuild varsayılan.
- **Failure isolation:** Bir dosya hatasında pipeline durmaz; log + raporda failed listesi.
- **Local-first:** Sorgu zamanında network çağrısı yok. Sadece Faz 3 harita external LLM.
- **Şeffaflık:** Kullanıcıya her zaman ham chunk + kaynak. LLM sentezi pipeline'a girmesin.
- **Path'ler:** `pathlib.Path` kullan, `os.path.join` yok. Encoding her zaman explicit `utf-8`.

## 9. Sonraki fazlara hazırlık

- **Faz 2 — Reranker:** `src/docq/rerank.py` yeni dosya, `bge-reranker-v2-m3` ile cross-encoder. `query.py` retrieval sonrasına entegre.
- **Faz 2 — Sparse:** `embed.py`'de `return_sparse=True` zaten parametre olarak hazır. LanceDB schema'sına sparse kolon ekle.
- **Faz 3 — Harita:** `src/docq/map_gen.py` yeni modül. Gemini client + per-file prompt template + `topics.yaml` writer + meta-call (cross-reference).
- **Faz 4 — Wikilink Enjeksiyon:** `src/docq/wikilink_inject.py` yeni modül. `topics.yaml`'dan `processed/*.md` içine `<!-- docq:links:start/end -->` marker bloklu `[[...]]` enjeksiyonu. `cli.py`'ye `docq inject` komutu eklenir (`--dry-run`, `--topics` flags).

Her faz başlamadan önce `memory-bank/fazlar/fazN.md` yaz; bittiğinde `progress.md` ve `activeContext.md`'yi güncelle.
