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

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/andrewskoblov/pathreview/commit/4af0fcc2518472b1561af9bb8528a31bab0695d6

**Reproduction summary:**
Ran the exact snippet from the issue against the unmodified code: `PIIScrubber().scrub("Call me at (555) 123-4567 or 555-123-4567")` returned `"Call me at (555) 123-4567 or [REDACTED]"` — the parenthesized number passed through untouched while the dashed one was redacted — and `detect()` returned no phone match for the parenthesized text at all. Confirmed the same failure through the test suite: `pytest tests/unit/test_pii_scrubber.py -q` showed 5 failing tests, 4 of which are exactly the ones the issue names (`test_us_phone_number_redaction`, `test_us_phone_formats`, `test_detect_phone_pii`, `test_phone_at_start_of_text`). Traced the root cause to the `phone_us` regex's separator character class (`[-.]?`), which never allows whitespace between digit groups, so any format with a space (parenthesized, or fully space-separated with a country code) fails to match.

**PLAN.md link:** https://github.com/andrewskoblov/pathreview/blob/fix/146-pii-phone-regex/PLAN.md

**Walkthrough video (recommended):** Not recorded — optional and not graded, skipping for now.

**Blockers or open questions:**
- I ended up implementing the actual fix (widening `phone_us`'s separator class to accept whitespace) alongside the reproduction rather than strictly sequencing "reproduce, then plan, then build" across separate weeks, since the fix itself was small once the root cause was clear. The commit linked above documents both the reproduction and the fix together — flagging in case that's not the expected chronology.
- Found a second, unrelated pre-existing bug while testing: the `street_address` pattern in the same file can greedily eat ordinary prose (e.g. "Python applications" partially matches because "appl" contains "pl", treated as the abbreviation for "Place"), which fails `test_mixed_pii_and_text`. Out of scope for #146 (not among its named tests) — noting here in case it's worth a follow-up issue.
- The 5th failing test (`test_mixed_pii_and_text`, tied to the `street_address` bug above) is still red after my fix — expected, since it's a different bug, but calling it out so it isn't mistaken for an incomplete fix.

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
