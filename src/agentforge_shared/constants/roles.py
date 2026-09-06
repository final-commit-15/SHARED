"""Platform role identifiers.

Role values are URI-friendly stable strings persisted in the database.
Expose them as plain strings here (plus a matching ``UserRole`` enum) so
database migrations and enumerations always agree.
"""

# System
ROLE_SYSTEM = "system"
ROLE_SUPER_ADMIN = "super_admin"
ROLE_SERVICE_ACCOUNT = "service_account"

# Platform administration
ROLE_ADMIN = "admin"
ROLE_OPERATOR = "operator"
ROLE_AUDITOR = "auditor"

# Standard users
ROLE_USER = "user"
ROLE_REVIEWER = "reviewer"
ROLE_CONTRIBUTOR = "contributor"
ROLE_VIEWER = "viewer"
ROLE_PENDING = "pending"

# Domain-specific
ROLE_AGENT_DEVELOPER = "agent_developer"
ROLE_AGENT_OPERATOR = "agent_operator"
ROLE_WORKFLOW_EDITOR = "workflow_editor"
ROLE_ORG_OWNER = "org_owner"
ROLE_ORG_ADMIN = "org_admin"
ROLE_ORG_MEMBER = "org_member"
ROLE_BILLING_ADMIN = "billing_admin"

# Explicitly anonymous (internal use).
ROLE_ANONYMOUS = "anonymous"

# Ordered privilege ranking: index 0 is the most privileged.
ROLE_HIERARCHY: tuple[str, ...] = (
    ROLE_SYSTEM,
    ROLE_SUPER_ADMIN,
    ROLE_ADMIN,
    ROLE_OPERATOR,
    ROLE_AUDITOR,
    ROLE_AGENT_DEVELOPER,
    ROLE_AGENT_OPERATOR,
    ROLE_WORKFLOW_EDITOR,
    ROLE_ORG_OWNER,
    ROLE_ORG_ADMIN,
    ROLE_ORG_MEMBER,
    ROLE_CONTRIBUTOR,
    ROLE_REVIEWER,
    ROLE_VIEWER,
    ROLE_USER,
    ROLE_PENDING,
    ROLE_ANONYMOUS,
)

ALL_ROLES: frozenset[str] = frozenset(ROLE_HIERARCHY)

# Roles that are allowed to manage platform-wide resources.
ADMIN_ROLES: frozenset[str] = frozenset(
    {ROLE_SYSTEM, ROLE_SUPER_ADMIN, ROLE_ADMIN, ROLE_OPERATOR}
)

# Roles exempt from rate limiting.
RATE_LIMIT_EXEMPT_ROLES: frozenset[str] = frozenset(
    {ROLE_SYSTEM, ROLE_SERVICE_ACCOUNT, ROLE_SUPER_ADMIN}
)
