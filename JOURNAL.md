# PathReview — Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/52

**Issue title:** Add a `contribution_streak` field to the GitHub analysis (longest consecutive days of commits)

**Tier:** [ ] Tier 1  [x] Tier 2  [ ] Tier 3

**Problem summary:**
The agent's GitHub analysis tool (`agent/tools/github_tool.py`) currently reports on a
user's repositories and activity, but has no way to measure how consistently someone
contributes over time. Right now the tool can't distinguish a developer with steady,
sustained activity from one with a single burst of commits, even though consistency is a
meaningful signal for a portfolio reviewer. A successful fix adds a `contribution_streak`
field that computes the longest run of consecutive days with at least one commit from the
user's GitHub contribution history, and wires that value into the tool's output alongside
the other GitHub analysis fields.

**Scope reasoning ("Is this right for me?"):**
This is labeled Tier 2 ("intermediate — requires cross-module understanding"), not Tier 1,
so I went in with eyes open that it touches more than an isolated bug fix. It's scoped to a
single file (`agent/tools/github_tool.py`) with a clear, well-defined feature request and no
ambiguity about what "done" looks like, which keeps it tractable. The main added work
versus a Tier 1 issue is that no test file is pre-listed, so I'll need to understand the
existing `BaseTool` interface and the agent orchestration wiring well enough to write my own
unit tests, per `docs/CONTRIBUTING.md`. Estimated effort is 4–6 hours, which fits the
Module 3 timeline.

**Branch name:** `feat/52-contribution-streak`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger
