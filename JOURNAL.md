## Week 7 — Issue selection

**Issue link:** [https://github.com/jamjamgobambam/pathreview/issues/102]

**Issue title:** [Add a before/after comparison view for users who have completed multiple reviews]

**Tier:** [ ] Tier 1  [ ] Tier 2  [X] Tier 3

**Problem summary:**
[Currently, users who submit their portfolios for multiple reviews over time cannot easily compare their past and present results to track their progress. This issue requires building a brand new comparison feature on the frontend that allows users to select two distinct reviews and view a side-by-side visual difference of their scores and feedback. A successful fix will involve creating a new page component (frontend/src/pages/ComparisonView.tsx) and a utility for formatting the data differences (frontend/src/utils/diffFormatter.ts), ultimately giving users a clear picture of their improvement.]

**Branch name:** [paste branch name here]

**Setup confirmation:** [X] App runs locally at localhost:5173

**Cohort ledger:** [X] Issue added to cohort ledger

**Checklist Reasoning:** I reviewed the "Is this right for me?" checklist before claiming this issue. 
* **Part 1 (Understanding):** I clearly understand the "done" state—a side-by-side UI showing diffs of two specific reviews. 
* **Part 2 (Tier Fit):** I selected a Tier 3 issue because I have strong prior experience with React and feel confident building a new component from scratch without getting overwhelmed. 
* **Part 3 (Codebase):** I've identified exactly where the new files (`ComparisonView.tsx` and `diffFormatter.ts`) need to be created and how they fit into the existing frontend structure. 
* **Part 4 (Scope):** The 7–10 hour estimate is realistic for my schedule over the next two weeks, and there are no external blockers.

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [https://github.com/ColonelToad/pathreview/commit/74aa05357fcd305273fcb5b7b68a9a5dd100201c]

**Reproduction summary:**
Because this is a feature gap rather than a bug, my reproduction involved navigating the local application to the user dashboard/review history view. I confirmed that there is currently no UI element, route, or utility that allows a user to select multiple reviews for comparison. I documented this missing state with a commit outlining where the entry point for the new feature should live.

**PLAN.md link:** [PLAN.md]

**Blockers or open questions:**
I need to investigate the existing data flow to see if a user's full review history is already available in the frontend state, or if I will need to modify the data-fetching logic to populate the comparison dropdowns.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
I have successfully implemented all sub-tasks from my PLAN.md. 
1. Created `frontend/src/utils/diffFormatter.ts` to calculate score deltas and identify text changes.
2. Built the `frontend/src/pages/ComparisonView.tsx` component to fetch the review history and display the side-by-side comparison.
3. Updated `frontend/src/App.tsx` to register the new `/compare` protected route.
4. Added a conditional "Compare Reviews" button to `frontend/src/pages/DashboardPage.tsx` that only appears if the user has 2 or more reviews.

**Next steps:**
Since I worked ahead and already wrote my unit tests, my next steps are to open a Draft PR, document the pre-existing test failures I found on `main`, and request a peer review before finalizing my submission.

**Blockers:**
I briefly ran into a blocker with the testing framework—the course guide referenced Python `pytest` setups, but the frontend uses `Vitest`. I successfully navigated this by matching the existing `Vitest` pattern found in the `frontend/src/components/__tests__/` directory.

---

### Check-in 2 (end of week)

**PR link:** [Insert link to your submitted pull request here]

**Branch:** [`feat/102-comparison-view`]

**What you built:**
I built a progress-tracking feature that allows users to visualize how their portfolio reviews have changed over time. The feature introduces a new `ComparisonView` page that fetches the user's review history, lets them select an older and newer review via dropdowns, and renders a side-by-side visual difference. It calculates absolute score deltas (highlighting improvements in green and regressions in red) and highlights whether written feedback was updated.

**Tests added or updated:**
I created a new test suite at `frontend/src/components/__tests__/DiffFormatter.test.tsx` (following the existing frontend test directory structure). It covers the `calculateScoreDiff` and `calculateTextDiff` utility functions, ensuring that positive, negative, and flat score trends are accurately calculated, text changes are detected, and missing data (`undefined`) is handled gracefully without crashing the UI.

**Self-review confirmation:** 
[X] make check passes  
[X] make test-unit passes 
*(Note: I observed 182 linting errors and 2 test failures in `ProfileForm.test.tsx` and `ReviewSection.test.tsx` upon creating my branch. My code introduces no new failures to the baseline).*

**Draft PR feedback received from:** [Insert name, Discord handle, or "none"]