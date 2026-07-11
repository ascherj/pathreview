# Contribution Journal

## Week 7 - Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/73

**Issue title:** `pii_scrubber.py` test coverage doesn't include address formats

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The PII scrubber includes a regular expression for street addresses, but its
unit tests do not meaningfully verify common US address formats. The existing
address-variations test loops over examples without making an assertion, so it
would pass even if no address were redacted. This affects the safety layer's
ability to prevent resume addresses from appearing in generated feedback. A
successful fix will add focused assertions for representative full and
abbreviated street suffixes while ensuring ordinary non-address text remains
unchanged.

**Branch name:** `test/73-address-format-coverage`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** N/A - TA advance validation, not a cohort claim

### Selection notes - "Is this right for me?"

- **Reproducible:** Yes. `test_address_variations` currently has no assertion,
  and the remaining address test checks a single full `Street` form with a weak
  either/or assertion.
- **Scope:** The stated work is limited to `tests/unit/test_pii_scrubber.py` and
  should take the estimated 2-3 hours. Production changes are out of scope
  unless a valid address case demonstrates a scrubber defect.
- **Context:** I located the address pattern in `safety/pii_scrubber.py`, the
  relevant unit test class, and the repository's pytest conventions.
- **Verification plan:** Run the focused PII scrubber tests first, followed by
  `make check` and `make test-unit` before opening the pull request.
- **Coordination:** The issue had no assignee or claim comments when selected. I
  posted a claim comment describing the reproduced gap and intended branch. I
  am completing the project in advance as a TA, so no cohort ledger or course
  portal submission is required.

## Week 8 - Reproduction & solution planning

**Reproduction commit link:** https://github.com/JPL11/pathreview/commit/8cceea475c19de9efa3ea8c9b99fb1b77eb8665b

**Reproduction summary:**
I added a parameterized test for a numbered street name and a dotted cardinal
direction. The scrubber only partially redacts `456 West 42nd Street` and does
not redact `789 N. Oak Avenue`, so both cases fail reliably.

**PLAN.md link:** https://github.com/JPL11/pathreview/blob/test/73-address-format-coverage/PLAN.md

**Walkthrough video (recommended):** Not recorded; this is a TA advance
validation and the video is not graded.

**Blockers or open questions:**
The repository's current PII test module has unrelated baseline failures for
parenthesized phone numbers and a false-positive address match inside regular
prose. The implementation must distinguish those upstream failures from this
issue's results. I also need to confirm whether apartment/unit designators are
expected to be included in the same redaction or handled as a separate pattern.
