"""Filesystem and path constants used by the package and services."""

DEFAULT_ENV_FILE = ".env"
DEFAULT_SECRETS_DIR = "./secrets"
LOCAL_STORAGE_DIR = "./storage"
LOGS_DIR = "./logs"
TEMP_DIR = "./tmp"
CONFIG_DIR = "./config"
SCHEMA_DIR = "./schemas"

# Package-level paths.
PACKAGE_ROOT = "agentforge_shared"
SCHEMA_VERSION_FILE = "VERSION"
BUILD_INFO_FILE = "build_info.json"

# Prefixed identifiers
EXECUTION_PATH_PREFIX = "/executions"
WORKFLOW_PATH_PREFIX = "/workflows"
AGENT_PATH_PREFIX = "/agents"
USERS_PATH_PREFIX = "/users"
MEMORY_PATH_PREFIX = "/memory"
SEARCH_PATH_PREFIX = "/search"

# Well-known data directories for agents.
AGENT_HOME = ".agentforge"
AGENT_CONFIG_FILE = "agent.json"
AGENT_LOGS_DIR = ".agentforge/logs"
AGENT_STATE_DIR = ".agentforge/state"
