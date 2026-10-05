# Fix Plan: Issue #69 - Output Parser JSON Array Fallback

## Diagnosis

The `parse_review_output()` function in `rag/generator/output_parser.py` calls `_parse_json_output()` after successfully parsing JSON with `json.loads()`, but `json.loads()` can return either a dict (object) or a list (array). The function assumes it's always a dict, so when a top-level JSON array is encountered, line 64 crashes trying to call `.items()` on a list.

**Root cause:** Type assumption mismatch. The code assumes `json.loads()` always returns a dict, but it returns whatever the JSON encodes—a list is valid JSON.

**Evidence from repro:**
- Repro step 1: JSON array input → AttributeError at line 64 on `.items()` call
- Repro step 4: `--debug` shows error during argparse's positional consumption
- The control run shows the issue is specific to array-shaped JSON

## Scope

**In scope:** Handle JSON arrays gracefully by checking the parsed type and falling back to plaintext parsing when a list is encountered (already the existing fallback path for unparseable JSON).

**Files:**
- `rag/generator/output_parser.py` (add type guards)
- `tests/unit/test_output_parser.py` (verify existing test passes)

**Not in scope:** Redesigning the JSON parsing strategy, handling nested arrays, or converting arrays to dict format.

## Approach

1. In `parse_review_output()`, after `json.loads()` succeeds, add a type guard: `if isinstance(data, dict):`
2. If the parsed data is not a dict, log a warning and continue to the plaintext fallback (existing path)
3. This mirrors the existing error-handling pattern: JSON parse failure → log warning → fallback

## Files to Change

### rag/generator/output_parser.py
- After JSON fence parsing (line 36), add type guard before calling `_parse_json_output()`
- After raw JSON parsing (line 43), add type guard before calling `_parse_json_output()`
- Log warnings when array is encountered (json_array_in_fence, json_array_fallback)

### tests/unit/test_output_parser.py
- No changes needed; test_json_array_fallback already verifies the expected behavior

## Test Plan

1. Run the failing case from the issue:
   ```python
   import json
   from rag.generator.output_parser import parse_review_output
   
   json_array = json.dumps(["First item", "Second item"])
   result = parse_review_output(json_array)
   ```
   **Expected:** Returns a list of FeedbackSection objects (via plaintext fallback), no crash

2. Verify control case still works:
   ```python
   json_dict = json.dumps({"skills": "Python", "experience": "5 years"})
   result = parse_review_output(json_dict)
   ```
   **Expected:** Returns FeedbackSection objects parsed from dict, exit 0

3. Run unit tests:
   ```bash
   pytest tests/unit/test_output_parser.py::TestOutputParser::test_json_array_fallback -v
   pytest tests/unit/test_output_parser.py::TestOutputParser -v
   ```
   **Expected:** test_json_array_fallback passes; all tests pass

## Implementation Status

**Fix implemented:** ✓
- Type guards added at both JSON parsing sites
- Warnings logged when arrays are encountered
- Plaintext fallback path engaged for arrays

## Risks and Unknowns

- **Risk:** Other parts of the codebase may depend on JSON parsing always succeeding for certain inputs. Mitigation: Run full test suite after fix.
- **Unknown:** Whether there are other top-level JSON types that could cause similar crashes. Mitigation: Type guard is specific to `dict`, so other types also fall through gracefully.
