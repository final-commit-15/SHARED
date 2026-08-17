"""Pagination helpers."""

from typing import List, TypeVar, Optional
from pydantic import BaseModel

from ..schemas.common import Pagination

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    page: int = 1
    per_page: int = 20


def paginate_list(items: List[T], page: int, per_page: int) -> tuple[List[T], Pagination]:
    """
    Slice a list and return the page items plus pagination metadata.
    """
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    page_items = items[start:end]
    pages = (total + per_page - 1) // per_page if total > 0 else 0

    pagination = Pagination(
        page=page,
        per_page=per_page,
        total=total,
        pages=pages,
    )
    return page_items, pagination