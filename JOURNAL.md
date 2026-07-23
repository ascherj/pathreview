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

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
All 5 sub-tasks from PLAN.md are done. Widened the `phone_us` separator
character class in `safety/pii_scrubber.py` to accept whitespace alongside
dash/dot, which fixes the four tests named in the issue. While writing a
stricter regression test (asserting the *exact* matched value, not just
"contains `[REDACTED]`"), I caught a second, related bug the loose existing
tests missed: the `\b` anchor can't match immediately before `(`, since a
preceding space and the paren are both non-word characters, so the match
was starting one character late and leaving the opening paren un-redacted
(`scrub("(555) 123-4567")` produced `"([REDACTED]"` instead of
`"[REDACTED]"`). Replaced both `\b` anchors with `(?<!\w)`/`(?!\w)`
lookarounds, which fixes that while still rejecting digits glued to
adjacent letters (no regression there). Added two new regression tests and
confirmed all 4 formats (`555-123-4567`, `(555) 123-4567`, `555.123.4567`,
`+1 555 123 4567`) redact cleanly with no leftover characters.

**Next steps:**
- Draft PR opened: https://github.com/ascherj/pathreview/pull/273
- Share the draft in the class Slack channel for peer/mentor review.
- Address any feedback, then mark the PR ready for review and fill in
  Check-in 2.

**Blockers:**
None for the fix itself. Documenting for the PR description: `ruff check .`
finds 176 pre-existing errors repo-wide (0 in the 2 files I touched),
`black --check .` finds 51 files that would be reformatted (0 of mine),
`mypy` (source dirs only, matching CI's scope) finds 99 pre-existing errors
in 25 files (`safety/pii_scrubber.py` is clean), and `pytest tests/unit`
has 49 pre-existing failures unrelated to this change (only 1 is in
`test_pii_scrubber.py` — `test_mixed_pii_and_text`, caused by an unrelated
`street_address` regex bug documented in PLAN.md's Risks section, not
something #146 asked me to fix).

---

### Check-in 2 (end of week)

**PR link:** https://github.com/ascherj/pathreview/pull/273

**Branch:** fix/146-pii-phone-regex

**What you built:**
Fixed `PIIScrubber.PII_PATTERNS["phone_us"]` in `safety/pii_scrubber.py` so
it redacts parenthesized (`(555) 123-4567`) and fully-spaced
(`+1 555 123 4567`) US phone number formats, not just the dashed/dotted
ones it already handled. This required two changes to the regex: widening
the separator character class to accept whitespace, and replacing the `\b`
word-boundary anchors with `(?<!\w)`/`(?!\w)` lookarounds, since `\b`
couldn't anchor immediately before an opening parenthesis and was leaving
it un-redacted.

**Tests added or updated:**
`tests/unit/test_pii_scrubber.py` — added
`test_detect_parenthesized_phone_matches_full_number` (asserts `detect()`
returns the exact value `"(555) 123-4567"`, catching the leading-paren bug
that looser existing assertions missed) and
`test_scrub_redacts_mixed_phone_formats_in_one_string` (asserts a dashed
and a parenthesized number in the same string are each redacted
independently). Also added missing mypy type annotations across the file's
existing test functions and removed two unused-variable assignments, both
needed to satisfy the local pre-commit hooks once I touched the file.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes
(both confirmed with 0 new failures introduced relative to `main` — see
Check-in 1 for the documented pre-existing failure counts)

**Draft PR feedback received from:** none — shared the link, no comments or
reviews came in by submission time.

## Week 10 — Iteration & reflection

### Reviewer feedback

**Feedback received:** [ ] Yes  [x] No — still awaiting review

**Summary of feedback:**
No comments or reviews landed on [PR #273](https://github.com/ascherj/pathreview/pull/273) by the end of the module.

**How you responded:**
N/A — nothing to respond to. The PR is marked ready for review and left open in case feedback arrives after submission.

---

### Reflection

**What was harder than you expected?**
Almost none of the difficulty was in the actual bug — the `phone_us` regex
fix is a two-line change. What actually ate time was the environment:
Docker Desktop wasn't running, the bundled ChromaDB container turned out
to be broken against NumPy 2.0 in its pinned image, `make setup` crashed on
a Unicode checkmark because Windows' default console codepage is cp1252,
and then `git commit` itself failed because the local `pre-commit` hook's
virtualenv build hit Windows' 260-character path limit inside the Windows
Store Python install's cache path. None of that was in the issue
description — it's the "getting to the point where you can even start"
tax that a written spec never mentions.

**What did you learn about working in a large codebase?**
The loose existing tests in `test_pii_scrubber.py` were themselves a
lesson: `assert "[REDACTED]" in scrubbed` passes even if the fix is
subtly wrong. Writing a stricter assertion (`assert value ==
"(555) 123-4567"`, checking the *exact* match) surfaced a second bug — the
leading `(` was never being redacted — that the issue report didn't
mention and the existing test suite couldn't have caught. In someone
else's codebase, the tests you inherit define the bar, but they don't
define correctness; you have to independently decide whether "green"
actually means "right."

**How did AI tools help — and where did they fall short?**
I worked through this with Claude Code driving most of the hands-on
execution — running the setup, diagnosing each environment failure,
proposing the regex fix, and writing the PLAN.md/JOURNAL.md drafts —
while I made the calls at each decision point: which issue to pick,
whether to fork/start Docker, when to accept a fix versus dig further,
and reviewing the diffs before they were committed. It was genuinely
fast at cross-referencing the codebase (tracing `PII_PATTERNS` through
both `scrub()` and `detect()`, or checking whether other tests already
covered a format) and at explaining *why* a regex failed rather than
just proposing a replacement. Where it fell short: it wouldn't have
caught the leading-paren bug on its own confidence — that only
surfaced because I asked for a stricter test rather than accepting
"tests pass" as the finish line, which is a reminder that AI output
is only as rigorous as the standard you hold it to.

**What would you do differently if you started over?**
I'd write the stricter regression test *before* declaring the fix done,
not after — the loose "contains [REDACTED]" tests gave false confidence
for longer than they should have. I'd also sequence reproduction and
planning more strictly before touching code; because the fix was small,
I ended up implementing it in the same pass as reproducing it rather
than reproduce → plan → build across separate steps, which the module
is explicitly structured to avoid.

**What are you most proud of from this module?**
Catching the second, unreported bug (the leading-paren redaction gap)
by refusing to trust a passing-but-loose test suite. It's a small thing
compared to shipping the whole fix, but it's the part that actually
required judgment rather than following the issue's repro steps.
