"""Execution lifecycle events."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from agentforge_shared.enums.events import EventSource, EventType
from agentforge_shared.enums.execution import (
    CancellationReason,
    ExecutionStatus,
    ExecutionTrigger,
)

from .base import BaseEvent


class ExecutionStartedEvent(BaseEvent):
    """Published when an agent execution begins."""

    event_type: EventType = EventType.EXECUTION_STARTED
    source: EventSource = EventSource.AGENTS

    execution_id: str = Field(..., description="Execution identifier.")
    agent_id: str
    workflow_run_id: str | None = None
    parent_execution_id: str | None = None
    trigger: ExecutionTrigger = ExecutionTrigger.MANUAL
    input: dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int | None = Field(default=None, ge=1)


class ExecutionCompletedEvent(BaseEvent):
    """Published when an execution finishes successfully."""

    event_type: EventType = EventType.EXECUTION_COMPLETED
    source: EventSource = EventSource.AGENTS

    execution_id: str
    agent_id: str
    status: ExecutionStatus = ExecutionStatus.COMPLETED
    output: dict[str, Any] = Field(default_factory=dict)
    duration_seconds: float = Field(default=0.0, ge=0)
    total_tokens: int = Field(default=0, ge=0)
    provider: str | None = None
    model: str | None = None


class ExecutionFailedEvent(BaseEvent):
    """Published when an execution fails."""

    event_type: EventType = EventType.EXECUTION_FAILED
    source: EventSource = EventSource.AGENTS

    execution_id: str
    agent_id: str
    error_code: str | None = None
    error_message: str | None = None
    retryable: bool = False
    attempts: int = Field(default=1, ge=1)
    duration_seconds: float = Field(default=0.0, ge=0)


class ExecutionCancelledEvent(BaseEvent):
    """Published when an execution is cancelled."""

    event_type: EventType = EventType.EXECUTION_CANCELLED
    source: EventSource = EventSource.AGENTS

    execution_id: str
    agent_id: str
    reason: CancellationReason = CancellationReason.USER
    requested_by: str | None = None
    steps_completed: int = Field(default=0, ge=0)


class ExecutionProgressEvent(BaseEvent):
    """Published periodically with execution progress."""

    event_type: EventType = EventType.EXECUTION_PROGRESS
    source: EventSource = EventSource.AGENTS

    execution_id: str
    agent_id: str
    percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    message: str | None = None
    step: str | None = None


__all__ = [
    "ExecutionStartedEvent",
    "ExecutionCompletedEvent",
    "ExecutionFailedEvent",
    "ExecutionCancelledEvent",
    "ExecutionProgressEvent",
]
