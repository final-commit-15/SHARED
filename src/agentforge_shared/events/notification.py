"""Notification and audit events."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from agentforge_shared.enums.events import EventSource, EventType
from agentforge_shared.enums.platform import AuditAction, NotificationChannel, NotificationStatus

from .base import BaseEvent


class NotificationSentEvent(BaseEvent):
    """Published when a notification is delivered."""

    event_type: EventType = EventType.NOTIFICATION_SENT
    source: EventSource = EventSource.BACKEND

    notification_id: str
    user_id: str
    channel: NotificationChannel = NotificationChannel.EMAIL
    status: NotificationStatus = NotificationStatus.DELIVERED
    template: str | None = None
    provider: str | None = None


class NotificationFailedEvent(BaseEvent):
    """Published when a notification could not be delivered."""

    event_type: EventType = EventType.NOTIFICATION_FAILED
    source: EventSource = EventSource.BACKEND

    notification_id: str
    user_id: str
    channel: NotificationChannel = NotificationChannel.EMAIL
    error: str | None = None
    attempts: int = Field(default=1, ge=1)


class AuditEvent(BaseEvent):
    """Published for auditable actions (compliance/security trail)."""

    event_type: EventType = EventType.AUDIT_EVENT
    source: EventSource = EventSource.BACKEND

    action: AuditAction
    target_type: str | None = None
    target_id: str | None = None
    actor_id: str | None = None
    ip_address: str | None = None
    outcome: str = Field(default="success", description="success | denied | failure")
    before: dict[str, Any] = Field(default_factory=dict)
    after: dict[str, Any] = Field(default_factory=dict)


__all__ = ["NotificationSentEvent", "NotificationFailedEvent", "AuditEvent"]
