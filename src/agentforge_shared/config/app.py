"""Application-level settings shared by every service."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from agentforge_shared.enums.platform import Environment

from .settings import BaseAgentForgeSettings, settings_config


class CorsSettings(BaseModel):
    """CORS policies exposed to the API layer."""

    allow_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        description="Origins allowed to call the API.",
    )
    allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    allow_headers: list[str] = Field(default_factory=lambda: ["*"])
    allow_credentials: bool = True
    expose_headers: list[str] = Field(default_factory=list)
    max_age: int = 600


class AppSettings(BaseAgentForgeSettings):
    """Top-level application configuration."""

    model_config = settings_config(
        BaseAgentForgeSettings.model_config, env_prefix="APP_"
    )

    name: str = Field(default="agentforge-platform", description="Service name used in logs and telemetry.")
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    debug: bool = Field(default=False, description="Enables debug mode and verbose error responses.")
    version: str = Field(default="0.1.0")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    timezone: str = Field(default="UTC")
    api_prefix: str = Field(default="/api")
    api_version: str = Field(default="v1")
    trusted_hosts: list[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1"])
    cors: CorsSettings = Field(default_factory=CorsSettings)
    allowed_origins: list[str] = Field(
        default_factory=list,
        description="Comma-separated CORS origins; merged with ``cors.allow_origins`` at load time.",
    )

    @field_validator("environment", mode="before")
    @classmethod
    def _coerce_environment(cls, value: object) -> Environment:
        if isinstance(value, Environment):
            return value
        return Environment.from_value(str(value))

    @field_validator("trusted_hosts", "allowed_origins", mode="before")
    @classmethod
    def _split_csv(cls, value: object) -> object:
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return value

    @property
    def is_production(self) -> bool:
        """Return ``True`` when running in a production environment."""
        return self.environment == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        """Return ``True`` when running in a local development environment."""
        return self.environment in {Environment.DEVELOPMENT, Environment.TESTING}

    @property
    def effective_allowed_origins(self) -> list[str]:
        """Merge the structured CORS origins with the flat list."""
        return list(dict.fromkeys([*self.cors.allow_origins, *self.allowed_origins]))
