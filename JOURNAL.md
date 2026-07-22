# PathReview — Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/146

**Issue title:** PII scrubber fails to redact parenthesized US phone numbers

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `PIIScrubber` class in `safety/pii_scrubber.py` is supposed to detect and
redact personally identifiable information — including US phone numbers —
before review content is generated or stored. Its phone-number regex only
matches dashed formats like `555-123-4567`, so a very common alternate
format, `(555) 123-4567`, slips through both `scrub()` (the text is returned
unredacted) and `detect()` (it reports no PII found at all). This means a
user's real phone number can end up unmasked in generated output whenever it
appears in the parenthesized style, which defeats the purpose of the safety
layer for a meaningful share of real-world resumes and portfolios. A
successful fix extends the phone-number pattern (or adds a second pattern)
to also match the parenthesized format without breaking the existing
dashed-format matches, and makes the four related unit tests in
`tests/unit/test_pii_scrubber.py` pass.

**Branch name:** fix/146-pii-phone-regex

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

**Scope check notes:**
- Fully contained to one file (`safety/pii_scrubber.py`) and its test file —
  no cross-module changes expected.
- Existing failing tests (`test_us_phone_number_redaction`,
  `test_us_phone_formats`, `test_detect_phone_pii`,
  `test_phone_at_start_of_text`) already define what "done" looks like, so
  there's low risk of scope creep or ambiguity about the fix.
- Doesn't depend on Docker services that are currently flaky in my local
  environment (the bundled `vector-db`/ChromaDB container fails to start due
  to a NumPy 2.0 incompatibility in the pinned image) — Postgres and Redis
  are healthy, and this issue doesn't touch either.
- Estimated effort is small (regex change + verifying no regressions in
  existing dashed-format tests), appropriate for a first issue in an
  unfamiliar codebase.

## Environment setup notes

- Forked to `andrewskoblov/pathreview`, cloned locally, `upstream` remote
  points to `ascherj/pathreview`.
- `.env` copied from `.env.example`; running with `LLM_PROVIDER=mock` (no
  API key needed for local dev).
- `docker compose up -d` brings up Postgres and Redis healthy. The
  `vector-db` (ChromaDB) container currently crashes on startup due to a
  `np.float_` removal in NumPy 2.0 vs. the pinned `chromadb/chroma:0.4.22`
  image — not required for this issue, but flagging in case it blocks a
  future RAG-related issue.
- `make setup` fails at the very last step on Windows because
  `scripts/seed_db.py` prints a Unicode checkmark that the default Windows
  console codepage (cp1252) can't encode — worked around by re-running the
  script with `PYTHONIOENCODING=utf-8`. All prior steps (venv, deps,
  migrations, seeding) completed successfully before that point.
- App confirmed running at `http://localhost:5173` (frontend) and
  `http://localhost:8000/docs` (API), both returning HTTP 200.
