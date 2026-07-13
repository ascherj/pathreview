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

**Reproduction commit link:** (filled after push)

**Reproduction summary:**
Opened local `docs/API.md` on branch `docs/89-api-profiles-request-schema`. Under Profiles and Reviews, only one-line endpoint summaries exist — no request body field tables, types, descriptions, or example values for `POST /profiles` or `POST /reviews`. Confirmed the live API at `http://localhost:8000/docs` / OpenAPI does expose request bodies (`multipart/form-data` for profiles, `application/json` ReviewCreate for reviews), so the gap is documentation-only and still present.

**PLAN.md link:** (filled after PLAN.md exists)

**Walkthrough video (recommended):**

**Blockers or open questions:**
Need to decide how to document `POST /profiles` accurately — the route uses multipart `Form`/`File` fields (`github_username`, `portfolio_url`, `resume_file`), not a pure JSON `ProfileCreate` body. Will capture that in PLAN.md and verify against OpenAPI during Week 9.
