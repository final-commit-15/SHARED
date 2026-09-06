"""Base configuration primitives for all AgentForge services.

Settings are loaded from (in decreasing precedence):

1. values passed directly to the constructor,
2. environment variables (case-insensitive, honouring ``env_prefix``),
3. ``.env`` files,
4. the secrets directory (one file per secret, file name == setting key),
5. defaults declared in each model.
"""

from __future__ import annotations

from typing import Any

from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

from agentforge_shared.constants.paths import DEFAULT_ENV_FILE, DEFAULT_SECRETS_DIR


class BaseAgentForgeSettings(BaseSettings):
    """Reusable base for every settings group in the platform."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE,
        secrets_dir=DEFAULT_SECRETS_DIR,
        extra="ignore",
        populate_by_name=True,
        validate_assignment=True,
        case_sensitive=False,
    )

    def non_secret(self) -> dict[str, Any]:
        """Serialize the settings, masking well-known secret field names.

        Used by health endpoints and diagnostics that must never leak
        credentials into logs or responses.
        """
        masked = {"password", "secret", "key", "token", "credential", "api_key"}
        dump = {
            k: ("***" if any(part in k.lower() for part in masked) else v)
            for k, v in self.model_dump(mode="json").items()
        }
        return dump


def settings_config(
    parent: SettingsConfigDict | None = None, **overrides: Any
) -> SettingsConfigDict:
    """Derive a new settings config from a parent config dict.

    ``SettingsConfigDict`` is a typed dictionary (not a mapping class), so it
    cannot be mutated in place; this helper returns a fresh merged dict.
    """
    merged: dict[str, Any] = dict(parent or {})
    merged.update(overrides)
    return SettingsConfigDict(merged)


__all__ = [
    "BaseAgentForgeSettings",
    "SettingsConfigDict",
    "ConfigDict",
    "settings_config",
]
