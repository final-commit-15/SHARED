"""LLM, embedding and vector store settings."""

from __future__ import annotations

from pydantic import Field, field_validator

from agentforge_shared.constants.limits import LLM_MAX_TOKENS
from agentforge_shared.constants.models import (
    DEFAULT_EMBEDDING_MODEL_OPENAI,
    DEFAULT_MODEL_OPENAI,
    DEFAULT_VECTOR_DIMENSIONS,
    DEFAULT_VECTOR_STORE,
    LLM_DEFAULT_TEMPERATURE,
    LLM_MAX_TEMPERATURE,
)
from agentforge_shared.enums.providers import (
    EmbeddingProvider,
    LLMProvider,
    VectorStoreType,
)

from .settings import BaseAgentForgeSettings, settings_config


class EmbeddingSettings(BaseAgentForgeSettings):
    """Embedding generation settings."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="EMBEDDING_")

    provider: EmbeddingProvider = Field(default=EmbeddingProvider.OPENAI)
    model: str = Field(default=DEFAULT_EMBEDDING_MODEL_OPENAI)
    api_key: str = Field(default="")
    dimensions: int = Field(default=1_536, ge=1, le=4_096)
    batch_size: int = Field(default=64, ge=1, le=512)
    timeout_seconds: int = Field(default=60, ge=1)
    max_retries: int = Field(default=3, ge=0, le=10)


class VectorStoreSettings(BaseAgentForgeSettings):
    """Vector store / retrieval settings."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="VECTOR_")

    store: VectorStoreType = Field(
        default=VectorStoreType.coerce(DEFAULT_VECTOR_STORE) or VectorStoreType.QDRANT
    )
    host: str = Field(default="localhost")
    port: int = Field(default=6333, ge=1, le=65535)
    url: str | None = Field(default=None)
    api_key: str = Field(default="")
    collection_prefix: str = Field(default="agentforge")
    dimensions: int = Field(default=DEFAULT_VECTOR_DIMENSIONS, ge=1)
    distance: str = Field(default="cosine")
    shard_number: int = Field(default=1, ge=1)
    replication_factor: int = Field(default=1, ge=1)
    timeout_seconds: int = Field(default=30, ge=1)
    use_hnsw: bool = Field(default=True)


class LLMSettings(BaseAgentForgeSettings):
    """Aggregate settings for all AI backends (chat + embeddings + vectors)."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="LLM_")

    provider: LLMProvider = Field(default=LLMProvider.OPENAI)
    model: str = Field(default=DEFAULT_MODEL_OPENAI)
    api_key: str = Field(default="", description="Provider API key (masked in logs).")
    base_url: str | None = Field(default=None)
    timeout_seconds: int = Field(default=120, ge=1)
    max_tokens: int = Field(default=LLM_MAX_TOKENS, ge=1)
    temperature: float = Field(
        default=LLM_DEFAULT_TEMPERATURE, ge=0.0, le=LLM_MAX_TEMPERATURE
    )
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    max_retries: int = Field(default=3, ge=0, le=10)
    organization: str | None = Field(default=None)
    request_timeout_seconds: int = Field(default=120, ge=1)
    context_window: int = Field(default=128_000, ge=1)

    embedding: EmbeddingSettings = Field(default_factory=EmbeddingSettings)
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)

    @field_validator("provider", mode="before")
    @classmethod
    def _coerce_provider(cls, value: object) -> LLMProvider:
        if isinstance(value, LLMProvider):
            return value
        return LLMProvider.coerce(value) or LLMProvider.CUSTOM
