"""bge-m3 dense embedding + LanceDB yazımı.

Faz 1: sadece dense vektör. Sparse + reranker Faz 2'de eklenecek.
"""

from __future__ import annotations

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
    """FlagEmbedding BGEM3FlagModel — ilk çağrıda model indirilir (~2 GB)."""
    from FlagEmbedding import BGEM3FlagModel  # type: ignore

    device = detect_device()
    use_fp16 = device == "cuda"
    _LOG.info("model yükleniyor: %s (device=%s, fp16=%s)", EMBEDDING_MODEL, device, use_fp16)
    return BGEM3FlagModel(EMBEDDING_MODEL, use_fp16=use_fp16, device=device)


def _batched(seq: list[str], n: int) -> Iterator[list[str]]:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def _embed_texts(model, texts: list[str]) -> np.ndarray:
    vectors: list[np.ndarray] = []
    for batch in tqdm(
        list(_batched(texts, EMBEDDING_BATCH_SIZE)),
        desc="embed",
        unit="batch",
    ):
        out = model.encode(
            batch,
            batch_size=len(batch),
            max_length=8192,
            return_dense=True,
            return_sparse=False,
            return_colbert_vecs=False,
        )
        dense = np.asarray(out["dense_vecs"], dtype=np.float32)
        vectors.append(dense)
    return np.vstack(vectors) if vectors else np.zeros((0, EMBEDDING_DIM), dtype=np.float32)


def build_index(*, batch_size: int | None = None) -> int:
    """chunks.parquet → store.lance/chunks. Var olan tabloyu üzerine yazar."""
    df = _load_chunks()
    if df.empty:
        _LOG.warning("chunk yok, index oluşturulmadı.")
        return 0

    texts = df["content"].tolist()
    model = _load_model()
    vectors = _embed_texts(model, texts)
    if vectors.shape[0] != len(df):
        raise RuntimeError(
            f"embedding/satır uyumsuzluğu: {vectors.shape[0]} vs {len(df)}"
        )
    if vectors.shape[1] != EMBEDDING_DIM:
        _LOG.warning(
            "model %d boyut döndürdü, config EMBEDDING_DIM=%d.",
            vectors.shape[1],
            EMBEDDING_DIM,
        )

    df_out = df.copy()
    df_out["vector"] = list(vectors)
    # LanceDB list/object kolonlarda zorluk çıkarmasın diye string'leştir.
    df_out["section_path_str"] = df_out["section_path"].apply(lambda xs: " > ".join(xs))

    import lancedb  # type: ignore

    db = lancedb.connect(STORE_DIR)
    if LANCE_TABLE in db.table_names():
        db.drop_table(LANCE_TABLE)

    # Schema'yı pyarrow'a bırakmak için to_pandas yeterli; LanceDB list[float32]'i otomatik tanır.
    db.create_table(LANCE_TABLE, data=df_out, mode="overwrite")
    _LOG.info("LanceDB yazıldı: %s (%d satır).", STORE_DIR / LANCE_TABLE, len(df_out))
    return len(df_out)
