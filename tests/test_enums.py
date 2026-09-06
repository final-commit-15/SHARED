"""Enum consistency tests."""

from agentforge_shared.enums.agent import AgentStatus
from agentforge_shared.enums.execution import ExecutionStatus
from agentforge_shared.enums.integration import IntegrationType


def test_agent_status_values():
    assert AgentStatus.DRAFT == "draft"
    assert AgentStatus.ACTIVE == "active"


def test_execution_status_values():
    assert ExecutionStatus.PENDING == "pending"
    assert ExecutionStatus.COMPLETED == "completed"


def test_integration_type_values():
    assert IntegrationType.SLACK == "slack"
    assert IntegrationType.OTHER == "other"
