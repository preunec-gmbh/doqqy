"""Workspace — bir doqqy korpusunun kök dizini ve türetilmiş yolları.

Tüm pipeline aşamaları yolları bu nesneden alır; modül seviyesinde
(import anında çözülen) yol sabiti yoktur. Aynı process içinde birden
fazla Workspace, birbirine karışmadan farklı korpuslara hizmet edebilir.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Workspace:
    root: Path

    @property
    def raw_dir(self) -> Path:
        return self.root / "raw"

    @property
    def processed_dir(self) -> Path:
        return self.root / "processed"

    @property
    def state_dir(self) -> Path:
        return self.root / ".doqqy"

    @property
    def chunks_parquet(self) -> Path:
        return self.state_dir / "chunks" / "chunks.parquet"

    @property
    def store_dir(self) -> Path:
        return self.state_dir / "store.lance"

    @property
    def topics_yaml(self) -> Path:
        return self.state_dir / "topics.yaml"

    @property
    def logs_dir(self) -> Path:
        return self.state_dir / "logs"

    @property
    def manifest_path(self) -> Path:
        return self.state_dir / "manifest.json"

    def ensure_dirs(self) -> None:
        for d in (
            self.raw_dir,
            self.processed_dir,
            self.state_dir,
            self.chunks_parquet.parent,
            self.logs_dir,
        ):
            d.mkdir(parents=True, exist_ok=True)
