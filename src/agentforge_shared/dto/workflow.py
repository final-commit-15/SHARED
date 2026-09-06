"""Workflow definition and run DTOs."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from agentforge_shared.enums.workflow import StepType, WorkflowRunStatus, WorkflowStatus
from agentforge_shared.schemas.base import ApiModel
from agentforge_shared.utils.datetime_helpers import utc_now


class WorkflowStep(ApiModel):
    """A single step inside a workflow definition."""

    id: str = Field(..., description="Step identifier (unique within workflow).")
    type: StepType = StepType.TASK
    name: str = Field(..., min_length=1, max_length=100)
    config: dict[str, Any] = Field(default_factory=dict)
    next: list[str] = Field(default_factory=list, description="Transition targets.")
    timeout_seconds: int | None = Field(default=None, ge=1)
    retries: int = Field(default=0, ge=0, le=10)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "s1",
                    "type": "task",
                    "name": "Summarize",
                    "config": {"agent": "summarizer"},
                    "next": ["s2"],
                }
            ]
        }
    }


class WorkflowRequest(ApiModel):
    """Request to create or update a workflow definition."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    steps: list[WorkflowStep] = Field(..., min_length=1, max_length=100)
    version: str | None = Field(default=None)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "research-pipeline",
                    "steps": [{"id": "s1", "type": "task", "name": "Search"}],
                }
            ]
        }
    }


class WorkflowResponse(ApiModel):
    """A persisted workflow definition."""

    id: str
    name: str
    description: str | None = None
    status: WorkflowStatus = WorkflowStatus.DRAFT
    steps: list[WorkflowStep]
    version: str = "1"
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowRun(ApiModel):
    """A single execution of a workflow."""

    id: str = Field(..., description="Run identifier.")
    workflow_id: str
    status: WorkflowRunStatus = WorkflowRunStatus.PENDING
    inputs: dict[str, Any] = Field(default_factory=dict)
    outputs: dict[str, Any] = Field(default_factory=dict)
    current_step_id: str | None = None
    error: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None


class WorkflowRunRequest(ApiModel):
    """Request to trigger a workflow run."""

    workflow_id: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str | None = Field(default=None, max_length=200)
    mode: str = Field(default="async", description="sync | async | streaming")


__all__ = [
    "WorkflowStep",
    "WorkflowRequest",
    "WorkflowResponse",
    "WorkflowRun",
    "WorkflowRunRequest",
]
