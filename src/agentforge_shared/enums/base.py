"""Shared behaviours for platform enumerations."""

from __future__ import annotations

from collections.abc import Iterable
from enum import Enum
from typing import Any, Self, TypeVar

_E = TypeVar("_E", bound="StringEnum")


class StringEnum(str, Enum):
    """A ``str``, ``Enum`` that exposes membership helpers.

    Every platform enum subclasses this to guarantee uniform behaviour:
    values are always strings, iterating is stable, and coercion from
    arbitrary user input never raises ugly ``ValueError`` stack traces.
    """

    def __str__(self) -> str:
        """Return the raw value (not ``ClassName.VALUE``)."""
        return self.value

    @classmethod
    def values(cls) -> list[str]:
        """Return all raw values in declaration order."""
        return [member.value for member in cls]

    @classmethod
    def names(cls) -> list[str]:
        """Return all member names in declaration order."""
        return [member.name for member in cls]

    @classmethod
    def is_valid(cls, value: Any) -> bool:
        """Return ``True`` when ``value`` matches one of the raw values."""
        return value in cls._value2member_map_

    @classmethod
    def coerce(cls, value: Any) -> Self | None:
        """Return the member whose value equals ``value`` (or ``None``).

        Accepts both raw values (``"active"``) and existing members.
        """
        return cls._value2member_map_.get(value)

    @classmethod
    def require(cls, value: Any, *, message: str | None = None) -> Self:
        """Return the member matching ``value`` or raise ``ValueError``."""
        member = cls.coerce(value)
        if member is None:
            hint = message or f"{cls.__name__} must be one of {cls.values()!r}"
            raise ValueError(f"{hint}, got {value!r}")
        return member

    @classmethod
    def has_any(cls, values: Iterable[Any]) -> bool:
        """Return ``True`` if any value in ``values`` is a valid member."""
        return any(cls.is_valid(v) for v in values)
