"""Public schemas for the AgentForge platform.

Domain entities (agents, executions, users, integrations) live in their
dedicated modules; the shared envelope and pagination models are exported here.
"""

from .agent import Agent, AgentConfig
from .base import (
    ApiModel,
    AuditMixin,
    MetadataSchema,
    PageInfo,
    ResourceSchema,
    TimestampMixin,
    TypedResource,
    UUIDMixin,
    ValidationErrorSchema,
    ValidationIssue,
)
from .common import (
    APIResponse,
    ErrorResponse,
    HealthResponse,
    MessageResponse,
    PaginatedResponse,
    Pagination,
    SuccessResponse,
)
from .execution import Execution, ExecutionResult
from .health import ComponentHealth, ReadinessResponse
from .integration import Integration
from .pagination import (
    CursorMeta,
    CursorPaginationParams,
    FilterCondition,
    FilterRequest,
    OffsetPaginationParams,
    PageMeta,
    PaginatedData,
    SearchRequestParams,
    SortRequest,
    SortSchema,
    decode_cursor,
    encode_cursor,
)
from .user import User

__all__ = [
    # domain entities
    "Agent",
    "AgentConfig",
    "Execution",
    "ExecutionResult",
    "User",
    "Integration",
    # shared envelope
    "ApiModel",
    "TimestampMixin",
    "UUIDMixin",
    "AuditMixin",
    "ResourceSchema",
    "MetadataSchema",
    "PageInfo",
    "ValidationIssue",
    "ValidationErrorSchema",
    "TypedResource",
    "APIResponse",
    "PaginatedResponse",
    "SuccessResponse",
    "MessageResponse",
    "ErrorResponse",
    "Pagination",
    # health
    "HealthResponse",
    "ComponentHealth",
    "ReadinessResponse",
    # pagination
    "OffsetPaginationParams",
    "CursorPaginationParams",
    "PageMeta",
    "CursorMeta",
    "PaginatedData",
    "SortRequest",
    "SortSchema",
    "FilterCondition",
    "FilterRequest",
    "SearchRequestParams",
    "encode_cursor",
    "decode_cursor",
]
