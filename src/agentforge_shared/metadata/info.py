"""Package/build/runtime metadata helpers."""

from __future__ import annotations

import os
import platform
import sys
from datetime import datetime
from typing import Any

from agentforge_shared.utils.datetime_helpers import utc_now


def get_version() -> str:
    """Return the agentforge-shared package version."""
    try:
        from importlib.metadata import version as _im_version

        return _im_version("agentforge-shared")
    except Exception:  # pragma: no cover - uninstalled source checkout
        return "0.1.0"


def build_info(
    *,
    service: str | None = None,
    version: str | None = None,
    commit: str | None = None,
    build_number: str | None = None,
    built_at: datetime | None = None,
) -> dict[str, Any]:
    """Assemble the standard build-metadata block."""
    return {
        "service": service,
        "version": version or get_version(),
        "commit_sha": commit,
        "build_number": build_number,
        "build_date": (built_at or utc_now()).isoformat(),
        "name": "agentforge-shared",
    }


def git_commit_sha(path: str | os.PathLike | None = None) -> str | None:
    """Read the current git commit SHA (head ref) for ``path``."""
    import subprocess

    base = str(path or ".")
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=base,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        sha = result.stdout.strip()
        return sha or None
    except (OSError, subprocess.SubprocessError):
        return None


def environment_metadata() -> dict[str, Any]:
    """Runtime environment facts for diagnostics."""
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "impl": platform.python_implementation(),
        "cwd": os.getcwd(),
        "env": dict(os.environ),
    }


def runtime_metadata(*, service: str | None = None, include_build: bool = True) -> dict[str, Any]:
    """Combined metadata block for startup logging/health payloads."""
    data: dict[str, Any] = {
        "version": get_version(),
        "started_at": utc_now().isoformat(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "service": service,
    }
    if include_build:
        data["build"] = build_info(service=service)
    return data


def redact_env(env: dict[str, str] | None = None) -> dict[str, str]:
    """Environment snapshot with secret-ish variables redacted."""
    from agentforge_shared.logging.masking import redact_dict

    snapshot = dict(env or os.environ)
    return {k: str(redact_dict({k: v})[k]) for k, v in snapshot.items()}


__all__ = ["get_version", "build_info", "git_commit_sha", "environment_metadata", "runtime_metadata", "redact_env"]
