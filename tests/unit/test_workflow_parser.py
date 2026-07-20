"""Tests for workflow_parser.py (issue #14)."""

import pytest

from ingestion.parsers.base import ParseResult
from ingestion.parsers.workflow_parser import WorkflowParser

PYTHON_CI = """
name: CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -v
      - run: ruff check .
"""

DOCKER_DEPLOY = """
name: Deploy
on:
  push:
    branches: [main]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
      - run: docker push my/image:latest
"""


@pytest.fixture
def parser():
    return WorkflowParser()


@pytest.mark.unit
class TestWorkflowParser:
    """Test suite for WorkflowParser."""

    def test_returns_parse_result(self, parser):
        result = parser.parse(PYTHON_CI)
        assert isinstance(result, ParseResult)
        assert result.source_type == "github_actions_workflow"

    def test_detects_github_actions_for_any_valid_workflow(self, parser):
        result = parser.parse(PYTHON_CI)
        assert "GitHub Actions" in result.metadata["ci_cd_skills"]

    def test_detects_python_ci_from_setup_action(self, parser):
        result = parser.parse(PYTHON_CI)
        assert "Python CI" in result.metadata["ci_cd_skills"]

    def test_detects_testing_and_linting_from_run_steps(self, parser):
        result = parser.parse(PYTHON_CI)
        skills = result.metadata["ci_cd_skills"]
        assert "Testing" in skills
        assert "Linting" in skills

    def test_detects_docker_from_action_and_run(self, parser):
        result = parser.parse(DOCKER_DEPLOY)
        assert "Docker" in result.metadata["ci_cd_skills"]

    def test_list_triggers_extracted(self, parser):
        result = parser.parse(PYTHON_CI)
        assert result.metadata["triggers"] == ["push", "pull_request"]

    def test_mapping_trigger_extracted_despite_yaml_boolean_on_key(self, parser):
        # YAML reads a bare `on:` as boolean True; the parser must still find it.
        result = parser.parse(DOCKER_DEPLOY)
        assert result.metadata["triggers"] == ["push"]

    def test_actions_used_recorded_without_version_suffix(self, parser):
        result = parser.parse(DOCKER_DEPLOY)
        assert "actions/checkout" in result.metadata["actions_used"]
        assert "docker/build-push-action" in result.metadata["actions_used"]

    def test_job_count(self, parser):
        result = parser.parse(PYTHON_CI)
        assert result.metadata["job_count"] == 1

    def test_skills_are_sorted_and_unique(self, parser):
        result = parser.parse(PYTHON_CI)
        skills = result.metadata["ci_cd_skills"]
        assert skills == sorted(skills)
        assert len(skills) == len(set(skills))

    def test_accepts_bytes_input(self, parser):
        result = parser.parse(PYTHON_CI.encode("utf-8"))
        assert "Python CI" in result.metadata["ci_cd_skills"]

    def test_summary_text_mentions_skills(self, parser):
        result = parser.parse(PYTHON_CI)
        assert "CI/CD skills" in result.text
        assert "Python CI" in result.text

    def test_kubectl_run_maps_to_kubernetes(self, parser):
        workflow = """
on: [push]
jobs:
  deploy:
    steps:
      - run: kubectl apply -f manifest.yaml
"""
        result = parser.parse(workflow)
        assert "Kubernetes" in result.metadata["ci_cd_skills"]

    def test_invalid_yaml_raises_value_error(self, parser):
        with pytest.raises(ValueError):
            parser.parse("on: [push\njobs: : :")

    def test_non_mapping_content_raises_value_error(self, parser):
        with pytest.raises(ValueError):
            parser.parse("just a plain string")

    def test_missing_jobs_raises_value_error(self, parser):
        with pytest.raises(ValueError):
            parser.parse("on: [push]\nname: CI")

    def test_steps_without_uses_or_run_are_ignored(self, parser):
        workflow = """
on: [push]
jobs:
  noop:
    steps:
      - name: A step with no action or command
"""
        result = parser.parse(workflow)
        # Only the baseline GitHub Actions skill is present.
        assert result.metadata["ci_cd_skills"] == ["GitHub Actions"]
