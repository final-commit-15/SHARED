"""Agent registration and lifecycle DTOs."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from agentforge_shared.enums.agent import AgentCapability, AgentStatus, AgentType
from agentforge_shared.enums.providers import LLMProvider
from agentforge_shared.schemas.base import ApiModel
from agentforge_shared.utils.datetime_helpers import utc_now


class AgentRegistration(ApiModel):
    """Payload used by agent runtimes to register themselves."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    type: AgentType = AgentType.CUSTOM
    provider: LLMProvider | str | None = Field(default=None)
    model: str | None = Field(default=None)
    capabilities: list[AgentCapability] = Field(default_factory=list)
    endpoint: str | None = Field(default=None, description="Runtime callback endpoint.")
    version: str | None = Field(default=None, description="Agent version string.")
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "research-agent",
                    "type": "task",
                    "provider": "openai",
                    "model": "gpt-4o-mini",
                    "capabilities": ["call_llm", "use_memory", "retrieve"],
                }
            ]
        }
    }


class AgentHeartbeat(ApiModel):
    """Heartbeat sent by a running agent instance."""

    agent_id: str
    status: AgentStatus = AgentStatus.ACTIVE
    healthy: bool = True
    latency_ms: int | None = Field(default=None, ge=0)
    metrics: dict[str, Any] = Field(default_factory=dict)
    sent_at: datetime = Field(default_factory=utc_now)


class AgentHealthCheck(ApiModel):
    """Result of a health probe against an agent runtime."""

    agent_id: str
    ok: bool
    message: str | None = None
    version: str | None = None
    checks: dict[str, Any] = Field(default_factory=dict)


__all__ = ["AgentRegistration", "AgentHeartbeat", "AgentHealthCheck"]
