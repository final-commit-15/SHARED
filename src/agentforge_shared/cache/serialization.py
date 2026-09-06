"""JSON serialization layer for cache values."""

from __future__ import annotations

from typing import Any

from agentforge_shared.utils.json_utils import dumps, dumps_bytes, loads, try_loads


def serialize(value: Any) -> bytes:
    """Serialize a value to UTF-8 JSON bytes."""
    return dumps_bytes(value)


def deserialize(raw: bytes | str | None) -> Any:
    """Deserialize a stored cache payload (``None`` stays ``None``)."""
    if raw is None:
        return None
    if isinstance(raw, bytes):
        return loads(raw.decode("utf-8"))
    return loads(raw)


def safe_deserialize(raw: bytes | str | None) -> Any:
    """Best-effort deserialize, returning ``None`` for corrupt payloads."""
    if raw is None:
        return None
    return try_loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)


__all__ = ["serialize", "deserialize", "safe_deserialize", "dumps", "loads"]
