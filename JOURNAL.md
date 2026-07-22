## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/156

**Issue title:** README scorer test fixture is too short for its own word-count assertion

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
There's a unit test in the README scoring module (part of the agent/ingestion
layer that analyzes a user's portfolio) that checks whether a README is long
enough to count as "comprehensive." The test provides a sample README fixture
to score, but that sample only has about 51 words, while the test itself
asserts the word count must be over 100 to earn the "comprehensive" label.
Because the fixture data doesn't actually meet the condition it's supposed to
satisfy, the test fails even though the scorer logic itself is working
correctly. A successful fix means updating the fixture (or the assertion, if
that turns out to be the better fix once I look at the code) so the test
actually exercises the "comprehensive" case it's meant to check.

**Branch name:** test/156-readme-scorer-fixture-length

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger
