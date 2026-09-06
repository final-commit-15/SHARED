"""Request logging middleware (structured access logs)."""

from __future__ import annotations

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from agentforge_shared.logging.logger import get_logger
from agentforge_shared.telemetry.metrics import record_api

_logger = get_logger("agentforge.http")


class AccessLogMiddleware(BaseHTTPMiddleware):
    """Emit one structured log line per request.

    Logs method, path, status, latency, and any bound request/correlation ids.

    Example::

        from agentforge_shared.middleware.logging import AccessLogMiddleware
        app.add_middleware(AccessLogMiddleware)
    """

    def __init__(self, app, *, include_query: bool = False, log_headers: tuple[str, ...] = ()) -> None:
        super().__init__(app)
        self._include_query = include_query
        self._log_headers = log_headers

    async def dispatch(self, request: Request, call_next) -> Response:
        started = time.perf_counter()
        try:
            response = await call_next(request)
        except BaseException:
            duration = time.perf_counter() - started
            _logger.exception(
                "request_failed",
                method=request.method,
                path=request.url.path,
                duration_ms=round(duration * 1000, 2),
            )
            raise
        duration = time.perf_counter() - started
        record_api(response.status_code, request.method, request.url.path)

        fields = {
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(duration * 1000, 2),
        }
        if self._include_query:
            fields["query"] = str(request.url.query)
        if self._log_headers:
            fields["headers"] = {h: request.headers.get(h) for h in self._log_headers}
        _logger.info("http_request", **fields)
        return response


__all__ = ["AccessLogMiddleware"]
