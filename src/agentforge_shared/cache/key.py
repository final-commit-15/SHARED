"""Cache key building helpers."""

from __future__ import annotations

import hashlib
from typing import Any


def build_key(*parts: Any, separator: str = ":", prefix: str | None = None) -> str:
    """Build a cache key from parts, hashing any composite length.

    Example::

        build_key("agent", "summary", "a1")          # 'agent:summary:a1'
        build_key("agent", {"id": "a1"}, prefix="v1") # 'v1:agent:<sha256>'
    """
    rendered: list[str] = []
    for part in parts:
        if isinstance(part, str):
            rendered.append(part)
        elif isinstance(part, (dict, list, tuple, set)):
            digest = hashlib.sha256(str(part).encode("utf-8")).hexdigest()[:16]
            rendered.append(str(part.__class__.__name__).lower() + f":{digest}")
        else:
            rendered.append(str(part))
    key = separator.join(rendered)
    if prefix:
        key = f"{prefix}{separator}{key}"
    return key


def with_namespace(base: str, namespace: str | None, *, separator: str = ":", prefix: str | None = None) -> str:
    """Prepend an optional namespace to ``base``."""
    parts = [namespace, base] if namespace else [base]
    return build_key(*parts, separator=separator, prefix=prefix)


def hash_value(value: Any, *, salt: str = "") -> str:
    """Deterministic short hash of a value (stable cache keys)."""
    return hashlib.sha256(f"{salt}{value}".encode()).hexdigest()[:24]


__all__ = ["build_key", "with_namespace", "hash_value"]
