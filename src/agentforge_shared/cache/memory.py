"""In-memory cache backend (tests, single-process apps)."""

from __future__ import annotations

import threading
import time
from typing import Any

from agentforge_shared.cache.base import SyncCacheBackend
from agentforge_shared.cache.serialization import deserialize, serialize


class MemoryCache(SyncCacheBackend):
    """Thread-safe dict-backed cache with TTL support.

    Example::

        from agentforge_shared.cache.memory import MemoryCache

        cache = MemoryCache()
        cache.set("k", {"ok": True}, ttl=60)
        assert cache.get("k") == {"ok": True}
    """

    def __init__(self, *, default_ttl: int | None = None) -> None:
        self._store: dict[str, tuple[bytes, float | None]] = {}
        self._default_ttl = default_ttl
        self._lock = threading.Lock()

    def _cleanup_locked(self) -> None:
        now = time.monotonic()
        stale = [k for k, (_, exp) in self._store.items() if exp is not None and exp <= now]
        for k in stale:
            del self._store[k]

    def get(self, key: str) -> Any | None:
        with self._lock:
            self._cleanup_locked()
            entry = self._store.get(key)
            if entry is None:
                return None
            value_bytes, _ = entry
        return deserialize(value_bytes)

    def get_many(self, *keys: str) -> list[Any | None]:
        """Fetch several keys; order matches ``keys`` (``None`` for misses)."""
        return [self.get(key) for key in keys]

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        expires: float | None = None
        seconds = self._default_ttl if ttl is None else ttl
        if seconds is not None:
            expires = time.monotonic() + max(0.0, float(seconds))
        with self._lock:
            self._store[key] = (serialize(value), expires)

    def delete(self, key: str) -> bool:
        with self._lock:
            existed = key in self._store
            self._store.pop(key, None)
            return existed

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def ttl(self, key: str) -> int | None:
        with self._lock:
            self._cleanup_locked()
            entry = self._store.get(key)
            if entry is None:
                return None
            _, expires = entry
        if expires is None:
            return None
        return max(0, int(expires - time.monotonic()))

    def clear(self) -> None:
        """Remove all entries."""
        with self._lock:
            self._store.clear()


__all__ = ["MemoryCache"]
