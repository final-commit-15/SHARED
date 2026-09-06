"""Trusted host and compression middleware."""

from __future__ import annotations

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class TrustedHostMiddleware(BaseHTTPMiddleware):
    """Reject requests whose ``Host`` header is not in the allow-list.

    Subdomains of an allowed host are accepted too.

    Example::

        from agentforge_shared.middleware.hosts import TrustedHostMiddleware
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=["api.example.com"])
    """

    def __init__(self, app, *, allowed_hosts: list[str] | None = None, allow_localhost: bool = True) -> None:
        super().__init__(app)
        hosts = list(allowed_hosts or [])
        if allow_localhost:
            hosts += ["localhost", "127.0.0.1", "[::1]"]
        self._allowed = set(hosts)

    async def dispatch(self, request: Request, call_next) -> Response:
        host = request.headers.get("host", "")
        hostname = host.split(":")[0]
        if hostname not in self._allowed and not self._allowed_match(hostname):
            from fastapi.responses import PlainTextResponse

            return PlainTextResponse("Invalid Host header", status_code=400)
        return await call_next(request)

    def _allowed_match(self, hostname: str) -> bool:
        return any(hostname == allowed or hostname.endswith(f".{allowed}") for allowed in self._allowed)


def configure_compression(app: FastAPI, *, minimum_size: int = 1000) -> None:
    """Enable gzip compression on ``app`` (starlette GZipMiddleware)."""
    from starlette.middleware.gzip import GZipMiddleware

    app.add_middleware(GZipMiddleware, minimum_size=minimum_size)


__all__ = ["TrustedHostMiddleware", "configure_compression"]
