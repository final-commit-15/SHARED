"""Backoff strategies and retry helpers built on ``tenacity``."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from tenacity import (
    AsyncRetrying,
    before_sleep_log,
    retry as tenacity_retry,
    retry_if_exception_type,
    stop_after_attempt,
    stop_after_delay,
    wait_exponential,
    wait_fixed,
    wait_random_exponential,
)

from agentforge_shared.exceptions.base import (
    CacheException,
    ProviderException,
    RetryExhaustedException,
    ServiceUnavailableException,
    StorageException,
)
from agentforge_shared.logging.logger import get_logger

logger = get_logger("agentforge.retry")

T = TypeVar("T")

#: Exceptions considered safe to retry by default.
DEFAULT_RETRYABLE_EXCEPTIONS: tuple[type[BaseException], ...] = (
    ProviderException,
    ServiceUnavailableException,
    StorageException,
    CacheException,
)

#: Other widely-retried exception types (registered alongside the defaults).
EXTRA_RETRYABLE_EXCEPTIONS: tuple[type[BaseException], ...] = ()


class RetryPolicy:
    """Declarative retry policy shared by sync and async callers.

    Example::

        from agentforge_shared.retry import RetryPolicy, retry_call

        policy = RetryPolicy(max_attempts=4, backoff="exponential", backoff_factor=0.5)
        result = retry_call(lambda: flaky_fn(), policy=policy)
    """

    def __init__(
        self,
        *,
        max_attempts: int = 3,
        backoff: str = "exponential",
        backoff_factor: float = 0.1,
        max_delay: float = 30.0,
        jitter: bool = True,
        retry_exceptions: tuple[type[BaseException], ...] | None = None,
        stop_after_seconds: float | None = None,
        log_level: int = logging.WARNING,
    ) -> None:
        """Configure the policy.

        Args:
            max_attempts: Total attempts (including the first).
            backoff: ``"exponential"`` | ``"linear"`` (via fixed) | ``"random"``.
            backoff_factor: Base delay for the backoff curve.
            max_delay: Upper bound for backoff delays (seconds).
            jitter: Add random jitter to the wait when supported.
            retry_exceptions: Exception types that trigger a retry.
            stop_after_seconds: Absolute deadline for retrying (overrides attempts when set).
        """
        self.max_attempts = max(1, max_attempts)
        self.backoff = backoff
        self.backoff_factor = max(0.0, backoff_factor)
        self.max_delay = max_delay
        self.jitter = jitter
        self.retry_exceptions = retry_exceptions or DEFAULT_RETRYABLE_EXCEPTIONS
        self.stop_after_seconds = stop_after_seconds
        self.log_level = log_level

        if self.backoff not in {"exponential", "linear", "random"}:
            raise ValueError(f"unknown backoff strategy: {self.backoff!r}")

    def with_exceptions(self, *extra: type[BaseException]) -> RetryPolicy:
        """Copy of this policy that also retries ``extra`` exception types."""
        combined = tuple(dict.fromkeys(self.retry_exceptions + extra))
        other = RetryPolicy(
            max_attempts=self.max_attempts,
            backoff=self.backoff,
            backoff_factor=self.backoff_factor,
            max_delay=self.max_delay,
            jitter=self.jitter,
            retry_exceptions=combined,
            stop_after_seconds=self.stop_after_seconds,
            log_level=self.log_level,
        )
        return other

    def _stop(self):
        if self.stop_after_seconds is not None:
            return stop_after_delay(self.stop_after_seconds)
        return stop_after_attempt(self.max_attempts)

    def _wait(self):
        if self.backoff == "linear":
            return wait_fixed(self.backoff_factor)
        if self.backoff == "random":
            return wait_random_exponential(multiplier=self.backoff_factor, max=self.max_delay)
        return wait_exponential(multiplier=self.backoff_factor, max=self.max_delay, exp_base=2)

    def _retry_kwargs(self) -> dict[str, Any]:
        return {
            "stop": self._stop(),
            "wait": self._wait(),
            "retry": retry_if_exception_type(self.retry_exceptions),
            "before_sleep": before_sleep_log(logger, self.log_level),
            "reraise": True,
        }


def _raise_appropriately(exc: BaseException, retryable: bool) -> None:
    """Raise ``RetryExhaustedException`` for exhausted retryables, else re-raise."""
    if retryable:
        raise RetryExhaustedException(
            message=f"retry attempts exhausted: {exc}",
            details={"cause": exc.__class__.__name__},
            cause=exc,
        ) from exc
    raise exc


def retry_call(
    fn: Callable[[], T],
    *,
    policy: RetryPolicy | None = None,
    on_retry: Callable[[BaseException], Any] | None = None,
) -> T:
    """Run ``fn`` synchronously under ``policy``.

    Raises:
        RetryExhaustedException: When a retryable exception exhausts attempts.
        Original exception: Raised as-is for non-retryable errors.
    """
    policy = policy or RetryPolicy()
    retryable = retry_if_exception_type(policy.retry_exceptions)

    @tenacity_retry(**policy._retry_kwargs())
    def _run() -> T:
        try:
            return fn()
        except BaseException as exc:  # noqa: BLE001 - reported via on_retry
            if retryable(exc):
                if on_retry is not None:
                    on_retry(exc)
                raise
            raise

    try:
        return _run()
    except BaseException as exc:  # noqa: BLE001 - tenacity re-raises
        _is_retryable = retryable(exc)
        if _is_retryable or exc.__class__.__name__ == "RetryError":
            _raise_appropriately(exc, _is_retryable)
        raise exc


async def retry_async_call(
    fn: Callable[[], Awaitable[T]],
    *,
    policy: RetryPolicy | None = None,
    on_retry: Callable[[BaseException], Any] | None = None,
) -> T:
    """Run ``fn`` asynchronously under ``policy``. Same semantics as ``retry_call``."""
    policy = policy or RetryPolicy()
    retryable = retry_if_exception_type(policy.retry_exceptions)
    retrying = AsyncRetrying(**policy._retry_kwargs())

    async def _attempt() -> T:
        try:
            return await fn()
        except BaseException as exc:  # noqa: BLE001
            if retryable(exc):
                if on_retry is not None:
                    on_retry(exc)
                raise
            raise

    try:
        async for attempt in retrying:
            with attempt:
                return await _attempt()
        raise AssertionError("unreachable")  # pragma: no cover
    except BaseException as exc:  # noqa: BLE001
        if retryable(exc) or exc.__class__.__name__ == "RetryError":
            _raise_appropriately(exc, retryable(exc))
        raise exc


__all__ = [
    "RetryPolicy",
    "retry_call",
    "retry_async_call",
    "DEFAULT_RETRYABLE_EXCEPTIONS",
]
