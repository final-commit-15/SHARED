"""Execution-related enumerations."""

from enum import Enum


class ExecutionStatus(str, Enum):
    """Possible states of an execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"