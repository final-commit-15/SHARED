"""Dict merge and JSON flattening utilities."""

from __future__ import annotations

import copy
from typing import Any


def merge_dicts(*dicts: dict[str, Any], deep: bool = True) -> dict[str, Any]:
    """Deep-merge a series of dictionaries.

    Later dictionaries win on key collisions. When ``deep`` is ``False``, keys
    are overwritten wholesale instead of merging nested dicts.
    """
    merged: dict[str, Any] = {}
    for source in dicts:
        if not source:
            continue
        for key, value in source.items():
            if (
                deep
                and key in merged
                and isinstance(value, dict)
                and isinstance(merged[key], dict)
            ):
                merged[key] = merge_dicts(merged[key], value, deep=True)
            else:
                merged[key] = copy.deepcopy(value)
    return merged


def update_nested(target: dict[str, Any], patch: dict[str, Any], *, in_place: bool = False) -> dict[str, Any]:
    """Apply ``patch`` onto ``target`` recursively (returns a new dict unless ``in_place``)."""
    result = target if in_place else copy.deepcopy(target)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = update_nested(result[key], value, in_place=False)
        else:
            result[key] = copy.deepcopy(value)
    return result


def flatten_dict(
    data: dict[str, Any],
    *,
    parent: str = "",
    separator: str = ".",
    include_lists: bool = False,
) -> dict[str, Any]:
    """Flatten a nested dict into a single-level dict with dotted keys.

    Example::

        flatten_dict({"a": {"b": 1}})  # -> {"a.b": 1}

    Args:
        data: Nested dictionary.
        parent: Internal prefix prefixing returned keys (usually empty).
        separator: Separator between path segments.
        include_lists: When ``True``, list items are indexed (``a.0.b``);
            otherwise lists are copied as-is.
    """
    flat: dict[str, Any] = {}

    def _walk(node: dict[str, Any], prefix: str) -> None:
        for key, value in node.items():
            full_key = f"{prefix}{separator}{key}" if prefix else key
            if isinstance(value, dict):
                _walk(value, full_key)
            elif isinstance(value, list) and include_lists:
                for index, item in enumerate(value):
                    item_key = f"{full_key}{separator}{index}"
                    if isinstance(item, dict):
                        _walk(item, item_key)
                    else:
                        flat[item_key] = item
            else:
                flat[full_key] = value

    _walk(data, parent)
    return flat


def unflatten_dict(
    data: dict[str, Any],
    *,
    separator: str = ".",
) -> dict[str, Any]:
    """Invert :func:`flatten_dict`: expand dotted keys back into a nested dict."""
    result: dict[str, Any] = {}
    for key, value in data.items():
        parts = key.split(separator)
        node = result
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value
    return result


def pick(data: dict[str, Any], keys: list[str] | tuple[str, ...]) -> dict[str, Any]:
    """Return a new dict containing only ``keys`` (missing keys omitted)."""
    return {key: data[key] for key in keys if key in data}


def omit(data: dict[str, Any], keys: list[str] | tuple[str, ...]) -> dict[str, Any]:
    """Return a copy of ``data`` with ``keys`` removed."""
    return {key: value for key, value in data.items() if key not in keys}


def prune_empty(node: dict[str, Any]) -> dict[str, Any]:
    """Recursively remove keys whose values are ``None``, ``{}`` or ``[]``."""
    pruned: dict[str, Any] = {}
    for key, value in node.items():
        if isinstance(value, dict):
            nested = prune_empty(value)
            if nested:
                pruned[key] = nested
        elif value is None or value == [] or value == {}:
            continue
        else:
            pruned[key] = value
    return pruned


def deep_merge(*dicts: dict[str, Any]) -> dict[str, Any]:
    """Alias exposing the default deep-merge behaviour."""
    return merge_dicts(*dicts, deep=True)


def get_path(data: dict[str, Any], path: str, *, separator: str = ".", default: Any = None) -> Any:
    """Return the value at ``path`` (dotted) or ``default``."""
    current: Any = data
    for part in path.split(separator):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return default
    return current


def set_path(data: dict[str, Any], path: str, value: Any, *, separator: str = ".", in_place: bool = False) -> dict[str, Any]:
    """Return ``data`` with ``value`` assigned at ``path``."""
    result = data if in_place else copy.deepcopy(data)
    parts = path.split(separator)
    node = result
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    node[parts[-1]] = value
    return result


__all__ = [
    "merge_dicts",
    "update_nested",
    "flatten_dict",
    "unflatten_dict",
    "pick",
    "omit",
    "prune_empty",
    "deep_merge",
    "get_path",
    "set_path",
]
