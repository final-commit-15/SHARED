"""Model-related metadata: provider defaults, context windows, temperature bounds."""

# Default models per provider
DEFAULT_MODEL_OPENAI = "gpt-4o-mini"
DEFAULT_MODEL_ANTHROPIC = "claude-3-5-sonnet-latest"
DEFAULT_MODEL_GEMINI = "gemini-1.5-pro"
DEFAULT_MODEL_OLLAMA = "llama3.2"
DEFAULT_MODEL_MISTRAL = "mistral-large-latest"
DEFAULT_MODEL_COHERE = "command-r-plus"
DEFAULT_MODEL_DEEPSEEK = "deepseek-chat"
DEFAULT_MODEL_GROQ = "llama-3.3-70b-versatile"

DEFAULT_EMBEDDING_MODEL_OPENAI = "text-embedding-3-small"
DEFAULT_EMBEDDING_MODEL_COHERE = "embed-english-v3.0"
DEFAULT_EMBEDDING_MODEL_HF = "all-MiniLM-L6-v2"

# Temperature bounds
LLM_MIN_TEMPERATURE = 0.0
LLM_MAX_TEMPERATURE = 2.0
LLM_DEFAULT_TEMPERATURE = 0.7

# Top-p bounds
LLM_MIN_TOP_P = 0.0
LLM_MAX_TOP_P = 1.0
LLM_DEFAULT_TOP_P = 1.0

# Token limits
LLM_DEFAULT_MAX_TOKENS = 1_024
LLM_MIN_MAX_TOKENS = 1
LLM_MAX_MAX_TOKENS = 128_000

# Context windows (approximate) keyed by provider/model family.
DEFAULT_CONTEXT_WINDOW = 128_000
CONTEXT_WINDOWS: dict[str, int] = {
    "gpt-3.5-turbo": 16_385,
    "gpt-4": 8_192,
    "gpt-4-32k": 32_768,
    "gpt-4-turbo": 128_000,
    "gpt-4o": 128_000,
    "gpt-4o-mini": 128_000,
    "claude-3-5-sonnet": 200_000,
    "claude-3-haiku": 200_000,
    "claude-3-opus": 200_000,
    "gemini-1.5-pro": 1_000_000,
    "gemini-1.5-flash": 1_000_000,
    "llama3.2": 128_000,
    "llama3.1": 128_000,
    "mistral-large": 128_000,
    "command-r-plus": 128_000,
    "deepseek-chat": 64_000,
}

# Embedding dimensions
EMBEDDING_DEFAULT_DIMENSIONS = 1_536
EMBEDDING_MAX_DIMENSIONS = 3_072

# Default vector stores
DEFAULT_VECTOR_STORE = "qdrant"
DEFAULT_VECTOR_DIMENSIONS = 1_536

# Token pricing inputs (USD per 1M tokens) used for cost estimation.
# These are approximations and must be refreshed from provider price sheets.
PRICING_PER_MILLION_TOKENS: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "command-r-plus": {"input": 3.00, "output": 15.00},
    "mistral-large": {"input": 2.00, "output": 6.00},
    "deepseek-chat": {"input": 0.27, "output": 1.10},
}

# Chunking defaults
DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 50
MAX_CHUNK_SIZE = 4_096
