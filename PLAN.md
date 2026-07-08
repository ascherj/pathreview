## Solution plan

**Issue:** Shared test fixture for a sample user profile is missing from `tests/fixtures/` — https://github.com/jamjamgobambam/pathreview/issues/106

### Understand
The test suite lacks a shared, reusable fixture that represents a realistic user
profile. Today, tests that need profile data either build one-off `Mock` objects
(e.g. the local `mock_profile` fixture in `tests/unit/test_review_service.py`) or
go without. The shared `tests/conftest.py` only exposes `sample_resume_text` and
`sample_readme_text`, and there is no `tests/fixtures/` directory at all.

- **Expected:** A shared `sample_user_profile` fixture is available to every test,
  exposing the fields defined on the `Profile` model so tests can rely on
  consistent, realistic data.
- **Actual:** No such fixture exists. A test that requests `sample_user_profile`
  errors at setup with `fixture 'sample_user_profile' not found` (see the Week 8
  reproduction commit `tests/unit/test_sample_user_profile_fixture.py`).

Root cause: the fixture was simply never authored; it is a missing test-support
asset, not a code bug.

### Map
Files/modules involved:
- `tests/conftest.py` — **add** the new `sample_user_profile` fixture here so it
  is shared across the whole suite (this is where the existing sample fixtures
  live). Primary file I expect to touch.
- `core/models/profile.py` — **read-only reference** for the exact field set:
  `id`, `user_id`, `github_username`, `resume_filename`, `resume_text`,
  `portfolio_url`, `created_at`, `updated_at`.
- `tests/unit/test_sample_user_profile_fixture.py` — **update** the Week 8
  reproduction test into a real assertion test that the fixture matches the
  `Profile` shape (turns the failing repro green).
- `tests/unit/test_review_service.py` — **optional follow-up**: its local
  `mock_profile` could be replaced by the shared fixture to prove reuse (only if
  low-risk).

### Plan
1. Decide the fixture's return shape. Return a real transient
   `core.models.profile.Profile` instance (not persisted to a DB) populated with
   deterministic sample values, so consumers get the same attribute access as
   production code. Document the choice in the fixture docstring.
2. Implement the `sample_user_profile` fixture in `tests/conftest.py` with fixed,
   readable values (e.g. `github_username="janedoe"`, a stable UUID string for
   `id`/`user_id`, a short `resume_text`, a `portfolio_url`).
3. Convert `tests/unit/test_sample_user_profile_fixture.py` from a reproduction
   into a passing verification test that asserts every `Profile` field is present
   and correctly typed.
4. (Optional) Refactor `test_review_service.py::mock_profile` to consume the
   shared fixture, demonstrating reuse without changing test behavior.
5. Run `make check` (ruff + black + mypy) and `make test-unit`; confirm the
   previously failing test now passes and nothing else regresses.

### Inputs & outputs
- **Input:** None at runtime — the fixture takes no arguments; it produces
  in-memory sample data. (If it returns a `Profile` instance, it depends only on
  importing the model, not on a database session.)
- **Output:** A `sample_user_profile` object exposing all `Profile` fields with
  deterministic values, injectable into any test via the `sample_user_profile`
  parameter.
- **Net change:** New fixture in `conftest.py`; one reproduction test flips from
  ERROR to PASS.

### Risks & unknowns
- **Return-shape decision (`Profile` instance vs. dict vs. Pydantic schema).**
  Returning a `Profile` ORM instance is closest to production but could surprise
  tests expecting a mapping. Mitigation: pick the ORM instance, document it, and
  keep the verification test's assertions attribute-based.
- **Constructing `Profile` without a DB session.** SQLAlchemy models can be
  instantiated as transient objects, but `created_at`/`updated_at` column
  defaults only apply on flush. Mitigation: set `created_at`/`updated_at`
  explicitly in the fixture so they are always populated.
- **mypy strictness.** The pre-commit `mypy` hook rejects untyped defs (already
  hit this once). Mitigation: fully annotate the fixture signature and return type.
- **Unknown:** whether maintainers expect the fixture to live in `conftest.py`
  (matching current convention) or literally under a new `tests/fixtures/`
  directory as the issue title implies. Mitigation: follow the existing
  `conftest.py` convention and note the choice in the PR description for reviewer
  confirmation.

### Edge cases
- A consumer accessing `resume_filename`/`resume_text` when they are `None` — the
  fixture should provide non-null sample values so nullable fields are exercised
  with realistic data, while still matching the `str | None` types.
- UUID fields (`id`, `user_id`) must be valid UUID strings, matching the model's
  `UUID(as_uuid=False)` column type, so tests that parse or compare them don't
  break.
- Timestamp fields (`created_at`, `updated_at`) must be timezone-aware
  `datetime` values, matching `DateTime(timezone=True)`.
- Fixture must remain deterministic across runs (no random values that would make
  assertions flaky).
