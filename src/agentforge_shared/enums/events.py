"""Event type enumerations for the platform event bus."""

from __future__ import annotations

from .base import StringEnum


class EventType(StringEnum):
    """Every event contract published across AgentForge services."""

    # Execution lifecycle
    EXECUTION_STARTED = "execution.started"
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"
    EXECUTION_CANCELLED = "execution.cancelled"
    EXECUTION_PROGRESS = "execution.progress"

    # Agents
    AGENT_CREATED = "agent.created"
    AGENT_UPDATED = "agent.updated"
    AGENT_REGISTERED = "agent.registered"
    AGENT_PUBLISHED = "agent.published"
    AGENT_DELETED = "agent.deleted"

    # Workflows
    WORKFLOW_CREATED = "workflow.created"
    WORKFLOW_UPDATED = "workflow.updated"
    WORKFLOW_PUBLISHED = "workflow.published"
    WORKFLOW_RUN_STARTED = "workflow.run.started"
    WORKFLOW_RUN_COMPLETED = "workflow.run.completed"
    WORKFLOW_RUN_FAILED = "workflow.run.failed"

    # Documents / indexing
    DOCUMENT_UPLOADED = "document.uploaded"
    DOCUMENT_INDEXED = "document.indexed"
    DOCUMENT_DELETED = "document.deleted"
    DOCUMENT_INDEX_FAILED = "document.index.failed"

    # Memory
    MEMORY_WRITTEN = "memory.written"
    MEMORY_DELETED = "memory.deleted"

    # Users / auth
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    USER_LOGGED_IN = "user.logged_in"
    USER_LOGGED_OUT = "user.logged_out"

    # Notifications
    NOTIFICATION_SENT = "notification.sent"
    NOTIFICATION_FAILED = "notification.failed"

    # Audit
    AUDIT_EVENT = "audit.event"

    # Platform / ops
    SYSTEM_STARTED = "system.started"
    SYSTEM_SHUTDOWN = "system.shutdown"
    DEPLOYMENT_DEPLOYED = "deployment.deployed"
    CONFIG_CHANGED = "config.changed"
    FEATURE_FLAG_CHANGED = "feature_flag.changed"


class EventSource(StringEnum):
    """Service that emitted an event."""

    BACKEND = "agentforge-backend"
    AGENTS = "agentforge-agents"
    AI_SERVICES = "agentforge-ai-services"
    INTEGRATIONS = "agentforge-integrations"
    FRONTEND = "agentforge-frontend"
    SCHEDULER = "agentforge-scheduler"
    SYSTEM = "agentforge-system"
    UNKNOWN = "unknown"


class EventDeliveryStatus(StringEnum):
    """Delivery outcome of an event on the bus."""

    OK = "ok"
    RETRY = "retry"
    FAILED = "failed"
    DROPPED = "dropped"


# Maps event types to their event-source of origin (informational).
EVENT_SOURCE_MAP: dict[EventType, EventSource] = {
    EventType.EXECUTION_STARTED: EventSource.AGENTS,
    EventType.EXECUTION_COMPLETED: EventSource.AGENTS,
    EventType.EXECUTION_FAILED: EventSource.AGENTS,
    EventType.EXECUTION_CANCELLED: EventSource.AGENTS,
    EventType.EXECUTION_PROGRESS: EventSource.AGENTS,
    EventType.AGENT_CREATED: EventSource.BACKEND,
    EventType.AGENT_UPDATED: EventSource.BACKEND,
    EventType.AGENT_REGISTERED: EventSource.AGENTS,
    EventType.AGENT_PUBLISHED: EventSource.BACKEND,
    EventType.AGENT_DELETED: EventSource.BACKEND,
    EventType.WORKFLOW_CREATED: EventSource.BACKEND,
    EventType.WORKFLOW_UPDATED: EventSource.BACKEND,
    EventType.WORKFLOW_PUBLISHED: EventSource.BACKEND,
    EventType.WORKFLOW_RUN_STARTED: EventSource.AGENTS,
    EventType.WORKFLOW_RUN_COMPLETED: EventSource.AGENTS,
    EventType.WORKFLOW_RUN_FAILED: EventSource.AGENTS,
    EventType.DOCUMENT_UPLOADED: EventSource.BACKEND,
    EventType.DOCUMENT_INDEXED: EventSource.AI_SERVICES,
    EventType.DOCUMENT_DELETED: EventSource.BACKEND,
    EventType.DOCUMENT_INDEX_FAILED: EventSource.AI_SERVICES,
    EventType.MEMORY_WRITTEN: EventSource.AGENTS,
    EventType.MEMORY_DELETED: EventSource.AGENTS,
    EventType.USER_CREATED: EventSource.BACKEND,
    EventType.USER_UPDATED: EventSource.BACKEND,
    EventType.USER_DELETED: EventSource.BACKEND,
    EventType.USER_LOGGED_IN: EventSource.BACKEND,
    EventType.USER_LOGGED_OUT: EventSource.BACKEND,
    EventType.NOTIFICATION_SENT: EventSource.BACKEND,
    EventType.NOTIFICATION_FAILED: EventSource.BACKEND,
    EventType.AUDIT_EVENT: EventSource.BACKEND,
    EventType.SYSTEM_STARTED: EventSource.SYSTEM,
    EventType.SYSTEM_SHUTDOWN: EventSource.SYSTEM,
    EventType.DEPLOYMENT_DEPLOYED: EventSource.SYSTEM,
    EventType.CONFIG_CHANGED: EventSource.SYSTEM,
    EventType.FEATURE_FLAG_CHANGED: EventSource.SYSTEM,
}
