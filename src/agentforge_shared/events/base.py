"""Base event contract shared by all platform events."""

from __future__ import annotations

from datetime import datetime
from typing import Any, ClassVar

from pydantic import Field

from agentforge_shared.enums.events import EventSource, EventType
from agentforge_shared.schemas.base import ApiModel
from agentforge_shared.utils.datetime_helpers import utc_now
from agentforge_shared.utils.uuid7 import uuid7_str


class BaseEvent(ApiModel):
    """Envelope every event on the AgentForge event bus carries.

    Attributes:
        event_id: Unique event identifier (UUIDv7 by default).
        event_type: Contract used by routing/subscriptions.
        source: Emitting service.
        occurred_at: UTC timestamp of emission.
        version: Schema version of the event body (default ``1``).
        correlation_id: Links an event to its originating API request chain.
        trace_id: OpenTelemetry trace id when tracing is enabled.
        tenant_id / organization_id / actor_id: Routing/audit context.
        payload: Free-form event body (validated by concrete event types).
    """

    event_id: str = Field(default_factory=uuid7_str, description="Globally-unique event identifier.")
    event_type: EventType
    source: EventSource = Field(default=EventSource.SYSTEM)
    occurred_at: datetime = Field(default_factory=utc_now)
    version: int = Field(default=1, ge=1)
    correlation_id: str | None = None
    trace_id: str | None = None
    tenant_id: str | None = None
    organization_id: str | None = None
    actor_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)

    SCHEMA_VERSION: ClassVar[int] = 1

    def key(self) -> str:
        """Return the routing key (``event_type`` value)."""
        return self.event_type.value

    def with_context(self, **context: Any) -> BaseEvent:
        """Return a copy with additional routing context applied."""
        update: dict[str, Any] = {}
        for field_name in ("correlation_id", "trace_id", "tenant_id", "organization_id", "actor_id"):
            if getattr(self, field_name) is None and field_name in context:
                update[field_name] = context[field_name]
        return self.model_copy(update=update)


__all__ = ["BaseEvent"]
