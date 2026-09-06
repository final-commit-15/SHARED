"""Collection and iterator utilities."""

from __future__ import annotations

import itertools
from collections.abc import (
    AsyncIterable,
    Awaitable,
    Callable,
    Generator,
    Iterable,
    Iterator,
    Sequence,
)
from typing import Any, TypeVar, cast

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")


def uniquify(values: Iterable[_T]) -> list[_T]:
    """Return ``values`` with duplicates removed, preserving order."""
    seen: set[_T] = set()
    result: list[_T] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def partition(predicate: Callable[[_T], bool], values: Iterable[_T]) -> tuple[list[_T], list[_T]]:
    """Split ``values`` into two lists: those satisfying ``predicate`` and the rest."""
    yes: list[_T] = []
    no: list[_T] = []
    for value in values:
        (yes if predicate(value) else no).append(value)
    return yes, no


def chunked(values: Sequence[_T], size: int) -> list[list[_T]]:
    """Split ``values`` into non-overlapping chunks of at most ``size`` items."""
    if size < 1:
        raise ValueError("size must be >= 1")
    return [list(values[i : i + size]) for i in range(0, len(values), size)]


def chunked_iter(values: Iterable[_T], size: int) -> Iterator[list[_T]]:
    """Lazy chunking iterator over any iterable."""
    if size < 1:
        raise ValueError("size must be >= 1")
    iterator = iter(values)
    while batch := list(itertools.islice(iterator, size)):
        yield batch


def flatten(nested: Iterable[Iterable[_T]]) -> list[_T]:
    """Flatten a nested list one level deep."""
    return [item for sublist in nested for item in sublist]


def flatten_deep(values: Any) -> list[Any]:
    """Recursively flatten arbitrarily nested iterables (excluding strings)."""

    def _walk(value: Any) -> Generator[Any, None, None]:
        if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
            yield value
            return
        for item in value:
            yield from _walk(item)

    return list(_walk(values))


def group_by(values: Iterable[_T], key_fn: Callable[[_T], _K]) -> dict[_K, list[_T]]:
    """Group ``values`` by the key returned by ``key_fn`` (insertion order)."""
    result: dict[_K, list[_T]] = {}
    for value in values:
        result.setdefault(key_fn(value), []).append(value)
    return result


def merge_dicts(*dicts: dict[_K, _V]) -> dict[_K, _V]:
    """Deep-merge any number of dictionaries; later keys win."""
    merged: dict[_K, _V] = {}
    for d in dicts:
        for key, value in d.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = cast(_V, merge_dicts(cast("dict[_K, _V]", merged[key]), cast("dict[_K, _V]", value)))
            else:
                merged[key] = value
    return merged


def get_in(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """Safely retrieve a nested value by a path of keys."""
    current: Any = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def deep_get(data: dict[str, Any], path: str, *, separator: str = ".", default: Any = None) -> Any:
    """Retrieve a value using a dotted ``path`` string."""
    return get_in(data, *path.split(separator), default=default)


def first(items: Iterable[_T], default: _T | None = None) -> _T | None:
    """Return the first item of an iterable, or ``default`` when empty."""
    for item in items:
        return item
    return default


def count(predicate: Callable[[_T], bool], values: Iterable[_T]) -> int:
    """Count items matching ``predicate``."""
    return sum(1 for v in values if predicate(v))


def batched(values: Iterable[_T], size: int) -> Iterator[list[_T]]:
    """Yield chunks of ``size`` from an iterable (alias of ``chunked_iter``)."""
    if size < 1:
        raise ValueError("size must be >= 1")
    iterator = iter(values)
    while batch := list(itertools.islice(iterator, size)):  # type: ignore[assignment]
        yield batch


def windowed(values: Iterable[_T], n: int) -> Iterator[tuple[_T, ...]]:
    """Yield overlapping windows of size ``n`` over ``values``."""
    if n < 1:
        raise ValueError("n must be >= 1")
    return cast(Iterator[tuple[_T, ...]], zip(*(itertools.islice(it, i, None) for i, it in enumerate(itertools.tee(values, n)))))


def n_smallest(values: Iterable[_T], n: int, *, key: Callable[[_T], Any] | None = None) -> list[_T]:
    """Return the ``n`` smallest items (lexically by ``key`` when provided)."""
    if n < 1:
        return []
    return sorted(values, key=key)[:n]


def dict_to_list(data: dict[_K, _V]) -> list[tuple[_K, _V]]:
    """Return the key/value pairs of a dict as a list of tuples."""
    return list(data.items())


def transpose(matrix: list[list[_T]]) -> list[list[_T]]:
    """Transpose a rectangular nested list (list of lists)."""
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]


def unique_pairs(values: Iterable[_T]) -> Iterator[tuple[_T, _T]]:
    """Yield all unordered pairs from ``values``."""
    items = list(values)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            yield items[i], items[j]


async def alist(iterable: AsyncIterable[_T]) -> list[_T]:
    """Collect an async iterable into a list."""
    return [item async for item in iterable]


async def aget_or_default(awaitable: Awaitable[_T], default: _T | None = None) -> _T | None:
    """Await ``awaitable`` and fall back to ``default`` on exception."""
    try:
        return await awaitable
    except Exception:
        return default


def index_by(values: Iterable[_T], key_fn: Callable[[_T], _K]) -> dict[_K, _T]:
    """Index ``values`` by ``key_fn`` (last match wins)."""
    result: dict[_K, _T] = {}
    for value in values:
        result[key_fn(value)] = value
    return result


def difference(left: Iterable[_T], right: Iterable[_T]) -> list[_T]:
    """Return items present in ``left`` but not ``right`` (order preserved)."""
    right_set = set(right)
    return [item for item in left if item not in right_set]


def intersection(left: Iterable[_T], right: Iterable[_T]) -> list[_T]:
    """Return items present in both iterables (order of ``left`` preserved)."""
    right_set = set(right)
    return [item for item in left if item in right_set]


def to_dict_list(records: Iterable[Any]) -> list[dict[str, Any]]:
    """Normalise objects into plain dicts (accepts dataclasses, models, mappings).

    Returns a list of dicts; non-mapping objects are returned as ``{"value": obj}``.
    """
    result: list[dict[str, Any]] = []
    for record in records:
        if isinstance(record, dict):
            result.append(record)
        elif hasattr(record, "model_dump"):
            result.append(cast("dict[str, Any]", record.model_dump()))
        elif hasattr(record, "__dict__"):  # noqa: SIM114 - simple fallback
            result.append(dict(record.__dict__))
        else:
            result.append({"value": record})
    return result


__all__ = [
    "uniquify",
    "partition",
    "chunked",
    "chunked_iter",
    "flatten",
    "flatten_deep",
    "group_by",
    "merge_dicts",
    "get_in",
    "deep_get",
    "first",
    "count",
    "batched",
    "windowed",
    "n_smallest",
    "dict_to_list",
    "transpose",
    "unique_pairs",
    "alist",
    "aget_or_default",
    "index_by",
    "difference",
    "intersection",
    "to_dict_list",
]
