"""Long-term memory read/write DTOs."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import Field

from agentforge_shared.schemas.base import ApiModel
from agentforge_shared.utils.datetime_helpers import utc_now


class MemoryItem(ApiModel):
    """A single stored memory record."""

    id: str | None = Field(default=None, description="Optional memory id.")
    key: str = Field(..., min_length=1, max_length=256, description="Lookup key.")
    content: Any = Field(..., description="Stored value (any JSON value).")
    namespace: str | None = Field(default=None)
    ttl: int | None = Field(default=None, ge=1, description="Seconds until expiry.")
    created_at: datetime = Field(default_factory=utc_now)


class MemoryRequest(ApiModel):
    """Request to store or query memory."""

    key: str = Field(..., min_length=1, max_length=256)
    value: Any = Field(default=None, description="Value to write (write mode).")
    action: Literal["get", "set", "delete", "exists"] = Field(default="get")
    namespace: str | None = Field(default=None)
    ttl: int | None = Field(default=None, ge=1)
    agent_id: str | None = Field(default=None)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "action": "set",
                    "key": "user:preferences:tone",
                    "value": {"tone": "concise"},
                    "namespace": "profiles",
                }
            ]
        }
    }


class MemoryResponse(ApiModel):
    """Result of a memory operation."""

    action: str
    key: str
    found: bool = False
    value: Any = Field(default=None, description="Retrieved value when applicable.")
    namespace: str | None = None
    ttl_remaining: int | None = Field(default=None, description="Seconds until expiry (get).")
    latency_ms: int | None = None
    message: str | None = None


class MemoryQueryRequest(ApiModel):
    """Request to query memory by key, prefix, or similarity."""

    agent_id: str | None = None
    keys: list[str] | None = Field(default=None)
    prefix: str | None = Field(default=None, description="Match keys starting with this prefix.")
    namespace: str | None = None
    limit: int = Field(default=50, ge=1, le=500)
    include_values: bool = Field(default=True)


class MemorySearchRequest(ApiModel):
    """Request to semantically search memory."""

    query: str = Field(..., min_length=1, max_length=2_000)
    agent_id: str | None = None
    namespace: str | None = None
    top_k: int = Field(default=5, ge=1, le=100)
    threshold: float = Field(default=0.0, ge=0.0, le=1.0)


class MemorySearchResult(ApiModel):
    """A similarity-matched memory entry."""

    key: str
    content: Any
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    namespace: str | None = None


__all__ = [
    "MemoryItem",
    "MemoryRequest",
    "MemoryResponse",
    "MemoryQueryRequest",
    "MemorySearchRequest",
    "MemorySearchResult",
]
