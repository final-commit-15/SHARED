"""Basic pagination helpers (legacy).

**Deprecated**: use :mod:`agentforge_shared.pagination` for the full-featured
offset/cursor pagination package.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from agentforge_shared.schemas.common import Pagination


class PaginationParams(BaseModel):
    """Offset pagination query parameters."""

    page: int = 1
    per_page: int = 20

    @property
    def offset(self) -> int:
        """Zero-based offset."""
        return (self.page - 1) * self.per_page


T = TypeVar("T")


def paginate_list(
    items: list[T],
    page: int,
    per_page: int,
) -> tuple[list[T], Pagination]:
    """Slice ``items`` and return the page plus pagination metadata."""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = items[start:end]
    pages = (total + per_page - 1) // per_page if total > 0 else 0
    return page_items, Pagination(page=page, per_page=per_page, total=total, pages=pages)


class Page(BaseModel, Generic[T]):
    """A single page of items with offset metadata."""

    items: list[T] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    per_page: int = 20

    @property
    def pages(self) -> int:
        """Total page count."""
        if self.per_page <= 0:
            return 0
        return (self.total + self.per_page - 1) // self.per_page

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict for API responses."""
        return self.model_dump()


__all__ = [
    "PaginationParams",
    "paginate_list",
    "Pagination",
    "Page",
]
