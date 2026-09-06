"""Execution-related Pydantic schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from agentforge_shared.enums.execution import (
    ExecutionMode,
    ExecutionStatus,
    ExecutionTrigger,
)
from agentforge_shared.utils.datetime_helpers import utc_now


class Execution(BaseModel):
    """Represents a single execution of an agent or workflow."""

    id: str = Field(..., description="Execution identifier.")
    agent_id: str = Field(..., description="Agent being executed.")
    input: dict[str, Any] = Field(default_factory=dict, description="Input data for the agent.")
    status: ExecutionStatus = ExecutionStatus.PENDING
    trigger: ExecutionTrigger = ExecutionTrigger.MANUAL
    mode: ExecutionMode = ExecutionMode.ASYNC
    attempt: int = Field(default=1, ge=1, description="Current retry attempt (1-based).")
    max_attempts: int = Field(default=1, ge=1)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    trace_id: str | None = Field(default=None, description="W3C trace id for correlation.")
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def duration_seconds(self) -> float | None:
        """Return the elapsed wall-clock duration when started/completed known."""
        if self.started_at is None:
            return None
        end = self.completed_at or utc_now()
        return max(0.0, (end - self.started_at).total_seconds())


class ExecutionResult(BaseModel):
    """Result returned to an execution caller."""

    execution_id: str
    status: ExecutionStatus
    output: dict[str, Any] | None = None
    error: str | None = None
    duration_seconds: float | None = None
    usage: dict[str, Any] | None = Field(default=None, description="Token/cost usage when reported.")


__all__ = ["Execution", "ExecutionResult"]
