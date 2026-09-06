"""Integration-related enumerations."""

from __future__ import annotations

from .base import StringEnum


class IntegrationType(StringEnum):
    """Types of external integrations."""

    SLACK = "slack"
    DISCORD = "discord"
    GITHUB = "github"
    JIRA = "jira"
    LINEAR = "linear"
    NOTION = "notion"
    CONFLUENCE = "confluence"
    SALESFORCE = "salesforce"
    HUBSPOT = "hubspot"
    ZAPIER = "zapier"
    PAGERDUTY = "pagerduty"
    WEBHOOK = "webhook"
    EMAIL = "email"
    SMS = "sms"
    OTHER = "other"


class IntegrationStatus(StringEnum):
    """Connectivity state of an integration."""

    UNVERIFIED = "unverified"
    ACTIVE = "active"
    DISABLED = "disabled"
    ERROR = "error"
    REVOKED = "revoked"
    EXPIRED = "expired"


class IntegrationAuthType(StringEnum):
    """Authentication mechanisms supported by integrations."""

    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    BASIC = "basic"
    BEARER = "bearer"
    SIGNATURE = "signature"
    NONE = "none"

    # Legacy alias matching the first release.
    OAUTH = "oauth2"


class WebhookEventStatus(StringEnum):
    """Delivery state of an outbound webhook."""

    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"
    DROPPED = "dropped"
