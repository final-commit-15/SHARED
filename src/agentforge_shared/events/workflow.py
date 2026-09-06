"""Workflow lifecycle events."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from agentforge_shared.enums.events import EventSource, EventType
from agentforge_shared.enums.workflow import WorkflowRunStatus

from .base import BaseEvent


class WorkflowCreatedEvent(BaseEvent):
    """Published when a workflow definition is created."""

    event_type: EventType = EventType.WORKFLOW_CREATED
    source: EventSource = EventSource.BACKEND

    workflow_id: str
    name: str
    version: str = "1"
    step_count: int = Field(default=0, ge=0)
    created_by: str | None = None


class WorkflowUpdatedEvent(BaseEvent):
    """Published when a workflow definition is updated."""

    event_type: EventType = EventType.WORKFLOW_UPDATED
    source: EventSource = EventSource.BACKEND

    workflow_id: str
    version: str = "1"
    changed_fields: list[str] = Field(default_factory=list)
    updated_by: str | None = None


class WorkflowPublishedEvent(BaseEvent):
    """Published when a workflow is published."""

    event_type: EventType = EventType.WORKFLOW_PUBLISHED
    source: EventSource = EventSource.BACKEND

    workflow_id: str
    version: str
    published_by: str | None = None


class WorkflowRunStartedEvent(BaseEvent):
    """Published when a workflow run begins."""

    event_type: EventType = EventType.WORKFLOW_RUN_STARTED
    source: EventSource = EventSource.AGENTS

    run_id: str
    workflow_id: str
    version: str | None = None
    status: WorkflowRunStatus = WorkflowRunStatus.RUNNING
    inputs: dict[str, Any] = Field(default_factory=dict)


class WorkflowRunCompletedEvent(BaseEvent):
    """Published when a workflow run completes."""

    event_type: EventType = EventType.WORKFLOW_RUN_COMPLETED
    source: EventSource = EventSource.AGENTS

    run_id: str
    workflow_id: str
    status: WorkflowRunStatus = WorkflowRunStatus.COMPLETED
    outputs: dict[str, Any] = Field(default_factory=dict)
    steps_completed: int = Field(default=0, ge=0)
    duration_seconds: float = Field(default=0.0, ge=0)


class WorkflowRunFailedEvent(BaseEvent):
    """Published when a workflow run fails."""

    event_type: EventType = EventType.WORKFLOW_RUN_FAILED
    source: EventSource = EventSource.AGENTS

    run_id: str
    workflow_id: str
    status: WorkflowRunStatus = WorkflowRunStatus.FAILED
    failed_step_id: str | None = None
    error_code: str | None = None
    error_message: str | None = None
    duration_seconds: float = Field(default=0.0, ge=0)


__all__ = [
    "WorkflowCreatedEvent",
    "WorkflowUpdatedEvent",
    "WorkflowPublishedEvent",
    "WorkflowRunStartedEvent",
    "WorkflowRunCompletedEvent",
    "WorkflowRunFailedEvent",
]
