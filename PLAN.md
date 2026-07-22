# Issue #149 Plan

## Reproduction

`StructuralChunker.chunk()` returns an empty list when given a non-empty plain-text document without Markdown headings.

## Expected behavior

A non-empty document without headings should still produce at least one valid chunk instead of being silently excluded from the RAG index.

## Files to inspect

- `ingestion/chunking/structural_chunker.py`
- `tests/unit/test_structural_chunker.py`

## Implementation plan

1. Read the current `StructuralChunker.chunk()` logic.
2. Identify why no-heading documents produce no sections.
3. Add a fallback for non-empty documents without headings.
4. Preserve existing behavior for documents with headings.
5. Confirm empty or whitespace-only documents are still handled correctly.
6. Update or add unit tests.

## Risk

The main risk is changing behavior for documents that already contain valid Markdown headings or creating one oversized chunk for long plain-text documents.

## Test plan

- Run the existing no-heading test.
- Run all structural chunker tests.
- Run `make check`.
- Run `make test-unit`.