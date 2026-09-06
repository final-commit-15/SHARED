"""Object / file storage settings."""

from __future__ import annotations

from pydantic import Field, field_validator

from agentforge_shared.enums.providers import StorageProvider

from .settings import BaseAgentForgeSettings, settings_config


class StorageSettings(BaseAgentForgeSettings):
    """Settings for the platform's object storage backend."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="STORAGE_")

    provider: StorageProvider = Field(default=StorageProvider.S3)
    bucket: str = Field(default="agentforge-storage")
    region: str = Field(default="us-east-1")
    access_key: str = Field(default="", description="Storage access key (masked in logs).")
    secret_key: str = Field(default="", description="Storage secret key (masked in logs).")
    endpoint_url: str | None = Field(default=None)
    force_path_style: bool = Field(default=True)
    local_dir: str = Field(default="./storage", description="Local filesystem root for the local provider.")
    max_upload_size_mb: int = Field(default=100, ge=1, le=10_240)
    sse_encryption: bool = Field(default=True)
    public_read: bool = Field(default=False)
    timeout_seconds: int = Field(default=30, ge=1)
    retry_attempts: int = Field(default=3, ge=0, le=10)

    @field_validator("provider", mode="before")
    @classmethod
    def _coerce_provider(cls, value: object) -> StorageProvider:
        if isinstance(value, StorageProvider):
            return value
        return StorageProvider.coerce(value) or StorageProvider.S3

    @property
    def is_local(self) -> bool:
        """Return ``True`` when using the local filesystem backend."""
        return self.provider == StorageProvider.LOCAL
