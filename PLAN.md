# Solution plan

**Issue:** `github_tool.py` raises `KeyError` when a repository has no description
— [issues manifest C-01 / #41](https://github.com/jamjamgobambam/pathreview/issues/41)

### Understand

**Reported root cause.** The issue reports that the GitHub tool reads
`repo_data['description'].strip()` directly. GitHub's REST API returns
`"description": null` for repositories created without a description (and may
omit fields entirely), so that access pattern throws an unhandled
`KeyError` / `AttributeError` and the repo-analysis step for that portfolio
crashes instead of degrading.

**What I actually found (Week 8 reproduction).** The failure *class* is real and
reproducible — feeding a `description: null` payload into
`repo_data['description'].strip()` raises `AttributeError`, and an absent key
raises `KeyError` (see `tests/unit/test_github_tool.py`). **But** the current
extraction in `_fetch_repo_metadata` already guards the value:

```python
"description": repo_json.get("description") or "",   # github_tool.py:101
```

So `GitHubTool.execute` no longer crashes — a null/missing description degrades
to `""`. The remaining, genuine gaps are:

1. **No regression test exists.** `tests/unit/test_github_tool.py` did not exist
   before this branch, so nothing prevents the guard from silently regressing
   back to the crashing form the issue describes.
2. **The guard dropped the `.strip()` normalisation** the issue references: the
   value is returned raw, so `"  padded  "` stays padded. A complete fix should
   be null-safe *and* strip surrounding whitespace.

**Expected vs. actual (after fix):**

| Input `description` | Current | Expected |
|---|---|---|
| `null` | `""` ✅ | `""` |
| key absent | `""` ✅ | `""` |
| `"  padded  "` | `"  padded  "` ❌ | `"padded"` |
| `"Hello"` | `"Hello"` ✅ | `"Hello"` |

### Map

Files I expect to touch:

- `agent/tools/github_tool.py` — the `_fetch_repo_metadata` method, line 101
  (the `description` extraction). This is the single source of the fix.
- `tests/unit/test_github_tool.py` — regression tests (added on this branch in
  Week 8; the `.strip()` case is currently `xfail` and flips to a passing
  assertion once the fix lands).

Not touched (verified during reproduction): no downstream consumer accesses the
description via unguarded subscript (`grep` for `repo_data[` / `.strip()` across
`agent/`, `api/`, `core/`, `rag/`, `ingestion/` found no other call sites), so
the blast radius is one method.

### Plan

1. **Harden the extraction.** Change line 101 to be null-safe *and* preserve the
   normalisation the issue references:
   `"description": (repo_json.get("description") or "").strip()`.
2. **Flip the xfail.** Remove `@pytest.mark.xfail` from
   `test_execute_description_is_stripped` so it becomes a live assertion.
3. **Run the unit suite** (`make test-unit` / `pytest tests/unit/test_github_tool.py -v`)
   and confirm all six cases pass with no new failures elsewhere.
4. **Lint/type-check** the changed file (`ruff`, `mypy agent/`) so the PR is clean.
5. **Open the PR** referencing the issue, summarising the reproduction finding
   (crash class real; guard already present; fix restores stripping + adds the
   missing regression test).

### Inputs & outputs

- **Input:** the JSON object returned by `GET /repos/{owner}/{repo}`, whose
  `description` field may be a string, `null`, or absent.
- **Output:** the `metadata` dict returned by `_fetch_repo_metadata`, whose
  `description` is always a `str` — empty for null/missing, whitespace-stripped
  otherwise. `GitHubTool.execute` returns `ToolResult(success=True, ...)` for all
  of these instead of raising.

### Risks & unknowns

- **Behavioural change from `.strip()`.** Restoring stripping alters output for
  descriptions with leading/trailing whitespace. Low risk (whitespace-only
  descriptions become `""`, which is the desired safe default), but I'll note it
  in the PR in case any consumer relied on raw spacing.
- **Scope creep vs. the filed issue.** The literal crash is already guarded, so
  the substantive change is the test + the `.strip()` restoration. I'll keep the
  PR tightly scoped and let the reproduction notes justify why the test is the
  core deliverable.
- **Seeded-repo mismatch.** The manifest describes a buggy `.strip()` line that
  isn't literally present in this snapshot; if maintainers expect a "remove the
  crash" diff, the reproduction section explains why the diff is test-first.
- **Unknown:** whether `_has_readme`'s extra network call should also be mocked
  in tests — handled by patching `_has_readme` so tests stay offline/unit.

### Edge cases

- `description` is `null` → `""`.
- `description` key entirely absent from the payload → `""`.
- `description` is `""` (empty string) → `""` (no crash on `.strip()`).
- `description` is whitespace-only, e.g. `"   "` → `""`.
- `description` has surrounding whitespace → trimmed.
- Normal non-empty description → passed through unchanged.
- Non-2xx responses (404/403) and network errors → still handled by the existing
  `execute` try/except (unchanged, but covered so the fix doesn't regress them).
