"""Execution-related enumerations."""

from __future__ import annotations

from .base import StringEnum


class ExecutionStatus(StringEnum):
    """Lifecycle states of a single execution."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"
    RETRYING = "retrying"
    PAUSED = "paused"

    @classmethod
    def is_terminal(cls, status: str) -> bool:
        """Return ``True`` for statuses that end an execution."""
        return status in {
            cls.COMPLETED.value,
            cls.FAILED.value,
            cls.CANCELLED.value,
            cls.TIMED_OUT.value,
        }

    @classmethod
    def is_active(cls, status: str) -> bool:
        """Return ``True`` for statuses that can still transition."""
        return status in {
            cls.PENDING.value,
            cls.QUEUED.value,
            cls.RUNNING.value,
            cls.RETRYING.value,
            cls.PAUSED.value,
        }


class ExecutionTrigger(StringEnum):
    """How an execution was started."""

    MANUAL = "manual"
    SCHEDULED = "scheduled"
    WEBHOOK = "webhook"
    EVENT = "event"
    API = "api"
    RETRY = "retry"
    TEST = "test"
    WORKFLOW = "workflow"


class ExecutionMode(StringEnum):
    """Execution concurrency / delivery mode."""

    SYNC = "sync"
    ASYNC = "async"
    STREAMING = "streaming"
    BATCH = "batch"


class CancellationReason(StringEnum):
    """Why an execution was cancelled."""

    USER = "user"
    TIMEOUT = "timeout"
    ERROR = "error"
    SHUTDOWN = "shutdown"
    RESOURCE_LIMIT = "resource_limit"
    POLICY = "policy"
    SUPERSEDED = "superseded"
