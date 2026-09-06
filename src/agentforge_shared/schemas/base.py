"""Reusable Pydantic base models, mixins, and shared building blocks."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from agentforge_shared.utils.datetime_helpers import utc_now

_T = TypeVar("_T")


class ApiModel(BaseModel):
    """Base model with strict-but-practical Pydantic v2 defaults."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=False,
    )


class TimestampMixin(ApiModel):
    """Adds ``created_at`` / ``updated_at`` timestamps handled by the platform."""

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class UUIDMixin(ApiModel):
    """Adds a UUID primary-key style field."""

    id: uuid.UUID = Field(..., description="Universally unique identifier.")


class AuditMixin(ApiModel):
    """Common audit bookkeeping fields attached to persisted entities."""

    created_by: str | uuid.UUID | None = Field(default=None, description="Principal who created the resource.")
    updated_by: str | uuid.UUID | None = Field(default=None, description="Principal who last updated the resource.")
    deleted_at: datetime | None = Field(default=None, description="Soft-delete timestamp.")
    version: int = Field(default=1, ge=1, description="Optimistic-locking version counter.")


class ResourceSchema(TimestampMixin, UUIDMixin):
    """Canonical persisted resource: ``id`` + timestamps + audit fields."""

    created_by: str | uuid.UUID | None = None
    updated_by: str | uuid.UUID | None = None
    deleted_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict, description="Arbitrary resource metadata.")


class MetadataSchema(ApiModel):
    """Free-form metadata container exposed by API responses."""

    total: int | None = Field(default=None)
    count: int | None = Field(default=None)
    page: int | None = Field(default=None)
    per_page: int | None = Field(default=None)
    pages: int | None = Field(default=None)
    next_cursor: str | None = Field(default=None)
    previous_cursor: str | None = Field(default=None)
    generated_at: datetime = Field(default_factory=utc_now)
    extra: dict[str, Any] = Field(default_factory=dict)


class PageInfo(ApiModel):
    """Pagination metadata for scraped list responses."""

    has_next: bool = Field(default=False)
    has_previous: bool = Field(default=False)
    start_index: int | None = Field(default=None, ge=0)
    end_index: int | None = Field(default=None, ge=0)


class ValidationIssue(ApiModel):
    """A single field-level validation problem."""

    loc: list[str | int] = Field(default_factory=list, description="Path to the offending field.")
    msg: str = Field("", description="Human-readable message.")
    type: str = Field("value_error", description="Pydantic error type.")
    input: Any = Field(default=None, description="As-supplied input that failed.")


class ValidationErrorSchema(ApiModel):
    """Structured payload for 422 responses."""

    success: bool = Field(default=False)
    code: str = Field("AF_VALIDATION_ERROR")
    message: str = Field("Validation failed.", description="Summary message.")
    errors: list[ValidationIssue] = Field(default_factory=list)


class TypedResource(ApiModel, Generic[_T]):
    """Generic envelope for a single typed resource in a response body."""

    data: _T


__all__ = [
    "ApiModel",
    "TimestampMixin",
    "UUIDMixin",
    "AuditMixin",
    "ResourceSchema",
    "MetadataSchema",
    "PageInfo",
    "ValidationIssue",
    "ValidationErrorSchema",
    "TypedResource",
]
