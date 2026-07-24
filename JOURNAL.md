# PathReview Contribution Journal

My running record of Module 3 work on PathReview. A new section is added each week.

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/156

**Issue title:** Fixture too short: `test_readme_with_all_quality_signals` asserts `comprehensive` but README has ~51 words

**Tier:** [x] Tier 1 [ ] Tier 2 [ ] Tier 3

**Problem summary:**
The unit test `test_readme_with_all_quality_signals` in `tests/unit/test_readme_scorer.py`
expects a high-quality README to be scored as `comprehensive`, but the sample README embedded
in the test only contains about 51 words. The scorer in `agent/tools/readme_scorer.py` is
actually behaving correctly: it labels anything under 100 words as `minimal` and only calls a
README `comprehensive` once it reaches 500+ words. So the test asserts an outcome the fixture
data can never produce, and it fails even though the scorer logic is right the defect is in
the test's fixture, not the production code. A successful fix expands the fixture README to a
realistic length (500+ words) while preserving all of its quality signals (installation, usage,
badges, a demo link, and a tech-stack section), so every assertion passes and the suite
reflects the scorer's true behavior.

**"Is this right for me?" checklist reasoning:**

- **Scope is small and contained:** the change is limited to one fixture string in a single
  test file. No production or runtime code changes, no database, no API, and no frontend,
  so the risk of breaking unrelated behavior is very low.
- **I understand the root cause:** I can reproduce the failure locally (`assert 51 > 100`) and
  I've traced it to the word-count thresholds in the scorer, the fixture is simply too short
  for the `comprehensive` category (which needs 500+ words), not a scorer bug.
- **Effort fits Tier 1:** this is a self-contained test fix I can complete and verify with
  `make test-unit` and `make check` well within the module window — appropriate for a first
  contribution to a large codebase.
- **Clear done criteria:** success is unambiguous — the previously failing test passes and the
  rest of the `readme_scorer` suite stays green.

**Branch name:** `fix/156-readme-scorer-fixture`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [REPRO_COMMIT_URL](https://github.com/sid-pandya/pathreview/commit/5e9df91223f4ddf453ff9c72e4b64bb8cee30e3d)

**Reproduction summary:**
I reproduced the bug by running the single failing test:
`.venv/bin/python -m pytest tests/unit/test_readme_scorer.py::TestReadmeScorer::test_readme_with_all_quality_signals -q`.
It fails at `assert data["word_count"] > 100` with `assert 51 > 100`, and the scorer logs
`category=minimal word_count=51`. This confirms the fixture README is only 51 words, so it can
never reach the `comprehensive` category (which requires >= 500 words) that the test asserts.
The scorer is behaving correctly; the defect is in the test fixture. (I also found and reverted
a stray uncommitted edit that had pasted notes into the fixture, pushing it to 101 words, which
still failed at `assert 'adequate' == 'comprehensive'` because 101 words is still below 500.)

**PLAN.md link:** https://github.com/sid-pandya/pathreview/blob/fix/156-readme-scorer-fixture/PLAN.md

**Walkthrough video (recommended):** not recorded (optional; may record and share in Slack)

**Blockers or open questions:**
None blocking. Open question: how far above 500 words to pad the fixture so it stays
`comprehensive` without becoming noisy. I will confirm the exact `str.split()` count by running
pytest rather than estimating, since code fences and markdown syntax also count as words.
