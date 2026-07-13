## Solution plan

**Issue:** [API reference doc is missing the `POST /profiles` request body schema](https://github.com/jamjamgobambam/pathreview/issues/89)

### Understand

Root cause: `docs/API.md` was written as a high-level endpoint index and never documented request payloads. Contributors and API consumers only see one-line summaries such as “Create a profile with resume and GitHub username,” so they cannot tell which fields exist, which are required, what types they use, or what example values look like without reading FastAPI/Pydantic code or opening Swagger.

Expected: For `POST /profiles` and `POST /reviews`, `docs/API.md` includes request body schemas with field names, types, short descriptions, and example values so the markdown reference is self-contained.

Actual (reproduced locally): Profiles and Reviews sections in `docs/API.md` have no request body sections. Live OpenAPI at `http://localhost:8000/docs` already exposes those bodies (`multipart/form-data` for profiles; JSON `ReviewCreate` for reviews), confirming this is a documentation gap, not a missing API feature.

### Map

Files expected to change (Week 9 implementation):

- `docs/API.md` — add request body documentation under Profiles and Reviews

Source-of-truth files to read (do not change for this issue):

- `api/routes/profiles.py` — `create_profile_endpoint` accepts `github_username` / `portfolio_url` as `Form` and `resume_file` as `File` (multipart), not JSON
- `api/schemas/profile.py` — `ProfileCreate` fields (`github_username`, `portfolio_url`, optional, max lengths)
- `api/routes/reviews.py` — `create_review_endpoint` takes JSON body `ReviewCreate`
- `api/schemas/review.py` — `ReviewCreate` with required `profile_id: UUID`
- Local OpenAPI / Swagger (`http://localhost:8000/openapi.json`, `/docs`) — cross-check content types and schema titles

### Plan

1. Document `POST /profiles` in `docs/API.md`: content type `multipart/form-data`; fields `github_username` (optional string), `portfolio_url` (optional string), `resume_file` (optional file; PDF or Markdown); note that auth is required; include example field values matching route/`ProfileCreate` constraints.
2. Document `POST /reviews` in `docs/API.md`: content type `application/json`; required `profile_id` (UUID) from `ReviewCreate`; include an example JSON body.
3. Mirror the existing `docs/API.md` style (short endpoint lines plus a clear Request body subsection with field list and examples — no new doc framework).
4. Cross-check the drafted markdown against live Swagger/OpenAPI (`Body_create_profile_endpoint_profiles_post` and `ReviewCreate`) so field names and content types match production behavior.
5. Optionally note common failure modes next to the schemas (e.g. resume MIME → 422) only if they stay concise and match route behavior in `api/routes/profiles.py`.

### Inputs & outputs

**Inputs:**

- Field definitions from `api/routes/profiles.py` and `api/schemas/profile.py` / `api/schemas/review.py`
- OpenAPI requestBody shapes for `/profiles` and `/reviews`
- Issue requirements: field descriptions and example values for both POST endpoints

**Outputs:**

- Updated `docs/API.md` sections that let a consumer construct valid `POST /profiles` and `POST /reviews` requests without opening Python sources
- No changes to runtime API schemas or route handlers for this issue

### Risks & unknowns

- **Multipart vs JSON for profiles:** Documenting `ProfileCreate` as JSON would be wrong; the real wire format is multipart (`api/routes/profiles.py`). Must document Form/File fields, not a JSON object.
- **Issue title vs body:** The title mentions only `POST /profiles`, but the issue body also requires `POST /reviews` — plan covers both so the PR closes the full issue.
- **Schema drift:** `ProfileCreate` max_length constraints may not all appear in the OpenAPI multipart body schema; prefer the route + Pydantic models and note optional max lengths carefully.
- **Auth:** Both endpoints use `get_current_user`; docs should mention that a JWT is required so examples are usable.

### Edge cases

- All profile fields omitted (empty multipart) — still a valid create if the API allows optional fields; document optionality clearly.
- Invalid resume upload (wrong MIME, e.g. `.docx`) — endpoint returns 422 (“Resume must be a PDF or Markdown file”); docs should state allowed types.
- Missing or malformed `profile_id` on `POST /reviews` — validation error (required UUID); example must use a valid UUID string.
- Unauthenticated requests — both POSTs require a JWT; document Authorization requirement so examples do not look like public endpoints.
