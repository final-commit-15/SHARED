"""Safe, forgiving parsing helpers that never raise on bad input."""

from __future__ import annotations

import ast
from datetime import datetime
from typing import Any, TypeVar

from agentforge_shared.utils.datetime_helpers import parse_iso
from agentforge_shared.utils.json_utils import try_loads

_T = TypeVar("_T")


def to_int(value: Any, default: int = 0) -> int:
    """Parse ``value`` as an int, returning ``default`` on failure."""
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    try:
        return int(str(value).strip())
    except (ValueError, TypeError, AttributeError):
        return default


def to_float(value: Any, default: float = 0.0) -> float:
    """Parse ``value`` as a float, returning ``default`` on failure."""
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except (ValueError, TypeError, AttributeError):
        return default


def to_bool(value: Any, default: bool = False) -> bool:
    """Parse ``value`` as a boolean, returning ``default`` on ambiguity.

    Recognises case-insensitive ``true/false/yes/no/1/0/on/off``.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value not in {0}
    if value is None:
        return default
    normalized = str(value).strip().lower()
    if normalized in {"true", "yes", "on", "1", "y", "t"}:
        return True
    if normalized in {"false", "no", "off", "0", "n", "f"}:
        return False
    return default


def to_str(value: Any, default: str = "") -> str:
    """Return the string form of ``value``, or ``default`` when ``None``."""
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip()
    try:
        if isinstance(value, (dict, list)):
            return try_loads(value) if isinstance(value, str) else repr(value)
        return str(value).strip()
    except Exception:
        return default


def to_list(value: Any, *, split: bool = False, delimiter: str = ",") -> list[Any]:
    """Coerce ``value`` into a list.

    - ``None`` -> ``[]``
    - list/tuple/set -> list
    - dict -> list of keys
    - string -> ``[value]`` (or split when ``split=True``)
    """
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    if isinstance(value, dict):
        return list(value.keys())
    if isinstance(value, str):
        if split:
            return [part.strip() for part in value.split(delimiter) if part.strip()]
        return [value]
    return [value]


def to_datetime(value: Any, default: datetime | None = None) -> datetime | None:
    """Parse ``value`` as a datetime (ISO or common formats), else ``default``."""
    if value is None:
        return default
    if isinstance(value, datetime):
        return value
    try:
        return parse_iso(str(value))
    except (ValueError, TypeError):
        return default


def parse_boolean_or_none(value: Any) -> bool | None:
    """Parse a boolean, returning ``None`` when the value is unrecognised."""
    parsed = to_bool(value, default=None)
    if parsed is None:  # pragma: no cover - defensive
        return None
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized not in {"true", "false", "yes", "no", "on", "off", "1", "0"}:
            return None
    return parsed


def eval_literal(value: str, default: Any = None) -> Any:
    """Safely evaluate a Python literal (str/int/float/bool/None/list/dict)."""
    if not isinstance(value, str):
        return value
    try:
        return ast.literal_eval(value.strip())
    except (ValueError, SyntaxError):
        return default


def safe_eval(value: str, default: Any = None) -> Any:
    """Alias of :func:`eval_literal` for readability in config code."""
    return eval_literal(value, default=default)


def parse_json(value: str | bytes, default: Any = None) -> Any:
    """Parse JSON, returning ``default`` on any failure."""
    return try_loads(value) if try_loads(value) is not None else default


def parse_int_list(value: Any, default: list[int] | None = None) -> list[int]:
    """Parse a comma-separated list of integers."""
    if isinstance(value, (list, tuple, set)):
        return [to_int(item) for item in value]
    if isinstance(value, str):
        return [to_int(part) for part in value.split(",") if part.strip().lstrip("-").isdigit()]
    return list(default) if default is not None else []


def parse_numeric(value: Any) -> int | float | None:
    """Return the numeric form of ``value`` (int or float) or ``None``."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value
    try:
        candidate = str(value).strip()
        return int(candidate)
    except (ValueError, TypeError, AttributeError):
        try:
            return float(str(value).strip())
        except (ValueError, TypeError, AttributeError):
            return None


def as_number(value: Any) -> int | float | None:
    """Alias of :func:`parse_numeric`."""
    return parse_numeric(value)


__all__ = [
    "to_int",
    "to_float",
    "to_bool",
    "to_str",
    "to_list",
    "to_datetime",
    "parse_boolean_or_none",
    "eval_literal",
    "safe_eval",
    "parse_json",
    "parse_int_list",
    "parse_numeric",
    "as_number",
]
