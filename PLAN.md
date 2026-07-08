## Solution plan

**Issue:** [API docs don't include example `curl` commands](https://github.com/jamjamgobambam/pathreview/issues/117)

### Understand

The issue is a documentation gap, not a backend behavior bug. `docs/API.md` currently lists the API base URL and endpoint names, then points readers to Swagger UI and ReDoc, but it does not provide copy-pasteable `curl` commands that a new contributor can run from a terminal to verify the local API.

Expected behavior: the API reference should let a contributor quickly test the running local backend at `http://localhost:8000` with concrete examples for health checks, authentication, profile creation, profile retrieval/deletion, review creation, review retrieval, and paginated review listing.

Actual behavior: a contributor can see that endpoints exist, but has to infer request methods, headers, authentication, JSON bodies, form data, and placeholder IDs manually from the backend route code or interactive docs.

### Map

Files I expect to touch:

- `docs/API.md` — primary file to update with `curl` examples.
- `PLAN.md` — this planning document.
- `JOURNAL.md` — Week 8 reproduction and planning entry.

Files I will inspect but do not expect to edit:

- `api/routes/health.py` — confirms `GET /health` behavior.
- `api/routes/auth.py` — confirms `POST /auth/register` accepts JSON and `POST /auth/login` uses OAuth2 form fields.
- `api/routes/profiles.py` — confirms authenticated profile endpoints and multipart form input for profile creation.
- `api/routes/reviews.py` — confirms authenticated review endpoints, pagination, and review status route.
- `api/schemas/user.py`, `api/schemas/profile.py`, `api/schemas/review.py` — confirm request and response field names.
- `docs/SETUP.md` — confirm local base URL and seeded test accounts for examples.

### Plan

1. Reproduce the documentation gap locally by opening `docs/API.md` and running a search such as `grep -n "curl" docs/API.md`, confirming that no `curl` examples exist.
2. Trace each documented endpoint to its FastAPI route and schema so the examples use the correct method, URL, content type, auth header, request body, and placeholder variables.
3. Rewrite `docs/API.md` into a clearer structure with a base URL, optional shell variables such as `TOKEN`, `PROFILE_ID`, and `REVIEW_ID`, then add one runnable `curl` example per endpoint.
4. Add short notes for common gotchas: login uses `application/x-www-form-urlencoded`, protected endpoints require `Authorization: Bearer $TOKEN`, profile creation uses multipart form fields, and ID placeholders should be replaced with values returned by earlier commands.
5. Validate the examples against the local dev server where possible, then run documentation-safe checks such as `make check` if the environment is already set up.

### Inputs & outputs

Inputs:

- A running local PathReview backend at `http://localhost:8000`.
- Optional seeded user credentials from setup, or a newly registered email/password.
- Example values for `github_username`, `portfolio_url`, `PROFILE_ID`, and `REVIEW_ID`.
- Optional resume file path for multipart profile creation.

Outputs:

- Updated `docs/API.md` with copy-pasteable `curl` examples.
- Clear examples for public endpoints and authenticated endpoints.
- Placeholders that make it obvious which values a contributor must replace.
- No functional backend, database, or frontend behavior changes.

### Risks & unknowns

- `POST /auth/login` uses FastAPI's `OAuth2PasswordRequestForm`, so a JSON login example would be wrong. I need to document it as form data with `username=<email>` and `password=<password>`.
- `POST /profiles` uses multipart form fields and an optional file upload, so the example must not imply it accepts JSON only.
- Review examples depend on a valid `PROFILE_ID`, so the docs should show the dependency order: register/login, create profile, then create review.
- `GET /reviews/{review_id}/status` exists in the route code but is not currently listed in `docs/API.md`; I need to decide whether to include it as an extra helpful example or keep the update limited to the endpoints already listed.
- Some commands may return different statuses depending on whether local services, seeded data, or background review processing are ready; the docs should avoid promising exact full response bodies where they may vary.

### Edge cases

- Invalid or missing bearer token should produce an authentication error on protected routes; examples should show the auth header consistently.
- Duplicate registration email may return an error, so registration examples should use a clearly replaceable email address.
- Missing or invalid `PROFILE_ID` / `REVIEW_ID` should return a not-found or validation error; examples should label these as placeholders.
- Resume upload is optional, but if shown, it should use a `.pdf`, `.md`, or plain text file because profile creation rejects unsupported resume types.
- Paginated review listing should include example `page` and `page_size` query parameters with reasonable values.
