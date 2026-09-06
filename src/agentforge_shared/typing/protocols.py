"""Shared protocols for service layer interfaces."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from .aliases import AsyncCloseable


@runtime_checkable
class HealthProbe(Protocol):
    """Protocol for components that report health."""

    async def health(self) -> bool: ...


@runtime_checkable
class Repository(Protocol):
    """Minimal async repository contract."""

    async def get(self, identifier: Any) -> Any | None: ...
    async def list(self, **filters: Any) -> list[Any]: ...
    async def save(self, entity: Any) -> Any: ...
    async def delete(self, identifier: Any) -> None: ...


@runtime_checkable
class UnitOfWork(AsyncCloseable, Protocol):
    """Async unit-of-work contract for transactional operations."""

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


@runtime_checkable
class TokenService(Protocol):
    """Contract for JWT token issuance/validation."""

    def create_access_token(self, subject: str, **claims: Any) -> str: ...
    def create_refresh_token(self, subject: str) -> str: ...
    def decode_token(self, token: str) -> dict[str, Any]: ...


@runtime_checkable
class RateLimiter(Protocol):
    """Contract implemented by rate limit providers."""

    async def allow(self, key: str, *args: Any, **kwargs: Any) -> bool: ...
    async def consume(self, key: str, *args: Any, **kwargs: Any) -> bool: ...


@runtime_checkable
class EventBus(Protocol):
    """Async event publishing contract."""

    async def publish(self, event: Any, **headers: Any) -> None: ...
    async def subscribe(self, handler: Any, *topics: str) -> None: ...


@runtime_checkable
class StorageClient(Protocol):
    """Object storage client contract."""

    async def upload(self, key: str, data: bytes, **options: Any) -> str: ...
    async def download(self, key: str) -> bytes: ...
    async def delete(self, key: str) -> None: ...
    async def exists(self, key: str) -> bool: ...


__all__ = [
    "HealthProbe",
    "Repository",
    "UnitOfWork",
    "TokenService",
    "RateLimiter",
    "EventBus",
    "StorageClient",
]
