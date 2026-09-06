"""Environment detection and helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

DEFAULT_ENV = "development"


def get_environment() -> str:
    """Return the current environment string (default ``"development"``)."""
    return os.getenv("APP_ENV", os.getenv("ENV", DEFAULT_ENV)).strip().lower()


def is_development() -> bool:
    """Return ``True`` when running in development."""
    return get_environment() in {"development", "dev", "local", ""}


def is_testing() -> bool:
    """Return ``True`` when running in a testing environment."""
    return get_environment() in {"test", "testing"}


def is_staging() -> bool:
    """Return ``True`` when running in staging."""
    return get_environment() == "staging"


def is_production() -> bool:
    """Return ``True`` when running in production."""
    return get_environment() == "production"


def is_ci() -> bool:
    """Return ``True`` when CI is detected (GitHub Actions, GitLab, Jenkins, etc.)."""
    for name in (
        "CI",
        "GITHUB_ACTIONS",
        "GITLAB_CI",
        "JENKINS_URL",
        "CIRCLECI",
        "BITBUCKET_PIPELINE",
        "TF_BUILD",
        "BUILDKITE",
    ):
        if os.getenv(name):
            return True
    return False


def env_int(key: str, default: int = 0) -> int:
    """Read an integer from the environment with a fallback."""
    try:
        return int(os.getenv(key, "").strip() or default)
    except (ValueError, TypeError):
        return default


def env_float(key: str, default: float = 0.0) -> float:
    """Read a float from the environment with a fallback."""
    try:
        return float(os.getenv(key, "").strip() or default)
    except (ValueError, TypeError):
        return default


def env_bool(key: str, default: bool = False) -> bool:
    """Read a boolean-like value from the environment.

    Truthy strings (case-insensitive): ``1``, ``true``, ``yes``, ``on``.
    """
    raw = os.getenv(key, "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "on", "t", "y"}


def env_list(key: str, delimiter: str = ",", default: str | None = None) -> list[str]:
    """Read a comma-separated list from the environment."""
    raw = os.getenv(key, "").strip()
    if not raw:
        return []
    return [part.strip() for part in raw.split(delimiter) if part.strip()]


def env_dict(
    keys: list[str] | tuple[str, ...],
    prefix: str = "",
) -> dict[str, Any]:
    """Build a dict by reading several environment variables at once."""
    return {key: os.getenv(f"{prefix}{key}") for key in keys}


def env_or(key: str, fallback: str) -> str:
    """Return the environment value for ``key``, or ``fallback``."""
    return os.getenv(key, "").strip() or fallback


def env_required(key: str, *, message: str | None = None) -> str:
    """Return the environment value for ``key`` or raise ``ValueError``."""
    value = os.getenv(key, "").strip()
    if not value:
        raise ValueError(message or f"Required environment variable {key!r} is not set")
    return value


def load_env_file(
    path: str | Path,
    *,
    override: bool = False,
) -> dict[str, str]:
    """Lightweight ``.env`` file parser (no external dependency).

    Returns every key/value pair parsed (overwrites ``os.environ`` when
    ``override`` is ``True``).
    """
    result: dict[str, str] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        result[key] = value
        if override:
            os.environ[key] = value
    return result


def verify_environment(
    *,
    required_keys: list[str] | None = None,
    optional_keys: list[str] | None = None,
) -> dict[str, str | None]:
    """Check that required keys are present; return their values."""
    report: dict[str, str | None] = {}
    for key in required_keys or []:
        value = os.getenv(key, "")
        report[key] = value.strip() or None
        if not value.strip():
            raise OSError(f"Required environment variable {key!r} is not set")
    for key in optional_keys or []:
        report[key] = os.getenv(key, "").strip() or None
    return report
