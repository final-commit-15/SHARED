"""Sorting, filtering, and search helpers for collections."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from agentforge_shared.schemas.pagination import FilterCondition, SortRequest


def sort_key(field: str, *, sort_desc: bool = False) -> Callable[[dict[str, Any]], Any]:
    """Return an item key extracting ``field`` (missing fields sort last)."""

    def _key(item: dict[str, Any]) -> tuple[bool, str]:
        value = item.get(field)
        missing = value is None
        return (missing, str(value if value is not None else ""))

    return _key


def apply_sort(
    items: list[dict[str, Any]],
    *,
    field: str | None = None,
    sort_desc: bool = False,
) -> list[dict[str, Any]]:
    """Sort a list of dicts by ``field`` (stable, missing-last)."""
    if field is None:
        return items
    return sorted(
        items,
        key=lambda item: (item.get(field) is None, str(item.get(field, ""))),
        reverse=sort_desc,
    )


def apply_sort_request(
    items: list[dict[str, Any]],
    sort_request: SortRequest | None,
) -> list[dict[str, Any]]:
    """Apply the primary sort from ``sort_request`` to ``items``."""
    if sort_request is None or not sort_request.sort:
        return items
    primary = sort_request.sort[0]
    return apply_sort(items, field=primary.field, sort_desc=primary.order.value == "desc")


_OPERATORS: dict[str, Callable[[Any, Any], bool]] = {
    "eq": lambda value, target: value == target,
    "ne": lambda value, target: value != target,
    "gt": lambda value, target: value > target,
    "gte": lambda value, target: value >= target,
    "lt": lambda value, target: value < target,
    "lte": lambda value, target: value <= target,
    "in": lambda value, target: value in target if isinstance(target, (list, tuple, set)) else False,
    "not_in": lambda value, target: value not in target if isinstance(target, (list, tuple, set)) else True,
    "contains": lambda value, target: target in value if isinstance(value, str) else False,
    "icontains": lambda value, target: target.lower() in value.lower() if isinstance(value, str) else False,
}


def matches_filter(item: dict[str, Any], condition: FilterCondition) -> bool:
    """Evaluate a single ``FilterCondition`` against a record."""
    value = item.get(condition.field)
    op = _OPERATORS.get(condition.op)
    if op is None:
        return False
    try:
        return bool(op(value, condition.value))
    except TypeError:
        return False


def apply_filters(items: list[dict[str, Any]], filters: list[FilterCondition] | None) -> list[dict[str, Any]]:
    """Retain records satisfying all filter conditions (AND)."""
    if not filters:
        return items
    return [item for item in items if all(matches_filter(item, condition) for condition in filters)]


def apply_search(items: list[dict[str, Any]], query: str | None, *fields: str) -> list[dict[str, Any]]:
    """Case-insensitive substring search across ``fields``."""
    if not query:
        return items
    needle = query.strip().lower()
    if not needle:
        return items

    def _hit(item: dict[str, Any]) -> bool:
        for field in fields:
            value = item.get(field)
            if isinstance(value, str) and needle in value.lower():
                return True
        return False

    return [item for item in items if _hit(item)]


__all__ = ["sort_key", "apply_sort", "apply_sort_request", "apply_filters", "apply_search", "matches_filter"]
