"""Execution-related Pydantic schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from ..enums.execution import ExecutionStatus


class Execution(BaseModel):
    """Represents a single execution of an agent."""
    id: str = Field(..., description="Execution identifier")
    agent_id: str = Field(..., description="Agent being executed")
    input: Dict[str, Any] = Field(..., description="Input data for the agent")
    status: ExecutionStatus = ExecutionStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExecutionResult(BaseModel):
    """Result of an execution, returned to the caller."""
    execution_id: str
    status: ExecutionStatus
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration_seconds: Optional[float] = None