"""Rate limiting configuration."""

from __future__ import annotations

from pydantic import Field, field_validator

from agentforge_shared.constants.roles import RATE_LIMIT_EXEMPT_ROLES

from .settings import BaseAgentForgeSettings, settings_config


class RateLimitRule(BaseAgentForgeSettings):
    """A single rate limit rule keyed by route/role."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="RATE_LIMIT_")

    name: str = Field(default="default", description="Rule name used as the Redis key suffix.")
    limit: int = Field(default=100, ge=1, le=100_000)
    window_seconds: int = Field(default=60, ge=1, le=86_400)
    burst: int = Field(default=200, ge=0)

    @field_validator("limit")
    @classmethod
    def _positive_limit(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Rate limit must be at least 1 request per window.")
        return value


class RateLimitSettings(BaseAgentForgeSettings):
    """Global rate limiting configuration."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="RATE_LIMIT_")

    enabled: bool = Field(default=True)
    default_limit: int = Field(default=100, ge=1)
    default_window_seconds: int = Field(default=60, ge=1)
    burst_limit: int = Field(default=200, ge=0)
    auth_limit: int = Field(default=1_000, ge=1)
    auth_window_seconds: int = Field(default=3_600, ge=1)
    exempt_roles: list[str] = Field(
        default_factory=lambda: list(RATE_LIMIT_EXEMPT_ROLES),
        description="Roles that are never rate limited.",
    )
    rules: list[RateLimitRule] = Field(default_factory=list)
    storage: str = Field(default="redis", description="redis | memory")
    key_prefix: str = Field(default="ratelimit")
    client_ip_header: str = Field(default="x-forwarded-for")

    @field_validator("exempt_roles", mode="before")
    @classmethod
    def _split_csv(cls, value: object) -> object:
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return value

    def find_rule(self, name: str) -> RateLimitRule | None:
        """Return the rule matching ``name``, if any."""
        for rule in self.rules:
            if rule.name == name:
                return rule
        return None
