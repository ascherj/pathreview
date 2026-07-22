"""Week 8 reproduction: offline eval runner is a stub (issue B-20).

Running `python scripts/run_evals.py` prints success and claims it wrote
`eval_results.json`, but no file is created, benchmark fixtures are missing,
and EvalSuite has no actionability score. These tests document that gap and
are expected to FAIL until Week 9 implements the runner.
"""

from pathlib import Path

import pytest

from rag.evaluator.eval_suite import EvalResult
from scripts import run_evals


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "sample_profiles"
EVAL_RESULTS = REPO_ROOT / "eval_results.json"


@pytest.mark.unit
class TestOfflineEvalRunnerGap:
    """Reproduce B-20: standalone eval runner does not produce a quality report."""

    def test_run_evals_writes_eval_results_json(self, monkeypatch, tmp_path):
        """Stub claims to write eval_results.json but does not create the file."""
        monkeypatch.chdir(tmp_path)
        run_evals.main()
        assert (tmp_path / "eval_results.json").exists(), (
            "B-20 reproduction: scripts/run_evals.py prints success but does not "
            "write eval_results.json (CI expects this file for PR comments)."
        )

    def test_benchmark_fixtures_directory_exists(self):
        """Curated benchmark portfolios under sample_profiles are missing."""
        assert FIXTURES_DIR.is_dir(), (
            "B-20 reproduction: tests/fixtures/sample_profiles/ does not exist; "
            "the runner has nowhere to load benchmark portfolios from."
        )

    def test_eval_result_includes_actionability_score(self):
        """Stub TODO scores actionability, but EvalResult has no such field."""
        assert "actionability_score" in EvalResult.__dataclass_fields__, (
            "B-20 reproduction: EvalResult lacks actionability_score; "
            "scripts/run_evals.py TODO lists actionability as a required metric."
        )
