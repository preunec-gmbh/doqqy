from __future__ import annotations

from pathlib import Path

from doqqy.ingest.base import Document, IngestError, base_metadata, content_hash, processed_path_for
from doqqy.workspace import Workspace


def _df_to_md_blocks(df, max_rows: int = 40) -> list[str]:
    """SHARED HELPER: Tabloyu 40 satırlık Markdown bloklarına böler."""
    df = df.fillna("") 
    df.columns = [str(col) for col in df.columns] 
    df = df.astype(str) 
    
    blocks = []
    num_rows = len(df)
    
    if num_rows == 0:
        return []
        
    for i in range(0, num_rows, max_rows):
        chunk = df.iloc[i : i + max_rows]
        md_table = chunk.to_markdown(index=False)
        blocks.append(md_table)
        
    return blocks


def ingest_xlsx(source: Path, ws: Workspace) -> Document:
    import pandas as pd     # heavy imports inside functions

    if not source.exists():
        raise IngestError(f"Excel dosyası mevcut değil: {source.name}")
    
    if source.stat().st_size == 0:
        raise IngestError(f"Excel dosyası boş: {source.name}")
    
    try:
        excel_file = pd.read_excel(source, sheet_name = None, engine = "openpyxl")
    except Exception as exc:
        raise IngestError(f"Excel okuma hatası ({source.name}): {exc}") from exc
    
    if not excel_file:
        raise IngestError(f"Excel dosyasında hiç sayfa yok: {source.name}")
    
    all_blocks = []
    valid_sheets = 0

    for sheet_name, df in excel_file.items():
        if df.empty or df.dropna(how = 'all').empty:
            continue  # boş sayfaları atla

        valid_sheets += 1
        md_tables = _df_to_md_blocks(df, max_rows = 40)

        if md_tables:
            # sayfa başına bir kez ## <sheet_name> eklenmeli
            sheet_content = f"## {sheet_name}\n\n" + "\n\n".join(md_tables)
            all_blocks.append(sheet_content)

    if valid_sheets == 0:
        raise IngestError(f"Excel dosyasındaki tüm sayfalar boş: {source.name}")
    
    full_content = "\n\n".join(all_blocks)

    meta = base_metadata(source, ws.root, kind="xlsx")
    meta["parser"] = "pandas"
    meta["content_hash"] = content_hash(full_content)

    return Document(
        source_path = source,
        processed_path = processed_path_for(source, ws),
        content = full_content,
        metadata = meta,
    )

