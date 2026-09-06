"""Streaming chunk and SSE DTOs."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from agentforge_shared.enums.execution import ExecutionStatus
from agentforge_shared.schemas.base import ApiModel

from ..dto.usage import TokenUsage


class StreamingChunk(ApiModel):
    """A single streaming delta produced during generation."""

    kind: Literal["text", "tool_call", "status", "usage", "error", "done"] = "text"
    index: int = Field(default=0, ge=0, description="Chunk sequence number.")
    delta: str | None = Field(default=None, description="Text delta when ``kind == 'text'``.")
    tool_call_id: str | None = None
    tool_name: str | None = None
    tool_input: dict[str, Any] | None = Field(default=None)
    status: ExecutionStatus | None = Field(default=None, description="Status transition event.")
    usage: TokenUsage | None = Field(default=None)
    error: str | None = Field(default=None)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "kind": "text",
                    "index": 0,
                    "delta": "The capital of France",
                }
            ]
        }
    }


class StreamEvent(ApiModel):
    """Encapsulated server-sent event (used by the SSE builder)."""

    event: str = Field(default="message", description="SSE event name.")
    data: Any = Field(default=None)
    id: str | None = Field(default=None)
    retry: int | None = Field(default=None)

    def encode(self) -> str:
        """Render the event as an SSE wire-format string."""
        from agentforge_shared.api.sse import encode_sse_event

        return encode_sse_event(event=self.event, data=self.data, event_id=self.id, retry=self.retry)


class StreamMetadata(ApiModel):
    """Metadata trailer emitted at the end of a stream."""

    execution_id: str | None = None
    finish_reason: str | None = None
    usage: TokenUsage | None = None
    latency_ms: int | None = None


__all__ = ["StreamingChunk", "StreamEvent", "StreamMetadata"]
