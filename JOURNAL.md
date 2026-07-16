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

**Reproduction commit link:** [paste your commit link here]

**Reproduction summary:**
Because this is a feature gap rather than a bug, my reproduction involved navigating the local application to the user dashboard/review history view. I confirmed that there is currently no UI element, route, or utility that allows a user to select multiple reviews for comparison. I documented this missing state with a commit outlining where the entry point for the new feature should live.

**PLAN.md link:** [PLAN.md]

**Blockers or open questions:**
I need to investigate the existing data flow to see if a user's full review history is already available in the frontend state, or if I will need to modify the data-fetching logic to populate the comparison dropdowns.