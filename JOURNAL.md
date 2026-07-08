# Module 3 Journal

## Week 7 — Issue Selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/78

**Issue title:** API response for profile creation doesn't include the profile_id field

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
When a client creates a profile via `POST /profiles`, the API returns a
`ProfileResponse` that exposes the record's primary key under the name `id`,
but never under the name `profile_id` that clients rely on for follow-up
requests (for example `GET /profiles/{profile_id}`). The value itself exists on
the database model, but the response schema in `api/schemas/profile.py` doesn't
surface a `profile_id` field, so clients have no field by that name to read. A
successful fix adds `profile_id` to the profile creation response, mapped from
the model's `id`, so the API contract matches what clients expect while keeping
existing behavior intact. This is scoped to the API layer, primarily the
`ProfileResponse` schema.

**Branch name:** `fix/78-profile-response-missing-profile-id`

**Setup confirmation:** [x] App runs locally at localhost:5173.  

**Cohort ledger:** [ ] Issue added to cohort ledger

---

### Selection Notes — "Is This Issue Right for Me?" Checklist

*Part 1: Understanding the Issue*

- *In My Own Words*: When a profile is created, the API currently returns the profile identifier as `id` instead of `profile_id`. Since clients need the `profile_id` field for future requests, the response is missing a field they depend on.
- *Part of The App Affected*: This issue is in the API layer, specifically the response schema in `api/schemas/profile.py`. This schema is used by the `POST /profiles` route in `api/routes/profiles.py`. I located and reviewed both files in the repository.
- *Before and After*: Before the fix, `POST /profiles` returns a response containing `{"id": ...}` but does not include `profile_id`. After the fix, the response should include `profile_id` with the profile's identifier.

*Part 2: Tier Fit*

- *Why This Tier Fits*: Tier 1 is the right match because this change is scoped to the `ProfileResponse` schema in a single file. It does not require major changes across different parts of the application or a deep understanding of the entire codebase. For a first open-source contribution, this is a manageable and well-defined issue.

*Part 3: Codebase Readiness*

- *Files Reviewed*: I looked through `ProfileResponse` in `api/schemas/profile.py`, the `Profile` model in `core/models/profile.py` (where the primary key is stored as `id`), and the `create_profile_endpoint` route that creates responses using `ProfileResponse.model_validate(new_profile)`.
- *Important Constraint Discovered*: The schema uses `from_attributes`, meaning new fields need to map to attributes that already exist on the ORM object. Since the model has `.id` but not `.profile_id`, simply adding a `profile_id` field may not work without additional mapping logic.
- *Testing Plan*: There is currently no dedicated profile test file under `tests/unit/`, so I plan to add tests for this behavior while following the structure of existing test files, such as `tests/unit/test_review_service.py`.

*Part 4: Scope And Time*

- *Estimated Effort*: The issue is estimated at 1–2 hours, plus time for writing tests, which makes it achievable before the Week 9 deadline.
- *Blockers or Dependencies*: No blockers or external dependencies are mentioned in the issue.
- *Claim Status*: I commented on the issue to claim it. The cohort ledger entry is still pending because I am waiting for the ledger link, and I will complete it before starting Week 8.

---

## Week 8 — Reproduction & Solution Planning

**Reproduction commit link:** https://github.com/sehr-abrar/pathreview/commit/35edb900b56be115e46fc8ac91c9386f707a0d56


**Reproduction summary:**
I reproduced the issue with a new failing test, `tests/unit/test_profile_schema.py`,
which validates a Profile-like object through `ProfileResponse` and asserts the
serialized payload contains a `profile_id` field. Running
`pytest tests/unit/test_profile_schema.py` fails with
`AssertionError: ProfileResponse is missing the 'profile_id' field (issue #78)`,
and the dumped payload confirms the response contains `id` but no `profile_id`.

**PLAN.md link:** https://github.com/sehr-abrar/pathreview/blob/fix/78-profile-response-missing-profile-id/PLAN.md

**Walkthrough video (recommended):** N/A — not recorded.

**Blockers or open questions:**
One open question for implementation (not a blocker): whether to keep the existing
`id` field alongside the new `profile_id` or replace it. My current plan keeps both
for backward compatibility, pending a quick check of `frontend/src/` for existing
consumers of `.id`.

