"""Agent-related enumerations."""

from __future__ import annotations

from .base import StringEnum


class AgentStatus(StringEnum):
    """Possible states of an agent over its lifecycle."""

    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    ERROR = "error"
    DEPLOYING = "deploying"
    DEPRECATED = "deprecated"


class AgentType(StringEnum):
    """Supported agent types."""

    CHAT = "chat"
    TASK = "task"
    EMBEDDING = "embedding"
    WORKFLOW = "workflow"
    RAG = "rag"
    MULTI_AGENT = "multi_agent"
    CUSTOM = "custom"


class AgentCapability(StringEnum):
    """What an agent can do at runtime."""

    CHAT = "chat"
    PLAN = "plan"
    EXECUTE_TOOLS = "execute_tools"
    USE_MEMORY = "use_memory"
    RETRIEVE = "retrieve"  # RAG retrieval
    GENERATE_EMBEDDINGS = "generate_embeddings"
    CALL_LLM = "call_llm"
    CALL_WEBHOOK = "call_webhook"
    SCHEDULE = "schedule"
    STREAM = "stream"
    SUMMARIZE = "summarize"
    TRANSLATE = "translate"
    CODE_EXECUTION = "code_execution"
    WEB_BROWSING = "web_browsing"
    FILE_ACCESS = "file_access"
