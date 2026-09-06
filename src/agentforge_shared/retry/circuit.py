"""Circuit breaker for protecting downstream services."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from agentforge_shared.exceptions.base import CircuitOpenException

T = TypeVar("T")


class CircuitState:
    """String constants for breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Stateful circuit breaker with automatic half-open probing.

    Example::

        from agentforge_shared.retry.circuit import CircuitBreaker

        breaker = CircuitBreaker(failure_threshold=5, reset_timeout=30)
        result = breaker.call(sync_fn)           # raises CircuitOpenException when open
        result = await breaker.call_async(async_fn)
    """

    def __init__(
        self,
        *,
        failure_threshold: int = 5,
        reset_timeout: float = 30.0,
        half_open_max: int = 1,
        name: str = "circuit",
        retryable_exceptions: tuple[type[BaseException], ...] = (Exception,),
    ) -> None:
        self.failure_threshold = max(1, failure_threshold)
        self.reset_timeout = max(0.0, reset_timeout)
        self.half_open_max = max(1, half_open_max)
        self.name = name
        self._retryable_exceptions = retryable_exceptions or (Exception,)

        self.state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._opened_at = 0.0
        self._half_open_attempts = 0
        self._lock = asyncio.Lock()

    @property
    def is_open(self) -> bool:
        """Whether calls are currently rejected."""
        return self.state == CircuitState.OPEN

    def _maybe_half_open(self) -> None:
        if self.state == CircuitState.OPEN and (time.monotonic() - self._opened_at) >= self.reset_timeout:
            self.state = CircuitState.HALF_OPEN
            self._half_open_attempts = 0

    def _allow_probe(self) -> bool:
        """Whether a half-open breaker permits another probe call."""
        if self.state != CircuitState.HALF_OPEN:
            return True
        return self._half_open_attempts < self.half_open_max

    def _record_success(self) -> None:
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._half_open_attempts = 0

    def _record_failure(self) -> None:
        self._consecutive_failures += 1
        self._half_open_attempts += 1
        if self.state == CircuitState.CLOSED and self._consecutive_failures >= self.failure_threshold or self.state == CircuitState.HALF_OPEN:
            self._transition_open()

    def _transition_open(self) -> None:
        self.state = CircuitState.OPEN
        self._opened_at = time.monotonic()
        self._half_open_attempts = 0

    def __enter__(self) -> CircuitBreaker:
        self._maybe_half_open()
        if not self._allow_probe():
            raise CircuitOpenException(message=f"circuit {self.name!r} is open")
        self._half_open_attempts += 1
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc is None:
            self._record_success()
            return False
        if isinstance(exc, self._retryable_exceptions):
            self._record_failure()
        return False

    def call(self, fn: Callable[[], T], *args: Any, **kwargs: Any) -> T:
        """Execute ``fn`` under the breaker (sync)."""
        with self:
            return fn(*args, **kwargs)

    async def call_async(self, fn: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any) -> T:
        """Execute ``fn`` under the breaker (async)."""
        async with self._lock:
            self._maybe_half_open()
            if not self._allow_probe():
                raise CircuitOpenException(message=f"circuit {self.name!r} is open")
            self._half_open_attempts += 1
        try:
            result = await fn(*args, **kwargs)
            async with self._lock:
                self._record_success()
            return result
        except BaseException as exc:  # noqa: BLE001 - reported as circuit failures
            async with self._lock:
                if isinstance(exc, self._retryable_exceptions):
                    self._record_failure()
            raise

    def reset(self) -> None:
        """Manually reset the breaker to the closed state."""
        self.state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._opened_at = 0.0
        self._half_open_attempts = 0

    def stats(self) -> dict[str, Any]:
        """Snapshot of breaker state for observability."""
        return {
            "name": self.name,
            "state": self.state,
            "consecutive_failures": self._consecutive_failures,
            "failure_threshold": self.failure_threshold,
            "reset_timeout": self.reset_timeout,
        }


__all__ = ["CircuitBreaker", "CircuitState"]
