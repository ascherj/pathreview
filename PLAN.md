# PathReview — Solution Plan

## Solution plan

**Issue:** [#146 — PII scrubber fails to redact parenthesized US phone numbers](https://github.com/ascherj/pathreview/issues/146)

### Understand

`PIIScrubber` (in `safety/pii_scrubber.py`) is supposed to redact US phone
numbers in any common format before profile/review content is stored or
shown. Its `PII_PATTERNS["phone_us"]` regex was:

```
\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b
```

The separator between digit groups (`[-.]?`) only allows a dash, a dot, or
nothing — never whitespace. That's fine for `555-123-4567`, but it breaks
the moment there's a space between groups, which happens in two very common
real-world formats:

- `(555) 123-4567` — there's a space after the closing paren, before the
  next 3-digit group.
- `+1 555 123 4567` — every group is separated by a space.

**Expected behavior:** both `scrub()` and `detect()` recognize these formats
and treat them as `phone_us` matches, exactly like the dashed format.

**Actual behavior:** `scrub()` returns the phone number completely
unredacted, and `detect()` reports zero phone matches for it — a real user
phone number in this format silently passes through the safety layer.

### Map

Files/functions touched:

- `safety/pii_scrubber.py` — `PIIScrubber.PII_PATTERNS["phone_us"]` (the
  regex itself). No other pattern, method, or caller needs to change;
  `scrub()` and `detect()` both just iterate `PII_PATTERNS`, so fixing the
  pattern fixes both call sites automatically.
- `tests/unit/test_pii_scrubber.py` — existing tests already specify the
  target behavior (`test_us_phone_number_redaction`,
  `test_us_phone_formats`, `test_detect_phone_pii`,
  `test_phone_at_start_of_text`); no new tests needed, just need to make
  these pass without breaking the other 20 tests in the file.

Not touched: `agent/`, `ingestion/`, `api/`, `rag/` — nothing outside the
safety layer depends on the internal shape of this regex.

### Plan

1. Reproduce the bug locally by running the exact snippet from the issue
   against the current code and confirming `scrub()`/`detect()` miss the
   parenthesized format (done — see JOURNAL.md Week 8 entry).
2. Widen the `phone_us` separator character classes to accept whitespace in
   addition to `-`/`.`, so `(555) 123-4567` and `+1 555 123 4567` match
   while `555-123-4567` and `555.123.4567` keep matching.
3. Run `tests/unit/test_pii_scrubber.py` and confirm the 4 tests named in
   the issue now pass, and that no previously-passing test in that file
   regresses.
4. Run the full unit suite to check for any accidental collateral matches
   in unrelated modules (e.g. a phone-shaped false positive appearing where
   it didn't before).
5. Run `make lint`/`ruff`/`black`/`mypy` on the touched file and fix any
   pre-existing style violations that block the pre-commit gate on this
   file, since `CONTRIBUTING.md` requires `make check` to pass before a PR.

### Inputs & outputs

- **Input:** arbitrary free-text strings (resume text, portfolio blurbs,
  review content) that may or may not contain a US phone number in any of
  the four common written formats.
- **Output of `scrub()`:** the same text with every detected PII substring
  replaced by `[REDACTED]`.
- **Output of `detect()`:** a list of `{"type", "value", "start", "end"}`
  dicts describing every match, used for reporting/monitoring rather than
  redaction.
- The fix changes *which substrings count as a match* for `phone_us`; it
  does not change the shape of the output for either method.

### Risks & unknowns

- **Over-matching risk:** loosening the separator to allow whitespace could
  cause the regex to span across unrelated digit-bearing text (e.g. two
  unrelated numbers separated by a sentence). Mitigated because the
  separator is still optional-single-character (`[-.\s]?`), not
  "any amount of whitespace/text" — a full sentence between digit groups
  still won't match.
- **Interaction with `street_address`:** `PII_PATTERNS` is a dict processed
  in insertion order (email → phone_us → phone_intl → ssn →
  street_address). While testing I found `street_address`'s regex has an
  unrelated pre-existing bug — it can greedily match ordinary prose (e.g.
  "5 years developing Python applications" gets partially eaten because
  "appl" contains the substring "Pl", which the pattern treats as the
  abbreviation for "Place"). This causes `test_mixed_pii_and_text` to fail
  regardless of the phone_us fix. It's out of scope for #146 (not among the
  tests the issue names), but worth flagging — could be its own follow-up
  issue.
- **Pre-commit/lint gate:** the file already violated ruff/black rules on
  `main` before I touched it (unsorted imports, two overlong lines, one
  unused loop variable). Any change to this file re-triggers those
  failures during `pre-commit`, since ruff lints the whole file, not just
  the diff. Needed a small mechanical cleanup (no logic change) to get a
  commit through cleanly.
- **Environment quirk (not a code risk, but worth noting):** the bundled
  `vector-db` (ChromaDB) Docker service fails to start locally due to a
  NumPy 2.0 incompatibility in the pinned image. Irrelevant to this issue
  since `pii_scrubber.py` has no dependency on the vector store, but it
  means I can't exercise any RAG-dependent code path locally right now.

### Edge cases

- Dashed format: `555-123-4567` — must keep working (regression risk).
- Dotted format: `555.123.4567` — must keep working.
- Parenthesized with space: `(555) 123-4567` — the bug this issue is about.
- Fully spaced with country code: `+1 555 123 4567`.
- Phone number at the very start of a string (`test_phone_at_start_of_text`)
  and at the very end (`test_phone_at_end_of_text`) — the `\b` word
  boundaries at each end of the pattern need to still work with no
  preceding/following character.
- Text with **no** phone number at all — must not introduce false
  positives (`test_text_with_no_pii`, `test_detect_no_false_positives`).
- Multiple phone numbers in the same text, possibly in different formats —
  `re.finditer`/`re.sub` should still catch each one independently.
