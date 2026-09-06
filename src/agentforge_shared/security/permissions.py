"""Permission/role enforcement helpers."""

from __future__ import annotations

from collections.abc import Iterable

from agentforge_shared.constants.permissions import (
    ROLE_PERMISSIONS as ROLE_PERMISSIONS_MAP,
)
from agentforge_shared.enums.platform import UserRole
from agentforge_shared.exceptions.base import (
    AuthorizationException,
    InsufficientPermissionException,
)

from ..security.scopes import scope_matches


class PermissionChecker:
    """Role-mapped permission checks against ``constants.permissions``.

    Example::

        from agentforge_shared.security.permissions import PermissionChecker
        from agentforge_shared.enums.platform import UserRole

        checker = PermissionChecker()
        assert checker.has_permission(UserRole.ADMIN, "agent:delete")
    """

    def __init__(
        self,
        mapping: dict[str, Iterable[str]] | None = None,
        *,
        actions: str = ".-locked",
    ) -> None:
        self._mapping: dict[str, Iterable[str]] = mapping or dict(ROLE_PERMISSIONS_MAP)

    def permissions_for(self, role: UserRole | str) -> set[str]:
        """Expand a role into its granted permission set."""
        key = role.value if isinstance(role, UserRole) else role
        return set(self._mapping.get(key, ()))

    def has_permission(self, role: UserRole | str, permission: str) -> bool:
        """Whether ``permission`` is granted to ``role``."""
        granted = self.permissions_for(role)
        if "*" in granted:
            return True
        if permission in granted:
            return True
        if ":" in permission:
            resource, action = permission.split(":", 1)
            return f"{resource}:*" in granted or f"*:{action}" in granted
        return False

    def has_all(self, role: UserRole | str, permissions: Iterable[str]) -> bool:
        """Whether every permission in ``permissions`` is granted."""
        return all(self.has_permission(role, p) for p in permissions)

    def has_any(self, role: UserRole | str, permissions: Iterable[str]) -> bool:
        """Whether at least one permission in ``permissions`` is granted."""
        return any(self.has_permission(role, p) for p in permissions)

    def require(self, role: UserRole | str, permission: str) -> str:
        """Raise ``InsufficientPermissionException`` when not granted.

        Returns the permission (for chaining) on success.
        """
        if not self.has_permission(role, permission):
            raise InsufficientPermissionException(
                message=f"permission {permission!r} required",
            )
        return permission

    def require_role(self, role: UserRole | str, required: UserRole | str) -> None:
        """Raise when ``role`` is below ``required`` in the hierarchy."""
        if role == required:
            return
        if isinstance(role, UserRole) and isinstance(required, UserRole):
            hierarchy = {
                UserRole.ADMIN: 100,
                UserRole.OPERATOR: 80,
                UserRole.ANALYST: 60,
                UserRole.AUDITOR: 50,
                UserRole.USER: 40,
            }
            if hierarchy.get(role, 0) >= hierarchy.get(required, 0):
                return
        raise AuthorizationException(message=f"role {required.value!r} required")


def require_permission(role: UserRole | str, permission: str, mapping: dict[str, Iterable[str]] | None = None) -> None:
    """Stateless ``require_permission`` helper using a fresh checker."""
    PermissionChecker(mapping).require(role, permission)
    return


def has_scopes_for_resource(role: UserRole | str, resource: str, action: str, granted: Iterable[str]) -> bool:
    """Combine role and explicit scope grants for ``resource:action`` access."""
    if role == UserRole.ADMIN:
        return True
    return scope_matches(f"{resource}:{action}", granted)


__all__ = ["PermissionChecker", "require_permission", "has_scopes_for_resource"]
