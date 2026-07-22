# Journal

## Week 7 — Issue selection

**Issue link:** [\[Issue-68\]](https://github.com/ascherj/pathreview/issues/68)

**Issue title:** Add a safety event count to the health check endpoint #68

**Tier:** [ x ] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The /health endpoint return service status but no safety metrics. The safety events last hour field. At this time the value is hardcoded to 0 instead of grabbing the actual event count from redis. This will need to be updated, which will then return the correct metric.

**Branch name:** fix/68-health-check-safety-event

**Setup confirmation:** [ x ] App runs locally at localhost:5173

**Cohort ledger:** [ x ] Issue added to cohort ledger

## Is This Issue Right for Me?

Use this checklist before you claim an issue on the pathreview tracker. Work through every question. If you're unsure about something, investigate before committing — a few minutes of research now saves several hours of being stuck in Week 9.

### Part 1 — Understanding the Issue

**Can I explain what this issue is asking for in my own words?**

Paraphrase the issue without looking at it. If you can't, you don't understand it well enough yet. Read the full issue body, look at any linked PRs or comments, and try again.

- [x] I can explain the problem and the expected behavior in 2–3 sentences without reading the issue.

**Do I understand which part of the app is affected?**

Check the labels on the issue — they often indicate the area (api, rag, ingestion, frontend, etc.). Look at the referenced files if any are mentioned. Find those files in the repo.

- [x] I've located the relevant files and confirmed they exist in the codebase.

**Do I understand what "done" looks like?**

Can you describe what the app should do (or not do) once the issue is fixed? If the issue has acceptance criteria, read them carefully. If it doesn't, try writing your own — that forces you to understand the scope.

- [x] I can describe a concrete before-and-after: what the user sees before the fix and what they see after.

### Part 2 — Tier Fit

Issues in the tracker are tagged with a tier level. Here's what each one means:

| Tier | Description | Typical scope |
| --- | --- | --- |
| Tier 1 | Self-contained, localized fix. The change lives in one or two files and doesn't require understanding how the whole system fits together. | Bug fix, missing validation, broken test, documentation update |
| Tier 2 | Requires understanding how two or more modules interact. May involve a service layer, database model, or API endpoint. | Feature addition, refactor, data flow bug |
| Tier 3 | Requires understanding the full system — multiple modules, possibly infrastructure or AI pipeline changes. | Architecture change, cross-cutting behavior, RAG or agent modification |

**Is the tier a realistic match for where I am right now?**

If this is my first open source contribution: I'm choosing Tier 1.
If I've contributed to large codebases before: Tier 2 or 3 is fair game.
I'm not choosing a Tier 3 issue to "challenge myself" if I haven't completed a Tier 1 or 2 first — scope surprises in Week 9 don't have a safety net.

- [x] I've chosen a tier that matches my experience level and I'm not overreaching.

### Part 3 — Codebase Readiness

**Can I find the relevant code?**

Before claiming the issue, locate the specific function, route, or module it describes. Don't rely on grep alone — open the file, read the surrounding context, and confirm you're in the right place.

- [x] I've found and read the specific code the issue references (not just the file — the function or section).

**Do I understand the surrounding code well enough to change it safely?**

You don't need to understand the whole codebase. But you need to understand the file you're about to edit well enough to predict what a change will break. Read the function signatures, docstrings, and any callers.

- [x] I've read enough surrounding context that I can write a rough plan for the fix without looking anything up.

**Have I read the relevant test file?**

Find the test file for the module your issue touches (tests/unit/ is the right place to start). Look at how existing tests are structured — fixtures, assertions, mock patterns. You'll need to write at least one new test.

- [x] I've found the test file for my module and read at least one test end-to-end.

### Part 4 — Scope and Time

**How many others are already working on this issue?**

Claims are non-exclusive — more than one student may work on the same issue, and your grade comes from your own artifacts, never from being first. Still, check the issue comments and the Claims column in the Issue Catalog tab of the cohort ledger: a less-crowded issue of the same tier can mean smoother coaching and peer review.

- [x] I've checked the issue comments and the ledger's Claims count, and I'm fine with how many others are on this issue.

**Is the scope realistic for Weeks 8–9?**

You have roughly two weeks to implement, test, and submit a PR. Tier 1 issues should take 3–6 hours of focused work. Tier 2 issues may take 8–12 hours. Tier 3 issues can take significantly longer.

Think about your week — other classes, work, other commitments. Is this achievable?

- [x] I've estimated the time this will take and I'm confident I can complete it before the Week 9 deadline.

**Are there any blockers or dependencies?**

Some issues say "blocked by #X" or reference another issue that needs to be resolved first. Check the issue for any such dependencies.

- [x] This issue has no open blockers or dependencies on other unresolved issues.

