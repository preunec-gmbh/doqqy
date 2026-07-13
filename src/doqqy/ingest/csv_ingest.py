from __future__ import annotations

import csv
from pathlib import Path

from doqqy.ingest.base import (Document, IngestError, base_metadata, content_hash, processed_path_for)
from doqqy.ingest.xlsx_ingest import _df_to_md_blocks
from doqqy.workspace import Workspace


def ingest_csv(source: Path, ws: Workspace) -> Document:
    import pandas as pd  # heavy import inside function

    if not source.exists():
        raise IngestError(f"CSV dosyası mevcut değil: {source.name}")

    if source.stat().st_size == 0:
        raise IngestError(f"CSV dosyası boş: {source.name}")

    encodings_to_try = ["utf-8", "cp1254", "latin1"]
    detected_delimiter = ","
    chosen_encoding = "utf-8"

    # kodlama ve ayıracı tespit et
    for enc in encodings_to_try:
        try:
            with source.open("r", encoding=enc) as f:
                sample = f.read(2048)

            if not sample.strip():
                raise IngestError(f"CSV dosyası boş: {source.name}")

            try:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample, delimiters=[",", ";", "\t", "|"])
                detected_delimiter = dialect.delimiter
            except csv.Error:
                detected_delimiter = ","

            chosen_encoding = enc
            break

        except UnicodeDecodeError:
            continue

    else:
        chosen_encoding = "utf-8"
        detected_delimiter = ","

    try:
        df = pd.read_csv(
            source,
            sep = detected_delimiter,
            encoding = chosen_encoding,
            engine = "python",
            on_bad_lines = "skip",
        )

        df = df.dropna(how = "all")
        df = df.dropna(axis = 1, how = "all")
        df = df.fillna("")

    except Exception as exc: 
        raise IngestError(f"CSV okunurken pandas hatası oluştu: {exc}") from exc

    if df.empty:
        raise IngestError("CSV dosyası geçerli veri içermiyor.")

    md_tables = _df_to_md_blocks(df)

    if not md_tables:
        raise IngestError("Boş tablo içeriği.")

    full_content = (f"# {source.stem}\n\n" + "\n\n".join(md_tables))

    meta = base_metadata(source, ws.root, kind="csv")
    meta["parser"] = "pandas"
    meta["delimiter"] = detected_delimiter
    meta["encoding"] = chosen_encoding
    meta["content_hash"] = content_hash(full_content)

    return Document(
        source_path = source,
        processed_path = processed_path_for(source, ws),
        content = full_content,
        metadata = meta,
    )

