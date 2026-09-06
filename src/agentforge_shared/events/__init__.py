"""Domain events for the AgentForge event bus."""

from .agent import (
    AgentCreatedEvent,
    AgentDeletedEvent,
    AgentPublishedEvent,
    AgentRegisteredEvent,
    AgentUpdatedEvent,
)
from .base import BaseEvent
from .document import (
    DocumentDeletedEvent,
    DocumentIndexedEvent,
    DocumentIndexFailedEvent,
    DocumentUploadedEvent,
)
from .execution import (
    ExecutionCancelledEvent,
    ExecutionCompletedEvent,
    ExecutionFailedEvent,
    ExecutionProgressEvent,
    ExecutionStartedEvent,
)
from .notification import AuditEvent, NotificationFailedEvent, NotificationSentEvent
from .system import (
    ConfigChangedEvent,
    DeploymentEvent,
    FeatureFlagEvent,
    SystemShutdownEvent,
    SystemStartedEvent,
)
from .user import (
    UserCreatedEvent,
    UserDeletedEvent,
    UserLoggedInEvent,
    UserLoggedOutEvent,
    UserUpdatedEvent,
)
from .workflow import (
    WorkflowCreatedEvent,
    WorkflowPublishedEvent,
    WorkflowRunCompletedEvent,
    WorkflowRunFailedEvent,
    WorkflowRunStartedEvent,
    WorkflowUpdatedEvent,
)

__all__ = [
    "BaseEvent",
    # execution
    "ExecutionStartedEvent",
    "ExecutionCompletedEvent",
    "ExecutionFailedEvent",
    "ExecutionCancelledEvent",
    "ExecutionProgressEvent",
    # agents
    "AgentCreatedEvent",
    "AgentUpdatedEvent",
    "AgentRegisteredEvent",
    "AgentPublishedEvent",
    "AgentDeletedEvent",
    # workflows
    "WorkflowCreatedEvent",
    "WorkflowUpdatedEvent",
    "WorkflowPublishedEvent",
    "WorkflowRunStartedEvent",
    "WorkflowRunCompletedEvent",
    "WorkflowRunFailedEvent",
    # documents
    "DocumentUploadedEvent",
    "DocumentIndexedEvent",
    "DocumentDeletedEvent",
    "DocumentIndexFailedEvent",
    # users / auth
    "UserCreatedEvent",
    "UserUpdatedEvent",
    "UserDeletedEvent",
    "UserLoggedInEvent",
    "UserLoggedOutEvent",
    # notifications / audit
    "NotificationSentEvent",
    "NotificationFailedEvent",
    "AuditEvent",
    # platform / ops
    "SystemStartedEvent",
    "SystemShutdownEvent",
    "DeploymentEvent",
    "ConfigChangedEvent",
    "FeatureFlagEvent",
]
