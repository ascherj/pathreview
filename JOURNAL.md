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