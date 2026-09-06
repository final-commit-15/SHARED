"""Decorators and helpers for caching function results."""

from __future__ import annotations

import functools
import hashlib
import inspect
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from agentforge_shared.cache.base import CacheBackend, SyncCacheBackend
from agentforge_shared.cache.key import build_key
from agentforge_shared.typing import Result, err, ok

T = TypeVar("T")


def _as_async(backend: Any, method: str, *args: Any, **kwargs: Any) -> Awaitable[Any]:
    """Invoke a backend method, adapting sync backends to async context."""
    fn = getattr(backend, method)
    if inspect.iscoroutinefunction(fn):
        return fn(*args, **kwargs)
    result = fn(*args, **kwargs)
    if inspect.isawaitable(result):
        return result

    async def _wrapped() -> Any:
        return result

    return _wrapped()


def _arguments_key(*args: Any, **kwargs: Any) -> str:
    """Build a stable key suffix from function arguments."""
    parts = [repr(arg) for arg in args]
    parts.extend(f"{k}={v!r}" for k, v in sorted(kwargs.items()))
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]


async def cached_async(
    func: Callable[..., Awaitable[T]],
    *,
    key_prefix: str,
    cache: CacheBackend,
    ttl: int | None = None,
    skip_cache: Callable[..., bool] | None = None,
    is_none: bool = False,
) -> Callable[..., Awaitable[T]]:
    """Decorate an async function to memoise its result in ``cache``.

    Args:
        func: Async function producing the value.
        key_prefix: Constant key prefix.
        cache: Async cache backend.
        ttl: Seconds to keep results (``None`` = backend default).
        skip_cache: Optional predicate; when ``True`` bypass the cache.
        is_none: Cache ``None`` results too (default: treat them as misses).
    """

    @functools.wraps(func)
    async def _wrapped(*args: Any, **kwargs: Any) -> T:
        if skip_cache is not None and skip_cache(*args, **kwargs):
            return await func(*args, **kwargs)
        key = build_key(key_prefix, _arguments_key(*args, **kwargs), separator=":")
        cached = await _as_async(cache, "get", key)
        if cached is not None or (is_none and await _as_async(cache, "exists", key)):
            return cached
        result = await func(*args, **kwargs)
        if result is not None or is_none:
            await _as_async(cache, "set", key, result, ttl=ttl)
        return result

    return _wrapped


def cached(
    func: Callable[..., T],
    *,
    key_prefix: str,
    cache: SyncCacheBackend,
    ttl: int | None = None,
    skip_cache: Callable[..., bool] | None = None,
) -> Callable[..., T]:
    """Synchronous memoisation decorator (see :func:`cached_async`)."""

    @functools.wraps(func)
    def _wrapped(*args: Any, **kwargs: Any) -> T:
        if skip_cache is not None and skip_cache(*args, **kwargs):
            return func(*args, **kwargs)
        key = build_key(key_prefix, _arguments_key(*args, **kwargs), separator=":")
        cached_value = cache.get(key)
        if cached_value is not None:
            return cached_value
        result = func(*args, **kwargs)
        if result is not None:
            cache.set(key, result, ttl=ttl)
        return result

    return _wrapped


async def memory(factory: Callable[[], Awaitable[T]], *, cache: CacheBackend, key: str, ttl: int | None = None) -> T:
    """Memoise a single async computation under ``key``.

    Example::

        value = await memory(lambda: expensive(), cache=cache, key="expensive:v1")
    """
    existing = await _as_async(cache, "get", key)
    if existing is not None:
        return existing
    result = await factory()
    if result is not None:
        await _as_async(cache, "set", key, result, ttl=ttl)
    return result


async def failing_memoize(
    factory: Callable[[], Awaitable[T]],
    *,
    cache: CacheBackend,
    key: str,
    ttl: int | None = None,
) -> Result[T, Any]:
    """Memoise a computation; failures are not stored and surface as ``Err``."""
    try:
        existing = await _as_async(cache, "get", key)
        if existing is not None:
            return ok(existing)
        result = await factory()
        await _as_async(cache, "set", key, result, ttl=ttl)
        return ok(result)
    except BaseException as exc:  # noqa: BLE001 - wrapped for callers
        return err(exc)


async def batch_memoize(
    keys: list[str],
    loader: Callable[[list[str]], Awaitable[list[T]]],
    *,
    cache: CacheBackend,
    prefix: str,
    ttl: int | None = None,
) -> dict[str, T]:
    """Fetch many keys, loading only the misses in one batch call.

    Returns a dict of ``key -> value`` for all requested keys.
    """
    full_keys = [build_key(prefix, k, separator=":") for k in keys]
    cached = await _as_async(cache, "get_many", *full_keys)
    misses = [keys[i] for i, item in enumerate(cached) if item is None]
    result: dict[str, T] = {}
    for key, item in zip(keys, cached):
        if item is not None:
            result[key] = item
    if not misses:
        return result
    loaded = await loader(misses)
    mapping = dict(zip(misses, loaded))
    for key, value in mapping.items():
        if value is not None:
            await _as_async(cache, "set", build_key(prefix, key, separator=":"), value, ttl=ttl)
            result[key] = value
    return result


__all__ = ["cached_async", "cached", "memory", "failing_memoize", "batch_memoize"]
