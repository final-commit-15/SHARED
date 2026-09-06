"""User and authentication events."""

from __future__ import annotations

from pydantic import Field

from agentforge_shared.enums.events import EventSource, EventType
from agentforge_shared.enums.platform import UserRole

from .base import BaseEvent


class UserCreatedEvent(BaseEvent):
    """Published when a user account is created."""

    event_type: EventType = EventType.USER_CREATED
    source: EventSource = EventSource.BACKEND

    user_id: str
    email: str
    role: UserRole = UserRole.USER
    organization_id: str | None = None
    created_by: str | None = None


class UserUpdatedEvent(BaseEvent):
    """Published when a user account changes."""

    event_type: EventType = EventType.USER_UPDATED
    source: EventSource = EventSource.BACKEND

    user_id: str
    changed_fields: list[str] = Field(default_factory=list)
    updated_by: str | None = None


class UserDeletedEvent(BaseEvent):
    """Published when a user account is deleted."""

    event_type: EventType = EventType.USER_DELETED
    source: EventSource = EventSource.BACKEND

    user_id: str
    deleted_by: str | None = None


class UserLoggedInEvent(BaseEvent):
    """Published when a user authenticates."""

    event_type: EventType = EventType.USER_LOGGED_IN
    source: EventSource = EventSource.BACKEND

    user_id: str
    method: str = Field(default="password", description="password | oauth | api-key | token")
    ip_address: str | None = None
    user_agent: str | None = None
    tenant_id: str | None = None


class UserLoggedOutEvent(BaseEvent):
    """Published when a user signs out."""

    event_type: EventType = EventType.USER_LOGGED_OUT
    source: EventSource = EventSource.BACKEND

    user_id: str
    ip_address: str | None = None


__all__ = [
    "UserCreatedEvent",
    "UserUpdatedEvent",
    "UserDeletedEvent",
    "UserLoggedInEvent",
    "UserLoggedOutEvent",
]
