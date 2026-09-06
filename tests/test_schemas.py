"""Basic schema tests."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from agentforge_shared.enums.agent import AgentStatus, AgentType
from agentforge_shared.schemas.agent import Agent, AgentConfig
from agentforge_shared.schemas.common import APIResponse


def test_agent_creation():
    config = AgentConfig(model="gpt-4")
    agent = Agent(
        id="test-123",
        name="Test Agent",
        type=AgentType.CHAT,
        configuration=config,
        status=AgentStatus.ACTIVE,
    )
    assert agent.id == "test-123"
    assert agent.type == AgentType.CHAT
    assert agent.status == AgentStatus.ACTIVE
    assert isinstance(agent.created_at, datetime)


def test_agent_invalid_type():
    with pytest.raises(ValidationError):
        Agent(
            id="test",
            name="Invalid",
            type="unknown",  # not in enum
            configuration=AgentConfig(model="test"),
        )


def test_api_response():
    data = {"key": "value"}
    resp = APIResponse(data=data, message="Success")
    assert resp.success is True
    assert resp.data == data
