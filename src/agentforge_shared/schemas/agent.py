"""Agent-related Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from agentforge_shared.enums.agent import AgentCapability, AgentStatus, AgentType
from agentforge_shared.utils.datetime_helpers import utc_now


class AgentConfig(BaseModel):
    """Runtime configuration for an agent instance."""

    model: str = Field(..., min_length=1, description="AI model to use (e.g. ``gpt-4o-mini``).")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1, le=128_000)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    system_prompt: str | None = Field(default=None, max_length=8_000)
    additional_params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("model")
    @classmethod
    def _model_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("model must not be blank")
        return value


class Agent(BaseModel):
    """Full agent representation returned by the platform."""

    id: str = Field(..., description="Unique agent identifier.")
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    type: AgentType = AgentType.CUSTOM
    capabilities: list[AgentCapability] = Field(default_factory=list)
    configuration: AgentConfig = Field(default_factory=AgentConfig)
    status: AgentStatus = AgentStatus.DRAFT
    owner_id: str | None = Field(default=None)
    tags: list[str] = Field(default_factory=list, max_length=20)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    def __str__(self) -> str:
        return f"Agent(id={self.id}, name={self.name}, type={self.type})"


__all__ = ["Agent", "AgentConfig"]
