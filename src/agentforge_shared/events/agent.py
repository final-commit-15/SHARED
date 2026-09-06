"""Agent lifecycle events."""

from __future__ import annotations

from pydantic import Field

from agentforge_shared.enums.agent import AgentStatus, AgentType
from agentforge_shared.enums.events import EventSource, EventType

from .base import BaseEvent


class AgentCreatedEvent(BaseEvent):
    """Published when an agent definition is created."""

    event_type: EventType = EventType.AGENT_CREATED
    source: EventSource = EventSource.BACKEND

    agent_id: str
    name: str
    agent_type: AgentType = AgentType.CUSTOM
    version: str | None = None
    created_by: str | None = None


class AgentUpdatedEvent(BaseEvent):
    """Published when an agent definition is updated."""

    event_type: EventType = EventType.AGENT_UPDATED
    source: EventSource = EventSource.BACKEND

    agent_id: str
    name: str
    version: str | None = None
    changed_fields: list[str] = Field(default_factory=list)
    updated_by: str | None = None


class AgentRegisteredEvent(BaseEvent):
    """Published when a runtime registers a live agent instance."""

    event_type: EventType = EventType.AGENT_REGISTERED
    source: EventSource = EventSource.AGENTS

    agent_id: str
    instance_id: str
    status: AgentStatus = AgentStatus.ACTIVE
    endpoint: str | None = None
    capabilities: list[str] = Field(default_factory=list)


class AgentPublishedEvent(BaseEvent):
    """Published when an agent is published (made available)."""

    event_type: EventType = EventType.AGENT_PUBLISHED
    source: EventSource = EventSource.BACKEND

    agent_id: str
    name: str
    version: str
    published_by: str | None = None


class AgentDeletedEvent(BaseEvent):
    """Published when an agent definition is deleted."""

    event_type: EventType = EventType.AGENT_DELETED
    source: EventSource = EventSource.BACKEND

    agent_id: str
    deleted_by: str | None = None


__all__ = [
    "AgentCreatedEvent",
    "AgentUpdatedEvent",
    "AgentRegisteredEvent",
    "AgentPublishedEvent",
    "AgentDeletedEvent",
]
