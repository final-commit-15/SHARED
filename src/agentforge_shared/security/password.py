"""Password hashing helpers (bcrypt)."""

from __future__ import annotations

import bcrypt

from agentforge_shared.exceptions.base import AuthenticationException


def hash_password(password: str, *, cost: int = 12) -> str:
    """Hash a plaintext password with a random salt.

    Returns the bcrypt string (includes the salt), never the plaintext.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")
    salt = bcrypt.gensalt(rounds=cost)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Constant-time check of ``password`` against a bcrypt hash."""
    if not password_hash:
        return False
    try:
        stored = password_hash.encode("utf-8")
        candidate = password.encode("utf-8")
        return bcrypt.hashpw(candidate, stored) == stored
    except (ValueError, TypeError):
        return False


def require_password(password: str, password_hash: str) -> None:
    """Raise :class:`AuthenticationException` when verification fails."""
    if not verify_password(password, password_hash):
        raise AuthenticationException(message="invalid credentials")
    return


__all__ = ["hash_password", "verify_password", "require_password"]
