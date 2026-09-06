"""Health-check schemas for ``/health`` endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from agentforge_shared.enums.platform import HealthStatus

from .base import ApiModel


def _utc_now_iso() -> str:
    return datetime.now().astimezone().isoformat()


class ComponentHealth(ApiModel):
    """Status of a single dependency (database, redis, LLM provider...)."""

    name: str = Field(..., description="Dependency name, e.g. ``redis``.")
    status: HealthStatus = HealthStatus.UNKNOWN
    latency_ms: float | None = Field(default=None, ge=0)
    error: str | None = Field(default=None)
    details: dict[str, Any] = Field(default_factory=dict)


class HealthResponse(ApiModel):
    """Aggregate service health payload.

    ``status`` is ``up`` when every component is healthy, ``degraded`` when at
    least one component is missing but the service still serves requests, and
    ``down`` when a critical dependency failed.
    """

    status: HealthStatus = HealthStatus.UP
    version: str = "0.1.0"
    service: str | None = Field(default=None, description="Service name reported by telemetry.")
    checks: list[ComponentHealth] = Field(default_factory=list)
    timestamp: str = Field(default_factory=_utc_now_iso)

    @property
    def is_healthy(self) -> bool:
        """Return ``True`` when every component reports ``up``."""
        return all(c.status == HealthStatus.UP for c in self.checks)

    def component(self, name: str) -> ComponentHealth | None:
        """Look up a component by name."""
        for check in self.checks:
            if check.name == name:
                return check
        return None


class ReadinessResponse(ApiModel):
    """Result of a readiness probe."""

    ready: bool = Field(..., description="True when the service can accept work.")
    status: HealthStatus = HealthStatus.UP
    components: dict[str, HealthStatus] = Field(default_factory=dict)


__all__ = [
    "ComponentHealth",
    "HealthResponse",
    "ReadinessResponse",
]
