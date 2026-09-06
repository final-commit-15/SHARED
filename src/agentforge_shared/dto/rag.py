"""RAG query/response DTOs."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from agentforge_shared.schemas.base import ApiModel

from ..dto.usage import TokenUsage


class RAGContext(ApiModel):
    """A retrieved context chunk returned to the caller."""

    id: str = Field(..., description="Chunk/document identifier.")
    text: str = Field(..., max_length=80_000)
    source: str | None = Field(default=None, description="Origin document/source name.")
    score: float = Field(default=0.0, ge=0.0, le=1.0, description="Similarity score.")
    metadata: dict[str, Any] = Field(default_factory=dict)


class RAGQueryRequest(ApiModel):
    """Request to run retrieval-augmented generation."""

    query: str = Field(..., min_length=1, max_length=8_000, description="User question.")
    collection: str | None = Field(default=None, description="Vector collection filter.")
    filters: dict[str, Any] = Field(default_factory=dict, description="Metadata filter predicates.")
    top_k: int = Field(default=4, ge=1, le=50, description="Number of contexts to retrieve.")
    with_generate: bool = Field(default=True, description="Generate an answer from contexts when true.")
    model: str | None = Field(default=None)
    threshold: float = Field(default=0.0, ge=0.0, le=1.0, description="Minimum similarity to include.")
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"query": "What are the payment terms?", "top_k": 4, "collection": "contracts"}
            ]
        }
    }


class RAGQueryResponse(ApiModel):
    """Response with retrieved contexts and an optional generated answer."""

    query: str
    contexts: list[RAGContext] = Field(default_factory=list)
    answer: str | None = Field(default=None, description="Generated answer when requested.")
    citations: list[str] = Field(default_factory=list, description="Source ids cited by the answer.")
    usage: TokenUsage = Field(default_factory=TokenUsage)
    latency_ms: int | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "What are the payment terms?",
                    "contexts": [{"id": "c1", "text": "Payment within 30 days...", "score": 0.92}],
                    "answer": "Payments are due within 30 days.",
                }
            ]
        }
    }


class RAGIndexRequest(ApiModel):
    """Request to index text into a retrieval collection."""

    collection: str = Field(..., min_length=1, max_length=64)
    documents: list[dict[str, Any]] = Field(..., description="Documents with ``text`` + metadata.")
    chunk_size: int = Field(default=512, ge=32, le=4096)
    chunk_overlap: int = Field(default=50, ge=0, le=1000)
    metadata: dict[str, Any] = Field(default_factory=dict)


__all__ = ["RAGContext", "RAGQueryRequest", "RAGQueryResponse", "RAGIndexRequest"]
