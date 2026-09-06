"""Unified search request/response DTOs."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from agentforge_shared.schemas.base import ApiModel


class SearchRequest(ApiModel):
    """Request to search documents, memory, or indexed content."""

    query: str = Field(..., min_length=1, max_length=2_000)
    scope: str = Field(default="documents", description="Search domain: documents | memory | knowledge | all")
    filters: dict[str, Any] = Field(default_factory=dict)
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    sort_field: str | None = Field(default=None)
    sort_desc: bool = Field(default=False)
    include_snippets: bool = Field(default=True)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"query": "onboarding checklist", "scope": "documents", "limit": 10}
            ]
        }
    }


class SearchHit(ApiModel):
    """A single search result."""

    id: str = Field(..., description="Document/record identifier.")
    title: str | None = None
    snippet: str | None = Field(default=None, description="Highlighted excerpt.")
    score: float | None = Field(default=None, ge=0.0, le=1.0)
    source: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SearchResponse(ApiModel):
    """Paginated search results."""

    query: str
    total: int = Field(default=0, ge=0)
    hits: list[SearchHit] = Field(default_factory=list)
    took_ms: int | None = None
    facets: dict[str, Any] = Field(default_factory=dict, description="Optional aggregate counts.")
    next_offset: int | None = Field(default=None, description="Offset for the next page, when present.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "onboarding",
                    "total": 2,
                    "hits": [{"id": "doc-1", "title": "Guide", "score": 0.9}],
                }
            ]
        }
    }


__all__ = ["SearchRequest", "SearchResponse", "SearchHit"]
