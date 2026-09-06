"""Middleware collection for FastAPI apps."""

from .context import RequestContextMiddleware
from .errors import ExceptionMiddlewareMixin, install_exception_middleware, unwrap_agentforge_error
from .hosts import TrustedHostMiddleware, configure_compression
from .logging import AccessLogMiddleware
from .ratelimit import InMemoryRateLimiter, RateLimitMiddleware
from .security import SECURITY_HEADERS, SecurityHeadersMiddleware, configure_cors
from .timing import PerformanceMiddleware

__all__ = [
    "RequestContextMiddleware",
    "AccessLogMiddleware",
    "PerformanceMiddleware",
    "SecurityHeadersMiddleware",
    "configure_cors",
    "TrustedHostMiddleware",
    "configure_compression",
    "RateLimitMiddleware",
    "InMemoryRateLimiter",
    "install_exception_middleware",
    "ExceptionMiddlewareMixin",
    "unwrap_agentforge_error",
    "SECURITY_HEADERS",
]
