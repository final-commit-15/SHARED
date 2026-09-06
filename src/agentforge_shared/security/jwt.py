"""JWT access/refresh token management (HS256)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from agentforge_shared.config.jwt import JWTSettings
from agentforge_shared.exceptions.base import (
    InvalidTokenException,
    TokenExpiredException,
)
from agentforge_shared.utils.datetime_helpers import utc_now


class JWTManager:
    """Issues and validates signed JWTs with optional refresh rotation.

    Example::

        from agentforge_shared.config.jwt import JWTSettings
        from agentforge_shared.security.jwt import JWTManager

        manager = JWTManager(JWTSettings(secret_key="a-very-long-secret--abcdef"))
        access = manager.create_access_token("user_123", role="admin")
        claims = manager.decode_token(access)          # {"sub": "user_123", "role": "admin", ...}
    """

    def __init__(self, settings: JWTSettings) -> None:
        self._settings = settings

    @property
    def settings(self) -> JWTSettings:
        return self._settings

    def create_access_token(
        self,
        subject: str,
        *,
        expires_in: int | None = None,
        issuer: str | None = None,
        audience: str | None = None,
        **claims: Any,
    ) -> str:
        """Create a signed access token for ``subject``."""
        now = utc_now()
        ttl = (
            timedelta(minutes=expires_in)
            if expires_in is not None
            else timedelta(minutes=self._settings.access_token_ttl_minutes)
        )
        payload: dict[str, Any] = {
            "sub": subject,
            "iat": now,
            "nbf": now,
            "exp": now + ttl,
            "iss": issuer or self._settings.issuer,
            "aud": audience or self._settings.audience,
        }
        payload.update(claims)
        return jwt.encode(payload, self._settings.secret_key, algorithm=self._settings.algorithm)

    def create_refresh_token(self, subject: str, *, expires_in: int | None = None, **claims: Any) -> str:
        """Create a signed refresh token (longer TTL, distinct type claim)."""
        now = utc_now()
        ttl = (
            timedelta(days=expires_in)
            if expires_in is not None
            else timedelta(days=self._settings.refresh_token_ttl_days)
        )
        payload: dict[str, Any] = {
            "sub": subject,
            "iat": now,
            "exp": now + ttl,
            "iss": self._settings.issuer,
            "aud": self._settings.audience,
            "type": "refresh",
        }
        payload.update(claims)
        return jwt.encode(payload, self._settings.secret_key, algorithm=self._settings.algorithm)

    def decode_token(
        self,
        token: str,
        *,
        audience: str | None = None,
        require_type: str | None = None,
    ) -> dict[str, Any]:
        """Decode and verify ``token``.

        Raises:
            InvalidTokenException: Malformed/untrusted signature.
            TokenExpiredException: ``exp`` passed (with leeway).
        """
        try:
            claims = jwt.decode(
                token,
                self._settings.secret_key,
                algorithms=self._settings.algorithms,
                audience=audience or self._settings.audience,
                issuer=self._settings.issuer,
            )
        except jwt.ExpiredSignatureError as exc:
            raise TokenExpiredException(message="token has expired") from exc
        except (JWTError, ValueError) as exc:
            raise InvalidTokenException(message="invalid or malformed token") from exc

        if require_type and claims.get("type") != require_type:
            raise InvalidTokenException(message=f"expected token type {require_type!r}")
        return claims

    def verify_access_token(self, token: str) -> dict[str, Any]:
        """Decode an access token (requires ``sub`` presence, no type check)."""
        claims = self.decode_token(token)
        if not claims.get("sub"):
            raise InvalidTokenException(message="token missing subject")
        return claims

    def verify_refresh_token(self, token: str) -> dict[str, Any]:
        """Decode a refresh token (requires ``type == 'refresh'``)."""
        return self.decode_token(token, require_type="refresh")

    def rotate_refresh_token(self, refresh_token: str, **new_claims: Any) -> tuple[str, str]:
        """Exchange a valid refresh token for a fresh pair (rotation).

        Returns:
            ``(new_access_token, new_refresh_token)``.
        """
        claims = self.verify_refresh_token(refresh_token)
        subject = claims["sub"]
        access = self.create_access_token(subject, **new_claims)
        refreshed = self.create_refresh_token(subject)
        return access, refreshed

    def expires_at(self, token: str) -> datetime:
        """Return the ``exp`` timestamp of a valid token."""
        claims = self.verify_access_token(token)
        exp = claims.get("exp")
        if exp is None:
            raise InvalidTokenException(message="token missing exp claim")
        return datetime.fromtimestamp(exp, tz=UTC)


__all__ = ["JWTManager"]
