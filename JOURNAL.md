# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/codepath/pathreview/issues/156

**Issue title:** README scorer test fixture is too short for its own word-count assertion #156

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:** The test `test_readme_with_all_quality_signals` in `tests/unit/test_readme_scorer.py` asserts that its fixture README has `word_count > 100` and `word_count_category == "comprehensive"`, but the fixture only contained roughly 51 words. The scorer's `_score_readme` method correctly classifies content under 500 words as `"adequate"` or `"minimal"`, so the test was failing against correct scorer behavior — not a scorer bug. The fix extends the fixture to over 500 words so it legitimately reaches the `"comprehensive"` threshold, making the test actually validate what it claims to validate. This affects `tests/unit/test_readme_scorer.py` only; no production code changes are needed.

**Selection reasoning:** I chose this Tier 1 issue because it has a clearly defined scope — exactly one test method in one file needs its fixture extended, with no changes to production code. The reproduce step (`pytest tests/unit/test_readme_scorer.py -q`) was a single command and the failure message (`assert 51 > 100`) made the root cause immediately obvious. This made it a good first issue for getting familiar with the project's test structure and pre-commit pipeline before tackling larger issues.

**Branch name:** fix/156-readme-scorer-fixture-word-count

**Setup confirmation:** [x] Local environment set up — `.venv` created, dependencies installed via `pip install -e ".[dev]"`, pre-commit hooks installed, and `make test-unit` runs successfully (issue confirmed reproduced locally)

**Cohort ledger:** [ ] Issue added to cohort ledger

---

**Branch URL:** https://github.com/olivertang40/pathreview/tree/fix/156-readme-scorer-fixture-word-count

**PR URL:** https://github.com/ascherj/pathreview/pull/231
