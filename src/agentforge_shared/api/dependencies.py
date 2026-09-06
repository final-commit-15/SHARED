"""FastAPI dependencies: auth, roles, permissions, and pagination."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Any

from fastapi import Depends, Request

from agentforge_shared.enums.platform import UserRole
from agentforge_shared.exceptions.base import (
    AuthenticationException,
    AuthorizationException,
)
from agentforge_shared.schemas.pagination import OffsetPaginationParams
from agentforge_shared.security.jwt import JWTManager
from agentforge_shared.security.permissions import PermissionChecker

#: Module-level JWTManager; set once by ``setup_auth``.
_jwt_mgr: JWTManager | None = None
_checker = PermissionChecker()


@dataclass
class Principal:
    """The authenticated identity carried on requests."""

    subject: str
    user_id: str | None = None
    role: UserRole | str | None = None
    scopes: list[str] = field(default_factory=list)
    tenant_id: str | None = None
    claims: dict[str, Any] = field(default_factory=dict)


def setup_auth(jwt_manager: JWTManager) -> None:
    """Register the JWT manager used by the authentication dependency.

    Example::

        from agentforge_shared.config.jwt import JWTSettings
        from agentforge_shared.security.jwt import JWTManager
        from agentforge_shared.api.dependencies import setup_auth

        setup_auth(JWTManager(JWTSettings(secret_key="...")))
    """
    global _jwt_mgr
    _jwt_mgr = jwt_manager


def auth_manager() -> JWTManager:
    """Return the configured JWT manager (raises when unconfigured)."""
    if _jwt_mgr is None:
        raise RuntimeError("setup_auth() must be called before using auth dependencies")
    return _jwt_mgr


def _extract_bearer(request: Request) -> str:
    header = request.headers.get("Authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise AuthenticationException(message="missing or invalid bearer token")
    return token.strip()


def verify_token(request: Request) -> Principal:
    """FastAPI dependency: decode the bearer token into a ``Principal``.

    Raises:
        AuthenticationException: Missing/invalid/expired token.
    """
    token = _extract_bearer(request)
    claims = auth_manager().verify_access_token(token)
    user_id = claims.get("user_id") or claims.get("sub")
    role_value = claims.get("role")
    role = role_value if role_value is None or isinstance(role_value, str) else str(role_value)
    return Principal(
        subject=str(claims.get("sub", "")),
        user_id=str(user_id) if user_id is not None else None,
        role=role,
        scopes=[str(s) for s in (claims.get("scopes") or [])],
        tenant_id=claims.get("tenant_id"),
        claims=claims,
    )


current_principal = Annotated[Principal, Depends(verify_token)]


def require_role(required: UserRole | str):
    """Factory returning a dependency that enforces a minimum role."""

    def _dependency(principal: Principal = current_principal) -> Principal:
        if principal.role is None:
            raise AuthorizationException(message="role-less token cannot be authorized")
        try:
            current = UserRole.coerce(principal.role)
        except ValueError:
            raise AuthorizationException(message=f"role {principal.role!r} not recognized")
        minimum = required if isinstance(required, UserRole) else UserRole.coerce(required)
        PermissionChecker().require_role(current, minimum)
        return principal

    return _dependency


def require_permission(permission: str):
    """Factory returning a dependency that enforces a specific permission."""

    def _dependency(principal: Principal = current_principal) -> Principal:
        if principal.role is None:
            raise AuthorizationException(message="role-less token cannot be authorized")
        _checker.require(principal.role, permission)
        return principal

    return _dependency


def get_pagination_dependencies(
    page: int = 1,
    page_size: int = 20,
    sort_by: str | None = None,
    sort_desc: bool = False,
) -> OffsetPaginationParams:
    """FastAPI dependency factory yielding ``OffsetPaginationParams``."""
    return OffsetPaginationParams(
        page=max(1, page),
        page_size=min(100, max(1, page_size)),
        sort_by=sort_by,
        sort_desc=sort_desc,
    )


def apply_pagination_dependencies(
    page: int = 1,
    page_size: int = 20,
    sort_by: str | None = None,
    sort_desc: bool = False,
):
    """Alias of :func:`get_pagination_dependencies` for ``Depends`` usage."""
    return Depends(get_pagination_dependencies(page, page_size, sort_by, sort_desc))


__all__ = [
    "Principal",
    "setup_auth",
    "auth_manager",
    "verify_token",
    "current_principal",
    "require_role",
    "require_permission",
    "get_pagination_dependencies",
    "apply_pagination_dependencies",
]
