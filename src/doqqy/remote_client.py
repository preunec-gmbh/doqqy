"""Thin HTTP client for `doqqy query --remote`: POSTs to a running `doqqy serve`.

Only the standard library is used here (no `requests`/`httpx` dependency) so the
remote query path stays as lightweight as the in-process one — the whole point
of `--remote` is to avoid paying for anything heavier than a socket connect.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from urllib.parse import quote

from doqqy.query import SearchHit
from doqqy.workspace import Workspace

_DEFAULT_TIMEOUT_S = 30.0


class RemoteQueryError(Exception):
    """Raised when the server cannot be reached or returns an error response."""


def query_remote(
    server_url: str,
    ws: Workspace,
    text: str,
    *,
    k: int,
    rerank: bool,
    tag: str | None,
    timeout: float = _DEFAULT_TIMEOUT_S,
) -> tuple[list[SearchHit], int]:
    """POST a query to the workspace endpoint and convert its JSON response to SearchHit objects."""
    workspace_id = quote(str(ws.root.resolve()), safe="/")
    url = f"{server_url.rstrip('/')}/v1/workspaces/{workspace_id}/query"
    payload = {"q": text, "top_k": k, "tag": tag, "rerank": rerank}
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RemoteQueryError(f"server returned HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RemoteQueryError(f"could not reach doqqy serve at {server_url}: {e.reason}") from e

    hits = [
        SearchHit(
            score=float(h["score"]),
            doc_id=str(h["doc_id"]),
            source=str(h["source"]),
            section_path=list(h.get("section_path") or []),
            content=str(h["content"]),
            # `extra` mirrors SearchHit directly; accept the older `scores`
            # field as well to preserve compatibility with existing servers.
            extra=_scores_to_extra(h.get("extra", h.get("scores"))),
        )
        for h in data["hits"]
    ]
    return hits, int(data.get("took_ms", 0))


def _scores_to_extra(scores: dict | None) -> dict:
    if not scores:
        return {}
    return {k: v for k, v in scores.items() if v is not None}
