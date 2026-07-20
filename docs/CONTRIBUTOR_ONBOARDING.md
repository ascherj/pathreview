# Contributor Onboarding Guide

This guide walks you through one full contribution to PathReview. You start at an
open issue. You finish at a pull request that is ready for review. Each step gives
the exact commands and the standard to follow.

If you only need a reference, see [SETUP.md](SETUP.md) for the environment and
[CONTRIBUTING.md](CONTRIBUTING.md) for the branch and commit rules. This guide
ties both together in the order you use them.

## Before you start

Install the tools in the [SETUP.md prerequisites](SETUP.md#prerequisites) table:
Git, Python 3.11, Node.js 18, Docker, and Docker Compose. You do not need to know
the whole codebase. You only need to run one part of it and change one thing well.

## Step 1 — Fork and clone

1. Open the repository on GitHub and select **Fork**. This creates your own copy.
2. Clone your fork. Replace `<your-username>` with your GitHub name:

   ```bash
   git clone https://github.com/<your-username>/pathreview.git
   cd pathreview
   ```

3. Add the original repository as `upstream`. You pull updates from it later:

   ```bash
   git remote add upstream https://github.com/ascherj/pathreview.git
   ```

Always clone your fork, not the original. You can only push branches to your fork.

## Step 2 — Set up the local environment

1. Copy the example environment file. The default values work for local use:

   ```bash
   cp .env.example .env
   ```

2. Start the backing services. Docker must run first:

   ```bash
   docker compose up -d
   ```

3. Run the first-time setup. This installs dependencies, applies migrations, and
   seeds the database:

   ```bash
   make setup
   ```

4. Start the application:

   ```bash
   make run
   ```

5. Open `http://localhost:5173` in your browser. Confirm that the app loads.

If a step fails, find the message in the [SETUP.md troubleshooting
section](SETUP.md#troubleshooting).

## Step 3 — Choose an issue

1. Open the issue tracker. Filter by a tier label.
2. Start with **Tier 1** for your first contribution. Tier 1 issues have a small,
   clear scope.
3. Read the issue in full. Make sure you understand what is broken and where.
4. Add a comment on the issue to claim it. This tells others that you work on it.

Pick an issue that you can explain in your own words. A clear scope now saves time
later.

## Step 4 — Create a branch

Create a branch from `main`. Use the naming format from CONTRIBUTING.md:

```
<type>/<issue-number>-<short-description>
```

For example, for issue 124:

```bash
git checkout main
git checkout -b fix/124-resume-parser-index-error
```

Use one of these types: `fix`, `feat`, `test`, `docs`, `refactor`, `perf`, or
`chore`. The issue number is the number on the GitHub issue page.

## Step 5 — Reproduce the problem

Confirm the problem on your machine before you change any code. Reproduction proves
that you understand the real behavior, not just the issue text.

- For a bug with a failing test, run that test and watch it fail:

  ```bash
  .venv/bin/pytest tests/unit/test_<name>.py -v
  ```

- For a bug with manual steps, follow the steps in the issue and record what you
  see.

Save the output. You use it later in your pull request description.

## Step 6 — Make the change

1. Find the file named in the issue. Read the surrounding code first.
2. Make the smallest change that fixes the problem.
3. Match the style of the code around your change.
4. Add or update tests. Every code change needs a test that covers it.

Keep your change focused. Do not fix unrelated problems in the same branch.

## Step 7 — Test and check your work

Run the project checks before you open a pull request:

```bash
make check       # Runs the linter, the formatter, and the type checker
make test-unit   # Runs the unit tests
```

Both must pass for the code you change. Fix any problem that your change causes.

## Step 8 — Commit your work

Use the Conventional Commits format from CONTRIBUTING.md:

```
<type>(<scope>): <description>
```

Use one of these scopes: `ingestion`, `rag`, `agent`, `safety`, `api`, or
`frontend`. Name the issue in the footer. For example:

```bash
git add path/to/changed_file.py tests/unit/test_changed_file.py
git commit -m "fix(ingestion): handle missing experience section in resume parser

Add a bounds check before the code reads the experience list.

Fixes #124"
```

Then push your branch to your fork:

```bash
git push -u origin fix/124-resume-parser-index-error
```

## Step 9 — Open a pull request

1. Open your fork on GitHub. Select **Compare & pull request** for your branch.
2. Set the base to `ascherj/pathreview` and the branch `main`.
3. Fill in every section of the pull request template:
   - **Summary** — say what the change does and why.
   - **Issue** — write `Closes #<number>`.
   - **Changes** — list the specific changes.
   - **Testing** — give the steps a reviewer follows to check your work.
   - **Notes for Reviewers** — point out anything that needs attention.
4. Create the pull request. Leave it as ready for review, not a draft.

A reviewer who has not seen your code must understand the change from the
description alone.

## Step 10 — Respond to review

1. Read each review comment.
2. Make the requested changes on the same branch.
3. Push again. The pull request updates on its own.
4. Reply to each comment so the reviewer knows what you changed.

Respond within 48 hours when you can. Clear replies keep the review short.

## Quick command reference

| Task | Command |
|---|---|
| Start services | `docker compose up -d` |
| First-time setup | `make setup` |
| Run the app | `make run` |
| Run unit tests | `make test-unit` |
| Run all checks | `make check` |
| Reset the database | `make reset-db` |

You now have the full path from an open issue to a pull request. Follow the same
steps for every contribution.
