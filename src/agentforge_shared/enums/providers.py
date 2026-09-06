"""Provider enumerations: LLMs, memory, embeddings, vector stores, search."""

from __future__ import annotations

from .base import StringEnum


class ProviderType(StringEnum):
    """Broad categories of external providers."""

    LLM = "llm"
    EMBEDDING = "embedding"
    VECTOR_STORE = "vector_store"
    MEMORY = "memory"
    OBJECT_STORAGE = "object_storage"
    SEARCH = "search"
    QUEUE = "queue"
    CACHE = "cache"
    DATABASE = "database"
    EMAIL = "email"
    SMS = "sms"
    GEOCODING = "geocoding"


class LLMProvider(StringEnum):
    """Supported large language model providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"  # Gemini
    MISTRAL = "mistral"
    COHERE = "cohere"
    DEEPSEEK = "deepseek"
    GROQ = "groq"
    OLLAMA = "ollama"
    AZURE_OPENAI = "azure_openai"
    AWS_BEDROCK = "aws_bedrock"
    LOCAL = "local"
    CUSTOM = "custom"


class EmbeddingProvider(StringEnum):
    """Supported embedding providers."""

    OPENAI = "openai"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    OLLAMA = "ollama"
    AZURE_OPENAI = "azure_openai"
    AWS_BEDROCK = "aws_bedrock"
    GOOGLE = "google"
    LOCAL = "local"
    CUSTOM = "custom"


class MemoryProvider(StringEnum):
    """Supported long-term memory backends."""

    REDIS = "redis"
    POSTGRES = "postgres"
    SQLITE = "sqlite"
    FAISS = "faiss"
    CONSTANTIME = "constantime"
    PINECONE = "pinecone"
    ZEP = "zep"
    IN_MEMORY = "in_memory"
    CUSTOM = "custom"


class VectorStoreType(StringEnum):
    """Supported vector databases."""

    QDRANT = "qdrant"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"
    MILVUS = "milvus"
    CHROMA = "chroma"
    FAISS = "faiss"
    PG_VECTOR = "pg_vector"
    OPENSEARCH = "opensearch"
    ELASTICSEARCH = "elasticsearch"
    REDIS = "redis"
    CUSTOM = "custom"


class SearchProvider(StringEnum):
    """Supported full-text / hybrid search engines."""

    ELASTICSEARCH = "elasticsearch"
    OPENSEARCH = "opensearch"
    MEILISEARCH = "meilisearch"
    TYPESENSE = "typesense"
    POSTGRES = "postgres"
    VESPA = "vespa"
    CUSTOM = "custom"


class StorageProvider(StringEnum):
    """Supported object storage providers."""

    S3 = "s3"
    GCS = "gcs"
    AZURE_BLOB = "azure_blob"
    LOCAL = "local"
    MINIO = "minio"
    CUSTOM = "custom"
