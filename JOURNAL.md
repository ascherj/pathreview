Week 7 — Issue selection

Issue link: Issue #117 — API docs don't include example curl commands

Issue title: API docs don't include example curl commands

Tier:  Tier 1 

Problem summary:
The PathReview API documentation identifies the available endpoints, but it does not provide command-line examples showing how to call them. This makes it difficult for new contributors to quickly test the API and confirm that their local backend is working correctly. The issue primarily affects docs/API.md rather than the application’s core frontend or backend logic. A successful fix will add clear and accurate curl commands that developers can copy and run against the local API.

“Is this right for me?” checklist reasoning:
I selected this Tier 1 issue because this is my first contribution to the PathReview codebase, and I am still becoming familiar with its architecture and development workflow. The task has a focused scope because the primary file involved is docs/API.md, rather than several interconnected source-code files. I understand the basic technologies involved, including HTTP requests, API endpoints, JSON, and command-line tools, and I can verify the examples by running the application locally. The expected result is also clear and testable: each documented curl command should match a real endpoint and produce the expected API response. Based on its limited scope, defined output, and Tier 1 label, this issue is appropriate for my current comfort level.

Branch name: docs/117-add-curl-examples

Setup confirmation: App runs locally at localhost:5173

Cohort ledger:Issue added to cohort ledger