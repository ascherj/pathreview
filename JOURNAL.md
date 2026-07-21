# PathReview Contribution Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/156

**Issue title:** README scorer test fixture is too short for its own word-count assertion

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
A README scorer unit test uses a sample README that does not contain enough words to satisfy the word-count assertion being tested. As a result, the test fails because its fixture does not represent the scenario that the assertion expects. This affects the README scorer tests in the agent portion of the codebase. A successful fix will update the test fixture with sufficient realistic content so the assertion can evaluate the intended scorer behavior correctly.

**Branch name:** `test/156-fix-readme-scorer-fixture`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger


## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/guillermobermejo/pathreview/commit/8a25c1b

**Reproduction summary:**
I reproduced the issue by running the `test_readme_with_all_quality_signals` test individually with pytest. The test failed because the fixture contained only 51 words, causing the scorer to categorize it as `minimal` while the test expected more than 100 words and the `comprehensive` category.

**PLAN.md link:** https://github.com/guillermobermejo/pathreview/blob/test/156-fix-readme-scorer-fixture/PLAN.md

**Walkthrough video (recommended):** Not completed (optional)

**Blockers or open questions:**
The existing test asserts that the word count is greater than 100, but the scorer requires at least 500 words for the `comprehensive` category. My current plan is to expand the fixture beyond 500 words while preserving all existing quality signals, but I may confirm whether the maintainers also want the word-count assertion aligned with the comprehensive threshold.