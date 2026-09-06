"""Token usage and cost estimation DTOs."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from agentforge_shared.schemas.base import ApiModel


class TokenUsage(ApiModel):
    """Token counts for an LLM call."""

    prompt_tokens: int = Field(default=0, ge=0)
    completion_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)

    @property
    def delta(self) -> int:
        """Alias for ``completion_tokens`` used by some providers."""
        return self.completion_tokens

    def add(self, other: TokenUsage) -> TokenUsage:
        """Combine this usage with another, returning a new instance."""
        return TokenUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
        )

    model_config = {
        "json_schema_extra": {
            "examples": [{"prompt_tokens": 120, "completion_tokens": 45, "total_tokens": 165}]
        }
    }


class CostEstimate(ApiModel):
    """Estimated financial cost of a call."""

    currency: str = Field(default="USD")
    input_cost: float = Field(default=0.0, ge=0.0)
    output_cost: float = Field(default=0.0, ge=0.0)
    total_cost: float = Field(default=0.0, ge=0.0)
    model: str | None = Field(default=None, description="Model the estimate applies to.")
    rate_reference: str | None = Field(default=None, description="Pricing source reference.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "currency": "USD",
                    "input_cost": 0.00018,
                    "output_cost": 0.00027,
                    "total_cost": 0.00045,
                    "model": "gpt-4o-mini",
                }
            ]
        }
    }


class UsageReport(ApiModel):
    """Aggregated usage for a scope over a period."""

    scope: str = Field(..., description="user | organization | project")
    scope_id: str | None = None
    period: str = Field(default="day", description="hour | day | month")
    total_prompt_tokens: int = Field(default=0, ge=0)
    total_completion_tokens: int = Field(default=0, ge=0)
    total_cost: float = Field(default=0.0, ge=0.0)
    request_count: int = Field(default=0, ge=0)
    breakdown: dict[str, Any] = Field(default_factory=dict)


__all__ = ["TokenUsage", "CostEstimate", "UsageReport"]
