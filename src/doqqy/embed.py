"""bge-m3 dense + sparse embedding + LanceDB yazımı."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

import numpy as np
import pandas as pd
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn, TimeElapsedColumn

from doqqy.config import (
    EMBEDDING_BATCH_SIZE,
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    LANCE_TABLE,
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


def build_index(ws: Workspace, *, batch_size: int | None = None) -> int:
    """chunks.parquet → store.lance/chunks. Var olan tabloyu üzerine yazar."""
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

    df_out = df.copy()
    df_out["vector"] = list(dense_vecs)
    df_out["sparse_vector"] = sparse_jsons
    df_out["section_path_str"] = df_out["section_path"].apply(lambda xs: " > ".join(xs))
    # Array olan tags alanını LanceDB'nin kolay filtreleyebilmesi için
    # string (virgülle ayrılmış değerler) formatına çevirelim.
    # Örn: ["bulut-saha", "x"] -> ",bulut-saha,x,"
    df_out["tags_str"] = df_out["tags"].apply(lambda ts: f",{','.join(ts)}," if ts is not None and len(ts) > 0 else "")

    import lancedb  # type: ignore

    db = lancedb.connect(ws.store_dir)
    if LANCE_TABLE in db.list_tables().tables:
        db.drop_table(LANCE_TABLE)

    db.create_table(LANCE_TABLE, data=df_out, mode="overwrite")

    # Aynı process'te bu workspace için açık tablo handle'ı varsa bayatladı — düşür.
    from doqqy.query import invalidate_table_cache  # noqa: PLC0415 — döngüsel import önlemi

    invalidate_table_cache(ws)
    _LOG.info("LanceDB yazıldı: %s (%d satır).", ws.store_dir / LANCE_TABLE, len(df_out))
    return len(df_out)
