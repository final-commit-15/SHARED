"""Result and Maybe types for functional, exception-free error handling.

These mirror common monadic patterns while staying lightweight and typed.
They are especially useful in service layers where a function may return data
**or** a structured error without raising.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, overload

from .aliases import JSONValue

_T = TypeVar("_T")
_E = TypeVar("_E")
_U = TypeVar("_U")


@dataclass(frozen=True)
class Ok(Generic[_T]):
    """Wraps a successful value."""

    value: _T


@dataclass(frozen=True)
class Err(Generic[_E]):
    """Wraps an error value."""

    error: _E


Result = Ok[_T] | Err[_E]
Maybe = _T | None


def ok(value: _T) -> Ok[_T]:
    """Construct an ``Ok`` result."""
    return Ok(value)


def err(error: _E) -> Err[_E]:
    """Construct an ``Err`` result."""
    return Err(error)


@overload
def is_ok(result: Ok[_T]) -> bool: ...
@overload
def is_ok(result: object) -> bool: ...
def is_ok(result: Any) -> bool:
    """Return ``True`` when ``result`` is an :class:`Ok`."""
    return isinstance(result, Ok)


@overload
def unwrap(result: Ok[_T]) -> _T: ...
@overload
def unwrap(result: Err[_E], default: _U) -> _U: ...
def unwrap(result: Result[_T, _E], default: Any = None) -> Any:
    """Return the wrapped value, or ``default`` (or ``None``) on error."""
    if isinstance(result, Ok):
        return result.value
    return default


def unwrap_or(result: Result[_T, _E], fallback: _T) -> _T:
    """Return the wrapped value or ``fallback`` on error."""
    if isinstance(result, Ok):
        return result.value
    return fallback


def unwrap_or_else(result: Result[_T, _E], fallback: Callable[[_E], _T]) -> _T:
    """Return the wrapped value or ``fallback(error)`` on error."""
    if isinstance(result, Ok):
        return result.value
    return fallback(result.error)


def map(result: Result[_T, _E], fn: Callable[[_T], _U]) -> Result[_U, _E]:
    """Apply ``fn`` to the wrapped value, preserving errors."""
    if isinstance(result, Ok):
        try:
            return Ok(fn(result.value))
        except Exception as exc:  # noqa: BLE001 - propagate as error value
            return Err(exc)  # type: ignore[return-value]
    return result  # type: ignore[return-value]


def map_err(result: Result[_T, _E], fn: Callable[[_E], _E]) -> Result[_T, _E]:
    """Transform the error value of ``result``."""
    if isinstance(result, Err):
        return Err(fn(result.error))
    return result  # type: ignore[return-value]


def bind(result: Result[_T, _E], fn: Callable[[_T], Result[_U, _E]]) -> Result[_U, _E]:
    """Chain a function that itself returns a :class:`Result`."""
    if isinstance(result, Ok):
        return fn(result.value)
    return result  # type: ignore[return-value]


def and_then(result: Result[_T, _E], fn: Callable[[_T], Result[_U, _E]]) -> Result[_U, _E]:
    """Alias of :func:`bind`."""
    return bind(result, fn)


def match(result: Result[_T, _E], *, ok_fn: Callable[[_T], _U], err_fn: Callable[[_E], _U]) -> _U:
    """Destructure ``result`` invoking the appropriate handler."""
    if isinstance(result, Ok):
        return ok_fn(result.value)
    return err_fn(result.error)


def from_exception(fn: Callable[..., _T], *args: Any, **kwargs: Any) -> Result[_T, Exception]:
    """Call ``fn`` and capture success/exception into a :class:`Result`."""
    try:
        return Ok(fn(*args, **kwargs))
    except Exception as exc:  # noqa: BLE001 - intentionally broad
        return Err(exc)


def maybe(value: _T | None) -> Maybe[_T]:
    """Wrap a value into a :class:`Maybe` (identity, provided for parity)."""
    return value


def maybe_or(value: _T | None, default: _T) -> _T:
    """Return ``value`` when not ``None``, otherwise ``default``."""
    return value if value is not None else default


def everything_ok(results: list[Result[_T, _E]]) -> bool:
    """Return ``True`` when every result is an :class:`Ok`."""
    return all(isinstance(r, Ok) for r in results)


def errors_only(results: list[Result[Any, _E]]) -> list[_E]:
    """Return the error values from a list of results."""
    return [r.error for r in results if isinstance(r, Err)]


def ok_values(results: list[Result[_T, Any]]) -> list[_T]:
    """Return the wrapped values from a list of results, dropping errors."""
    return [r.value for r in results if isinstance(r, Ok)]


def to_result(value: _T | Exception) -> Result[_T, Exception]:
    """Convert a raw value or exception into a :class:`Result`."""
    if isinstance(value, BaseException):
        return Err(value)
    return Ok(value)


__all__ = [
    "Ok",
    "Err",
    "Result",
    "Maybe",
    "ok",
    "err",
    "is_ok",
    "unwrap",
    "unwrap_or",
    "unwrap_or_else",
    "map",
    "map_err",
    "bind",
    "and_then",
    "match",
    "from_exception",
    "maybe",
    "maybe_or",
    "everything_ok",
    "errors_only",
    "ok_values",
    "to_result",
    "JSONValue",
]
