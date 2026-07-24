## Solution plan

**Issue:** README scorer test fixture is too short for its own word-count assertion — https://github.com/ascherj/pathreview/issues/156

### Understand
The test `test_readme_with_all_quality_signals` in `tests/unit/test_readme_scorer.py`
asserts two things about its own fixture README: `word_count > 100` and
`word_count_category == "comprehensive"`. The fixture README currently
contains only 51 words (confirmed by running the test and reading the
`readme_scorer` log line: `word_count=51`). Looking at the actual scoring
logic in `agent/tools/readme_scorer.py`, `word_count_category` is set to
`"comprehensive"` only when `word_count >= 500` (below 100 is `"minimal"`,
100–499 is `"adequate"`). So the fixture doesn't just need to cross 100
words — it needs to cross 500 words to satisfy both assertions. The
expected behavior is that a long, feature-rich README (the kind the test
is trying to represent) scores as `"comprehensive"`; the actual behavior
is the test fails immediately at the word-count line before that even
gets checked, because the fixture is far too short.

### Map
- `tests/unit/test_readme_scorer.py` — contains the fixture (inline
  triple-quoted string, lines 19–49) and the two failing/adjacent
  assertions (lines 56–57). This is the only file that needs to change.
- `agent/tools/readme_scorer.py` — not changed, but read to confirm the
  500-word threshold for `"comprehensive"` (function `_score_readme`,
  the `if/elif/else` block categorizing `word_count_category`).

### Plan
1. Re-read the existing fixture to preserve its structure (headings,
   install/usage code blocks, badges, demo link) since those also drive
   the `has_installation_section`, `has_usage_section`, `has_badges`,
   and `has_demo_link` assertions elsewhere in the same test — the fix
   must not break those.
2. Extend the fixture content so total word count is comfortably over
   500 (targeting ~550–650 words for margin), by adding realistic
   prose under existing sections (e.g., a longer project description,
   an expanded Features list, a Configuration or Contributing section)
   rather than filler text, so the fixture still reads like a real README.
3. Run `.venv/bin/pytest tests/unit/test_readme_scorer.py -q` locally
   and confirm the specific test now passes and word_count prints
   ≥500 in the captured log output.
4. Run the full test file (`-q`, no `-k` filter) to confirm no other
   tests in the same file were affected by the fixture change.
5. Run `make check` to catch any formatting/lint issues introduced by
   the edit (the fixture is inside a Python file, so black/ruff apply).

### Inputs & outputs
- Input: the fixture README string passed to `scorer.execute({"readme_content": readme})`
  inside the test.
- Output: the test should pass, with `result.data["word_count"] > 100`,
  `result.data["word_count_category"] == "comprehensive"`, and all other
  existing assertions in the same test (`has_installation_section`, etc.)
  still `True`, since I'm only adding words, not removing existing
  section markers.

### Risks & unknowns
- Risk: adding too many words to badge/link lines could accidentally
  change regex matches (e.g., `has_badges`, `has_demo_link` patterns in
  `readme_scorer.py`) if I'm not careful to keep those lines intact —
  mitigated by only adding new prose/sections, not editing existing
  lines.
- Unknown: whether the maintainer intended the fixture to hit
  "adequate" (100–499) instead of "comprehensive," which would mean the
  *assertion* on line 57 is the actual bug, not the fixture. I'm treating
  the fixture as the thing to fix (per the issue's suggested "extend the
  fixture" framing), but I'll note this alternative in the PR description
  in case a reviewer disagrees.
- Risk: other tests in `test_readme_scorer.py` (22 currently passing)
  could rely on a *short* fixture elsewhere — need to confirm I'm only
  editing the one fixture inside this specific test method, not a
  shared fixture used by other tests.

### Edge cases
- **Boundary word count:** the code uses `elif word_count < 500` so a
  count of exactly 500 already qualifies as "comprehensive" — but I'm
  targeting 550-650 words rather than sitting right at 500, so a small
  future edit to the fixture doesn't accidentally tip it back under the
  threshold and reintroduce this same failure.
- **Indentation inside the triple-quoted string:** the fixture is
  embedded in a Python test method with leading whitespace on every
  line. `content.split()` (used in `_score_readme`) splits on any
  whitespace and ignores this indentation, so it shouldn't inflate the
  word count — but I'll manually verify the printed `word_count` in the
  test log matches what I'd expect from the added prose alone.
- **Accidental duplicate pattern matches:** if new prose happens to
  include a second `![...](...)`-style image link or another phrase
  matching the demo-link regex, `has_badges`/`has_demo_link` would still
  correctly evaluate to `True` (they're boolean, not counts), so this
  isn't a real risk, but I confirmed it by rereading the regex checks
  in `readme_scorer.py` rather than assuming.
- **Other tests in the same file:** confirmed by reading the file that
  the other 22 tests in `test_readme_scorer.py` each define their own
  separate fixture strings, so extending this one fixture cannot affect
  any other test's expected word count or category.
