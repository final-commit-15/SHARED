"""PII / secret masking for log output."""

from __future__ import annotations

import re
from typing import Any

#: Keys whose values are fully redacted.
SECRET_KEYS: frozenset[str] = frozenset(
    {
        "password",
        "passwd",
        "secret",
        "secret_key",
        "secrets",
        "token",
        "access_token",
        "refresh_token",
        "api_key",
        "apikey",
        "api-key",
        "jwt",
        "authorization",
        "cookie",
        "cookie_value",
        "private_key",
        "private-key",
        "client_secret",
        "db_password",
        "redis_password",
        "signature",
        "x_api_key",
        "x-agentforge-signature",
    }
)

#: Keys masked partially (e.g. email becomes ``j***@domain.com``).
PARTIAL_KEYS: frozenset[str] = frozenset(
    {
        "email",
        "phone",
        "phone_number",
        "card_number",
        "ssn",
        "ip",
        "ip_address",
    }
)

_EMAIL_RE = re.compile(r"^([^@\s]+)@([^@\s]+)$")


def mask_sensitive_fields(_logger: Any, _method_name: str, event_dict: dict) -> dict:
    """structlog processor that redacts sensitive context values.

    Secret keys are replaced with ``"***"``; partial keys keep a hint.
    """
    for key, value in list(event_dict.items()):
        lowered = str(key).lower()
        if lowered in SECRET_KEYS:
            event_dict[key] = "***"
        elif lowered in PARTIAL_KEYS and isinstance(value, str) and value:
            event_dict[key] = partially_mask(value)
    return event_dict


def partially_mask(value: str, *, keep_head: int = 1, keep_tail: int = 2) -> str:
    """Mask the middle of a string, preserving a head/tail hint."""
    if len(value) <= keep_head + keep_tail + 1:
        return "*" * len(value)
    if keep_tail == 2 and "@" in value:
        match = _EMAIL_RE.match(value)
        if match and "." in match.group(2):
            local, domain = match.group(1), match.group(2)
            masked_local = local[0] + ("*" * max(1, len(local) - 1)) if local else "*"
            return f"{masked_local}@{domain}"
    return value[:keep_head] + "*" * (len(value) - keep_head - keep_tail) + value[-keep_tail:]


def mask_value(key: str, value: Any) -> Any:
    """Return a masked copy of ``value`` depending on ``key``."""
    lowered = str(key).lower()
    if lowered in SECRET_KEYS:
        return "***"
    if lowered in PARTIAL_KEYS and isinstance(value, str):
        return partially_mask(value)
    return value


def redact_dict(data: dict) -> dict:
    """Deep-copy ``data`` with sensitive keys masked (for audit logs)."""
    out: dict[str, Any] = {}
    for key, value in data.items():
        masked_key = str(key).lower()
        if mask_value(masked_key, value) is not value:
            out[key] = mask_value(masked_key, value)
        elif isinstance(value, dict):
            out[key] = redact_dict(value)
        elif isinstance(value, list):
            out[key] = [redact_dict(item) if isinstance(item, dict) else item for item in value]
        else:
            out[key] = value
    return out


__all__ = ["mask_sensitive_fields", "partially_mask", "mask_value", "redact_dict", "SECRET_KEYS", "PARTIAL_KEYS"]
