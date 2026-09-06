"""Workflow, task, tool, and document enumerations."""

from __future__ import annotations

from .base import StringEnum


class WorkflowStatus(StringEnum):
    """Lifecycle of a workflow definition."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ACTIVE = "active"
    DISABLED = "disabled"
    ARCHIVED = "archived"
    ERROR = "error"


class WorkflowRunStatus(StringEnum):
    """Status of a specific workflow run."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"


class TaskPriority(StringEnum):
    """Priority assigned to tasks."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BACKLOG = "backlog"


class TaskStatus(StringEnum):
    """Lifecycle of a task inside a workflow or queue."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"
    RETRYING = "retrying"


class ToolType(StringEnum):
    """Categories of tools an agent can invoke."""

    HTTP = "http"
    FUNCTION = "function"
    FILE = "file"
    DATABASE = "database"
    WEBHOOK = "webhook"
    CALENDAR = "calendar"
    MESSAGING = "messaging"
    SEARCH = "search"
    CODE_EXECUTION = "code_execution"
    CUSTOM = "custom"


class StepType(StringEnum):
    """Workflow step kinds."""

    TASK = "task"
    AGENT = "agent"
    TOOL = "tool"
    CONDITION = "condition"
    LOOP = "loop"
    PARALLEL = "parallel"
    SWITCH = "switch"
    HUMAN_APPROVAL = "human_approval"
    TRANSFORM = "transform"
    DELAY = "delay"
    NOTIFY = "notify"
    END = "end"


class StepTrigger(StringEnum):
    """What starts a workflow."""

    MANUAL = "manual"
    SCHEDULE = "schedule"
    EVENT = "event"
    WEBHOOK = "webhook"
    API = "api"
    CHILD = "child"


class DocumentType(StringEnum):
    """Document kinds supported by the ingestion pipeline."""

    TEXT = "text"
    MARKDOWN = "markdown"
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    CODE = "code"
    CSV = "csv"
    JSON = "json"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    UNKNOWN = "unknown"


class DocumentStatus(StringEnum):
    """Ingestion / indexing state of a document."""

    UPLOADED = "uploaded"
    PARSING = "parsing"
    CHUNKING = "chunking"
    EMBEDDING = "embedding"
    INDEXED = "indexed"
    FAILED = "failed"
    DELETED = "deleted"
    REINDEXING = "reindexing"


class ChunkingStrategy(StringEnum):
    """How documents are split into chunks."""

    FIXED = "fixed"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    RECURSIVE = "recursive"
    SEMANTIC = "semantic"
    TOKEN_BASED = "token_based"
    LAYOUT_AWARE = "layout_aware"


class WorkflowEventReason(StringEnum):
    """Why a workflow stopped."""

    COMPLETED = "completed"
    TIMEOUT = "timeout"
    ERROR = "error"
    CANCELLED = "cancelled"
    MAX_STEPS = "max_steps"
    HUMAN = "human"
