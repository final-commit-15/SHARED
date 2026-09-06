"""Redis / cache backend settings."""

from __future__ import annotations

from pydantic import Field, field_validator

from .settings import BaseAgentForgeSettings, settings_config


class RedisSettings(BaseAgentForgeSettings):
    """Connection settings for Redis (cache, pub/sub, locks, rate limits)."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="REDIS_")

    url: str = Field(default="redis://localhost:6379/0", description="Full redis URL.")
    host: str = Field(default="localhost")
    port: int = Field(default=6379, ge=1, le=65535)
    db: int = Field(default=0, ge=0, le=15)
    password: str = Field(default="", description="Redis password (masked in logs).")
    username: str | None = Field(default=None)
    ssl: bool = Field(default=False)
    max_connections: int = Field(default=50, ge=1, le=1000)
    socket_timeout: int = Field(default=5, ge=1)
    socket_connect_timeout: int = Field(default=5, ge=1)
    socket_keepalive: bool = Field(default=True)
    health_check_interval: int = Field(default=30, ge=1)
    decode_responses: bool = Field(default=False, description="Return bytes instead of str when false.")

    @field_validator("url", mode="before")
    @classmethod
    def _default_url(cls, value: object) -> object:
        return value if isinstance(value, str) and value else "redis://localhost:6379/0"
