"""Telemetry: tracing (OpenTelemetry) and metrics (Prometheus)."""

from .metrics import (
    clear_metrics,
    counter,
    gauge,
    get_registry,
    histogram,
    is_enabled as metrics_enabled,
    record_api,
    record_db_duration,
    record_execution,
    record_llm_call,
    record_redis_duration,
    set_health,
    setup_metrics,
    timed,
)
from .otel import (
    get_active_span_context,
    get_tracer,
    is_enabled as tracing_enabled,
    setup_otel,
    span,
    start_span,
)

__all__ = [
    # otel
    "setup_otel",
    "tracing_enabled",
    "get_tracer",
    "start_span",
    "get_active_span_context",
    "span",
    # prometheus
    "setup_metrics",
    "metrics_enabled",
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
