"""Pagination schemas used by list endpoints."""

from __future__ import annotations

import base64
import json
from typing import Any, Generic, TypeVar

from pydantic import Field, model_validator

from agentforge_shared.enums.platform import SortOrder

from .base import ApiModel
from .common import Pagination  # noqa: F401  (re-export for backward compatibility)

T = TypeVar("T")


class OffsetPaginationParams(ApiModel):
    """Query parameters for classic offset-based pagination."""

    page: int = Field(1, ge=1, description="Page number, 1-indexed.")
    per_page: int = Field(20, ge=1, le=100, description="Items per page (max 100).")

    @property
    def offset(self) -> int:
        """Zero-based offset for slicing."""
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        """Alias of ``per_page`` for query builders."""
        return self.per_page


class CursorPaginationParams(ApiModel):
    """Query parameters for cursor-based (keyset) pagination."""

    cursor: str | None = Field(default=None, description="Opaque cursor from a previous response.")
    limit: int = Field(20, ge=1, le=100, description="Items to return.")

    @model_validator(mode="after")
    def _validate_limit(self) -> CursorPaginationParams:
        if self.limit < 1:
            raise ValueError("limit must be at least 1")
        if self.limit > 100:
            raise ValueError("limit must not exceed 100")
        return self


class SortSchema(ApiModel):
    """Single sort instruction: field name + direction."""

    field: str = Field(..., min_length=1, description="Sort key (whitelist in callers).")
    order: SortOrder = SortOrder.ASC


class SortRequest(ApiModel):
    """Collection of sort instructions with deduplication."""

    sort: list[SortSchema] = Field(default_factory=list, max_length=10)

    def __iter__(self):  # pragma: no cover - convenienece
        return iter(self.sort)


class FilterCondition(ApiModel):
    """A single filter predicate.

    ``value`` is scalar or a list of scalars for ``in`` filters.
    Supported ``op`` values: ``eq, ne, gt, gte, lt, lte, in, not_in, contains, icontains``.
    """

    field: str = Field(..., min_length=1)
    op: str = Field("eq", description="Comparison operator.")
    value: Any = Field(default=None)


class FilterRequest(ApiModel):
    """Collection of filter predicates combined with AND by default."""

    filters: list[FilterCondition] = Field(default_factory=list, max_length=50)


class SearchRequestParams(ApiModel):
    """Query parameters for searching/filtering a collection."""

    q: str | None = Field(default=None, description="Free-text search query.")
    sort_field: str | None = Field(default=None)
    sort_order: SortOrder = Field(default=SortOrder.ASC)
    filters: list[FilterCondition] = Field(default_factory=list)


class PageMeta(ApiModel):
    """Rich metadata for offset pagination responses."""

    page: int
    page_size: int = Field(alias="per_page", description="Alias: ``per_page``.")
    total: int
    pages: int
    has_next: bool = False
    has_previous: bool = Field(alias="has_prev", default=False)

    model_config = {"populate_by_name": True}


class CursorMeta(ApiModel):
    """Rich metadata for cursor pagination responses."""

    next_cursor: str | None = None
    previous_cursor: str | None = None
    limit: int = Field(default=20, ge=1, le=100)
    total: int | None = None
    has_more: bool = False


class PaginatedData(ApiModel, Generic[T]):
    """Generic paginated payload combining items with page metadata.

    One of ``page_meta``/``cursor_meta`` must be provided when constructing
    directly; lenient when only ``items`` are supplied.
    """

    items: list[T] = Field(default_factory=list)
    page_meta: PageMeta | None = None
    cursor_meta: CursorMeta | None = None
    sort_by: str | None = None
    sort_desc: bool = False
    total: int | None = None

    @model_validator(mode="after")
    def _validate_meta(self) -> PaginatedData[T]:
        if self.page_meta is not None and self.cursor_meta is not None:
            raise ValueError("page_meta and cursor_meta are mutually exclusive")
        if self.total is None:
            if self.page_meta is not None:
                self.total = self.page_meta.total
            elif self.cursor_meta is not None:
                self.total = self.cursor_meta.total
        return self


def encode_cursor(payload: dict[str, Any]) -> str:
    """Encode a pagination cursor as a URL-safe opaque string."""
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    return base64.urlsafe_b64encode(raw.encode("utf-8")).decode("ascii")


def decode_cursor(cursor: str) -> dict[str, Any] | None:
    """Decode an opaque cursor produced by :func:`encode_cursor`.

    Returns ``None`` if the cursor is malformed/expired.
    """
    try:
        raw = base64.urlsafe_b64decode(cursor.encode("ascii")).decode("utf-8")
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            return None
        return payload
    except (ValueError, LookupError):
        return None


# ---------------------------------------------------------------------------
# Backward-compatible export comment retained. ``Pagination`` is imported
# from ``schemas.common`` at the top of this module so ``from ...pagination
# import Pagination`` keeps working.
# ---------------------------------------------------------------------------

__all__ = [
    "OffsetPaginationParams",
    "CursorPaginationParams",
    "SortSchema",
    "SortRequest",
    "FilterCondition",
    "FilterRequest",
    "SearchRequestParams",
    "PageMeta",
    "CursorMeta",
    "PaginatedData",
    "Pagination",
    "encode_cursor",
    "decode_cursor",
]
