# Address Format Coverage Plan

## Solution plan

**Issue:** [`pii_scrubber.py` test coverage doesn't include address formats
(#73)](https://github.com/jamjamgobambam/pathreview/issues/73)

### Understand

`PIIScrubber.PII_PATTERNS["street_address"]` recognizes a house number, an
alphabetic street name, and a known street suffix. The existing
`test_address_variations` iterates over three inputs without asserting anything,
so it cannot catch a regression. The pattern also excludes digits and periods
from the street-name portion: it partially redacts `456 West 42nd Street` as
`[REDACTED] 42nd Street` and misses `789 N. Oak Avenue` entirely. In addition,
the suffix alternatives have no final word boundary, which can match short
suffixes such as `Ct` inside ordinary words.

Expected behavior is for a recognized street address to be replaced as one
complete `[REDACTED]` value and reported by `detect()` as `street_address` with
positions covering the complete match. Actual behavior ranges from full
redaction for a simple address to partial redaction, missed detection, and false
positives for more complex text.

### Map

- `safety/pii_scrubber.py`
  - `PIIScrubber.PII_PATTERNS["street_address"]` defines detection boundaries.
  - `PIIScrubber.scrub()` replaces each regex match.
  - `PIIScrubber.detect()` exposes the matched value and source positions.
- `tests/unit/test_pii_scrubber.py`
  - `test_street_address_redaction` covers one simple full-suffix form.
  - `test_address_variations` currently has no assertions.
  - `test_common_street_address_formats_are_fully_redacted` is the failing
    reproduction added in Week 8.

### Plan

1. Replace the assertion-free address loop with parameterized cases covering
   full and abbreviated suffixes, numbered street names, and cardinal
   directions with and without periods.
2. Add exact assertions for both `scrub()` output and `detect()` metadata so a
   partial match cannot pass merely because some `[REDACTED]` text appears.
3. Refine the `street_address` pattern to accept common ordinal/directional
   tokens and add explicit match boundaries around suffix alternatives.
4. Add negative cases based on resume prose, including years of experience and
   words containing short suffix text, to prevent the broader pattern from
   increasing false positives.
5. Run the focused address tests, the complete PII scrubber module, and
   `make check && make test-unit`; separate any known upstream failures from
   regressions introduced by this change.

### Inputs & outputs

The input is free-form resume or portfolio text that may contain a US street
address. Representative inputs include `123 Main Street`, `456 West 42nd
Street`, `789 N. Oak Avenue`, and suffix abbreviations such as `Ave` or `Rd`.

For `scrub()`, the output should preserve surrounding non-PII text while
replacing the entire recognized address with one `[REDACTED]` marker. For
`detect()`, the output should include one `street_address` item whose value and
start/end offsets identify the complete address. Text without an address should
remain unchanged and produce no street-address detection.

### Risks & unknowns

- Expanding allowed street-name characters in `safety/pii_scrubber.py` could
  increase false positives in resume prose; the existing match inside
  `applications` demonstrates that this risk is real.
- The issue asks for test coverage, but the new reproduction proves production
  behavior is also incorrect. The final PR should explain why a narrowly scoped
  pattern correction is necessary for the tests to represent useful behavior.
- Apartment, suite, and unit designators may be considered part of the address,
  but the current pattern stops at the street suffix. Maintainer expectations
  should determine whether this issue includes unit text.
- The PII module already has unrelated phone-test failures and legacy Ruff/Mypy
  failures. Verification must report these separately rather than weakening new
  address assertions to obtain a green suite.

### Edge cases

- Full and abbreviated suffixes: `Street`/`St`, `Avenue`/`Ave`, `Road`/`Rd`.
- Numbered and ordinal names such as `42nd Street` and `5th Avenue`.
- Cardinal directionals such as `N Oak Ave`, `N. Oak Avenue`, and `SW Main Rd`.
- Hyphenated or apostrophized street names without consuming nearby prose.
- Optional punctuation after a suffix and, pending scope confirmation,
  apartment/suite designators.
- Ordinary numbers and words that are not addresses, including years of
  experience, version numbers, and words containing `St`, `Dr`, or `Ct`.
- Multiple addresses in one string, empty input, and repeated scrubbing, which
  should remain idempotent.
