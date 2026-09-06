"""Cache protocols and value types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@dataclass
class CachedValue:
    """A cached value plus its expiry metadata."""

    value: Any
    ttl_remaining_seconds: int | None = None

    @property
    def expired(self) -> bool:
        return self.ttl_remaining_seconds is not None and self.ttl_remaining_seconds <= 0


@runtime_checkable
class CacheBackend(Protocol):
    """Contract implemented by all cache backends."""

    async def get(self, key: str) -> Any | None: ...
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None: ...
    async def delete(self, key: str) -> bool: ...
    async def exists(self, key: str) -> bool: ...
    async def ttl(self, key: str) -> int | None: ...


@runtime_checkable
class SyncCacheBackend(Protocol):
    """Contract for synchronous cache backends."""

    def get(self, key: str) -> Any | None: ...
    def set(self, key: str, value: Any, ttl: int | None = None) -> None: ...
    def delete(self, key: str) -> bool: ...
    def exists(self, key: str) -> bool: ...
    def ttl(self, key: str) -> int | None: ...


__all__ = ["CacheBackend", "SyncCacheBackend", "CachedValue"]
