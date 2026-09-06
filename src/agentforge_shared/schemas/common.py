"""Common API response schemas shared by every AgentForge service."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import Field

from agentforge_shared.enums.platform import HealthStatus

from .base import ApiModel

T = TypeVar("T")


class Pagination(ApiModel):
    """Offset pagination metadata embedded in list responses."""

    page: int = Field(1, ge=1, description="Current page (1-indexed).")
    per_page: int = Field(20, ge=1, le=100, description="Items per page.")
    total: int = Field(0, ge=0, description="Total number of matching items.")
    pages: int | None = Field(None, ge=0, description="Total number of pages.")

    @property
    def has_next(self) -> bool:
        """Return ``True`` when a subsequent page exists."""
        if self.pages is None:
            return False
        return self.page < self.pages

    @property
    def has_previous(self) -> bool:
        """Return ``True`` when a previous page exists."""
        return self.page > 1


class APIResponse(ApiModel, Generic[T]):
    """Standard API response envelope.

    Usage::

        APIResponse[User](data=user, message="ok")
    """

    success: bool = True
    data: T
    message: str | None = None
    pagination: Pagination | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now().astimezone())
    version: str = Field("1", description="Response schema/API version.")

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Serialize while coalescing ``success`` with the error path."""
        payload = super().model_dump(*args, **kwargs)
        payload["success"] = bool(self.success)
        return payload


class PaginatedResponse(APIResponse[T]):
    """Standard paginated list response.

    Usage::

        PaginatedResponse[User](data=[...], pagination=Pagination(...))
    """

    data: list[T] = Field(default_factory=list)
    pagination: Pagination = Field(default_factory=Pagination)


class SuccessResponse(ApiModel):
    """A response body that only signals success (no data payload)."""

    success: bool = True
    message: str = "OK"
    timestamp: datetime = Field(default_factory=lambda: datetime.now().astimezone())


class MessageResponse(ApiModel):
    """A response that carries a single message string."""

    success: bool = True
    message: str = Field(..., description="Human-readable message.")
    code: str | None = None


class ErrorResponse(ApiModel):
    """Standard API error response."""

    success: bool = False
    error: str = Field(..., description="Error message.")
    code: str | None = None
    details: Any = None
    request_id: str | None = Field(default=None, description="Request that produced this error.")
    timestamp: datetime = Field(default_factory=lambda: datetime.now().astimezone())


class HealthResponse(ApiModel):
    """Health check payload returned by ``/health`` endpoints.

    **Deprecated**: use :class:`~agentforge_shared.schemas.health.HealthResponse`.
    Kept for backward compatibility with the first release.
    """

    status: HealthStatus = HealthStatus.UP
    version: str = "0.1.0"
    checks: dict[str, HealthStatus] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now().astimezone())


__all__ = [
    "Pagination",
    "APIResponse",
    "PaginatedResponse",
    "SuccessResponse",
    "MessageResponse",
    "ErrorResponse",
    "HealthResponse",
]
