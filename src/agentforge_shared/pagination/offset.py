"""Offset-based pagination helpers."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

from agentforge_shared.schemas.common import Pagination
from agentforge_shared.schemas.pagination import PageMeta, PaginatedData

T = TypeVar("T")


def offset_params(page: int | None = None, page_size: int | None = None, **defaults: int) -> tuple[int, int]:
    """Normalise and clamp offset pagination parameters.

    Returns ``(page, page_size)`` with sane bounds (``page`` >= 1,
    ``page_size`` in ``[1, 100]``).
    """
    page = int(page if page is not None else defaults.get("page", 1))
    page_size = int(page_size if page_size is not None else defaults.get("page_size", 20))
    page = max(1, page)
    page_size = min(100, max(1, page_size))
    return page, page_size


def paginate(
    items: Sequence[T],
    *,
    total: int,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[T], Pagination]:
    """Slice ``items`` (a full result set) by offset page.

    Returns:
        The page slice and a ``Pagination`` metadata object.
    """
    page, page_size = offset_params(page, page_size)
    total = max(0, int(total))
    start = (page - 1) * page_size
    page_items = list(items[start : start + page_size]) if start < len(items) else []
    pages = max(1, -(-total // page_size))
    return page_items, Pagination(total=total, page=page, page_size=page_size, pages=pages)


def offset_data(
    items: Sequence[T],
    *,
    total: int,
    page: int = 1,
    page_size: int = 20,
    sort_by: str | None = None,
    sort_desc: bool = False,
) -> PaginatedData[T]:
    """Build ``PaginatedData`` with computed ``PageMeta``."""
    page, page_size = offset_params(page, page_size)
    pages = max(1, -(-int(total) // page_size))
    page_meta = PageMeta(
        page=page,
        page_size=page_size,
        total=int(total),
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )
    return PaginatedData[T](
        page_meta=page_meta,
        items=list(items),
        sort_by=sort_by,
        sort_desc=sort_desc,
    )


def apply_offset(ll: int, *, page: int = 1, page_size: int = 20) -> tuple[int, int]:
    """Compute the ``(offset, limit)`` window for a query."""
    page, page_size = offset_params(page, page_size)
    return (page - 1) * page_size, page_size


__all__ = ["offset_params", "paginate", "apply_offset", "offset_data"]
