"""Structured logging: configuration, context, masking, audit, and loggers."""

from .audit import AuditLogger, audit_event, audit_logger
from .config import (
    CONSOLE_PROCESSORS_NO_COLOR,
    JSON_PROCESSORS,
    configure_console_logging,
    configure_logging,
    reset_logging,
)
from .context import (
    BoundContext,
    bind_context,
    clear_context,
    context_dict,
    get_request_id,
    reset_context,
    unbind_context,
    with_context,
)
from .logger import get_logger, log_scope, logger
from .masking import (
    PARTIAL_KEYS,
    SECRET_KEYS,
    mask_sensitive_fields,
    mask_value,
    partially_mask,
    redact_dict,
)

__all__ = [
    # configuration
    "configure_logging",
    "configure_console_logging",
    "reset_logging",
    "JSON_PROCESSORS",
    "CONSOLE_PROCESSORS_NO_COLOR",
    # loggers
    "get_logger",
    "logger",
    "log_scope",
    # context
    "bind_context",
    "unbind_context",
    "clear_context",
    "reset_context",
    "context_dict",
    "get_request_id",
    "BoundContext",
    "with_context",
    # masking
    "mask_sensitive_fields",
    "mask_value",
    "partially_mask",
    "redact_dict",
    "SECRET_KEYS",
    "PARTIAL_KEYS",
    # audit
    "audit_event",
    "AuditLogger",
    "audit_logger",
]
