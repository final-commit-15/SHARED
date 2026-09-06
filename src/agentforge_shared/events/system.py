"""Platform/operations events."""

from __future__ import annotations

from pydantic import Field

from agentforge_shared.enums.events import EventSource, EventType

from .base import BaseEvent


class SystemStartedEvent(BaseEvent):
    """Published when a service completes startup."""

    event_type: EventType = EventType.SYSTEM_STARTED
    source: EventSource = EventSource.SYSTEM

    service: str = Field(..., description="Service name.")
    version: str | None = None
    environment: str | None = None
    started_at: str | None = None


class SystemShutdownEvent(BaseEvent):
    """Published when a service shuts down gracefully."""

    event_type: EventType = EventType.SYSTEM_SHUTDOWN
    source: EventSource = EventSource.SYSTEM

    service: str
    reason: str | None = None
    uptime_seconds: float | None = Field(default=None, ge=0)


class DeploymentEvent(BaseEvent):
    """Published when a deployment is rolled out."""

    event_type: EventType = EventType.DEPLOYMENT_DEPLOYED
    source: EventSource = EventSource.SYSTEM

    deployment_id: str
    service: str
    from_version: str | None = None
    to_version: str
    deployed_by: str | None = None


class ConfigChangedEvent(BaseEvent):
    """Published when runtime configuration is reloaded."""

    event_type: EventType = EventType.CONFIG_CHANGED
    source: EventSource = EventSource.SYSTEM

    service: str
    changed_keys: list[str] = Field(default_factory=list)
    reloaded_by: str | None = None


class FeatureFlagEvent(BaseEvent):
    """Published when a feature flag flips."""

    event_type: EventType = EventType.FEATURE_FLAG_CHANGED
    source: EventSource = EventSource.SYSTEM

    flag: str
    enabled: bool
    rollout_percentage: int = Field(default=100, ge=0, le=100)
    changed_by: str | None = None


__all__ = [
    "SystemStartedEvent",
    "SystemShutdownEvent",
    "DeploymentEvent",
    "ConfigChangedEvent",
    "FeatureFlagEvent",
]
