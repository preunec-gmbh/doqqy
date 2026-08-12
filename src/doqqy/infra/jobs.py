"""In-process job queue implementation for asynchronous task execution."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from doqqy.workspace import Workspace


@dataclass
class Job:
    """Arka planda çalışan bir işin durumunu temsil eden veri sınıfı."""
    id: str
    kind: str  # "ingest_embed" | "map" | "reindex"
    workspace_root: str
    payload: dict = field(default_factory=dict)
    status: str = "queued"  # "queued" | "running" | "succeeded" | "failed"
    progress: float = 0.0
    error: str | None = None


class JobQueue(Protocol):
    """Tüm iş kuyruğu sistemlerinin uyması gereken soyut arayüz (Protocol)."""
    async def enqueue(self, kind: str, ws: Workspace, payload: dict) -> str:
        ...

    async def get(self, job_id: str) -> Job | None:
        ...


class InProcessQueue:
    """Yerel tek kullanıcılı çalışma (doqqy serve) için bellek içi iş kuyruğu.

    NOTE: Asenkron iş yürütücüsü (execution worker) API-ARCHITECTURE.md §2.4 uyarınca
    Build Step 5 (Upload & Ingestion) aşamasında bağlanacaktır. Step 3 için bu sınıf
    iş durumu takibi ve JobQueue protokol iskeletini sağlar.
    """

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}

    async def enqueue(self, kind: str, ws: Workspace, payload: dict) -> str:
        """Kuyruğa yeni bir iş ekler ve benzersiz bir job_id döndürür."""
        job_id = str(uuid.uuid4())
        job = Job(
            id=job_id,
            kind=kind,
            workspace_root=str(ws.root.resolve()),
            payload=payload,
            status="queued",
        )
        self._jobs[job_id] = job
        return job_id

    async def get(self, job_id: str) -> Job | None:
        """job_id ile işin mevcut durumunu sorgular."""
        return self._jobs.get(job_id)

    def update_job(
        self,
        job_id: str,
        status: str,
        progress: float = 0.0,
        error: str | None = None,
    ) -> None:
        """İşin ilerleme ve durumunu günceller."""
        if job_id in self._jobs:
            job = self._jobs[job_id]
            job.status = status
            job.progress = progress
            job.error = error
