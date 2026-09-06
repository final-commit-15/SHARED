"""Audit logging for compliance-critical actions."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from agentforge_shared.enums.platform import AuditAction
from agentforge_shared.logging.masking import redact_dict
from agentforge_shared.utils.datetime_helpers import utc_now

from ..logging.logger import get_logger

_audit = get_logger("agentforge.audit")


def audit_event(
    action: AuditAction | str,
    *,
    actor_id: str | None = None,
    target_type: str | None = None,
    target_id: str | None = None,
    tenant_id: str | None = None,
    ip_address: str | None = None,
    outcome: str = "success",
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    occurred_at: datetime | None = None,
) -> None:
    """Emit a structured audit log entry.

    Secrets inside ``before``/``after`` are redacted before emitting.

    Example::

        from agentforge_shared.enums.platform import AuditAction
        from agentforge_shared.logging.audit import audit_event

        audit_event(AuditAction.UPDATE, actor_id="u1", target_type="agent", target_id="ag-1")
    """
    action_value = action.value if isinstance(action, AuditAction) else str(action)
    payload: dict[str, Any] = {
        "audit": True,
        "action": action_value,
        "outcome": outcome,
        "actor_id": actor_id,
        "target_type": target_type,
        "target_id": target_id,
        "tenant_id": tenant_id,
        "ip_address": ip_address,
        "occurred_at": (occurred_at or utc_now()).isoformat(),
    }
    if before is not None:
        payload["before"] = redact_dict(before)
    if after is not None:
        payload["after"] = redact_dict(after)
    if metadata:
        payload["metadata"] = metadata
    _audit.info("audit", **payload)


class AuditLogger:
    """Thin wrapper making audit emission convenient in services."""

    def __init__(self, *, default_actor: str | None = None, default_tenant: str | None = None) -> None:
        self.default_actor = default_actor
        self.default_tenant = default_tenant

    def record(self, action: AuditAction | str, **kwargs: Any) -> None:
        """Record one audit entry with defaults applied."""
        audit_event(
            action,
            actor_id=kwargs.pop("actor_id", self.default_actor),
            tenant_id=kwargs.pop("tenant_id", self.default_tenant),
            **kwargs,
        )

    def record_change(self, *, target_type: str, target_id: str, before: dict, after: dict, **kwargs: Any) -> None:
        """Record a state-change audit entry with before/after snapshots."""
        self.record(
            AuditAction.UPDATE,
            target_type=target_type,
            target_id=target_id,
            before=before,
            after=after,
            **kwargs,
        )


audit_logger = AuditLogger()

__all__ = ["audit_event", "AuditLogger", "audit_logger"]
