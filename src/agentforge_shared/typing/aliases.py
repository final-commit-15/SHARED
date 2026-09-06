"""Generic typed aliases and protocols used across the platform."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterable, Iterator
from typing import Any, Literal, Protocol, TypeAlias, TypeVar, runtime_checkable

_T = TypeVar("_T")
_E = TypeVar("_E")

# Primitive JSON scalars
JSONPrimitive: TypeAlias = str | int | float | bool | None

# Any JSON-serialisable value.
JSONValue: TypeAlias = (
    JSONPrimitive
    | "JSONObject"
    | list["JSONValue"]
)

# A JSON object (string-keyed map).
JSONObject: TypeAlias = dict[str, "JSONValue"]

# Recursive full JSON type.
JSON: TypeAlias = JSONValue

# Convenience: any value acceptable by a JSON serializer.
JSONSerializable: TypeAlias = Any

# A JSON-like payload (nodes can be objects/arrays/primitives).
JsonDict: TypeAlias = dict[str, Any]

# Callables
AsyncCallable: TypeAlias = Callable[..., Awaitable[Any]]
AsyncCallableT: TypeAlias = Callable[..., Awaitable[_T]]
SyncCallableT: TypeAlias = Callable[..., _T]
AsyncIteratorT: TypeAlias = AsyncIterator[_T]
IteratorT: TypeAlias = Iterator[_T]
CoroutineFn: TypeAlias = Callable[..., Awaitable[_T]]

# Primitive identifier types
Primitive: TypeAlias = str | int | float | bool | bytes | None
Identifier: TypeAlias = str | int
Scalar: TypeAlias = str | int | float | bool | None
DictStr: TypeAlias = dict[str, Any]
ListStr: TypeAlias = list[str]
OptListStr: TypeAlias = list[str] | None
OptStr: TypeAlias = str | None

# Environment / mode literals
EnvName: TypeAlias = Literal["development", "testing", "staging", "production"]
ConflictLevel: TypeAlias = Literal["error", "warn", "merge"]

# Callback / hook
Hook: TypeAlias = Callable[..., Any]


@runtime_checkable
class JsonSerializable(Protocol):
    """Protocol for objects that can be converted to plain Python data."""

    def to_dict(self) -> dict[str, Any]: ...


@runtime_checkable
class AsyncCloseable(Protocol):
    """Protocol for resources that must be closed asynchronously."""

    async def aclose(self) -> None: ...


@runtime_checkable
class SyncCloseable(Protocol):
    """Protocol for resources that must be closed synchronously."""

    def close(self) -> None: ...


@runtime_checkable
class Identifiable(Protocol):
    """Protocol for entities exposing an ``id``."""

    @property
    def id(self) -> str | int: ...


@runtime_checkable
class LoggerLike(Protocol):
    """Minimal logging contract implemented by structlog and stdlib loggers."""

    def debug(self, *args: Any, **kwargs: Any) -> None: ...
    def info(self, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, *args: Any, **kwargs: Any) -> None: ...
    def error(self, *args: Any, **kwargs: Any) -> None: ...
    def exception(self, *args: Any, **kwargs: Any) -> None: ...


@runtime_checkable
class Cache(Protocol):
    """Async cache interface implemented by :mod:`agentforge_shared.cache`."""

    async def get(self, key: str, default: _T | None = None) -> _T | None: ...
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None: ...
    async def delete(self, key: str) -> None: ...
    async def exists(self, key: str) -> bool: ...


@runtime_checkable
class Provider(Protocol):
    """Common provider interface for LLMs/embeddings/vector stores."""

    name: str
    async def health(self) -> bool: ...


@runtime_checkable
class Retryable(Protocol):
    """Anything that exposes a retry policy hook."""

    def retries(self) -> int: ...


@runtime_checkable
class Validator(Protocol):
    """Protocol for validators returning a boolean or raising."""

    def __call__(self, value: Any) -> bool: ...


__all__ = [
    "JSONPrimitive",
    "JSONValue",
    "JSONObject",
    "JSON",
    "JSONSerializable",
    "JsonDict",
    "AsyncCallable",
    "AsyncCallableT",
    "SyncCallableT",
    "AsyncIteratorT",
    "IteratorT",
    "CoroutineFn",
    "Primitive",
    "Identifier",
    "Scalar",
    "DictStr",
    "ListStr",
    "OptListStr",
    "OptStr",
    "EnvName",
    "ConflictLevel",
    "Hook",
    "JsonSerializable",
    "AsyncCloseable",
    "SyncCloseable",
    "Identifiable",
    "LoggerLike",
    "Cache",
    "Provider",
    "Retryable",
    "Validator",
]
