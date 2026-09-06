"""Prometheus metrics registry and helpers (no-op when disabled)."""

from __future__ import annotations

import time
from typing import Any

_ENABLED = False

_registry = None
_metrics: dict[str, Any] = {}


def setup_metrics(*, enabled: bool = True) -> bool:
    """Initialise the Prometheus client registry.

    Returns:
        ``True`` when metrics are active.
    """
    global _ENABLED, _registry
    if not enabled:
        _ENABLED = False
        return False
    try:
        from prometheus_client import CollectorRegistry

        _registry = CollectorRegistry()
        _ENABLED = True
        return True
    except ImportError:  # pragma: no cover
        _ENABLED = False
        return False


def is_enabled() -> bool:
    """Whether the metrics registry has been initialised."""
    return _ENABLED


def get_registry():
    """Return the Prometheus registry (may be ``None``)."""
    return _registry


def _metric(scaffold, name: str, doc: str, labels: tuple[str, ...] | None = None, **kwargs: Any):
    """Return (and cache) a registered metric."""
    key = (name, tuple(labels or ()))
    if key in _metrics:
        return _metrics[key]
    if _registry is None:
        return None
    metric = scaffold(
        name,
        doc,
        labelnames=list(labels or ()),
        registry=_registry,
        **kwargs,
    )
    _metrics[key] = metric
    return metric


def counter(name: str, doc: str = "", labels: tuple[str, ...] | None = None):
    """Get or create a Prometheus Counter."""
    from prometheus_client import Counter

    return _metric(Counter, name, doc, labels)


def histogram(name: str, doc: str = "", labels: tuple[str, ...] | None = None, buckets: list[float] | None = None):
    """Get or create a Prometheus Histogram."""
    from prometheus_client import Histogram

    kwargs = {"buckets": buckets} if buckets else {}
    return _metric(Histogram, name, doc, labels, **kwargs)


def gauge(name: str, doc: str = "", labels: tuple[str, ...] | None = None):
    """Get or create a Prometheus Gauge."""
    from prometheus_client import Gauge

    return _metric(Gauge, name, doc, labels)


# --- High-level domain metrics -------------------------------------------------


def record_execution(service: str, outcome: str, duration_seconds: float, labels: dict[str, str] | None = None) -> None:
    """Record an execution counter and duration histogram."""
    if not _ENABLED:
        return
    counter("agentforge_executions_total", "Executions attempted", ("service", "outcome")).labels(service, outcome).inc()
    histogram("agentforge_execution_duration_seconds", "Execution duration", ("service", "outcome")).labels(
        service, outcome
    ).observe(duration_seconds)


def record_api(status_code: int, method: str, path: str) -> None:
    """Record an HTTP request counter label by status/method/path."""
    if not _ENABLED:
        return
    counter("agentforge_http_requests_total", "HTTP requests", ("status", "method", "path")).labels(
        str(status_code), method, path
    ).inc()


def record_llm_call(provider: str, model: str, duration_seconds: float) -> None:
    """Record an LLM call histogram."""
    if not _ENABLED:
        return
    histogram("agentforge_llm_call_duration_seconds", "LLM call duration", ("provider", "model")).labels(
        provider, model
    ).observe(duration_seconds)


def record_db_duration(operation: str, duration_seconds: float) -> None:
    """Record a database operation histogram."""
    if not _ENABLED:
        return
    histogram("agentforge_db_operation_duration_seconds", "DB operation duration", ("operation",)).labels(
        operation
    ).observe(duration_seconds)


def record_redis_duration(operation: str, duration_seconds: float) -> None:
    """Record a Redis operation histogram."""
    if not _ENABLED:
        return
    histogram("agentforge_redis_operation_duration_seconds", "Redis operation duration", ("operation",)).labels(
        operation
    ).observe(duration_seconds)


def set_health(component: str, status: str) -> None:
    """Set a health gauge (``up``=1, else 0)."""
    if not _ENABLED:
        return
    gauge("agentforge_health", "Component health", ("component",)).labels(component).set(1 if status == "up" else 0)


def clear_metrics() -> None:
    """Drop cached metrics (used in tests)."""
    _metrics.clear()


class timed:
    """Context manager recording a metric for the wrapped block.

    Example::

        with timed("agentforge_task_duration_seconds", {"task": "summarize"}):
            run_task()
    """

    def __init__(self, name: str, labels: dict[str, str] | None = None, *, counter_name: str | None = None) -> None:
        self.name = name
        self.labels = labels or {}
        self.counter_name = counter_name

    def __enter__(self) -> timed:
        self._start = time.monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        duration = max(0.0, time.monotonic() - self._start)
        if _ENABLED:
            label_keys = tuple(self.labels.keys())
            label_values = tuple(self.labels.values())
            hist = histogram(self.name, "Block duration", label_keys)
            if hist is not None:
                hist.labels(*label_values).observe(duration)
            if self.counter_name:
                ctr = counter(self.counter_name, "Block counter", label_keys)
                if ctr is not None:
                    ctr.labels(*label_values).inc()
        return False


__all__ = [
    "setup_metrics",
    "is_enabled",
    "get_registry",
    "counter",
    "histogram",
    "gauge",
    "record_execution",
    "record_api",
    "record_llm_call",
    "record_db_duration",
    "record_redis_duration",
    "set_health",
    "clear_metrics",
    "timed",
]
