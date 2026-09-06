"""Embedding generation DTOs."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, model_validator

from agentforge_shared.enums.providers import EmbeddingProvider
from agentforge_shared.schemas.base import ApiModel


class EmbeddingRequest(ApiModel):
    """Request to embed one or more text inputs."""

    inputs: list[str] | str = Field(..., description="Text or list of texts to embed.")
    model: str | None = Field(default=None, description="Embedding model override.")
    provider: EmbeddingProvider | str | None = Field(default=None)
    encoding_format: Literal["float", "base64"] = Field(default="float")
    dimensions: int | None = Field(default=None, ge=1, le=4096)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _coerce_inputs(self) -> EmbeddingRequest:
        if isinstance(self.inputs, str):
            self.inputs = [self.inputs]
        if not self.inputs:
            raise ValueError("at least one input is required")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"inputs": ["The quick brown fox", "jumps over the lazy dog"]}
            ]
        }
    }


class EmbeddingResponse(ApiModel):
    """Response containing generated embedding vectors."""

    embeddings: list[list[float]] | list[str] = Field(
        ..., description="Float vectors or base64-encoded strings."
    )
    model: str | None = None
    dimensions: int
    total_tokens: int = Field(default=0, ge=0)
    latency_ms: int | None = None
    encoding_format: Literal["float", "base64"] = "float"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "embeddings": [[0.001, -0.02, 0.15, -0.004]],
                    "model": "text-embedding-3-small",
                    "dimensions": 1536,
                    "total_tokens": 6,
                }
            ]
        }
    }


__all__ = ["EmbeddingRequest", "EmbeddingResponse"]
