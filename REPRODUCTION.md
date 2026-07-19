# Issue #152 Reproduction

## Issue

The faithfulness checker could not mark short claims as supported because it required at least two meaningful overlapping tokens between a claim and the retrieved context.

## Environment

- Python 3.13.1
- pytest 9.1.1
- Base commit: `664c3d7`
- Fix branch: `fix/152-short-claim-support`

## Reproduction command

```bash
python -m pytest tests/unit/test_faithfulness_checker.py -k "partial_support_returns_middle_score or multiple_context_chunks or multiple_claims_varying_support" -v
```

## Result before the fix

At commit `664c3d7`, the three selected tests failed:

- `test_partial_support_returns_middle_score`
- `test_multiple_context_chunks`
- `test_multiple_claims_varying_support`

Each test returned a faithfulness score of `0.0`, even when the retrieved context supported one or more short claims.

```text
3 failed, 19 deselected
```

## Result after the fix

On branch `fix/152-short-claim-support`, the same command passed:

```text
3 passed, 21 deselected
```

## Conclusion

The issue was successfully reproduced on the original implementation. The updated checker now recognizes supported short claims while maintaining stricter matching behavior for longer claims.