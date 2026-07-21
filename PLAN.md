# Solution Plan — Issue #156

## Issue

**Title:** README scorer test fixture is too short for its own word-count assertion  
**Link:** https://github.com/ascherj/pathreview/issues/156  
**Tier:** Tier 1  
**Working branch:** `test/156-fix-readme-scorer-fixture`

## Problem Summary

The `test_readme_with_all_quality_signals` unit test is intended to verify that a comprehensive README containing all supported quality signals receives a high score. However, its README fixture contains only 51 words. The test asserts that the word count is greater than 100 and that its category is `comprehensive`, so the fixture does not satisfy its own expectations.

The README scorer categorizes content with fewer than 100 words as `minimal`, content from 100 through 499 words as `adequate`, and content with at least 500 words as `comprehensive`. The scorer correctly categorizes the current 51-word fixture as `minimal`, indicating that the problem is in the test fixture rather than the scoring implementation.

## Reproduction

Run the affected test from the repository root:

```bash
pytest tests/unit/test_readme_scorer.py::TestReadmeScorer::test_readme_with_all_quality_signals -vv
```

### Observed result

The test fails with:

```text
assert 51 > 100
```

The captured scorer output reports:

```text
category=minimal
word_count=51
```

### Expected result

The fixture should contain enough meaningful content to represent a comprehensive README. The test should pass while continuing to verify installation instructions, usage instructions, badges, a demo link, a technology-stack section, a comprehensive word-count category, and a high overall score.

## Root Cause

The production scorer and the fixture have conflicting definitions of the test scenario. The scorer requires at least 500 words for the `comprehensive` category, while the fixture contains only 51 words. Because the test is specifically named `test_readme_with_all_quality_signals` and expects the `comprehensive` category, the fixture does not contain enough content to model the scenario it is intended to test.

## Proposed Solution

Expand the README fixture in `test_readme_with_all_quality_signals` with realistic project documentation until it contains at least 500 words. Preserve all existing quality signals, including:

- Installation instructions
- Usage instructions and an example
- Feature descriptions
- Technology-stack information
- Build and coverage badges
- A live demo link

The preferred change is to correct the test fixture rather than modify the production scorer. The scorer’s thresholds are already validated by dedicated word-count category tests.

## Implementation Steps

1. Update the README fixture inside `test_readme_with_all_quality_signals`.
2. Add meaningful sections and explanations that resemble a realistic comprehensive README.
3. Ensure the expanded fixture contains at least 500 words so the scorer returns the `comprehensive` category.
4. Preserve the fixture’s installation, usage, badge, demo-link, and technology-stack signals.
5. Run the affected test and confirm that all of its assertions pass.
6. Run the complete README scorer test file to check for regressions.
7. Run the repository’s required formatting, linting, type-checking, and unit-test commands before opening the pull request.

## Files to Modify

### `tests/unit/test_readme_scorer.py`

Expand the fixture used by `test_readme_with_all_quality_signals`. No production-code changes are currently expected.

### `JOURNAL.md`

Record the reproduction result, root-cause analysis, planned solution, and later implementation results.

## Files Inspected

### README scorer implementation

The implementation was inspected to confirm the word-count thresholds and overall-score calculation. It categorizes a README as `comprehensive` when its word count is at least 500.

### `tests/unit/test_readme_scorer.py`

The test file was inspected to compare the failing fixture with the dedicated tests for the `minimal`, `adequate`, and `comprehensive` categories.

## Validation Plan

First, run the affected test:

```bash
pytest tests/unit/test_readme_scorer.py::TestReadmeScorer::test_readme_with_all_quality_signals -vv
```

Then run the complete README scorer test file:

```bash
pytest tests/unit/test_readme_scorer.py -q
```

Finally, run the repository’s required checks:

```bash
make check
make test-unit
```

The change will be considered successful when:

- The affected test passes.
- The fixture is categorized as `comprehensive`.
- All expected README quality signals remain `True`.
- The overall score remains above `0.7`.
- No other README scorer tests regress.
- The project’s required checks pass.

## Risks and Unknowns

- Expanding the fixture to only slightly more than 100 words would satisfy the first assertion but would still produce the `adequate` category. The fixture must contain at least 500 words to satisfy the existing scorer behavior.
- Repetitive filler could make the fixture difficult to understand and maintain. The added content should resemble useful project documentation.
- Added text must preserve the keywords and Markdown patterns used to detect installation, usage, badges, demo links, and the technology stack.
- The existing assertion checks for more than 100 words even though the expected `comprehensive` category begins at 500 words. The fixture can satisfy both assertions without changing them, but aligning the word-count assertion more directly with the comprehensive threshold may require maintainer guidance.
- The full unit-test suite may contain unrelated failures documented in other open issues. Any unrelated failures will be recorded separately and not addressed as part of issue #156.

## Out of Scope

- Changing the scorer’s word-count thresholds
- Redesigning the overall scoring formula
- Modifying other README scorer tests unless required by the fixture correction
- Addressing unrelated test-suite failures