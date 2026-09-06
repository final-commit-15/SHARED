"""Exception handling middleware for FastAPI apps."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from agentforge_shared.api.errors import register_exception_handlers
from agentforge_shared.exceptions.base import BaseAgentForgeException


class ExceptionMiddlewareMixin:
    """Mixin providing structured error responses for AgentForge apps."""

    def install_exception_handlers(self) -> None:
        """Register AgentForge exception handlers on the wrapping app."""
        register_exception_handlers(self._app)


def install_exception_middleware(app: FastAPI) -> None:
    """Install structured exception handling on ``app``.

    Example::

        from agentforge_shared.middleware.errors import install_exception_middleware
        install_exception_middleware(app)
    """
    register_exception_handlers(app)


async def unwrap_agentforge_error(request: Request, exc: BaseAgentForgeException) -> JSONResponse:
    """Dependency-friendly alias returning a JSON error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


__all__ = [
    "install_exception_middleware",
    "ExceptionMiddlewareMixin",
    "unwrap_agentforge_error",
]
