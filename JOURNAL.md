# PathReview — Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/106

**Issue title:** Shared test fixture for a sample user profile is missing from `tests/fixtures/`

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The test suite has no reusable fixture representing a sample user profile, so
tests that need profile data either invent ad-hoc `Mock` objects or duplicate
setup. For example, `tests/unit/test_review_service.py` defines its own local
`mock_profile` fixture, and `tests/conftest.py` only provides `sample_resume_text`
and `sample_readme_text` — there is no shared profile fixture and no
`tests/fixtures/` directory at all. This affects the test layer around the
`Profile` model in `core/models/profile.py` (fields: `id`, `user_id`,
`github_username`, `resume_filename`, `resume_text`, `portfolio_url`,
`created_at`, `updated_at`). A successful fix adds a shared `sample_user_profile`
fixture that mirrors the real `Profile` schema, so any test can depend on
consistent, realistic profile data instead of redefining it, reducing
duplication and drift.

**"Is this right for me?" checklist notes:**
- **Scope** — Small and well-bounded: add one shared fixture (plus a short test
  that consumes it). No production code changes required.
- **Effort** — Matches the Tier 1 estimate; a single self-contained fixture.
- **Dependencies** — None external. Runs entirely under `pytest`; no DB, API
  keys, or services needed since the fixture is in-memory data.
- **Understanding** — I verified the gap directly: no `tests/fixtures/` dir and
  no profile fixture in `conftest.py`. I read the `Profile` model to know exactly
  which fields the fixture should carry.
- **Verification** — I can prove it works with `make test-unit`.

**Branch name:** `test/106-sample-user-profile-fixture`

**Setup confirmation:** [ ] App runs locally at localhost:5173
<!-- Not yet verified: initial `make setup` stopped at the DB migration step
because the Docker services were not running. Will re-run `docker compose up -d`
then `make setup`, confirm http://localhost:5173, and check this box. -->

**Cohort ledger:** [ ] Issue added to cohort ledger
<!-- To be completed from my GitHub account using the instructor-provided ledger link. -->

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/sravanibhamidipaty/pathreview/commit/40761cc6a4243ed83c4bf3cbe91192496f449cbb

**Reproduction summary:**
I added a unit test (`tests/unit/test_sample_user_profile_fixture.py`) that
requests a `sample_user_profile` fixture and ran it with `pytest`. It fails at
setup with `fixture 'sample_user_profile' not found`, and the reported available
fixtures list shows only `sample_readme_text` and `sample_resume_text` — proving
the shared profile fixture is genuinely missing from `tests/conftest.py`.

**PLAN.md link:** https://github.com/sravanibhamidipaty/pathreview/blob/test/106-sample-user-profile-fixture/PLAN.md

**Walkthrough video (recommended):** _(not recorded)_

**Blockers or open questions:**
Open question for the maintainer: the issue title says the fixture should live in
`tests/fixtures/`, but the existing sample fixtures (`sample_resume_text`,
`sample_readme_text`) live in `tests/conftest.py`. I plan to follow the current
`conftest.py` convention and confirm in the PR. Also deciding whether the fixture
should return a transient `Profile` ORM instance vs. a plain dict — leaning toward
the `Profile` instance for production parity.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
Implemented the core of the fix from PLAN.md. Sub-tasks 1–3 are done: decided the
fixture returns a transient `Profile` ORM instance (production parity, no DB
needed), added the `sample_user_profile` fixture to `tests/conftest.py`, and
converted the Week 8 reproduction test into a passing verification test
(`tests/unit/test_sample_user_profile_fixture.py`, 4 assertions covering type,
all fields non-null, valid UUIDs, and timezone-aware timestamps).

**Next steps:**
Run the full `make check` / `make test-unit` gates to confirm no new failures,
open a draft PR for peer feedback, and finalize the PR description. Sub-task 4
(refactoring `test_review_service.py::mock_profile` to reuse the fixture) is
optional — deferring it to keep this PR focused and avoid entangling with that
file's pre-existing failures.

**Blockers:**
None. Noted that the repo ships with many pre-existing failures unrelated to
#106; documenting them so they aren't mistaken for regressions.

---

### Check-in 2 (end of week)

**PR link:** https://github.com/jamjamgobambam/pathreview/pull/133
<!-- Currently opened as a DRAFT for peer feedback. Mark "Ready for review"
before the deadline once peer/mentor feedback is addressed. -->

**Branch:** `test/106-sample-user-profile-fixture`

**What you built:**
A shared `sample_user_profile` pytest fixture in `tests/conftest.py` that returns
a deterministic, in-memory `Profile` model instance with realistic, non-null
values for every column. Any test can now inject consistent profile data via the
`sample_user_profile` parameter instead of hand-rolling mocks.

**Tests added or updated:**
`tests/unit/test_sample_user_profile_fixture.py` — 4 unit tests asserting the
fixture is a `Profile` instance, exposes all fields non-null, uses valid UUID
strings for `id`/`user_id`, and uses timezone-aware `created_at`/`updated_at`.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes
<!-- Interpreted per the assignment for a codebase with documented pre-existing
failures: my changes introduce NO new failures. Baseline before my change:
53 failing / 375 passing unit tests; ruff ~182 errors; mypy stub errors — all
pre-existing and unrelated to #106. After my change: same 53 failing, 379 passing
(4 new tests). My changed files pass ruff, black, and the mypy pre-commit hook. -->

**Draft PR feedback received from:** none yet (draft opened for peer/mentor review)
