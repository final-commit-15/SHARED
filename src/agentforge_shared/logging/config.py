"""Structured logging configuration built on ``structlog``."""

from __future__ import annotations

import logging
import sys

import structlog

from agentforge_shared.enums.platform import LogLevel

from ..logging.context import context_dict, reset_context
from ..logging.masking import (
    SECRET_KEYS as MASK_KEYS,  # noqa: F401  (re-export)
    mask_sensitive_fields,
)


def _drop_empty_kwargs(_logger: logging.Logger, _method_name: str, event_dict: dict) -> dict:
    """Strip ``None``-valued and empty-list context fields."""
    return {k: v for k, v in event_dict.items() if v is not None and v != () and v != []}


def _to_numeric_level(level: str | int | LogLevel) -> int:
    if isinstance(level, LogLevel):
        return getattr(logging, level.value.upper(), logging.INFO)
    if isinstance(level, int):
        return level
    return getattr(logging, level.upper(), logging.INFO)


def configure_logging(
    *,
    level: str | int | LogLevel = "INFO",
    json: bool = True,
    cache_logger_on_first_use: bool = True,
) -> None:
    """Configure structlog and the stdlib logging root logger.

    Args:
        level: Log threshold.
        json: Emit JSON lines (``True``) or pretty console output (``False``).
        cache_logger_on_first_use: Reuse loggers for performance.

    Example::

        from agentforge_shared.logging.config import configure_logging

        configure_logging(level="INFO", json=True)
    """
    numeric = _to_numeric_level(level)
    processors: list = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        _drop_empty_kwargs,
        mask_sensitive_fields,
    ]
    if json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty()))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(numeric),
        logger_factory=structlog.PrintLoggerFactory(sys.stdout),
        cache_logger_on_first_use=cache_logger_on_first_use,
    )
    logging.basicConfig(level=numeric, format="%(message)s", stream=sys.stdout)


def configure_console_logging(*, level: str | int = "INFO", colors: bool = True) -> None:
    """Configure pretty console (human) logging without JSON output."""
    configure_logging(level=level, json=False)
    if not colors:
        structlog.configure(
            processors=CONSOLE_PROCESSORS_NO_COLOR,
        )


#: JSON-rendered processor chain (reused by tests and custom setups).
JSON_PROCESSORS: list = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    _drop_empty_kwargs,
    mask_sensitive_fields,
    structlog.processors.JSONRenderer(),
]

#: Pretty-print processor chain (no ANSI colors).
CONSOLE_PROCESSORS_NO_COLOR: list = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="%H:%M:%S", utc=True),
    _drop_empty_kwargs,
    mask_sensitive_fields,
    structlog.dev.ConsoleRenderer(colors=False),
]


def reset_logging() -> None:
    """Restore a blank logging state (used between tests)."""
    structlog.reset_defaults()
    reset_context()


__all__ = [
    "configure_logging",
    "configure_console_logging",
    "reset_logging",
    "JSON_PROCESSORS",
    "CONSOLE_PROCESSORS_NO_COLOR",
    "MASK_KEYS",
    "context_dict",
]
