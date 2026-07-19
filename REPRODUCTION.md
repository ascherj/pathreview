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