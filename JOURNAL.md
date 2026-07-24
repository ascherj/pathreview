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

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/sidhya-ganesh/pathreview/commit/891886febe90fa19a925fef97c633f7fafe324ce

**Reproduction summary:**
Ran `.venv/bin/pytest tests/unit/test_readme_scorer.py -q` and confirmed
`test_readme_with_all_quality_signals` fails with `assert 51 > 100`. The
captured log line shows `word_count=51, category=minimal`, confirming
the fixture README is far shorter than the test's own assertions require.

**PLAN.md link:** https://github.com/sidhya-ganesh/pathreview/blob/test/156-readme-scorer-fixture-length/PLAN.md

**Walkthrough video (recommended):** Not recorded

**Blockers or open questions:**
While reading the scorer logic, I found that "comprehensive" actually
requires >=500 words, not just >100 as the issue text implies. This
means my fix will need to extend the fixture much further than a quick
read of the issue would suggest. Documented this in PLAN.md's Risks
section — no blocker, just noting the scope is slightly larger than
it first appeared.

## Week 9 - Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
Completed PLAN.md steps 1-2: re-read the existing fixture to identify
which markers had to be preserved (install/usage keywords, badges, demo
link), then extended it from 51 to 599 words by adding realistic
Configuration, Contributing, Testing, and License sections. Confirmed
via `.venv/bin/pytest tests/unit/test_readme_scorer.py -q` that all 23
tests in the file now pass (was 22/23 before).

**Next steps:**
Complete PLAN.md steps 3-5: run the full unit test suite and `make check`
to confirm no regressions outside the fixture change, document any
pre-existing failures, then open the PR with a fully filled template.

**Blockers:**
None.

---

### Check-in 2 (end of week)

**PR link:** https://github.com/ascherj/pathreview/pull/278

**Branch:** test/156-readme-scorer-fixture-length

**What you built:**
Extended the fixture README inside test_readme_with_all_quality_signals
from 51 words to 599 words, since the scorer categorizes word_count_category
as "comprehensive" only when word_count is 500 or higher, not just over 100
as the issue text implied. No production code changed, only the test's
own sample data.

**Tests added or updated:**
Modified tests/unit/test_readme_scorer.py. No new test was added since
the bug was in the existing test's fixture data, not missing coverage.
Verified all 23 tests in the file pass (was 22/23 before), including
test_readme_with_all_quality_signals now correctly hitting the
"comprehensive" code path with word_count=599.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes

Note: both are true for my changed file specifically. The codebase has
182 pre-existing lint errors and 52 pre-existing test failures unrelated
to test_readme_scorer.py (confirmed via git stash comparison and grep
that none reference my file), documented in the PR description.

**Draft PR feedback received from:** none
