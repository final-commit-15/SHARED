"""Version helpers: current version, SemVer, APIVersion compliance, deprecation."""

from __future__ import annotations

from typing import Any
from warnings import warn

from .semver import (
    SemVer,
    compatible_version,
    deprecated_version,
    is_supported,
    parse_version,
)


def get_version() -> str:
    """Return the agentforge-shared package version."""
    try:
        from importlib.metadata import version as _im_version

        return _im_version("agentforge-shared")
    except Exception:  # pragma: no cover - uninstalled source checkout
        return "0.1.0"


def current() -> SemVer:
    """Current library version as ``SemVer``."""
    return SemVer.parse(get_version())


def strict_version(required: str, *, semver: bool = True) -> Any:
    """Validate that a required dependency version constraint is parseable.

    Returns the parsed ``SemVer`` when ``semver`` else the original string.
    """
    parsed = parse_version(required)
    return parsed if semver else str(parsed)


def check_api_version(request_version: str, *, server_version: str, min_client: str) -> bool:
    """Verify a client's API version is compatible with the server.

    Returns ``False`` (never raises) when the client is older than
    ``min_client`` or newer than ``server_version``.
    """
    current = SemVer.parse(server_version)
    client = parse_version(request_version)
    return is_supported(client, min_version=min_client, max_version=str(current))


def deprecated(name: str, *, replacement: str | None = None, removal_version: str | None = None) -> None:
    """Emit a :class:`DeprecationWarning` for ``name``.

    Example::

        def old_thing(): deprecated("old_thing", replacement="new_thing")
    """
    message = f"{name} is deprecated"
    if replacement:
        message += f"; use {replacement} instead"
    if removal_version:
        message += f"; will be removed in {removal_version}"
    warn(message, DeprecationWarning, stacklevel=2)


__all__ = [
    "SemVer",
    "get_version",
    "current",
    "strict_version",
    "check_api_version",
    "deprecated",
    "parse_version",
    "is_supported",
    "compatible_version",
    "deprecated_version",
]
