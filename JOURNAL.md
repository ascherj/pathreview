## Week 7 — Issue selection

**Issue link:** (https://github.com/ascherj/pathreview/issues/59)

**Issue title:** Add an end-to-end agent test using a fully stubbed tool suite

**Tier:** [ ] Tier 1  [ ] Tier 2  [ x ] Tier 3

**Problem summary:**
[In 3–5 sentences, in your own words: what the issue is (not a copy-paste of
the title), what is currently broken or missing, and what a successful fix
would accomplish. Naming the part of the codebase it affects is helpful context.]

Adding integration test for the full agent lifecycle. Given is a major component of this application, we'd want to these tests to run after every PR to ensure our agent lifeceycle is not broken during any code contribution or feature development. Integration tests allow us to catch mistakes before merging it into main/master/develop branch and shortens the feedback cycle.

**Branch name:** test/59-end-to-end-agent-test

**Setup confirmation:** [ x ] App runs locally at localhost:5173

**Cohort ledger:** [ x ] Issue added to cohort ledger

## Initial State - Before working on anything
- Ran unit test suite, 35 failing before any work is done
