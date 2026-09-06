"""Correlation and request id middleware."""

from __future__ import annotations

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from agentforge_shared.constants.headers import CORRELATION_ID_HEADER, REQUEST_ID_HEADER
from agentforge_shared.logging.context import bind_context, clear_context
from agentforge_shared.utils.uuid7 import uuid7_str


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Assign request/correlation ids, bind log context, and expose them.

    Reads an incoming ``X-Correlation-ID`` when present, otherwise generates
    one; always generates a fresh ``X-Request-ID``.

    Example::

        from agentforge_shared.middleware.context import RequestContextMiddleware
        app.add_middleware(RequestContextMiddleware)
    """

    def __init__(self, app, *, header_override_prefix: str = "", request_id_header: str = REQUEST_ID_HEADER) -> None:
        super().__init__(app)
        self._request_id_header = request_id_header
        _ = header_override_prefix

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get(self._request_id_header) or uuid7_str()
        correlation_id = request.headers.get(CORRELATION_ID_HEADER) or request_id

        request.state.request_id = request_id
        request.state.correlation_id = correlation_id

        bind_context(request_id=request_id, correlation_id=correlation_id)

        response = await call_next(request)
        response.headers[self._request_id_header] = request_id
        response.headers[CORRELATION_ID_HEADER] = correlation_id
        clear_context()
        return response


__all__ = ["RequestContextMiddleware"]
