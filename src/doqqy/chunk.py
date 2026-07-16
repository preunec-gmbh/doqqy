"""Header-aware chunking.

processed/*.md → chunks/chunks.parquet

Pipeline:
1. Frontmatter ayır, body al.
2. MarkdownHeaderTextSplitter ile H1..H4 başlıklara göre böl.
3. Section çok uzunsa, kod bloklarını ve tabloları atomik tutarak paragraf bazında alt-böl.
4. Section çok kısaysa, kendi başına chunk olur (MVP'de merge yok).
5. Aynı doküman içinde prev/next chunk bağlantıları kurulur.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

import frontmatter
import pandas as pd
from langchain_text_splitters import MarkdownHeaderTextSplitter
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from doqqy.config import (
    CHUNK_MAX_TOKENS,
    get_logger,
)
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.chunk")

# Approx 4 karakter ≈ 1 token (multilingual ortalama). Tam tokenizer Faz 2'de.
_MAX_CHARS = CHUNK_MAX_TOKENS * 4

_HEADERS_TO_SPLIT = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
    ("####", "h4"),
]

# Fenced code block — başlangıçtan kapanışa kadar.
_CODE_BLOCK_RE = re.compile(r"```.*?\n.*?```", re.DOTALL)
# GitHub-flavored markdown tablo bloğu (başlık satırı + ayraç satırı + en az 1 veri satırı).
_TABLE_BLOCK_RE = re.compile(
    r"(?:^\|.+\|\s*\n)(?:^\|[\s:|-]+\|\s*\n)(?:^\|.+\|\s*\n?)+",
    re.MULTILINE,
)
# Tek satırda tamamen bold olan ifadeler: __Başlık__ veya **Başlık**
_BOLD_HEADING_RE = re.compile(r"^(?:\*\*|__)(.+?)(?:\*\*|__)$", re.MULTILINE)


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    source: str
    doc_type: str
    content: str
    tags: list[str] = field(default_factory=list)
    section_path: list[str] = field(default_factory=list)
    char_count: int = 0
    prev_chunk: str | None = None
    next_chunk: str | None = None


def _atomic_blocks(text: str) -> list[str]:
    """Metni atomik bloklara böl: code/table tek parça, geri kalan paragrafa.

    Hiçbir blok max_chars'tan uzun değilse çıktının toplam karakter sayısı korunur.
    """
    # Atomik bloklar (code + table) sınırlarını topla
    atomics: list[tuple[int, int]] = []
    for rgx in (_CODE_BLOCK_RE, _TABLE_BLOCK_RE):
        for m in rgx.finditer(text):
            atomics.append((m.start(), m.end()))
    atomics.sort()

    blocks: list[str] = []
    pos = 0
    for start, end in atomics:
        if start > pos:
            prose = text[pos:start]
            blocks.extend(p for p in (s.strip() for s in re.split(r"\n{2,}", prose)) if p)
        atomic = text[start:end].strip()
        if atomic:
            blocks.append(atomic)
        pos = end
    if pos < len(text):
        tail = text[pos:]
        blocks.extend(p for p in (s.strip() for s in re.split(r"\n{2,}", tail)) if p)
    return blocks


def _pack_blocks(blocks: list[str], max_chars: int) -> list[str]:
    """Greedy packing: ardışık blokları max_chars sınırına kadar topla."""
    chunks: list[str] = []
    buf: list[str] = []
    buf_len = 0
    for block in blocks:
        # Tek başına çok büyük blok (örn. dev kod bloğu): kendi chunk'ı olur.
        if len(block) > max_chars:
            if buf:
                chunks.append("\n\n".join(buf))
                buf, buf_len = [], 0
            chunks.append(block)
            continue
        add_len = len(block) + (2 if buf else 0)
        if buf_len + add_len > max_chars:
            chunks.append("\n\n".join(buf))
            buf, buf_len = [block], len(block)
        else:
            buf.append(block)
            buf_len += add_len
    if buf:
        chunks.append("\n\n".join(buf))
    return chunks


def _split_section(text: str) -> list[str]:
    if len(text) <= _MAX_CHARS:
        return [text]
    return _pack_blocks(_atomic_blocks(text), _MAX_CHARS)


def _section_path_from_meta(meta: dict[str, str]) -> list[str]:
    path: list[str] = []
    for key in ("h1", "h2", "h3", "h4"):
        if value := meta.get(key):
            path.append(value)
    return path


def chunk_file(md_path: Path, ws: Workspace) -> list[Chunk]:
    with md_path.open("r", encoding="utf-8") as fh:
        post = frontmatter.load(fh)
    fm = post.metadata or {}
    body = post.content

    try:
        doc_id = str(md_path.relative_to(ws.root)).replace("\\", "/")
    except ValueError:
        doc_id = md_path.name

    source = fm.get("source", doc_id)
    doc_type = fm.get("type", "md")

    tags_raw = fm.get("tags")
    if tags_raw is None:
        tags = []
    elif isinstance(tags_raw, str):
        tags = [tags_raw]
    elif isinstance(tags_raw, list):
        if not all(isinstance(t, str) for t in tags_raw):
            _LOG.warning("Geçersiz etiket formatı: etiket listesi string olmayan elemanlar içeriyor. Boş listeye çevriliyor: %s", tags_raw)
            tags = []
        else:
            tags = tags_raw
    else:
        _LOG.warning("Geçersiz etiket tipi: %s. Boş listeye çevriliyor.", type(tags_raw))
        tags = []

    # Tek satırda tamamen bold olan ifadeleri ## başlığa çevir (Word'de Heading stili yerine
    # bold kullanan dokümanlar için: __A224. Toplantı__ → ## A224. Toplantı)
    body = _BOLD_HEADING_RE.sub(r"## \1", body)

    splitter = MarkdownHeaderTextSplitter(_HEADERS_TO_SPLIT, strip_headers=False)
    raw_sections = splitter.split_text(body) if body.strip() else []

    if not raw_sections:
        # Hiç header yoksa: tüm dokümanı tek section kabul et.
        raw_sections = [type("Tmp", (), {"page_content": body, "metadata": {}})()]

    chunks: list[Chunk] = []
    for section in raw_sections:
        path = _section_path_from_meta(section.metadata)
        for piece in _split_section(section.page_content.strip()):
            if not piece.strip():
                continue
            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    doc_id=doc_id,
                    source=source,
                    doc_type=doc_type,
                    tags=tags,
                    content=piece,
                    section_path=path,
                    char_count=len(piece),
                )
            )

    # Doküman içi prev/next bağla
    for i, c in enumerate(chunks):
        c.prev_chunk = chunks[i - 1].chunk_id if i > 0 else None
        c.next_chunk = chunks[i + 1].chunk_id if i < len(chunks) - 1 else None

    return chunks


def chunk_directory(ws: Workspace, *, processed_dir: Path | None = None) -> list[Chunk]:
    processed_dir = processed_dir or ws.processed_dir
    if not processed_dir.exists():
        raise FileNotFoundError(f"processed dizini yok: {processed_dir}")

    md_files = sorted(processed_dir.rglob("*.md"))
    all_chunks: list[Chunk] = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]chunk[/bold cyan]"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("chunk", total=len(md_files))
        for md_file in md_files:
            progress.update(task, description=f"[dim]{md_file.name}[/dim]", advance=1)
            try:
                file_chunks = chunk_file(md_file, ws)
                all_chunks.extend(file_chunks)
            except Exception as exc:  # noqa: BLE001
                _LOG.exception("chunk hatası: %s — %s", md_file, exc)

    if not all_chunks:
        _LOG.warning("hiç chunk üretilmedi.")
        return []

    df = pd.DataFrame([asdict(c) for c in all_chunks])
    ws.chunks_parquet.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ws.chunks_parquet, index=False)
    _LOG.info("yazıldı: %s (%d chunk).", ws.chunks_parquet, len(all_chunks))
    return all_chunks
