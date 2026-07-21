# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/codepath/pathreview/issues/156

**Issue title:** README scorer test fixture is too short for its own word-count assertion #156

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:** The test `test_readme_with_all_quality_signals` in `tests/unit/test_readme_scorer.py` asserts that the fixture README has a `word_count > 100` and a `word_count_category` of `"comprehensive"`, but the fixture itself only contained roughly 51 words. The scorer's `_score_readme` method correctly categorizes content under 500 words as `"adequate"` or `"minimal"`, so the test was failing against correct scorer behavior. The fix extends the fixture to over 500 words so it legitimately reaches the `"comprehensive"` threshold, making the test validate what it was always intended to validate.

**Branch name:** fix/156-readme-scorer-fixture-word-count

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger
