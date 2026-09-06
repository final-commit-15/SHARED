"""FastAPI exception handler integration for AgentForge exceptions."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from agentforge_shared.exceptions.base import (
    BaseAgentForgeException,
    ValidationException,
)


def _headers(payload: dict[str, Any], status: int) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if status == 429:
        payload_headers = payload.get("data", {}).get("headers", {})
        if isinstance(payload_headers, dict):
            headers.update({str(k): str(v) for k, v in payload_headers.items()})
    return headers


def exception_to_response(exc: BaseAgentForgeException, request: Request | None = None) -> JSONResponse:
    """Convert an AgentForge exception into a JSON response."""
    payload = exc.to_dict()
    if request is not None:
        payload.setdefault("request_id", getattr(request.state, "request_id", None))
    return JSONResponse(
        status_code=exc.status_code,
        content=payload,
        headers=_headers(payload, exc.status_code),
    )


async def agentforge_exception_handler(request: Request, exc: BaseAgentForgeException) -> JSONResponse:
    """FastAPI handler registered for ``BaseAgentForgeException``."""
    return exception_to_response(exc, request)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Map FastAPI/Pydantic validation errors onto AgentForge error format."""
    errors = exc.errors()
    payload = ValidationException(details=errors)
    body = payload.to_dict()
    body["request_id"] = getattr(request.state, "request_id", None)
    return JSONResponse(status_code=payload.status_code, content=body)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all AgentForge exception handlers to a FastAPI app.

    Args:
        app: The ``FastAPI`` application instance.
    """
    app.add_exception_handler(BaseAgentForgeException, agentforge_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)


__all__ = [
    "exception_to_response",
    "agentforge_exception_handler",
    "validation_exception_handler",
    "register_exception_handlers",
]
