"""Backwards-compatible exports for the original constants module.

New code should import from the dedicated submodules (``api``, ``headers``,
``limits``, ``timeouts``, ``paths``, ``roles``, ``permissions``, ``errors``,
``mime_types``, ``models``).
"""

from .api import API_DEFAULT_PER_PAGE, API_MAX_PER_PAGE, API_VERSION
from .limits import DEFAULT_PAGE_LIMIT, MAX_PAGE_LIMIT
from .models import DEFAULT_MODEL_OPENAI
from .timeouts import DEFAULT_TIMEOUT_SECONDS

# Legacy values kept for compatibility with early adopters.
SUPPORTED_AGENT_TYPES: list[str] = ["chat", "task", "embedding", "custom"]
SUPPORTED_INTEGRATION_TYPES: list[str] = [
    "slack",
    "discord",
    "github",
    "jira",
    "webhook",
    "other",
]

__all__ = [
    "API_VERSION",
    "API_MAX_PER_PAGE",
    "API_DEFAULT_PER_PAGE",
    "DEFAULT_PAGE_LIMIT",
    "MAX_PAGE_LIMIT",
    "DEFAULT_TIMEOUT_SECONDS",
    "DEFAULT_MODEL_OPENAI",
    "SUPPORTED_AGENT_TYPES",
    "SUPPORTED_INTEGRATION_TYPES",
]
