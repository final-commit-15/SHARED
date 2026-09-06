"""agentforge-shared: shared foundational package for AgentForge microservices.

Provides configuration, exceptions, enums, schemas, DTOs, events, security,
middleware, logging, telemetry, retry, cache, pagination, validation, and
versioning utilities used across the AgentForge platform.

Example::

    from agentforge_shared.config.loader import get_settings
    from agentforge_shared.logging.config import configure_logging

    configure_logging()
    settings = get_settings()
"""

from __future__ import annotations

__version__ = "0.1.0"
__title__ = "agentforge-shared"
__description__ = "Shared foundation package for AgentForge microservices."
__author__ = "AgentForge"
__license__ = "MIT"

from . import (  # noqa: F401  # noqa: F401  # noqa: F401
    api,
    cache,
    constants,
    dto,
    enums,
    events,
    exceptions,
    logging,
    metadata,
    middleware,
    pagination,
    retry,
    schemas,
    security,
    telemetry,
    typing,
    utils,
    validation,
    version,
)
from .config.loader import (
    AgentForgeSettings,
    build_settings,
    get_settings,
    refresh_settings,
)
from .logging.logger import get_logger

__all__ = [
    "__version__",
    "api",
    "cache",
    "constants",
    "dto",
    "enums",
    "events",
    "exceptions",
    "logging",
    "metadata",
    "middleware",
    "pagination",
    "retry",
    "schemas",
    "security",
    "telemetry",
    "typing",
    "utils",
    "validation",
    "version",
    # config
    "AgentForgeSettings",
    "get_settings",
    "build_settings",
    "refresh_settings",
    # logging
    "get_logger",
]
