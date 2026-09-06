"""Platform-wide enumerations: users, notifications, health, audit, environment."""

from __future__ import annotations

from .base import StringEnum


class Environment(StringEnum):
    """Deployment environments supported by the platform."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

    @classmethod
    def from_value(cls, value: str | None) -> Environment:
        """Coerce an arbitrary string, defaulting to development."""
        return cls.coerce(value) or cls.DEVELOPMENT


class UserRole(StringEnum):
    """Roles a principal may hold."""

    SYSTEM = "system"
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    OPERATOR = "operator"
    AUDITOR = "auditor"
    AGENT_DEVELOPER = "agent_developer"
    AGENT_OPERATOR = "agent_operator"
    WORKFLOW_EDITOR = "workflow_editor"
    ORG_OWNER = "org_owner"
    ORG_ADMIN = "org_admin"
    ORG_MEMBER = "org_member"
    CONTRIBUTOR = "contributor"
    REVIEWER = "reviewer"
    VIEWER = "viewer"
    USER = "user"
    PENDING = "pending"
    ANONYMOUS = "anonymous"
    SERVICE_ACCOUNT = "service_account"

    @classmethod
    def is_admin(cls, role: str) -> bool:
        """Return ``True`` for roles with platform administration rights."""
        return role in {
            cls.SYSTEM.value,
            cls.SUPER_ADMIN.value,
            cls.ADMIN.value,
            cls.OPERATOR.value,
        }


class PermissionScope(StringEnum):
    """High-level scopes a token or API key can carry."""

    READ = "read"
    WRITE = "write"
    READ_WRITE = "read_write"
    ADMIN = "admin"
    EXECUTE = "execute"
    INTERNAL = "internal"


class NotificationType(StringEnum):
    """Notification kinds emitted by the platform."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class NotificationChannel(StringEnum):
    """Delivery channels for notifications."""

    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    SLACK = "slack"
    DISCORD = "discord"
    WEBHOOK = "webhook"
    IN_APP = "in_app"


class NotificationStatus(StringEnum):
    """Lifecycle of a notification."""

    QUEUED = "queued"
    DISPATCHING = "dispatching"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"
    DISMISSED = "dismissed"


class HealthStatus(StringEnum):
    """Health check outcomes."""

    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"
    STARTING = "starting"
    UNKNOWN = "unknown"


class LogLevel(StringEnum):
    """Log levels aligned with Python's logging module."""

    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditAction(StringEnum):
    """Actions recorded by the audit logger."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    IMPERSONATE = "impersonate"
    EXPORT = "export"
    IMPORT = "import"
    PUBLISH = "publish"
    DEPLOY = "deploy"
    EXECUTE = "execute"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    GRANT = "grant"
    REVOKE = "revoke"
    CONFIG_CHANGE = "config_change"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"
    MFA_ENABLE = "mfa_enable"
    MFA_DISABLE = "mfa_disable"


class SortOrder(StringEnum):
    """Sort direction for list endpoints."""

    ASC = "asc"
    DESC = "desc"


class SourceType(StringEnum):
    """Origin of a request or record."""

    API = "api"
    WEB = "web"
    MOBILE = "mobile"
    CLI = "cli"
    INTERNAL = "internal"
    SCHEDULER = "scheduler"
    WEBHOOK = "webhook"
    SYSTEM = "system"


class SenderType(StringEnum):
    """Who sent a message or triggered an event."""

    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"
    WORKFLOW = "workflow"
    INTEGRATION = "integration"
    BOT = "bot"


class IdempotencyStatus(StringEnum):
    """Outcome of an idempotency key lookup."""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    INVALID = "invalid"
