"""OAuth-style scope parsing and checking."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(scope_string: str | None) -> list[str]:
    """Parse a space-separated scope string into a sorted list.

    Handles both ``"read:agents write:agents"`` and space-separated lists.
    Empty/None yields ``[]``.
    """
    if not scope_string:
        return []
    parts = scope_string.replace(",", " ").split()
    return sorted({p for p in parts if p})


def scope_matches(required: str, granted: Iterable[str]) -> bool:
    """Check whether ``required`` is granted, honouring ``resource:action``.

    ``read:agents`` is granted by ``read:agents`` or the wildcard ``read:*``.
    A bare ``*`` grants everything.
    """
    granted_list = list(granted)
    if "*" in granted_list:
        return True
    if required in granted_list:
        return True
    if ":" in required:
        resource, action = required.split(":", 1)
    else:
        return False
    return f"{resource}:*" in granted_list or f"*:{action}" in granted_list


def has_scope(scopes: Iterable[str], required: str) -> bool:
    """Alias of :func:`scope_matches` (simple presence check)."""
    return scope_matches(required, scopes)


def has_all_scopes(scopes: Iterable[str], required: Iterable[str]) -> bool:
    """Require every scope in ``required`` to be granted."""
    required_list = list(required)
    if not required_list:
        return True
    return all(scope_matches(r, scopes) for r in required_list)


def has_any_scope(scopes: Iterable[str], required: Iterable[str]) -> bool:
    """Require at least one of ``required`` to be granted."""
    required_list = list(required)
    if not required_list:
        return True
    return any(scope_matches(r, scopes) for r in required_list)


def scopes_diff(granted: Iterable[str], required: Iterable[str]) -> list[str]:
    """Return the scopes that are required but not granted."""
    granted_list = list(granted)
    return [r for r in required if not scope_matches(r, granted_list)]


__all__ = [
    "parse_scopes",
    "scope_matches",
    "has_scope",
    "has_all_scopes",
    "has_any_scope",
    "scopes_diff",
]
