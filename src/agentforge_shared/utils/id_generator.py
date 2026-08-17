"""ID generation utilities."""

import uuid


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with an optional prefix."""
    uid = uuid.uuid4().hex[:12]
    return f"{prefix}_{uid}" if prefix else uid


def generate_agent_id() -> str:
    return generate_id("agent")


def generate_execution_id() -> str:
    return generate_id("exec")


def generate_user_id() -> str:
    return generate_id("user")


def generate_integration_id() -> str:
    return generate_id("int")