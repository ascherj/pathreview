# Solution Plan for Issue #153

**Issue:** Faithfulness checker crashes when a context chunk has `text: None` 
[](https://github.com/jamjamgobambam/pathreview/issues/153)

## 1. Understand the Problem (Deductive Analysis)

### Root Cause (Step-by-step reasoning)
1. The `FaithfulnessChecker.check()` method builds a concatenated `context_text` string from multiple `context_chunks`.
2. It uses a list comprehension: `chunk.get("text", "")`.
3. **Key insight**: Python's `dict.get(key, default)` **only** returns the default if the *key is missing*. If the key exists with value `None`, it returns `None`.
4. This `None` value is then fed into `" ".join([...])`, which strictly requires string elements → `TypeError: sequence item 0: expected str instance, NoneType found`.
5. This occurs in real RAG pipelines when retrieval layers (DB, vector store, etc.) return incomplete chunks with explicit `None` for text fields.

### Expected vs Actual Behavior
- **Expected**: Graceful degradation — treat missing/invalid text as empty string, return a valid `float` score (typically `0.0` for no context).
- **Actual**: Hard crash, breaking the entire evaluation flow and any downstream processes (e.g., scoring feedback in review systems).

### Why This Matters
Malformed context is common in production RAG systems (network issues, partial DB records, schema evolution). The checker must be robust.

## 2. Mapping & Scope
- **Primary Target**: `rag/evaluator/faithfulness_checker.py` (the `check()` method).
- **Supporting**: `tests/unit/test_faithfulness_checker.py` (add regression test).
- **No impact** on other modules (isolated fix).

## 3. Detailed Implementation Plan
1. **Reproduce & Confirm**:
   - Run the minimal repro in Python REPL with `[{"text": None}]`.
   - Note exact line number and traceback.

2. **Safe Text Normalization** (Core Fix):
   - Change to `(chunk.get("text") or "")` — this correctly handles `None`, `False`, empty string, etc.
   - Add comment explaining the defensive programming choice.

3. **Unit Test Enhancement**:
   - Strengthen `test_none_context_chunk_text` to assert `score == 0.0` (or range) and no exception.
   - Test additional edge cases: missing key, empty list, empty string.

4. **Validation**:
   - Run full test suite: `pytest tests/unit/test_faithfulness_checker.py -q`.
   - Manual verification of the reproduction command.
   - Pre-commit hooks (ruff, black, mypy) pass.

5. **Documentation**:
   - Update `PLAN.md`, `JOURNAL.md`.
   - Add inline comments in code.

## 4. Inputs & Outputs (Formal Spec)
- **Inputs**:
  - `feedback`: `str` (generated text/claims).
  - `context_chunks`: `list[dict]` — each dict may have `"text": str | None | missing`.
- **Outputs**:
  - `float` in [0.0, 1.0] representing support ratio.
  - No exceptions for valid input shapes.

## 5. Risks, Unknowns & Mitigations
- **Risk 1**: Over-normalizing `None` hides data quality issues → Mitigation: Log when `None` is encountered.
- **Risk 2**: Score calculation edge cases (empty claims list) → Mitigation: Existing `if not claims` guard.
- **Unknown**: Downstream effects on LLM-based scoring (if any) — verified safe with current heuristic.

## 6. Edge Cases (Exhaustive)
- `context_chunks = [{"text": None}]` ← primary
- `context_chunks = [{}]` (no "text" key)
- `context_chunks = []` (no chunks)
- `context_chunks = [{"text": ""}]` (empty text)
- `context_chunks = [{"text": "valid"}] + None mixed`

## 7. Success Criteria
- Reproduction no longer crashes.
- All tests green.
- Code passes linting/formatting.
- PR ready with clear description.

**Status**: Implemented & Verified ✅
