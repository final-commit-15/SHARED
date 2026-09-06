"""Execution engine settings."""

from __future__ import annotations

from pydantic import Field

from agentforge_shared.constants.limits import (
    EXECUTION_CONCURRENCY_LIMIT,
    EXECUTION_DEFAULT_TIMEOUT_SECONDS,
    EXECUTION_QUEUE_CAPACITY,
)

from .settings import BaseAgentForgeSettings, settings_config


class ExecutionSettings(BaseAgentForgeSettings):
    """Tuning for the execution engine (agents & workflows)."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="EXECUTION_")

    default_timeout_seconds: int = Field(default=EXECUTION_DEFAULT_TIMEOUT_SECONDS, ge=1)
    max_timeout_seconds: int = Field(default=3_600, ge=1)
    max_retries: int = Field(default=3, ge=0, le=10)
    retry_backoff_base: float = Field(default=1.0, ge=0.1)
    retry_backoff_max: float = Field(default=60.0, ge=1.0)
    retry_jitter: float = Field(default=0.1, ge=0.0, le=1.0)
    concurrency_limit: int = Field(default=EXECUTION_CONCURRENCY_LIMIT, ge=1)
    queue_capacity: int = Field(default=EXECUTION_QUEUE_CAPACITY, ge=1)
    max_payload_bytes: int = Field(default=1_048_576, ge=1)
    store_intermediate_results: bool = Field(default=True)
    persist_events: bool = Field(default=True)
    default_mode: str = Field(default="async", description="sync | async | streaming | batch")
    worker_refresh_seconds: int = Field(default=10, ge=1)
