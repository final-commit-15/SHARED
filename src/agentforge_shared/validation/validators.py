"""Validation helpers for common input types (Pydantic-friendly).

Each validator returns the refined value and raises ``ValueError`` (or a
custom exception) on invalid input, matching Pydantic v2 field-validator
semantics so they can be used both standalone and in ``@field_validator``.
"""

from __future__ import annotations

import re
import uuid as _uuid
from pathlib import Path

from agentforge_shared.constants.limits import (
    MAX_EMAIL_LENGTH,
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
)

_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(value: str, *, allow_none: bool = False) -> str | None:
    """Validate and return an email address (lowercased)."""
    if value is None:
        if allow_none:
            return None
        raise ValueError("email must not be None")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("email must be a non-empty string")
    email = value.strip().lower()
    if len(email) > MAX_EMAIL_LENGTH:
        raise ValueError(f"email exceeds max length of {MAX_EMAIL_LENGTH}")
    if not _EMAIL_REGEX.match(email):
        raise ValueError("invalid email address")
    return email


def validate_password(
    value: str,
    *,
    min_length: int = MIN_PASSWORD_LENGTH,
    max_length: int = MAX_PASSWORD_LENGTH,
    require_upper: bool = True,
    require_lower: bool = True,
    require_digit: bool = False,
    require_symbol: bool = False,
) -> str:
    """Validate a password string against strength requirements.

    Returns the original password (never stored) or raises ``ValueError``.
    """
    if value is None:
        raise ValueError("password must not be None")
    if not isinstance(value, str):
        raise ValueError("password must be a string")
    if len(value) < min_length:
        raise ValueError(f"password must be at least {min_length} characters")
    if len(value) > max_length:
        raise ValueError(f"password must be at most {max_length} characters")
    if require_upper and not any(c.isupper() for c in value):
        raise ValueError("password must contain an uppercase letter")
    if require_lower and not any(c.islower() for c in value):
        raise ValueError("password must contain a lowercase letter")
    if require_digit and not any(c.isdigit() for c in value):
        raise ValueError("password must contain a digit")
    if require_symbol and not any(not c.isalnum() for c in value):
        raise ValueError("password must contain a symbol")
    return value


def validate_url(value: str, *, require_scheme: bool = True) -> str:
    """Validate and return a URL string."""
    if value is None:
        raise ValueError("url must not be None")
    text = (value or "").strip()
    if not text:
        raise ValueError("url must be a non-empty string")
    if " " in text or "\n" in text or "\t" in text:
        raise ValueError("url must not contain whitespace")
    scheme, _, rest = text.partition("://")
    if require_scheme and not (_ and rest):
        raise ValueError("url must include a scheme (e.g. https://)")
    if not require_scheme and not _:
        raise ValueError("invalid url")
    return text


def validate_uuid(value: str | _uuid.UUID | None, *, version: int | None = None) -> _uuid.UUID:
    """Validate and normalise a UUID string into a ``uuid.UUID``."""
    if value is None:
        raise ValueError("uuid must not be None")
    if isinstance(value, _uuid.UUID):
        candidate = value
    else:
        try:
            candidate = _uuid.UUID(str(value))
        except (ValueError, AttributeError) as exc:
            raise ValueError(f"invalid uuid: {value!r}") from exc
    if version is not None and candidate.version != version:
        raise ValueError(f"expected uuid version {version}, got {candidate.version}")
    return candidate


def validate_filename(value: str, *, max_length: int = 200) -> str:
    """Validate a filename (no path separators / control chars)."""
    import os as _os

    if value is None:
        raise ValueError("filename must not be None")
    name = (value or "").strip()
    if not name:
        raise ValueError("filename must be a non-empty string")
    if len(name) > max_length:
        raise ValueError(f"filename exceeds max length {max_length}")
    for sep in ("/", "\\", "\x00"):
        if sep in name:
            raise ValueError(f"filename must not contain {sep!r}")
    if name in {".", ".."} or name.startswith("~"):
        raise ValueError("illegal filename")
    if _os.sep in name:
        raise ValueError("filename must not contain path separators")
    return name


