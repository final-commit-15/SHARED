"""Fast JSON serialization utilities built on ``orjson``.

orjson is used when available; the module falls back to stdlib json so the
library works even in minimal installs.
"""

from __future__ import annotations

import json as _stdlib_json
from collections.abc import Callable
from typing import Any

try:
    import orjson
except ImportError:  # pragma: no cover - only reached without orjson
    orjson = None  # type: ignore[assignment]


def dumps(
    payload: Any,
    *,
    sort_keys: bool = False,
    indent: int | None = None,
) -> str:
    """Serialize ``payload`` to a JSON string.

    Uses :mod:`orjson` when installed (fast, correct UTC ``datetime`` handling,
    rejects ``NaN`` by default), otherwise falls back to :mod:`json`.
    """
    if orjson is not None:
        return orjson.dumps(payload, default=_default_encoder).decode("utf-8")
    return _stdlib_json.dumps(
        payload,
        sort_keys=sort_keys,
        indent=indent,
        default=lambda obj: _default_encoder(obj) if obj is not None else None,
    )


def dumps_bytes(payload: Any, *, sort_keys: bool = False) -> bytes:
    """Serialize ``payload`` to a UTF-8 byte string."""
    if orjson is not None:
        if sort_keys:
            return orjson.dumps(payload, option=orjson.OPT_SORT_KEYS)
        return orjson.dumps(payload)
    return _stdlib_json.dumps(payload, sort_keys=sort_keys, ensure_ascii=False).encode("utf-8")


def loads(value: str | bytes, *, fail_silently: bool = False) -> Any:
    """Deserialize JSON ``value``.

    Returns ``None`` on parse errors when ``fail_silently`` is ``True``,
    otherwise re-raises the underlying error.
    """
    try:
        if orjson is not None:
            return orjson.loads(value)
        return _stdlib_json.loads(value)
    except (ValueError, TypeError, UnicodeDecodeError):
        if fail_silently:
            return None
        raise


def try_loads(value: str | bytes) -> Any:
    """Deserialize JSON, returning ``None`` instead of raising on errors."""
    return loads(value, fail_silently=True)


def is_valid_json(value: str | bytes) -> bool:
    """Return ``True`` when ``value`` parses as valid JSON."""
    try:
        loads(value)
        return True
    except (ValueError, TypeError, UnicodeDecodeError):
        return False


def _default_encoder(obj: Any) -> Any:  # pragma: no cover - thin passthrough
    """Fallback encoder for orjson-unsupported objects."""
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if isinstance(obj, set):
        return sorted(obj)
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    if hasattr(obj, "model_dump"):  # pydantic v2
        return obj.model_dump(mode="json")
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def register_encoder(fn: Callable[[Any], Any]) -> None:
    """Register a global fallback encoder (thread-safe append-only list).

    This is a lightweight registry; consumers that need full control should
    pass a ``default`` callable directly to their serializer instead.
    """
    _EXTRA_ENCODERS.append(fn)


_EXTRA_ENCODERS: list[Callable[[Any], Any]] = []


__all__ = [
    "dumps",
    "dumps_bytes",
    "loads",
    "try_loads",
    "is_valid_json",
    "register_encoder",
]
