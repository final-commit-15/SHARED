"""JWT and token configuration."""

from __future__ import annotations

from pydantic import Field, model_validator

from .settings import BaseAgentForgeSettings, settings_config


class JWTSettings(BaseAgentForgeSettings):
    """Settings used by the :mod:`agentforge_shared.security` package."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="JWT_")

    secret_key: str = Field(default="change-me", description="HMAC secret (min 32 chars in production).")
    algorithm: str = Field(default="HS256", description="JOSE signing algorithm (HS256 supported).")
    access_token_ttl_minutes: int = Field(default=30, ge=1)
    refresh_token_ttl_days: int = Field(default=7, ge=1)
    issuer: str = Field(default="agentforge")
    audience: str = Field(default="agentforge-api")
    leeway_seconds: int = Field(default=10, ge=0)
    require_exp: bool = Field(default=True)
    max_clock_skew_seconds: int = Field(default=30, ge=0)
    allowed_algorithms: str = Field(
        default="HS256", description="Comma-separated list of accepted signing algorithms."
    )

    @model_validator(mode="after")
    def _validate_secret(self) -> JWTSettings:
        if self.secret_key in {"change-me", "changeme", "secret", ""}:
            raise ValueError(
                "JWT_SECRET_KEY must be set to a strong, unique value; refusing insecure defaults."
            )
        return self

    @property
    def algorithms(self) -> list[str]:
        """Return the accepted algorithms as a list."""
        return [a.strip() for a in self.allowed_algorithms.split(",") if a.strip()]
