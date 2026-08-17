"""Agent-related Pydantic schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from ..enums.agent import AgentStatus, AgentType
from ..utils.datetime_helpers import utc_now   # <-- new import


class AgentConfig(BaseModel):
    """Configuration for an agent instance."""
    model: str = Field(..., description="AI model to use")
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(1024, gt=0)
    additional_params: Dict[str, Any] = Field(default_factory=dict)


class Agent(BaseModel):
    """Full agent representation."""
    id: str = Field(..., description="Unique agent identifier")
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: AgentType
    configuration: AgentConfig
    status: AgentStatus = AgentStatus.DRAFT
    created_at: datetime = Field(default_factory=utc_now)   # <-- changed
    updated_at: datetime = Field(default_factory=utc_now)   # <-- changed

    def __str__(self) -> str:
        return f"Agent(id={self.id}, name={self.name})"