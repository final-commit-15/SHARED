"""Async helpers for concurrent execution in a synchronous world."""

from __future__ import annotations

import asyncio
import functools
from collections.abc import Callable, Coroutine
from concurrent.futures import ThreadPoolExecutor
from typing import Any, TypeVar

_T = TypeVar("_T")
_DEFAULT_EXECUTOR = ThreadPoolExecutor(max_workers=32)


def run_sync(coro: Coroutine[Any, Any, _T]) -> _T:
    """Run an async coroutine from a synchronous context, reusing the event loop.

    Raises:
        RuntimeError: if the event loop is already running.
    """
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # Inside an already-running loop (e.g. pytest-asyncio in sync tests):
        # schedule via the thread pool to avoid deadlocking.
        future = asyncio.run_coroutine_threadsafe(coro, _DEFAULT_EXECUTOR)
        return future.result()
    return loop.run_until_complete(coro)


def run_async(coro: Coroutine[Any, Any, _T]) -> _T:
    """Shorthand alias of :func:`run_sync`."""
    return run_sync(coro)


async def gather_tasks(
    *coros: Coroutine[Any, Any, _T],
    return_exceptions: bool = False,
) -> list[Any]:
    """Run a set of coroutines concurrently.

    Args:
        *coros: Any number of coroutines.
        return_exceptions: When ``True``, exceptions are captured as result
            values rather than raising immediately.
    """
    tasks = [asyncio.create_task(c) for c in coros]
    return list(
        await asyncio.gather(*tasks, return_exceptions=return_exceptions)
    )


async def run_with_limit(
    coros: list[Coroutine[Any, Any, _T]],
    limit: int = 16,
    return_exceptions: bool = False,
) -> list[Any]:
    """Run coroutines with a concurrency limit (``Semaphore``-based)."""
    if limit < 1:
        raise ValueError("limit must be >= 1")
    sem = asyncio.Semaphore(limit)

    async def _limited(coro: Coroutine[Any, Any, _T]) -> _T:
        async with sem:
            return await coro

    tasks = [asyncio.create_task(_limited(c)) for c in coros]
    return list(await asyncio.gather(*tasks, return_exceptions=return_exceptions))


async def wait_all(
    *coros: Coroutine[Any, Any, Any],
    timeout: float | None = None,
) -> list[Any]:
    """Run coroutines with an optional hard timeout (raises on expiry)."""
    tasks = [asyncio.create_task(c) for c in coros]
    done, pending = await asyncio.wait(tasks, timeout=timeout)
    if pending:
        for task in pending:
            task.cancel()
        raise TimeoutError(f"{len(pending)} tasks exceeded the {timeout}s timeout")
    return [task.result() for task in done]


def sync_to_async(
    fn: Callable[..., _T],
    *,
    executor: ThreadPoolExecutor | None = None,
) -> Callable[..., Coroutine[Any, Any, _T]]:
    """Wrap a synchronous callable so it runs in an executor via ``asyncio``."""
    @functools.wraps(fn)
    async def _wrapper(*args: Any, **kwargs: Any) -> _T:
        loop = asyncio.get_running_loop()
        bound = functools.partial(fn, *args, **kwargs)
        return await loop.run_in_executor(executor or _DEFAULT_EXECUTOR, bound)
    return _wrapper


async def async_retry(
    fn: Callable[..., Coroutine[Any, Any, _T]],
    *args: Any,
    retries: int = 3,
    backoff: float = 1.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    **kwargs: Any,
) -> _T:
    """Simple async retry with exponential back-off."""
    last_exc: BaseException | None = None
    for attempt in range(retries + 1):
        try:
            return await fn(*args, **kwargs)
        except exceptions as exc:
            last_exc = exc
            if attempt < retries:
                await asyncio.sleep(backoff * (2 ** attempt))
    raise last_exc  # type: ignore[misc]


def sync_retry(
    fn: Callable[..., _T],
    *args: Any,
    retries: int = 3,
    backoff: float = 1.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    **kwargs: Any,
) -> _T:
    """Synchronous retry with exponential back-off."""
    import time as _time

    last_exc: BaseException | None = None
    for attempt in range(retries + 1):
        try:
            return fn(*args, **kwargs)
        except exceptions as exc:
            last_exc = exc
            if attempt < retries:
                _time.sleep(backoff * (2 ** attempt))
    raise last_exc  # type: ignore[misc]


def create_task(coro: Coroutine[Any, Any, _T], name: str | None = None) -> asyncio.Task[_T]:  # noqa: D103
    """Fire-and-forget convenience wrapper."""
    return asyncio.create_task(coro, name=name)


def ensure_async(fn: Callable[..., _T]) -> Callable[..., Coroutine[Any, Any, _T]]:
    """Wrap a sync function so it returns a coroutine, or passthrough async."""
    if asyncio.iscoroutinefunction(fn):
        return fn  # type: ignore[return-value]

    @functools.wraps(fn)
    async def _async_wrapper(*args: Any, **kwargs: Any) -> _T:
        return await asyncio.get_running_loop().run_in_executor(
            _DEFAULT_EXECUTOR, functools.partial(fn, *args, **kwargs)
        )
    return _async_wrapper


__all__ = [
    "run_sync",
    "run_async",
    "gather_tasks",
    "run_with_limit",
    "wait_all",
    "sync_to_async",
    "async_retry",
    "sync_retry",
    "create_task",
    "ensure_async",
]
