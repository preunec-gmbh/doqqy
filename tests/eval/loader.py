"""Değerlendirme korpusu ve queries.yaml için yükleyici modül."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from doqqy.chunk import chunk_directory
from doqqy.embed import build_index
from doqqy.infra.settings import Settings
from doqqy.ingest import ingest_directory
from doqqy.workspace import Workspace
from tests.eval.models import EvalQuery

DEFAULT_QUERIES_PATH = Path(__file__).parent / "queries.yaml"
DEFAULT_CORPUS_RAW_DIR = Path(__file__).parent / "corpus" / "raw"


def load_eval_queries(yaml_path: Path | None = None) -> list[EvalQuery]:
    """queries.yaml dosyasından referans sorguları ayrıştırır ve doğrular."""
    path = yaml_path or DEFAULT_QUERIES_PATH
    if not path.exists():
        raise FileNotFoundError(f"Değerlendirme sorgu dosyası bulunamadı: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or "queries" not in data:
        raise ValueError(f"Geçersiz sorgu dosyası formatı ({path}): 'queries' anahtarı bekleniyor")

    queries: list[EvalQuery] = []
    for item in data["queries"]:
        q = EvalQuery(
            query=item["query"],
            expected_doc_id=item["expected_doc_id"],
            expected_section=item.get("expected_section"),
            category=item.get("category", "general"),
            reason=item.get("reason", "").strip(),
            tag_filter=item.get("tag_filter"),
        )
        queries.append(q)

    return queries


def build_eval_workspace(
    target_dir: Path,
    corpus_raw_dir: Path | None = None,
    backend: str = "lancedb",
    settings: Settings | None = None,
) -> Workspace:
    """Test korpusu üzerinde geçici Workspace kurup gerçek (un-mocked) pipeline'ı çalıştırır.

    İşlem adımları:
    1. tests/eval/corpus/raw dizinini target_dir/raw altına kopyala
    2. ingest_directory(ws)
    3. chunk_directory(ws)
    4. build_index(ws, settings=settings)
    """
    src_raw = corpus_raw_dir or DEFAULT_CORPUS_RAW_DIR
    if not src_raw.exists():
        raise FileNotFoundError(f"Fixture korpus raw dizini bulunamadı: {src_raw}")

    dest_raw = target_dir / "raw"
    if dest_raw.exists():
        shutil.rmtree(dest_raw)
    shutil.copytree(src_raw, dest_raw)

    ws = Workspace(target_dir)
    ws.ensure_dirs()

    ingest_result = ingest_directory(ws)
    if len(ingest_result.failed) > 0:
        raise RuntimeError(f"Ingest {len(ingest_result.failed)} dosya için başarısız oldu: {ingest_result.failed}")

    chunks = chunk_directory(ws)
    if not chunks:
        raise RuntimeError("Chunking fixture korpusu için 0 chunk üretti")

    app_settings = settings or Settings(vector_backend=backend)
    embedded_count = build_index(ws, settings=app_settings)
    if embedded_count == 0:
        raise RuntimeError("Embedding vektör deposunda 0 kayıt üretti")

    return ws
