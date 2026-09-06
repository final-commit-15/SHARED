"""Redis cache backend (async-first with a sync companion).

Redis is an optional dependency; import this module lazily so the library
works without it. TTLs are expressed in whole seconds.
"""

from __future__ import annotations

from typing import Any

try:
    import redis as _redis
    from redis import asyncio as aioredis
except ImportError:  # pragma: no cover
    _redis = None  # type: ignore[assignment]
    aioredis = None  # type: ignore[assignment]

from agentforge_shared.cache.base import CacheBackend
from agentforge_shared.cache.key import build_key
from agentforge_shared.cache.serialization import deserialize, serialize


class RedisCache(CacheBackend):
    """Async Redis-backed cache with JSON serialization and TTL.

    Example::

        from agentforge_shared.cache.redis import RedisCache

        cache = RedisCache.from_url("redis://localhost:6379/0")
        await cache.set("greeting", {"text": "hello"}, ttl=60)
        value = await cache.get("greeting")
    """

    DEFAULT_PREFIX = "agf:cache"

    def __init__(
        self,
        client: Any = None,
        *,
        namespace: str | None = None,
        prefix: str = DEFAULT_PREFIX,
        default_ttl: int | None = None,
    ) -> None:
        if aioredis is None:
            raise RuntimeError("redis is not installed; pip install redis")
        self._client: Any = client or aioredis.Redis(decode_responses=True)
        self.namespace = namespace
        self.prefix = prefix
        self.default_ttl = default_ttl

    @classmethod
    def from_url(
        cls,
        url: str,
        *,
        namespace: str | None = None,
        prefix: str = DEFAULT_PREFIX,
        default_ttl: int | None = None,
        **redis_kwargs: Any,
    ) -> RedisCache:
        """Create a cache from a Redis URL.

        Args:
            url: e.g. ``redis://localhost:6379/0``.
            redis_kwargs: Extra kwargs forwarded to ``aioredis.Redis.from_url``.
        """
        if aioredis is None:
            raise RuntimeError("redis is not installed; pip install redis")
        client = aioredis.Redis.from_url(
            url,
            decode_responses=redis_kwargs.pop("decode_responses", True),
            **redis_kwargs,
        )
        return cls(client, namespace=namespace, prefix=prefix, default_ttl=default_ttl)

    def _key(self, key: str) -> str:
        if key.startswith(self.prefix):
            return key
        if self.namespace:
            return build_key(self.namespace, key, prefix=self.prefix, separator=":")
        return build_key(key, prefix=self.prefix, separator=":")

    async def get(self, key: str) -> Any | None:
        raw = await self._client.get(self._key(key))
        return deserialize(raw)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        payload = serialize(value)
        expires = self.default_ttl if ttl is None else ttl
        full_key = self._key(key)
        if expires is not None:
            await self._client.set(full_key, payload, ex=max(1, int(expires)))
        else:
            await self._client.set(full_key, payload)

    async def set_many(self, mapping: dict[str, Any], ttl: int | None = None) -> None:
        """Write several keys in one round trip."""
        pipe = self._client.pipeline()
        for key, value in mapping.items():
            payload = serialize(value)
            full_key = self._key(key)
            if ttl is not None:
                pipe.set(full_key, payload, ex=max(1, int(ttl)))
            else:
                pipe.set(full_key, payload)
        await pipe.execute()

    async def get_many(self, *keys: str) -> list[Any | None]:
        """Fetch several keys; order matches ``keys`` (``None`` for misses)."""
        raw = await self._client.mget([self._key(k) for k in keys])
        return [deserialize(item) for item in raw]

    async def delete(self, key: str) -> bool:
        return bool(await self._client.delete(self._key(key)))

    async def exists(self, key: str) -> bool:
        return bool(await self._client.exists(self._key(key)))

    async def ttl(self, key: str) -> int | None:
        value = await self._client.ttl(self._key(key))
        if value is None or value < 0:
            return None
        return int(value)

    async def flush(self) -> None:
        """Delete all keys with this cache's prefix."""
        cursor, done = 0, False
        while not done:
            cursor, keys = await self._client.scan(cursor, match=f"{self.prefix}:*", count=100)
            if keys:
                await self._client.delete(*keys)
            done = cursor == 0

    async def close(self) -> None:
        """Close the underlying connection pool."""
        try:
            await self._client.aclose()
        except AttributeError:
            await self._client.close()

    def sync(self) -> _SyncRedisCache:
        """Return a synchronous view over the same Redis instance."""
        return _SyncRedisCache(self._client, prefix=self.prefix, namespace=self.namespace)


class _SyncRedisCache:
    """Synchronous facade mirroring :class:`RedisCache` operations."""

    def __init__(self, client: Any, *, prefix: str, namespace: str | None) -> None:
        self._client = client
        self.prefix = prefix
        self.namespace = namespace

    def _key(self, key: str) -> str:
        return build_key(key, prefix=self.prefix, separator=":")

    def get(self, key: str) -> Any | None:
        raw = self._client.get(self._key(key))
        return deserialize(raw)

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        if ttl is not None:
            self._client.set(self._key(key), serialize(value), ex=max(1, int(ttl)))
        else:
            self._client.set(self._key(key), serialize(value))

    def delete(self, key: str) -> bool:
        return bool(self._client.delete(self._key(key)))

    def exists(self, key: str) -> bool:
        return bool(self._client.exists(self._key(key)))

    def ttl(self, key: str) -> int | None:
        value = self._client.ttl(self._key(key))
        if value is None or value < 0:
            return None
        return int(value)


__all__ = ["RedisCache"]
