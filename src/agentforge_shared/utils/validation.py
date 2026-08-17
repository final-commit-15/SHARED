"""Common validation helpers."""

from typing import Any, List


def validate_non_empty(value: Any, field_name: str) -> None:
    """Raise ValueError if value is empty or None."""
    if value is None:
        raise ValueError(f"{field_name} cannot be None")
    if hasattr(value, "__len__") and len(value) == 0:
        raise ValueError(f"{field_name} cannot be empty")


def validate_range(value: int, min_val: int, max_val: int, field_name: str) -> None:
    """Raise ValueError if value is outside [min_val, max_val]."""
    if not (min_val <= value <= max_val):
        raise ValueError(f"{field_name} must be between {min_val} and {max_val}")