"""Response timing middleware (append X-Process-Time header)."""

from __future__ import annotations

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Measure request time and expose it via a response header.

    Example::

        from agentforge_shared.middleware.timing import PerformanceMiddleware
        app.add_middleware(PerformanceMiddleware, header="X-Process-Time")
    """

    def __init__(self, app, *, header: str = "X-Process-Time", enabled: bool = True) -> None:
        super().__init__(app)
        self.header = header
        self.enabled = enabled

    async def dispatch(self, request: Request, call_next) -> Response:
        started = time.perf_counter()
        response = await call_next(request)
        if self.enabled:
            response.headers[self.header] = f"{time.perf_counter() - started:.4f}"
        return response


__all__ = ["PerformanceMiddleware"]
