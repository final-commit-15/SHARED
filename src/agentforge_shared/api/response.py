"""Response envelope builders for FastAPI handlers."""

from __future__ import annotations

from typing import Any, TypeVar

from agentforge_shared.schemas.common import APIResponse

T = TypeVar("T")


def ok(data: T, message: str = "OK") -> APIResponse[T]:
    """Build a successful ``APIResponse`` envelope."""
    return APIResponse[T](data=data, message=message)


def created(data: T, message: str = "Created") -> APIResponse[T]:
    """Build a successful 201-style ``APIResponse`` envelope."""
    return APIResponse[T](data=data, message=message)


def no_content(message: str = "No Content") -> APIResponse[None]:
    """Build an empty, successful response envelope."""
    return APIResponse[None](data=None, message=message)


def success(message: str = "OK", data: Any = None) -> dict[str, Any]:
    """Build a plain success dictionary (direct-JSON responses)."""
    return {"success": True, "message": message, "data": data}


def fail(message: str, code: str = "error", details: Any = None) -> dict[str, Any]:
    """Build a plain failure dictionary for error payloads."""
    return {"success": False, "message": message, "code": code, "details": details}


__all__ = ["ok", "created", "no_content", "success", "fail"]
