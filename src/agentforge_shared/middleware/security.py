"""Security-oriented middleware: security headers, CORS, trusted hosts."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

SECURITY_HEADERS: dict[str, str] = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Append hardened security headers to every response."""

    def __init__(self, app, *, headers: dict[str, str] | None = None) -> None:
        super().__init__(app)
        self._headers = {**SECURITY_HEADERS, **(headers or {})}

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        for key, value in self._headers.items():
            if key not in response.headers:
                response.headers[key] = value
        return response


def configure_cors(app: FastAPI, *, allow_origins: list[str] | None = None) -> None:
    """Add permissive-but-configurable CORS middleware to ``app``."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins or ["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition", "X-Request-ID", "X-Correlation-ID"],
    )


__all__ = ["SecurityHeadersMiddleware", "configure_cors", "SECURITY_HEADERS"]
