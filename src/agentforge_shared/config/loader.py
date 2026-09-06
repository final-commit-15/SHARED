"""Settings bundle and cached loaders for AgentForge services.

Usage::

    settings = get_settings()
    redis_config = settings.redis
    jwt_config = settings.jwt

Individual groups can also be loaded independently::

    from agentforge_shared.config.loader import get_jwt_settings
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import Field

from agentforge_shared.exceptions import ConfigurationException

from .app import AppSettings
from .database import DatabaseSettings
from .execution import ExecutionSettings
from .jwt import JWTSettings
from .llm import LLMSettings
from .ratelimit import RateLimitSettings
from .redis import RedisSettings
from .settings import BaseAgentForgeSettings, settings_config
from .storage import StorageSettings
from .telemetry import PrometheusSettings, TelemetrySettings


class AgentForgeSettings(BaseAgentForgeSettings):
    """Aggregate configuration for an entire service."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, extra="ignore")

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    telemetry: TelemetrySettings = Field(default_factory=TelemetrySettings)
    prometheus: PrometheusSettings = Field(default_factory=PrometheusSettings)
    ratelimit: RateLimitSettings = Field(default_factory=RateLimitSettings)
    execution: ExecutionSettings = Field(default_factory=ExecutionSettings)

    def health_overview(self) -> dict[str, Any]:
        """Return a small, secret-free snapshot for health endpoints."""
        return {
            "app": self.app.name,
            "environment": self.app.environment.value,
            "version": self.app.version,
        }


@lru_cache(maxsize=1)
def get_settings() -> AgentForgeSettings:
    """Return the process-wide settings bundle (cached)."""
    return AgentForgeSettings()


@lru_cache(maxsize=1)
def get_app_settings() -> AppSettings:
    """Return cached application settings."""
    return AppSettings()


@lru_cache(maxsize=1)
def get_database_settings() -> DatabaseSettings:
    """Return cached database settings."""
    return DatabaseSettings()


@lru_cache(maxsize=1)
def get_redis_settings() -> RedisSettings:
    """Return cached redis settings."""
    return RedisSettings()


@lru_cache(maxsize=1)
def get_jwt_settings() -> JWTSettings:
    """Return cached JWT settings."""
    return JWTSettings()


@lru_cache(maxsize=1)
def get_llm_settings() -> LLMSettings:
    """Return cached LLM settings."""
    return LLMSettings()


@lru_cache(maxsize=1)
def get_storage_settings() -> StorageSettings:
    """Return cached storage settings."""
    return StorageSettings()


@lru_cache(maxsize=1)
def get_telemetry_settings() -> TelemetrySettings:
    """Return cached telemetry settings."""
    return TelemetrySettings()


@lru_cache(maxsize=1)
def get_prometheus_settings() -> PrometheusSettings:
    """Return cached prometheus settings."""
    return PrometheusSettings()


@lru_cache(maxsize=1)
def get_rate_limit_settings() -> RateLimitSettings:
    """Return cached rate limit settings."""
    return RateLimitSettings()


@lru_cache(maxsize=1)
def get_execution_settings() -> ExecutionSettings:
    """Return cached execution settings."""
    return ExecutionSettings()


def refresh_settings() -> None:
    """Clear every cached settings loader (useful in tests)."""
    for fn in (
        get_settings,
        get_app_settings,
        get_database_settings,
        get_redis_settings,
        get_jwt_settings,
        get_llm_settings,
        get_storage_settings,
        get_telemetry_settings,
        get_prometheus_settings,
        get_rate_limit_settings,
        get_execution_settings,
    ):
        fn.cache_clear()


def build_settings(**overrides: Any) -> AgentForgeSettings:
    """Construct a settings bundle with explicit overrides applied.

    Raises:
        ConfigurationException: when any settings group fails to validate.
    """
    try:
        return AgentForgeSettings(**overrides)
    except Exception as exc:  # noqa: BLE001 - surface any settings error
        raise ConfigurationException(
            message=f"Invalid service configuration: {exc}",
            cause=exc,
        ) from exc
