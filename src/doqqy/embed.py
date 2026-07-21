"""bge-m3 dense + sparse embedding + LanceDB yazımı."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from doqqy.infra.settings import Settings  # Settings sadece tip kontrolü için import ediliyor

import numpy as np
import pandas as pd
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from doqqy.config import (
    EMBEDDING_BATCH_SIZE,
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    detect_device,
    get_logger,
)
from doqqy.workspace import Workspace

_LOG = get_logger("doqqy.embed")


def _load_chunks(ws: Workspace) -> pd.DataFrame:
    if not ws.chunks_parquet.exists():
        raise FileNotFoundError(
            f"{ws.chunks_parquet} yok — önce `doqqy chunk` çalıştır."
        )
    return pd.read_parquet(ws.chunks_parquet)


def _load_model():
    from FlagEmbedding import BGEM3FlagModel  # type: ignore

    device = detect_device()
    use_fp16 = device == "cuda"
    _LOG.info("model yükleniyor: %s (device=%s, fp16=%s)", EMBEDDING_MODEL, device, use_fp16)
    return BGEM3FlagModel(EMBEDDING_MODEL, use_fp16=use_fp16, device=device)


def _batched(seq: list[str], n: int) -> Iterator[list[str]]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def _embed_texts(model, texts: list[str]) -> tuple[np.ndarray, list[str]]:
    """Dense vektörler + sparse vektörler (JSON string listesi) döner."""
    dense_list: list[np.ndarray] = []
    sparse_list: list[str] = []

    batches = list(_batched(texts, EMBEDDING_BATCH_SIZE))
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]embed[/bold cyan]"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task("embed", total=len(batches))
        for batch in batches:
            out = model.encode(
                batch,
                batch_size=len(batch),
                max_length=1024,
                return_dense=True,
                return_sparse=True,
                return_colbert_vecs=False,
            )
            dense = np.asarray(out["dense_vecs"], dtype=np.float32)
            dense_list.append(dense)
            for sparse_dict in out["lexical_weights"]:
                sparse_list.append(json.dumps({str(k): float(v) for k, v in sparse_dict.items()}))
            progress.advance(task)

    dense_arr = np.vstack(dense_list) if dense_list else np.zeros((0, EMBEDDING_DIM), dtype=np.float32)
    return dense_arr, sparse_list


def build_index(ws: Workspace, *, batch_size: int | None = None, settings: Settings | None = None) -> int:
    """chunks.parquet → store.lance/chunks. Overwrites the existing table."""
    df = _load_chunks(ws)
    if df.empty:
        _LOG.warning("chunk yok, index oluşturulmadı.")
        return 0

    texts = df["content"].tolist()
    model = _load_model()
    dense_vecs, sparse_jsons = _embed_texts(model, texts)

    if dense_vecs.shape[0] != len(df):
        raise RuntimeError(
            f"embedding/satır uyumsuzluğu: {dense_vecs.shape[0]} vs {len(df)}"
        )
    if dense_vecs.shape[1] != EMBEDDING_DIM:
        _LOG.warning(
            "model %d boyut döndürdü, config EMBEDDING_DIM=%d.",
            dense_vecs.shape[1],
            EMBEDDING_DIM,
        )

    total_sparse_tokens = sum(len(json.loads(s)) for s in sparse_jsons)
    _LOG.info(
        "sparse vektörler: toplam %d token (ortalama %.1f/chunk)",
        total_sparse_tokens,
        total_sparse_tokens / len(sparse_jsons) if sparse_jsons else 0,
    )

    # Build ChunkRecord list
    from doqqy.infra.vectorstore.base import ChunkRecord
    from doqqy.infra.vectorstore.factory import make_store

    records = []
    for i, (_, row) in enumerate(df.iterrows()):
        sparse_vec = {int(k): float(v) for k, v in json.loads(sparse_jsons[i]).items()}

        tags = list(row["tags"]) if row.get("tags") is not None else []
        section_path = list(row["section_path"]) if row.get("section_path") is not None else []

        prev_chunk = row.get("prev_chunk")
        if pd.isna(prev_chunk) or prev_chunk is None:
            prev_chunk = None
        else:
            prev_chunk = str(prev_chunk)

        next_chunk = row.get("next_chunk")
        if pd.isna(next_chunk) or next_chunk is None:
            next_chunk = None
        else:
            next_chunk = str(next_chunk)

        rec = ChunkRecord(
            chunk_id=str(row["chunk_id"]),
            doc_id=str(row["doc_id"]),
            source=str(row["source"]),
            doc_type=str(row["doc_type"]),
            tags=tags,
            content=str(row["content"]),
            section_path=section_path,
            char_count=int(row["char_count"]),
            prev_chunk=prev_chunk,
            next_chunk=next_chunk,
            dense=np.asarray(dense_vecs[i], dtype=np.float32),
            sparse=sparse_vec,
        )
        records.append(rec)

    # Initialize store via factory and atomically rebuild from scratch.
    # full_rebuild() uses create_table(mode="overwrite") — a single LanceDB operation
    # that keeps the old table readable until the new one is fully written (no crash window).
    # recreate()+upsert() is reserved for the incremental path (issue #16: doqqy sync).
    with make_store(ws, settings) as store:
        n = store.full_rebuild(records, dim=EMBEDDING_DIM)

    _LOG.info("Vector store updated with %d records.", n)

    return n
