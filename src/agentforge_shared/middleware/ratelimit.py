"""Rate limiting middleware with pluggable backend."""

from __future__ import annotations

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from agentforge_shared.exceptions.base import RateLimitException
from agentforge_shared.typing import RateLimiter


class InMemoryRateLimiter(RateLimiter):
    """Simple per-key windowed limiter (single process; for demos/tests)."""

    def __init__(self, *, limit: int = 100, window_seconds: int = 60) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = {}

    async def allow(self, key: str, *args, **kwargs) -> bool:
        import time

        now = time.monotonic()
        hits = [t for t in self._hits.get(key, []) if now - t < self.window_seconds]
        if len(hits) >= self.limit:
            self._hits[key] = hits
            return False
        hits.append(now)
        self._hits[key] = hits
        return True

    async def consume(self, key: str, *args, **kwargs) -> bool:
        return await self.allow(key, *args, **kwargs)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Enforce a global rate limit per client key.

    The client key defaults to the client IP; supply a ``key_fn`` to key on
    API keys or user ids instead.

    Example::

        from agentforge_shared.middleware.ratelimit import (
            RateLimitMiddleware, InMemoryRateLimiter,
        )
        app.add_middleware(
            RateLimitMiddleware,
            limiter=InMemoryRateLimiter(limit=100, window_seconds=60),
        )
    """

    def __init__(
        self,
        app,
        *,
        limiter: RateLimiter | None = None,
        limit: int = 100,
        window_seconds: int = 60,
        key_fn=None,
        exempt_paths: tuple[str, ...] = ("/health", "/metrics"),
    ) -> None:
        super().__init__(app)
        self._limiter = limiter or InMemoryRateLimiter(limit=limit, window_seconds=window_seconds)
        self._key_fn = key_fn or (lambda request: request.client.host if request.client else "unknown")
        self._exempt = exempt_paths

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in self._exempt:
            return await call_next(request)
        key = self._key_fn(request)
        allowed = await self._limiter.allow(key)
        if not allowed:
            raise RateLimitException(
                message="rate limit exceeded",
                details={"key": key, "retry_after": self._retry_after},
            )
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self._limit)
        response.headers["X-RateLimit-Remaining"] = str(self._remaining or 0)
        return response

    @property
    def _retry_after(self) -> int:
        limiter = self._limiter
        window = getattr(limiter, "window_seconds", 60)
        return int(window)

    @property
    def _limit(self) -> int:
        return getattr(self._limiter, "limit", 100)

    @property
    def _remaining(self) -> int | None:
        limiter = self._limiter
        limit = getattr(limiter, "limit", 100)
        hits = getattr(limiter, "_hits", {})
        return max(0, limit - len(hits))


__all__ = ["RateLimitMiddleware", "InMemoryRateLimiter"]
