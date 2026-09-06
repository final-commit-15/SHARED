"""Pagination response builders."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

from agentforge_shared.schemas.common import PaginatedResponse, Pagination
from agentforge_shared.schemas.pagination import (
    CursorMeta,
    PageMeta,
    PaginatedData,
)

T = TypeVar("T")


def paginated_response(
    items: Sequence[T],
    *,
    total: int | None = None,
    page: int = 1,
    page_size: int = 20,
    message: str = "OK",
) -> PaginatedResponse[T]:
    """Build a ``PaginatedResponse`` from a slice of items and totals.

    ``total`` defaults to ``len(items)``; when the caller supplies the true
    total this must be called once per page.
    """
    count = len(items)
    total = count if total is None else total
    pages = max(1, -(-total // page_size))
    return PaginatedResponse[T](
        data=items,
        message=message,
        meta=Pagination(total=total, page=page, page_size=page_size, pages=pages),
    )


def paginated_data(
    items: Sequence[T],
    *,
    total: int,
    page: int = 1,
    page_size: int = 20,
    sort_by: str | None = None,
    sort_desc: bool = False,
) -> PaginatedData[T]:
    """Build ``PaginatedData`` with computed ``PageMeta`` and next cursor."""
    pages = max(1, -(-total // page_size))
    page_meta = PageMeta(
        page=page,
        page_size=page_size,
        total=total,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )
    return PaginatedData[T](
        page_meta=page_meta,
        items=items,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )


def cursor_data(
    items: Sequence[T],
    *,
    next_cursor: str | None,
    has_more: bool,
    total: int | None = None,
    sort_by: str | None = None,
    sort_desc: bool = False,
) -> PaginatedData[T]:
    """Build ``PaginatedData`` with cursor-based ``CursorMeta``."""
    cursor_meta = CursorMeta(
        next_cursor=next_cursor,
        has_more=has_more,
        total=total,
    )
    return PaginatedData[T](
        page_meta=None,
        cursor_meta=cursor_meta,
        items=items,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )


__all__ = ["paginated_response", "paginated_data", "cursor_data"]
