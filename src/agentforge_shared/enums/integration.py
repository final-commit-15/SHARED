"""Integration-related enumerations."""

from enum import Enum


class IntegrationType(str, Enum):
    """Types of external integrations."""
    SLACK = "slack"
    DISCORD = "discord"
    GITHUB = "github"
    JIRA = "jira"
    WEBHOOK = "webhook"
    OTHER = "other"