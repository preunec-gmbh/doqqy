"""bge-m3 dense + sparse embedding + LanceDB yazımı."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

import numpy as np
import pandas as pd
from tqdm import tqdm

from docq.config import (
    CHUNKS_PARQUET,
    EMBEDDING_BATCH_SIZE,
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    LANCE_TABLE,
    STORE_DIR,
    detect_device,
    get_logger,
)

_LOG = get_logger("docq.embed")


def _load_chunks() -> pd.DataFrame:
    if not CHUNKS_PARQUET.exists():
        raise FileNotFoundError(
            f"{CHUNKS_PARQUET} yok — önce `docq chunk` çalıştır."
        )
    return pd.read_parquet(CHUNKS_PARQUET)


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

    for batch in tqdm(
        list(_batched(texts, EMBEDDING_BATCH_SIZE)),
        desc="embed",
        unit="batch",
    ):
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

        # sparse: list[dict[int, float]] → JSON string olarak sakla
        for sparse_dict in out["lexical_weights"]:
            # token id int olabilir, JSON key string olmalı
            sparse_list.append(json.dumps({str(k): float(v) for k, v in sparse_dict.items()}))

    dense_arr = np.vstack(dense_list) if dense_list else np.zeros((0, EMBEDDING_DIM), dtype=np.float32)
    return dense_arr, sparse_list


def build_index(*, batch_size: int | None = None) -> int:
    """chunks.parquet → store.lance/chunks. Var olan tabloyu üzerine yazar."""
    df = _load_chunks()
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

    import lancedb  # type: ignore

    db = lancedb.connect(STORE_DIR)
    if LANCE_TABLE in db.table_names():
        db.drop_table(LANCE_TABLE)

    db.create_table(LANCE_TABLE, data=df_out, mode="overwrite")
    _LOG.info("LanceDB yazıldı: %s (%d satır).", STORE_DIR / LANCE_TABLE, len(df_out))
    return len(df_out)
