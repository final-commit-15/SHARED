"""Agent-related enumerations."""

from enum import Enum


class AgentStatus(str, Enum):
    """Possible states of an agent."""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class AgentType(str, Enum):
    """Supported agent types."""
    CHAT = "chat"
    TASK = "task"
    EMBEDDING = "embedding"
    CUSTOM = "custom"