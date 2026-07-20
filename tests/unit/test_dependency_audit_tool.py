"""Reproduction test for issue #53: missing dependency audit agent tool."""

import importlib


def test_dependency_audit_tool_is_available_for_agent_reviews():
    """DependencyAuditTool should exist so the agent can audit project dependencies."""
    module = importlib.import_module("agent.tools.dependency_audit_tool")

    tool_class = getattr(module, "DependencyAuditTool")
    tool = tool_class()

    assert tool.name == "dependency_audit"
