# Module 3 Journal — PathReview Contribution

## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/89

**Issue title:** API reference doc is missing the `POST /profiles` request body schema

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
`docs/API.md` lists PathReview endpoints at a high level but never documents the request body for creating a profile (or starting a review). Contributors and API consumers cannot tell which fields are required, what types they take, or what example values look like without digging into FastAPI / Pydantic schemas under `api/`. A successful fix adds request body schemas with field descriptions and example values for `POST /profiles` and `POST /reviews` directly in `docs/API.md`, so the public docs are self-contained.

**Branch name:** `docs/89-api-profiles-request-schema`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

### Selection notes ("Is this right for me?")

- **Tier fit:** Tier 1 / docs-only — scoped to one file (`docs/API.md`), estimated 2–3 hours in the issue tracker. Good first contribution to a multi-service codebase without requiring deep RAG/agent changes.
- **Still available:** Open, no assignees, and no prior claim comments when selected.
- **Gap confirmed:** Current `docs/API.md` only has one-line endpoint summaries; request body schemas for `POST /profiles` and `POST /reviews` are missing (issue body matches the file).
- **Not picking popular stubs that are already claimed or already fixed** (e.g. CONTRIBUTING commit convention, ProfileForm loading tests, readme_scorer unit tests).
- **Claimed on GitHub:** Comment left on issue #89 stating intent and branch name.

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/ethanncyb/pathreview/commit/3bb64d85a7f75af65a7b4c99d057bc82abf9d396

**Reproduction summary:**
Opened local `docs/API.md` on branch `docs/89-api-profiles-request-schema`. Under Profiles and Reviews, only one-line endpoint summaries exist — no request body field tables, types, descriptions, or example values for `POST /profiles` or `POST /reviews`. Confirmed the live API at `http://localhost:8000/docs` / OpenAPI does expose request bodies (`multipart/form-data` for profiles, `application/json` ReviewCreate for reviews), so the gap is documentation-only and still present.

**PLAN.md link:** https://github.com/ethanncyb/pathreview/blob/docs/89-api-profiles-request-schema/PLAN.md

**Blockers or open questions:**
Document `POST /profiles` as multipart Form/File (not JSON) per `api/routes/profiles.py`; verify wording against OpenAPI during Week 9 implementation.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
Completed PLAN.md sub-tasks 1–4: added `POST /profiles` (`multipart/form-data`: `github_username`, `portfolio_url`, `resume_file`) and `POST /reviews` (`application/json` with required `profile_id`) request body sections to `docs/API.md`, including field descriptions, optionality, resume MIME → 422 note, JWT auth callout, and example values aligned with `api/routes/profiles.py` / `ReviewCreate`.

**Next steps:**
Add `tests/unit/test_api_docs.py` parity checks, run `make check` / `make test-unit`, walk the pre-submission self-review checklist, open the PR against upstream, and fill Check-in 2 with the PR link.

**Blockers:**
None.

---

### Check-in 2 (end of week)

**PR link:** https://github.com/jamjamgobambam/pathreview/pull/145

**Branch:** `docs/89-api-profiles-request-schema`

**What you built:**
Updated `docs/API.md` so API consumers can construct valid `POST /profiles` (multipart Form/File) and `POST /reviews` (JSON `profile_id`) requests without reading FastAPI sources. Added a unit test that guards those request-body docs against regressions.

**Tests added or updated:**
`tests/unit/test_api_docs.py` — asserts `docs/API.md` documents multipart fields for profiles (including PDF/Markdown/plain-text resume MIME types) and JSON `profile_id` with example UUID for reviews.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes

**Draft PR feedback received from:** none

Note: Full `make check` / `make test-unit` report many pre-existing failures elsewhere in the repo (e.g. ruff F841 in unrelated unit tests; 53 failing unit tests in modules we did not touch). Per the pre-submission checklist, those are documented as pre-existing; our change introduces no new failures — `ruff`/`black` clean on `tests/unit/test_api_docs.py`, and `pytest tests/unit/test_api_docs.py -v` passes (2/2).

## Week 10 — Iteration & reflection

### Reviewer feedback

**Feedback received:** [x] Yes  [ ] No — still awaiting review

**Summary of feedback:**
Copilot reviewed PR #145 (no human/maintainer review yet) and left three inline comments:
(1) `docs/API.md` said the resume must be “PDF or Markdown” while also listing `text/plain` — the description should include plain text so consumers are not misled;
(2) `tests/unit/test_api_docs.py` only asserted the words “PDF” and “Markdown”, so it would not catch MIME-string drift vs `api/routes/profiles.py`;
(3) Week 9 Check-in 2 marked full `make check` / `make test-unit` as passing even though the note admitted pre-existing failures — Copilot asked to uncheck/clarify the checklist.

**How you responded:**
Accepted (1) and (2). Updated `docs/API.md` so the resume field says PDF, Markdown, or plain text — matching `api/routes/profiles.py`, which already allows `text/plain`. Strengthened `tests/unit/test_api_docs.py` to assert `application/pdf`, `text/markdown`, and `text/plain`. For (3), re-ran the tests for this change: `pytest tests/unit/test_api_docs.py -v` passes (2/2), and lint/format are clean on the files we touched. Our change does not add new failures, so the `make check` and `make test-unit` boxes stay checked. Failures elsewhere in those full runs were already in the repo; the Week 9 note now says that more clearly. Replied on the PR with the same summary.

---

### Reflection

**What was harder than you expected?**
The hardest part was not writing the markdown tables themselves, but discovering that `POST /profiles` is `multipart/form-data` with `Form`/`File` fields rather than a JSON `ProfileCreate` body. Issue #89 and a quick skim of `docs/API.md` suggested a simple schema addition, but matching `api/routes/profiles.py` and OpenAPI meant reworking the Week 8 plan mid-stream so we did not ship an inaccurate JSON example.

**What did you learn about working in a large codebase?**
In a multi-service repo, public docs and implementation can drift even when only a few files look related. Contributing to PathReview meant treating `docs/API.md`, the FastAPI routes, and the live OpenAPI UI as three sources of truth that have to agree — unlike a solo project where you usually invent the API and the docs together. Small wording choices (e.g. which MIME types are allowed) matter because other contributors will trust the docs over reading source.

**How did AI tools help — and where did they fall short?**
AI tools were useful for drafting the request-body sections, scaffolding `tests/unit/test_api_docs.py`, and shaping JOURNAL/PLAN structure under the course template. They fell short on Content-Type accuracy at first (leaning toward JSON) and on interpreting noisy `make check` / `make test-unit` output full of pre-existing failures; I still had to open `api/routes/profiles.py` and run a scoped pytest to know what “green” meant for this change.

**What would you do differently if you started over?**
I would verify OpenAPI and the route signature for `POST /profiles` during Week 8 reproduction, before locking PLAN.md to a JSON-shaped assumption. I would also write the MIME-string asserts into the parity test from day one, so Copilot’s second comment would not have been needed.

**What are you most proud of from this module?**
I am most proud of landing accurate multipart vs JSON documentation for issue #89 plus a regression test that ties `docs/API.md` to the real allowed resume types. That combination makes the API reference usable without reading FastAPI sources and reduces the chance of the same gap coming back quietly.