def validate_file_path(value: Path | str) -> Path:
    """Validate a filesystem path (exists-and-is-file is not required)."""
    path = Path(value)
    if path.name in {"", "."}:
        raise ValueError("invalid file path")
    return path


def validate_json_string(value: str) -> str:
    """Validate that ``value`` is well-formed JSON and return it unchanged."""
    from agentforge_shared.utils.json_utils import loads

    if value is None:
        raise ValueError("json must not be None")
    if not isinstance(value, str):
        raise ValueError("json must be a string")
    try:
        loads(value)
    except (ValueError, TypeError) as exc:
        raise ValueError("invalid JSON") from exc
    return value


_CRON_REGEX = re.compile(
    r"^(\*|[0-5]?\d|\*/[1-5]?\d|\d+-\d+)(,\s*(?!$)(\*|[0-5]?\d|\*/[1-5]?\d|\d+-\d+))*(\s+"
    r"(\*|[01]?\d|2[0-3]|\*/[012]?\d|\d+-\d+)(,\s*(?!$)(\*|[01]?\d|2[0-3]|\*/[012]?\d|\d+-\d+))*\s*){4}$"
)


def validate_cron(value: str, *, standard: bool = True) -> str:
    """Validate a 5-field (or 6-field) cron expression.

    Args:
        value: Cron expression. Supports ``*``, ``*/n``, ranges, commas.
        standard: When ``True`` require 5 fields; when ``False`` allow 6.

    Returns:
        The trimmed expression, or raises ``ValueError``.
    """
    if value is None:
        raise ValueError("cron must not be None")
    expr = (value or "").strip()
    if not expr:
        raise ValueError("cron expression must not be empty")
    fields = expr.split()
    expected = 5 if standard else 6
    if len(fields) != expected:
        raise ValueError(f"cron must have {expected} fields, got {len(fields)}")
    if not _CRON_REGEX.match(expr):
        raise ValueError(f"invalid cron expression: {value!r}")
    return expr


def validate_environment(value: str, *, allowed: list[str] | None = None) -> str:
    """Validate that ``value`` is a known environment name."""
    from agentforge_shared.enums.platform import Environment

    name = (value or "").strip().lower()
    if allowed is not None:
        if name not in {a.strip().lower() for a in allowed}:
            raise ValueError(f"environment must be one of {allowed}")
        return name
    try:
        Environment.coerce(name) is not None
    except (ValueError, AttributeError):
        pass
    if name not in Environment.values():
        raise ValueError(f"environment must be one of {Environment.values()}")
    return name


def validate_identifier(value: str, *, min_length: int = 1, max_length: int = 64) -> str:
    """Validate a slug-ish identifier (lowercase, alnum, ``-``/``_``)."""
    if value is None:
        raise ValueError("identifier must not be None")
    ident = (value or "").strip()
    if len(ident) < min_length or len(ident) > max_length:
        raise ValueError(f"identifier length must be in [{min_length}, {max_length}]")
    if not re.match(r"^[a-zA-Z0-9_\-]+$", ident):
        raise ValueError("identifier must contain only alphanumerics, '-' or '_'")
    return ident


def validate_phone(value: str | int, *, allow_plus: bool = True) -> str:
    """Validate a phone number (E.164-ish formatting)."""
    text = str(value).strip()
    if not text:
        raise ValueError("phone must not be empty")
    if allow_plus and text.startswith("+"):
        digits = text[1:]
        if not digits.isdigit() or not 3 <= len(digits) <= 15:
            raise ValueError("invalid phone number")
        return text
    if not text.isdigit() or not 3 <= len(text) <= 15:
        raise ValueError("invalid phone number")
    return text


def is_valid_email(value: str) -> bool:
    """Return a bool (never raises) for email validity checks."""
    try:
        validate_email(value)
        return True
    except ValueError:
        return False


__all__ = [
    "validate_email",
    "validate_password",
    "validate_url",
    "validate_uuid",
    "validate_filename",
    "validate_file_path",
    "validate_json_string",
    "validate_cron",
    "validate_environment",
    "validate_identifier",
    "validate_phone",
    "is_valid_email",
]
