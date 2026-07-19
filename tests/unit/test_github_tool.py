"""Tests for github_tool.py

Reproduction + regression coverage for issue #41 (manifest C-01):
"`github_tool.py` raises `KeyError` when a repository has no description".

Reported failure
----------------
The issue states the tool accesses ``repo_data['description'].strip()``
directly, so a repository whose GitHub API response has a ``null`` description
(or no ``description`` key at all) triggers an unhandled ``KeyError`` /
``AttributeError`` and the whole repo-analysis step crashes.

Reproduction finding (Week 8)
-----------------------------
Reproducing the reported access pattern against a real-shaped
"repo with no description" payload confirms the failure class is real:

    >>> {"name": "r", "description": None}["description"].strip()
    AttributeError: 'NoneType' object has no attribute 'strip'
    >>> {"name": "r"}["description"].strip()
    KeyError: 'description'

However, the tool's *current* extraction in ``_fetch_repo_metadata`` already
guards the value with ``repo_json.get("description") or ""``, so
``GitHubTool.execute`` no longer crashes on a null/missing description — it
returns ``description == ""``. What is missing is (a) any test locking that
behaviour in so it cannot silently regress, and (b) the whitespace
normalisation implied by the reported ``.strip()`` (the guard returns the raw
value, un-stripped). See PLAN.md.

``test_reported_pattern_reproduces_issue_41`` reproduces the reported crash.
The ``execute`` tests below are the regression lock. The Week 9 fix restores the
null-safe ``.strip()`` normalisation, so ``...description_is_stripped`` now passes.
"""

from unittest.mock import patch

import pytest

from agent.tools.github_tool import GitHubTool


def _repo_payload(**overrides) -> dict:
    """A GitHub REST repo payload shaped like the real API response."""
    payload = {
        "name": "my-repo",
        "description": "A useful repository",
        "language": "Python",
        "stargazers_count": 3,
        "forks_count": 1,
        "open_issues_count": 0,
        "pushed_at": "2024-01-01T00:00:00Z",
        "topics": [],
        "homepage": None,
    }
    payload.update(overrides)
    return payload


class _FakeResponse:
    def __init__(self, payload: dict, status: int = 200):
        self._payload = payload
        self.status_code = status

    def json(self) -> dict:
        return self._payload

    def raise_for_status(self) -> None:
        pass


@pytest.mark.unit
class TestGitHubToolDescriptionHandling:
    """Issue #41 — repositories with a null/missing description."""

    @pytest.fixture
    def tool(self):
        return GitHubTool()

    @pytest.mark.parametrize(
        "payload, expected_exc",
        [
            ({"name": "r", "description": None}, AttributeError),  # null value
            ({"name": "r"}, KeyError),  # key absent
        ],
    )
    def test_reported_pattern_reproduces_issue_41(self, payload, expected_exc):
        """Reproduce the exact crash the issue reports: repo_data['description'].strip()."""
        with pytest.raises(expected_exc):
            _ = payload["description"].strip()

    def test_execute_null_description_does_not_crash(self, tool):
        """A repo with description=null must degrade to "" instead of crashing."""
        with (
            patch(
                "agent.tools.github_tool.httpx.get",
                return_value=_FakeResponse(_repo_payload(description=None)),
            ),
            patch.object(GitHubTool, "_has_readme", return_value=True),
        ):
            result = tool.execute({"github_username": "octocat", "repo_name": "my-repo"})

        assert result.success is True
        assert result.error is None
        assert result.data["description"] == ""

    def test_execute_missing_description_key_does_not_crash(self, tool):
        """A payload with no description key at all must also degrade to ""."""
        payload = _repo_payload()
        del payload["description"]
        with (
            patch("agent.tools.github_tool.httpx.get", return_value=_FakeResponse(payload)),
            patch.object(GitHubTool, "_has_readme", return_value=True),
        ):
            result = tool.execute({"github_username": "octocat", "repo_name": "my-repo"})

        assert result.success is True
        assert result.data["description"] == ""

    def test_execute_preserves_present_description(self, tool):
        """A normal description must still be passed through unchanged."""
        with (
            patch(
                "agent.tools.github_tool.httpx.get",
                return_value=_FakeResponse(_repo_payload(description="Hello world")),
            ),
            patch.object(GitHubTool, "_has_readme", return_value=True),
        ):
            result = tool.execute({"github_username": "octocat", "repo_name": "my-repo"})

        assert result.data["description"] == "Hello world"

    def test_execute_description_is_stripped(self, tool):
        """The fix restores null-safe whitespace stripping of the description (issue #41)."""
        with (
            patch(
                "agent.tools.github_tool.httpx.get",
                return_value=_FakeResponse(_repo_payload(description="  padded  ")),
            ),
            patch.object(GitHubTool, "_has_readme", return_value=True),
        ):
            result = tool.execute({"github_username": "octocat", "repo_name": "my-repo"})

        assert result.data["description"] == "padded"
