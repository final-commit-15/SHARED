"""Global constants used across services."""

API_VERSION = "v1"

DEFAULT_PAGE_LIMIT = 20
MAX_PAGE_LIMIT = 100

DEFAULT_TIMEOUT_SECONDS = 30

# Keep these in sync with the corresponding enums
SUPPORTED_AGENT_TYPES = ["chat", "task", "embedding", "custom"]
SUPPORTED_INTEGRATION_TYPES = ["slack", "discord", "github", "jira", "webhook", "other"]