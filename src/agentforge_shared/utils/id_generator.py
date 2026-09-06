"""ID generation utilities.

**Deprecated**: prefer :mod:`agentforge_shared.utils.uuid7` for new code,
which emits orderable, time-encoded identifiers.
"""

from __future__ import annotations

import uuid

from agentforge_shared.utils.uuid7 import generate_uuid7_id  # noqa: F401


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with an optional prefix (legacy uuid4-based)."""
    uid = uuid.uuid4().hex[:12]
    return f"{prefix}_{uid}" if prefix else uid


def generate_agent_id() -> str:
    """Generate a prefixed agent identifier (legacy)."""
    return generate_id("agent")


def generate_execution_id() -> str:
    """Generate a prefixed execution identifier (legacy)."""
    return generate_id("exec")


def generate_user_id() -> str:
    """Generate a prefixed user identifier (legacy)."""
    return generate_id("user")


def generate_integration_id() -> str:
    """Generate a prefixed integration identifier (legacy)."""
    return generate_id("int")


__all__ = [
    "generate_id",
    "generate_agent_id",
    "generate_execution_id",
    "generate_user_id",
    "generate_integration_id",
]
