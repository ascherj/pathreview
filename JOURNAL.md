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
