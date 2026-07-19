# Solution plan

**Issue:** Faithfulness checker can never mark short claims as supported  
**Issue link:** [Issue #152](https://github.com/jamjamgobambam/pathreview.git)

## Understand

The faithfulness checker decides whether claims in generated feedback are supported by retrieved context.

The root cause is that the current matching logic requires at least two meaningful overlapping tokens between a claim and the context. Short claims such as "Knows Python" may contain only one meaningful domain-specific token after common words are removed. Even when the retrieved context explicitly mentions Python, the claim is incorrectly marked unsupported.

Expected behavior:

- A short claim should be considered supported when its meaningful subject appears in the context.
- Longer claims should continue requiring stronger token overlap.

Actual behavior:

- Valid short claims receive no support.
- This can cause the overall faithfulness score to incorrectly become `0.0`.

## Map

The main files involved are:

- `rag/evaluator/faithfulness_checker.py`
  - Contains the `FaithfulnessChecker` implementation.
  - Contains claim extraction, tokenization, and claim-support matching logic.
- `tests/unit/test_faithfulness_checker.py`
  - Contains the unit tests used to reproduce and verify the issue.
- `REPRODUCTION.md`
  - Documents the failing behavior on the original commit and the passing behavior after the fix.

The main logic to investigate is the function that determines whether an extracted claim is supported by the combined retrieved context.

## Plan

1. Review the existing claim extraction and token-overlap logic in `rag/evaluator/faithfulness_checker.py`.
2. Normalize claims and context through a shared tokenization helper so comparisons use consistent lowercase meaningful tokens.
3. Detect short claims containing three or fewer meaningful tokens.
4. Allow one meaningful overlapping token to support a short claim while preserving the existing two-token requirement for longer claims.
5. Ensure competency-list claims such as Python, JavaScript, and Docker are evaluated separately when appropriate.
6. Add or update tests in `tests/unit/test_faithfulness_checker.py` for short supported claims, unsupported short claims, multiple context chunks, and mixed support.
7. Run the focused regression tests and the complete faithfulness checker test suite.

## Inputs & outputs

### Inputs

The checker receives:

- Generated feedback as a string.
- Retrieved context chunks containing supporting text.

Example input:

- Feedback: `"Python expert. Knows Rust. Skilled with Docker."`
- Context: `"Python and Docker expertise shown in projects."`

### Outputs

The checker returns a floating-point faithfulness score between `0.0` and `1.0`.

For the example above:

- Python should be supported.
- Docker should be supported.
- Rust should be unsupported.
- The resulting score should represent partial support instead of incorrectly returning `0.0`.

## Risks & unknowns

- Reducing the overlap threshold too broadly could create false positives for unrelated claims sharing one generic word.
- The short-claim rule must only use meaningful tokens after stop-word filtering.
- Programming language names such as Python or Rust must not be removed or treated as generic words.
- Claim extraction may combine several technologies into one sentence, which could hide partially supported competencies.
- Changes in `rag/evaluator/faithfulness_checker.py` could affect existing scoring behavior for longer claims.
- The full unit test suite must be checked for regressions after changing the matching threshold.

## Edge cases

The fix should handle:

- A one-token competency claim that appears in the context, such as `"Python."`
- A short claim whose meaningful token does not appear in the context.
- Multiple short claims with a mixture of supported and unsupported technologies.
- Different capitalization, such as `"python"` versus `"Python"`.
- Punctuation around technology names.
- Empty feedback.
- Empty context chunks.
- Context split across multiple chunks.
- Longer claims that share only one token and should remain unsupported.
- Repeated claims or repeated context terms without artificially increasing the score.