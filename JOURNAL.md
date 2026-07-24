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

## Week 10 - Iteration & reflection



### Reviewer feedback

**Feedback received:** [x] Yes  [ ] No

 

**Summary of feedback:**

AI01010 left a comment on PR #278 on July 23, 2026. They pointed out:

1. The PR title ("Test/156 readme scorer fixture length") doesn't follow the Conventional Commits style used in the actual commit messages (e.g., `test(agent): ...`), per CONTRIBUTING.md.

2. The fixture word count jump from 51 to 599 words is large, and a reviewer might ask whether something closer to 550 would have worked, or whether 599 was arbitrary — worth explaining the margin choice explicitly in the PR itself (it was only in PLAN.md).

3. The claim that integration tests weren't run because "this change has no integration surface" was asserted rather than confirmed — a stricter reviewer might want proof that no integration suite imports this fixture.

**How you responded:**

I addressed point 1 by editing the PR title to match the Conventional Commits format used elsewhere in the repo. For point 2, I explained my reasoning in a reply comment: the 599-word choice was intentional margin, not arbitrary — since the scorer's threshold is >= 500, I aimed for roughly 100 words of buffer so that minor future edits to the fixture couldn't accidentally drop it back under the threshold and reintroduce the original bug. For point 3, rather than leaving it as an unverified assumption, I actually checked it and reported back: I ran `grep -rn "test_readme_scorer|readme_scorer" tests/integration/`, which returned no matches, confirming the fixture isn't referenced outside the unit test file — and I updated the PR description to reflect that this was verified, not just assumed.

 

---



### Reflection

**What was harder than you expected?**

The environment setup took far longer than the actual code fix. I'm on

Windows, so I had to install WSL, then Docker Desktop with WSL

integration, then hit a Postgres port conflict, then a Node.js path

issue where npm was accidentally running through Windows instead of

Linux and failing on UNC paths. The actual bug fix, extending a test

fixture from 51 to 599 words, took maybe 15 minutes once the

environment worked. I underestimated how much of "contributing to a

codebase" is actually "getting the codebase to run" in the first place.

**What did you learn about working in a large codebase?**

I learned that a plan can be wrong the moment you actually read the

code, and that's fine as long as you catch it before writing the fix.

My PLAN.md initially assumed I just needed to push the fixture past

100 words per the issue text, but reading agent/tools/readme_scorer.py

directly showed the "comprehensive" category actually required 500+

words. If I'd trusted the issue description alone, I would have shipped

a fix that still failed. Reading the actual source before touching

anything, rather than working purely off the issue's summary, felt

like the single most important habit this module reinforced.

**How did AI tools help - and where did they fall short?**

AI was most useful for the parts that are tedious but not judgment

calls: writing Conventional Commits messages, drafting the PR

template sections in the project's format, and debugging environment

errors one at a time through the make/Docker/npm chain. Where it fell

short was scope discovery. I had to be the one to actually run the

test, read the failure output, and open readme_scorer.py to find the

real 500-word threshold. The verification step, actually running

pytest and reading the log line showing word_count and category, was

something I had to do and interpret myself.

**What would you do differently if you started over?**

I would read the actual scorer implementation before writing PLAN.md,

not after starting to reproduce the issue. I did read it, but only

once I was already deep into the reproduction step, which meant

redoing some of my mental model of the fix. I would also request peer

review earlier in the week rather than at the very end, since Week 9's

instructions specifically say to open a draft PR early for feedback,

and I only opened mine once the fix was already complete.

**What are you most proud of from this module?**

Getting a fully broken WSL/Docker/Node environment working from

scratch, on a strict deadline, without giving up on the first few

failures: make not found, Postgres not reachable, npm running through

the wrong OS entirely. Each failure had a real, findable cause once I

looked closely rather than assumed the whole approach was wrong. That

persistence mattered more here than the actual test fix itself did.

