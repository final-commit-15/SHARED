"""Database connection settings."""

from __future__ import annotations

from pydantic import Field, field_validator

from .settings import BaseAgentForgeSettings, settings_config


class DatabaseSettings(BaseAgentForgeSettings):
    """Connection and pool tuning for the primary database."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="DB_")

    engine: str = Field(default="postgresql", description="Database engine: postgresql, mysql, sqlite...")
    driver: str = Field(default="postgresql+asyncpg", description="SQLAlchemy driver string.")
    host: str = Field(default="localhost")
    port: int = Field(default=5432, ge=1, le=65535)
    name: str = Field(default="agentforge")
    user: str = Field(default="agentforge")
    password: str = Field(default="", description="Database password (masked in logs).")
    pool_size: int = Field(default=10, ge=1, le=500)
    max_overflow: int = Field(default=20, ge=0, le=1000)
    pool_timeout: int = Field(default=30, ge=1)
    pool_recycle: int = Field(default=3600, ge=1)
    echo: bool = Field(default=False, description="Log all SQL statements (development only).")
    ssl_mode: str = Field(default="disable")
    connect_timeout: int = Field(default=10, ge=1)
    query_timeout: int = Field(default=30, ge=1)
    retry_attempts: int = Field(default=3, ge=0, le=10)
    retry_backoff_seconds: float = Field(default=1.0, ge=0.1, le=60)

    @field_validator("driver")
    @classmethod
    def _normalize_driver(cls, value: str) -> str:
        if value == "asyncpg" or value.startswith("postgres"):
            return "postgresql+asyncpg"
        return value

    @property
    def dsn(self) -> str:
        """Assemble a SQLAlchemy DSN from the parts."""
        return (
            f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )

    @property
    def dsn_safe(self) -> str:
        """Assemble a DSN with the password redacted (for logs)."""
        return (
            f"{self.driver}://{self.user}:***@{self.host}:{self.port}/{self.name}"
        )

    @property
    def is_sqlite(self) -> bool:
        """Return ``True`` for sqlite connections."""
        return "sqlite" in self.driver
