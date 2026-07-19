# Plan for Issue #152

## Goal

Allow the faithfulness checker to correctly recognize short supported claims without increasing false positives.

## Approach

1. Reproduce the issue on the original implementation.
2. Review how claims are tokenized and matched against retrieved context.
3. Keep the existing overlap threshold for longer claims.
4. Add special handling for short claims (three or fewer meaningful tokens) so that one meaningful overlap is sufficient.
5. Run the affected unit tests and the full faithfulness checker test suite.
6. Confirm the fix does not regress existing behavior.