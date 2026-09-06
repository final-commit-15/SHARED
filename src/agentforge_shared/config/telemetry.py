"""OpenTelemetry and Prometheus settings."""

from __future__ import annotations

from pydantic import Field, field_validator

from .settings import BaseAgentForgeSettings, settings_config


class TelemetrySettings(BaseAgentForgeSettings):
    """Settings controlling tracing, metrics and instrumentation."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="OTEL_")

    service_name: str = Field(default="agentforge-service")
    service_version: str = Field(default="0.1.0")
    environment: str = Field(default="development")
    traces_exporter: str = Field(default="console", description="otlp | jaeger | console | none")
    metrics_exporter: str = Field(default="console", description="otlp | console | none")
    exporter_otlp_endpoint: str = Field(default="http://localhost:4317")
    exporter_otlp_headers: str = Field(default="", description="Comma-separated 'k=v' headers.")
    sample_ratio: float = Field(default=0.1, ge=0.0, le=1.0, description="Trace sampling ratio.")
    resource_attributes: str = Field(default="", description="Comma-separated 'key=value' resource attributes.")

    @field_validator("sample_ratio")
    @classmethod
    def _clamp_ratio(cls, value: float) -> float:
        return max(0.0, min(1.0, value))

    @property
    def tracing_enabled(self) -> bool:
        """Return ``True`` when an OTLP/jaeger exporter is configured."""
        return self.traces_exporter.lower() not in {"none", ""}

    @property
    def metrics_enabled(self) -> bool:
        """Return ``True`` when metrics export is not disabled."""
        return self.metrics_exporter.lower() not in {"none", ""}


class PrometheusSettings(BaseAgentForgeSettings):
    """Settings for the embedded Prometheus metrics registry."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="PROMETHEUS_")

    enabled: bool = Field(default=True)
    prefix: str = Field(default="agentforge_")
    metrics_path: str = Field(default="/metrics")
    namespace: str = Field(default="")
    subsystem: str = Field(default="")
    max_metric_name_length: int = Field(default=200, ge=50)


class ObservabilitySettings(BaseAgentForgeSettings):
    """Aggregate observability settings (tracing + metrics)."""

    model_config = settings_config(BaseAgentForgeSettings.model_config, env_prefix="OBS_")

    telemetry: TelemetrySettings = Field(default_factory=TelemetrySettings)
    prometheus: PrometheusSettings = Field(default_factory=PrometheusSettings)
