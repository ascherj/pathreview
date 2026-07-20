# Solution Plan — Faithfulness checker short-claim scoring (#152, #153)

Last updated: 2026-07-19

## Scope

Fix the faithfulness checker so the short factual claims reported in issue #152 can be
scored as supported, without replacing the module's lexical-overlap model with a
hand-built entailment system. Also prevent the `None`-text crash described in issue
#153.

In scope:

- the issue's exact `Knows Python. Knows SQL.` reproduction;
- punctuation- and Unicode-safe tokenization;
- a narrowly gated one-token support rule;
- graded partial support for the existing middle-score tests;
- `None` context text;
- regression tests for false support introduced by the short-claim rule.

Out of scope:

- general natural-language entailment;
- entity/coreference resolution;
- semantic negation or antonym reasoning;
- changing retrieval, generation, prompts, or API behavior;
- unrelated repository-wide lint, formatting, and type debt.

## Reproduction on `main`

Environment: Python 3.11.9, base SHA `d5f196d`.

```python
from rag.evaluator.faithfulness_checker import FaithfulnessChecker

checker = FaithfulnessChecker()
checker.check(
    "Knows Python. Knows SQL.",
    [{"text": "python expert"}, {"text": "sql expert"}],
)
# main: 0.0
```

The original implementation requires at least two non-stop-word overlaps. Each issue
claim has only one concrete fact token, so neither can pass. Three related tests also
expose punctuation and all-or-nothing scoring gaps. A context chunk with `text=None`
raises while the context strings are joined.

## Final design

### 1. Normalize tokens without inventing component matches

- Normalize text to Unicode NFC and use case-folding.
- Normalize curly apostrophes.
- Preserve `C++`, `C#`, accented words, contractions, and word-internal compounds;
  remove soft-hyphen display hints.
- Preserve ASCII/Unicode hyphen and underscore compounds as one token, so `Go` does
  not match `go-to-market`, `C` does not match `Objective-C`, and `Python` does not
  match `non_python` or `Non–Python`.
- Preserve ampersand compounds so bare `R` does not match `R&D`.
- Strip ordinary punctuation, so `Python,` matches `python`.

### 2. Keep the original multi-token floor

Material predicates and qualifiers remain claim terms. A multi-token claim is fully
supported only after at least two of its terms match, preserving `main`'s core rule.
For example, `Python expert` does not collapse to `python`, and `Uses Kubernetes` does
not collapse to `kubernetes`.

When a claim contains a concrete anchor, matching generic portfolio words cannot
substitute for that missing anchor. Claims made entirely of generic terms retain the
original two-match behavior. This is a lexical guard, not a completeness claim about
all possible descriptors.

### 3. Gate the one-token exception to issue-shaped claims

One matched concrete token can support a claim only when either:

1. the claim contains one term after the original function-word filter; or
2. it has the ordered reporting form `Knows <fact>` or
   `[The] candidate knows <fact>`, and removing that prefix leaves one term.

The order check matters: `Python knows` and `Knows candidate Python` do not receive the
exception. Material claims such as `Python expert`, `AWS certified`, and
`Python developer` retain the two-match floor.

### 4. Preserve graded partial evidence below the support threshold

Each claim receives an overlap score. A claim that does not meet the support rule is
capped at `0.4`, strictly below the `0.5` support threshold. This lets the existing
partial-support tests return a middle score without classifying a one-token fragment of
a multi-token claim as supported.

### 5. Handle missing context text

Tokenize `chunk.get("text") or ""` so an explicit `None` is treated as empty context
and valid sibling chunks still contribute evidence.

### 6. Extract short and dotted technical claims

Split on terminal punctuation, but not a period inside a technical token such as
`Node.js`; also recognize a capitalized sentence start when the writer omits whitespace
after a period. Keep each nonempty tokenizable fragment, including bare `SQL`, `C++`,
`C#`, `Go`, and `R`, while retaining the original ten-claim cap.

## Rejected approaches

- **Lower the overlap threshold globally.** This makes ordinary material claims pass
  on a single shared technology token.
- **Remove all role, verb, and qualifier words as stop words.** This collapses
  `Python expert`, `Uses Kubernetes`, and `AWS certified` to unsafe one-token claims.
- **Add a negation/qualifier grammar.** That would turn a focused short-claim fix into
  an unreliable entailment system and create more false positives and false negatives.
- **Claim general entailment.** The module is a bag-of-tokens heuristic. An NLI/LLM
  judge is the appropriate follow-up for semantic faithfulness.

## Test plan

Keep all 22 original test functions and add focused regressions for:

- issue #152 matching and unrelated-context asymmetry;
- issue #153 `None` handling, including a valid sibling chunk;
- punctuation, canonical Unicode, curly apostrophes, `C++`, and `C#`;
- ASCII/Unicode hyphen and underscore compounds;
- generic-only mismatch controls;
- bidirectional material mismatches (`expert/novice`, `uses/avoids`,
  `Python/Non-Python`, `certified/novice`);
- exact controls and compatible extra context;
- reporter order and the one-token eligibility boundary;
- an executable adversarial matrix;
- explicit lexical limitations.

## Verified local result

Final local evidence incorporated into this plan:

- issue reproduction: `1.0`;
- unrelated `Knows SQL` context: `0.0`;
- module: **42 passed** (22 original + 20 added test functions);
- adversarial matrix: **49 rows**, zero mismatches;
- branch `make test-unit`: **49 failed / 399 passed / 3 warnings**, exit 2;
- fresh `main` baseline: **53 failed / 375 passed / 3 warnings**, exit 2;
- exact failure comparison: the four issue-related failures are repaired and no new
  failure identity appears;
- touched files: Ruff clean and Black clean;
- production module: `mypy --strict --no-incremental` clean;
- repo-wide Ruff: 180 existing errors, exit 2 (`main`: 182);
- repo-wide mypy: 103 existing errors, exit 2 (same as `main`);
- repo-wide Black check: 50 existing files, exit 1 (`main`: 52);
- integration target: zero tests collected, pytest exit 5 / Make exit 2;
- `make check` not run because its `format` prerequisite rewrites the repository;
  equivalent non-mutating checks are reported separately above.

## Honest limitations

The checker still cannot determine semantic entailment. In particular:

- `Knows Python` can be supported by a context that repeats `Python` inside a negated
  statement such as `No Python knowledge`; this is the explicit tradeoff introduced
  by issue #152's one-token requirement;
- contradictions retaining two overlaps can pass (for example, `Senior Python
  developer` vs `Junior Python developer`), matching the original heuristic;
- sentence-level entity attribution is not modeled;
- two shared, unlisted generic-looking descriptors can satisfy the lexical floor;
- preserving compounds can reject context where a component match was intended.

These behaviors are pinned or documented rather than described as solved.

## Submission boundary

Keep the branch local until the owner completes the course/public actions: fork, claim
#152, add the cohort-ledger entry, push, open the PR, complete both bi-weekly check-ins,
and personalize the reflection. No push or public mutation is part of this local plan.
