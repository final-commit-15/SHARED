"""Chat conversation DTOs."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from agentforge_shared.enums.platform import SenderType
from agentforge_shared.schemas.base import ApiModel

from ..dto.usage import TokenUsage

Role = Literal["system", "user", "assistant", "tool"]


class ChatMessage(ApiModel):
    """A single message in a chat conversation."""

    role: SenderType | Role = Field("user", description="Sender of the message.")
    content: str = Field(..., max_length=64_000, description="Message body.")
    name: str | None = Field(default=None, description="Optional participant name.")
    tool_call_id: str | None = Field(default=None, description="Tool invocation correlation.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"role": "user", "content": "Summarize this document for me."}
            ]
        }
    }


class ChatRequest(ApiModel):
    """Request payload for a chat completion."""

    conversation_id: str | None = Field(default=None, description="Ongoing conversation identifier.")
    messages: list[ChatMessage] = Field(..., min_length=1, max_length=200)
    agent_id: str | None = Field(default=None, description="Optional agent override.")
    model: str | None = Field(default=None, description="Optional model override.")
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(default=None, ge=1, le=128_000)
    stream: bool = Field(default=False, description="Request streaming when true.")
    tools: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [{"role": "user", "content": "Hello!"}],
                    "stream": False,
                    "temperature": 0.7,
                }
            ]
        }
    }


class ChatResponse(ApiModel):
    """Response payload for a chat completion."""

    conversation_id: str
    message: ChatMessage
    finish_reason: str | None = Field(default=None, description="Why generation stopped.")
    usage: TokenUsage = Field(default_factory=TokenUsage)
    latency_ms: int | None = Field(default=None)
    model: str | None = Field(default=None)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "conversation_id": "conv_123",
                    "message": {"role": "assistant", "content": "Hi there!"},
                    "usage": {"prompt_tokens": 12, "completion_tokens": 3},
                }
            ]
        }
    }


__all__ = ["ChatMessage", "ChatRequest", "ChatResponse", "Role"]
