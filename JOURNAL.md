## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/156

**Issue title:** README scorer test fixture is too short for its own word-count assertion

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Why this fits:** I chose a Tier 1 issue because this is my first time working
in a codebase this size (multi-service Python + React with FastAPI, Postgres,
Redis, and a vector store), and I wanted my first contribution to be scoped
enough that I could understand the entire problem — not just patch around it.
Issue #156 touches exactly one test file and one fixture, with no cross-module
dependencies, an existing test that already defines the expected behavior, and
a clear reproduction command (`pytest tests/unit/test_readme_scorer.py -q`).
That combination meant I could verify I understood both the bug and the fix
before writing any code, which felt like the right first step before taking on
an issue that requires tracing logic across multiple files or modules.

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
