"""Execution request/response DTOs."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from agentforge_shared.enums.execution import ExecutionStatus
from agentforge_shared.schemas.base import ApiModel


class ExecutionRequest(ApiModel):
    """Request to start an agent/workflow execution."""

    agent_id: str = Field(..., description="Agent to execute.")
    input: dict[str, Any] = Field(default_factory=dict, description="Agent input payload.")
    mode: Literal["sync", "async", "streaming", "batch"] = "async"
    timeout_seconds: int | None = Field(default=None, ge=1, le=3600)
    idempotency_key: str | None = Field(default=None, max_length=200)
    metadata: dict[str, Any] = Field(default_factory=dict)
    callbacks: list[str] | None = Field(default=None, description="Webhook URLs notified on completion.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"agent_id": "agent_1", "input": {"task": "write summary"}, "mode": "async"}
            ]
        }
    }


class ExecutionResponse(ApiModel):
    """Response describing a submitted/executed job."""

    execution_id: str
    status: ExecutionStatus
    agent_id: str
    output: dict[str, Any] | None = Field(default=None)
    error: str | None = Field(default=None)
    duration_seconds: float | None = Field(default=None, ge=0)
    usage: dict[str, Any] | None = Field(default=None, description="Token/cost usage when reported.")
    stream_url: str | None = Field(default=None, description="SSE endpoint when streaming.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "execution_id": "exec_123",
                    "status": "completed",
                    "agent_id": "agent_1",
                    "output": {"summary": "..."},
                    "duration_seconds": 2.4,
                }
            ]
        }
    }


class ExecutionCancelRequest(ApiModel):
    """Request to cancel a running execution."""

    reason: str = Field(default="user request", max_length=200)


class ExecutionRetryRequest(ApiModel):
    """Request to re-run a failed execution."""

    execution_id: str
    input_override: dict[str, Any] | None = Field(default=None)


__all__ = [
    "ExecutionRequest",
    "ExecutionResponse",
    "ExecutionCancelRequest",
    "ExecutionRetryRequest",
]
