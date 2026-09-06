"""Timeouts and decorators for execution/retry flows."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from agentforge_shared.exceptions.base import TimeoutException

from ..retry.backoff import RetryPolicy, retry_async_call, retry_call

T = TypeVar("T")


def with_timeout(fn: Callable[[], T], timeout_seconds: float, *, name: str = "operation") -> T:
    """Run ``fn`` in a thread and enforce ``timeout_seconds``.

    Raises:
        TimeoutException: When the deadline passes.
    """
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(fn)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError as exc:
            future.cancel()
            raise TimeoutException(message=f"{name} timed out after {timeout_seconds}s") from exc


async def async_with_timeout(fn: Callable[[], Awaitable[T]], timeout_seconds: float, *, name: str = "operation") -> T:
    """Run an async callable and raise :class:`TimeoutException` on overrun."""
    try:
        return await asyncio.wait_for(fn(), timeout=timeout_seconds)
    except TimeoutError as exc:
        raise TimeoutException(message=f"{name} timed out after {timeout_seconds}s") from exc


def with_retry(
    *,
    max_attempts: int = 3,
    backoff: str = "exponential",
    backoff_factor: float = 0.1,
    timeout_seconds: float | None = None,
    retry_exceptions: tuple[type[BaseException], ...] | None = None,
    name: str = "operation",
) -> Callable[[Callable[[], T]], Callable[[], T]]:
    """Decorator applying retry policy and an optional per-attempt timeout.

    Works on synchronous zero-argument callables; for async callables use
    :func:`with_async_retry`.
    """
    policy = RetryPolicy(
        max_attempts=max_attempts,
        backoff=backoff,
        backoff_factor=backoff_factor,
        retry_exceptions=retry_exceptions,
    )

    def _decorator(fn: Callable[[], T]) -> Callable[[], T]:
        def _wrapped() -> T:
            def _attempt() -> T:
                if timeout_seconds is not None:
                    return with_timeout(fn, timeout_seconds, name=name)
                return fn()

            return retry_call(_attempt, policy=policy)

        return _wrapped

    return _decorator


def with_async_retry(
    *,
    max_attempts: int = 3,
    backoff: str = "exponential",
    backoff_factor: float = 0.1,
    timeout_seconds: float | None = None,
    retry_exceptions: tuple[type[BaseException], ...] | None = None,
    name: str = "operation",
) -> Callable[[Callable[[], Awaitable[T]]], Callable[[], Awaitable[T]]]:
    """Async variant of :func:`with_retry`."""
    policy = RetryPolicy(
        max_attempts=max_attempts,
        backoff=backoff,
        backoff_factor=backoff_factor,
        retry_exceptions=retry_exceptions,
    )

    def _decorator(fn: Callable[[], Awaitable[T]]) -> Callable[[], Awaitable[T]]:
        async def _wrapped() -> T:
            async def _attempt() -> T:
                if timeout_seconds is not None:
                    return await async_with_timeout(fn, timeout_seconds, name=name)
                return await fn()

            return await retry_async_call(_attempt, policy=policy)

        return _wrapped

    return _decorator


__all__ = ["with_timeout", "async_with_timeout", "with_retry", "with_async_retry"]
