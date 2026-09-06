"""Logger factory for structlog-bound loggers."""

from __future__ import annotations

import structlog

from ..logging.config import configure_logging  # noqa: F401  (re-export for convenience)
from ..logging.context import BoundContext


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a structlog logger bound to the current context.

    Args:
        name: Logger name; ``None`` derives a module-level logger.

    Returns:
        Bound logger supporting ``.info/.warning/.error/...`` with kwargs.
    """
    if name is None:
        import __main__

        name = getattr(__main__, "__name__", "agentforge")
    return structlog.get_logger(name=name)


logger = get_logger("agentforge")


def log_scope(**bindings: object):  # type: ignore[no-untyped-def]
    """Create a scoped logger bound to ``bindings`` for a block.

    The context is restored when the block exits.

    Example::

        with log_scope(execution_id="e1", agent_id="a1") as log:
            log.info("started")
    """
    ctx = BoundContext(**bindings)

    class _Scope(BoundContext):
        def __enter__(self):
            ctx.__enter__()
            return get_logger()

        def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
            return ctx.__exit__(exc_type, exc_val, exc_tb)

    return _Scope()


__all__ = ["get_logger", "logger", "log_scope"]
