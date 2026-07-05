# Contribution Journal

A running record of my Module 3 open-source contribution work on **PathReview**.

## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/41

**Issue title:** `github_tool.py` raises `KeyError` when a repository has no description

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The agent's GitHub analysis tool reads repository metadata from the GitHub REST
API and pulls out fields like the repo description. The reported bug is that the
description field is accessed directly (without checking whether it is present or
`null`), so any repository created without a description makes the tool throw a
`KeyError` / `AttributeError` and the whole repo-analysis step for that user's
portfolio crashes instead of degrading gracefully. A successful fix makes the
tool treat a missing or `null` description as an empty string (a safe default),
so analysis completes normally for description-less repos, and adds a unit test
that reproduces the missing-description case so the regression can't come back.
This lives entirely in the agent subsystem — `agent/tools/github_tool.py` — plus
a new/updated test in `tests/unit/test_github_tool.py`.

**Branch name:** fix/41-github-tool-keyerror-no-description

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

### "Is this right for me?" — scope reasoning

- **Single subsystem, small blast radius.** The change touches one file in the
  `agent` subsystem plus one test file. No cross-cutting API/DB/frontend work.
- **Estimated effort is 1–2 hours** and it's labelled `good first issue` +
  `tier-1` — appropriate for a first contribution to a large codebase.
- **Clear reproduction and success criteria.** "Repo with no description →
  should not crash" is easy to write a failing test for and to verify green.
- **Skills match.** Straightforward Python (dict access / null handling) plus a
  pytest unit test — no unfamiliar tooling required.
- **Risk note for the fix (later weeks).** When I read the current code in my
  fork, `agent/tools/github_tool.py` already guards the description with
  `repo_json.get("description") or ""`, and `tests/unit/test_github_tool.py`
  does not yet exist. So the actual work will lean toward *adding the missing
  regression test* (and confirming the guard holds for the exact case the issue
  describes) rather than patching a live crash. I'll confirm the current
  behaviour against the issue's repro before opening the PR.

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/RyannWinn/pathreview/commit/48e2d6f9c8367a8f62897d5151dc9ef0dec79515

**Reproduction summary:**
I stood up the project locally (Python 3.11.15 venv, `pip install -e ".[dev]"`)
and drove `GitHubTool.execute` with a mocked GitHub API response whose
`description` was `null`, plus a variant with the key absent. Reproducing the
exact access pattern the issue reports — `repo_data['description'].strip()` —
confirms the reported failure class is real: it raises `AttributeError` on a
`null` value and `KeyError` when the key is missing. However, the tool's *live*
extraction already guards this (`repo_json.get("description") or ""`), so
`execute` returns `description == ""` instead of crashing. The genuine gaps are
that (a) no regression test existed to lock the behaviour in, and (b) the guard
dropped the whitespace `.strip()` normalisation the issue references. I captured
all of this in `tests/unit/test_github_tool.py` (5 passing + 1 `xfail` for the
not-yet-restored stripping).

**PLAN.md link:** [PLAN.md](PLAN.md)

**Walkthrough video (recommended):** _(not recorded yet)_

**Blockers or open questions:**
The manifest describes a buggy `.strip()` line that isn't literally present in
this seeded snapshot, so my fix is test-first (regression lock) plus restoring
null-safe stripping rather than a "remove the crash" diff. Open question for a
mentor: do maintainers want the PR scoped purely to the regression test, or is
restoring `.strip()` normalisation in scope for issue #41 too?
