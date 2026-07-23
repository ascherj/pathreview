"""Test demonstrating the agent state persistence issue (Issue #47).

This test shows that ContextManager results are lost when the Orchestrator
is re-initialized, simulating what happens on an API restart during a
long-running review.
"""

from unittest.mock import MagicMock

from agent.memory.context_manager import ContextManager
from agent.memory.session_store import SessionStore
from agent.orchestrator import Orchestrator


class MockTool:
    """Mock tool for testing."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.execution_count = 0

    def execute(self, input_data: dict) -> dict:
        """Execute mock tool."""
        self.execution_count += 1
        return {
            "result": f"Result from {self.name}",
            "input_hash": ContextManager.hash_input(input_data),
        }


def test_context_manager_memory_lost_on_restart() -> None:
    """REPRODUCTION: Demonstrate that ContextManager results are lost on restart.

    This test simulates:
    1. First orchestrator run stores cached results in memory
    2. Orchestrator is re-initialized (simulating server restart)
    3. New orchestrator has empty ContextManager
    4. Same tool execution doesn't hit the cache (BUG)
    """
    # Setup: Create first orchestrator and execute a tool
    mock_tool = MockTool("github_tool")
    tools = {"github_tool": mock_tool}

    orchestrator_1 = Orchestrator(tools=tools)
    tool_input = {"repo": "test-repo", "username": "test-user"}
    input_hash = ContextManager.hash_input(tool_input)

    # First execution: tool runs, result is cached in memory
    orchestrator_1._execute_tool("github_tool", tool_input)
    assert mock_tool.execution_count == 1
    assert orchestrator_1.context_manager.get_tool_result("github_tool", input_hash) is not None

    # Simulate server restart: Create new Orchestrator instance
    # (In real scenario, this is what happens when the API process restarts)
    orchestrator_2 = Orchestrator(tools=tools)

    # BUG: New orchestrator has empty ContextManager
    assert len(orchestrator_2.context_manager.results) == 0

    # Second execution: tool runs AGAIN because cache is empty
    # Even though we have the exact same input, we don't hit the cache
    orchestrator_2._execute_tool("github_tool", tool_input)
    assert mock_tool.execution_count == 2  # Tool executed twice instead of once!

    # In a long-running review (5+ repositories), this repeated re-execution
    # causes:
    # - Loss of progress if the server restarts mid-review
    # - Wasted API calls and compute
    # - User loses all cached results


def test_session_store_persists_results_but_not_context_cache() -> None:
    """REPRODUCTION: Show SessionStore persists some state but not ContextManager cache.

    This demonstrates the gap: SessionStore saves tool_results to Redis,
    but ContextManager cache is not synchronized with Redis.
    """
    # Setup
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    mock_redis.setex.return_value = True

    session_store = SessionStore(mock_redis)
    mock_tool = MockTool("readme_scorer")
    tools = {"readme_scorer": mock_tool}

    # Create orchestrator with session store
    orchestrator = Orchestrator(tools=tools, session_store=session_store)

    profile_id = "profile-123"
    profile_data = {
        "readme_content": "# My Project\nGreat project!",
        "github_username": "testuser",
    }

    # Run orchestrator (executes and caches results)
    orchestrator.run(profile_id, profile_data)

    # SessionStore saves tool_results to Redis
    assert mock_redis.setex.called

    # BUT: If we restart and re-initialize Orchestrator,
    # the ContextManager cache is empty even though SessionStore has data
    # The cached_results in context_manager are not persisted/restored

    orchestrator_2 = Orchestrator(tools=tools, session_store=session_store)

    # This new orchestrator has empty context cache
    assert len(orchestrator_2.context_manager.results) == 0
    # Even though SessionStore could theoretically retrieve it


if __name__ == "__main__":
    test_context_manager_memory_lost_on_restart()
    test_session_store_persists_results_but_not_context_cache()
    print("✓ Reproduction tests pass - Issue #47 confirmed")
