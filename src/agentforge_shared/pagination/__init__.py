"""Pagination toolkit: offset/cursor helpers, filtering, and schemas."""

from agentforge_shared.schemas.common import Pagination  # noqa: F401
from agentforge_shared.schemas.pagination import (
    CursorMeta,
    CursorPaginationParams,
    FilterCondition,
    FilterRequest,
    OffsetPaginationParams,
    PageMeta,
    PaginatedData,
    SearchRequestParams,
    SortRequest,
    SortSchema,
    decode_cursor as schema_decode_cursor,
    encode_cursor as schema_encode_cursor,
)

from .cursor import batch_cursor, cursor_data, decode_cursor, encode_cursor
from .filtering import (
    apply_filters,
    apply_search,
    apply_sort,
    apply_sort_request,
    matches_filter,
    sort_key,
)
from .offset import apply_offset, offset_data, offset_params, paginate

__all__ = [
    # offset
    "offset_params",
    "paginate",
    "apply_offset",
    "offset_data",
    # cursor
    "encode_cursor",
    "decode_cursor",
    "cursor_data",
    "batch_cursor",
    # filtering / sort / search
    "apply_sort",
    "apply_sort_request",
    "apply_filters",
    "apply_search",
    "matches_filter",
    "sort_key",
    # schemas
    "OffsetPaginationParams",
    "CursorPaginationParams",
    "PageMeta",
    "CursorMeta",
    "PaginatedData",
    "SortSchema",
    "SortRequest",
    "FilterCondition",
    "FilterRequest",
    "SearchRequestParams",
    "Pagination",
]
