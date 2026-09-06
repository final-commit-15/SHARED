"""Cursor-based pagination helpers."""

from __future__ import annotations

import base64
import json
from typing import Any, TypeVar

from agentforge_shared.schemas.pagination import CursorMeta, PaginatedData

T = TypeVar("T")


def encode_cursor(payload: dict[str, Any]) -> str:
    """Base64-encode a cursor payload (URL-safe, opaque).

    Example::

        encode_cursor({"id": "agent_42", "created_at": "2026-01-01T00:00:00Z"})
    """
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def decode_cursor(cursor: str | None) -> dict[str, Any] | None:
    """Decode a cursor string back to its payload (``None`` when invalid)."""
    if not cursor:
        return None
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        raw = base64.urlsafe_b64decode(padded.encode("ascii"))
        return json.loads(raw.decode("utf-8"))
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return None


def cursor_data(
    items: list[T],
    *,
    next_cursor: str | None,
    has_more: bool,
    total: int | None = None,
    sort_by: str | None = None,
    sort_desc: bool = False,
) -> PaginatedData[T]:
    """Build ``PaginatedData`` carrying cursor metadata."""
    return PaginatedData[T](
        page_meta=None,
        cursor_meta=CursorMeta(next_cursor=next_cursor, has_more=has_more, total=total),
        items=items,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )


def batch_cursor(key: list[str] | str) -> str:
    """Build a cursor whose payload is a list of sort keys."""
    keys = key if isinstance(key, list) else [key]
    return encode_cursor({"keys": keys})


__all__ = ["encode_cursor", "decode_cursor", "cursor_data", "batch_cursor"]
