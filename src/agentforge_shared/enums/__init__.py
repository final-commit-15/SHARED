"""Public enumerations for the AgentForge platform."""

from .agent import AgentCapability, AgentStatus, AgentType
from .base import StringEnum
from .events import EVENT_SOURCE_MAP, EventDeliveryStatus, EventSource, EventType
from .execution import (
    CancellationReason,
    ExecutionMode,
    ExecutionStatus,
    ExecutionTrigger,
)
from .integration import (
    IntegrationAuthType,
    IntegrationStatus,
    IntegrationType,
    WebhookEventStatus,
)
from .platform import (
    AuditAction,
    Environment,
    HealthStatus,
    IdempotencyStatus,
    LogLevel,
    NotificationChannel,
    NotificationStatus,
    NotificationType,
    PermissionScope,
    SenderType,
    SortOrder,
    SourceType,
    UserRole,
)
from .providers import (
    EmbeddingProvider,
    LLMProvider,
    MemoryProvider,
    ProviderType,
    SearchProvider,
    StorageProvider,
    VectorStoreType,
)
from .workflow import (
    ChunkingStrategy,
    DocumentStatus,
    DocumentType,
    StepTrigger,
    StepType,
    TaskPriority,
    TaskStatus,
    ToolType,
    WorkflowEventReason,
    WorkflowRunStatus,
    WorkflowStatus,
)

__all__ = [
    "StringEnum",
    # agents
    "AgentStatus",
    "AgentType",
    "AgentCapability",
    # execution
    "ExecutionStatus",
    "ExecutionTrigger",
    "ExecutionMode",
    "CancellationReason",
    # integrations
    "IntegrationType",
    "IntegrationStatus",
    "IntegrationAuthType",
    "WebhookEventStatus",
    # platform
    "Environment",
    "UserRole",
    "PermissionScope",
    "NotificationType",
    "NotificationChannel",
    "NotificationStatus",
    "HealthStatus",
    "LogLevel",
    "AuditAction",
    "SortOrder",
    "SourceType",
    "SenderType",
    "IdempotencyStatus",
    # providers
    "ProviderType",
    "LLMProvider",
    "MemoryProvider",
    "EmbeddingProvider",
    "VectorStoreType",
    "StorageProvider",
    "SearchProvider",
    # workflows / tasks / tools / documents
    "WorkflowStatus",
    "WorkflowRunStatus",
    "WorkflowEventReason",
    "TaskPriority",
    "TaskStatus",
    "ToolType",
    "StepType",
    "StepTrigger",
    "DocumentType",
    "DocumentStatus",
    "ChunkingStrategy",
    # events
    "EventType",
    "EventSource",
    "EventDeliveryStatus",
    "EVENT_SOURCE_MAP",
]
