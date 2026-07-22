# Week 8 — Issue Selection

## Issue Information

| Field | Details |
|-------|---------|
| **Issue Link** | https://github.com/jamjamgobambam/pathreview/issues/153 |
| **Issue Title** | Faithfulness checker crashes when a context chunk has `text: None` |
| **Tier** | ✅ Tier 1 |
| **Branch** | `fix/153-faithfulness-none-text` |
| **Repository** | `jamjamgobambam/pathreview` |
| **Primary Component** | `rag/evaluator/faithfulness_checker.py` |
| **Setup Confirmation** | ✅ Successfully cloned the repository, installed dependencies, and verified the application runs locally at `localhost:5173`. |
| **Cohort Ledger** | ✅ Issue added to the cohort ledger prior to beginning development. |

---

# Project Context

Before beginning implementation, I wanted to understand where this issue fit within the overall architecture of the project. Rather than treating Issue #153 as an isolated bug, I spent time exploring the repository structure, reviewing the evaluation pipeline, and identifying how the affected component interacted with the rest of the application.

PathReview uses a Retrieval-Augmented Generation (RAG) workflow to evaluate AI-generated responses. Instead of trusting a generated answer on its own, the application retrieves supporting context from a knowledge base and evaluates whether the generated response is actually supported by that evidence.

One of the components responsible for this verification is the `FaithfulnessChecker`, located in:

```text
rag/evaluator/faithfulness_checker.py
```

The evaluator serves as a quality-control layer within the RAG pipeline. Its responsibility is to compare claims made by the language model against the retrieved context and determine whether those claims are sufficiently supported before assigning a faithfulness score.

Although Issue #153 initially appeared to describe a simple edge case, it affected a critical part of the evaluation pipeline. If the component failed while processing malformed retrieval data, the entire evaluation process terminated before a score could be calculated. Because the evaluator is part of the application's quality assurance workflow, improving its resilience directly improves the reliability of the system as a whole.

---

# Problem Summary

I selected **Issue #153** because it presented an opportunity to improve the robustness of the evaluation pipeline without changing any user-facing functionality or altering the underlying faithfulness scoring algorithm.

The issue described a scenario in which the `FaithfulnessChecker` crashed whenever one of the retrieved context chunks contained:

```python
{"text": None}
```

Although this may appear to be a relatively uncommon edge case, retrieval systems frequently process incomplete or inconsistent data originating from external sources. Production software should therefore expect malformed inputs and continue operating whenever it is safe to do so, rather than terminating unexpectedly.

My objective for this issue was not only to resolve the immediate exception, but also to understand **why** the existing implementation failed, **where** the incorrect assumption originated, and **how** the fix could be implemented while preserving the existing behavior for all valid inputs.

Instead of immediately modifying the code, I approached the issue as an engineering investigation. I first reproduced the failure locally, traced the execution path through the evaluator, reviewed the surrounding implementation, and analyzed how retrieved context was transformed before reaching the faithfulness scoring logic.

Taking this investigative approach helped ensure that the final solution addressed the underlying cause of the problem rather than simply suppressing the exception. It also provided a better understanding of how data flows through the RAG evaluation pipeline and highlighted the importance of defensive programming when working with external or partially structured data.
# Engineering Investigation Timeline

Resolving Issue #153 required more than identifying the failing line of code. Before making any changes, I wanted to understand how the `FaithfulnessChecker` fit into the larger RAG evaluation workflow, how context data entered the component, and whether the existing implementation was making assumptions about the structure of retrieved data.

My goal was to avoid creating a narrow patch that only fixed the reported test case. Instead, I wanted to understand the underlying failure mode and implement a solution that improved reliability while preserving the existing behavior of the evaluation pipeline.

---

## Phase 1 — Repository Exploration and Environment Setup

The first step was becoming familiar with the repository and confirming that my local development environment matched the expected project configuration.

I began by:

- Cloning the PathReview repository.
- Installing the required dependencies.
- Verifying the application could run successfully locally.
- Reviewing the repository structure to understand how the frontend, backend, and evaluation components were organized.
- Identifying where the RAG evaluation logic was located.

After exploring the project structure, I narrowed my investigation to:

```text
rag/
 └── evaluator/
     └── faithfulness_checker.py
```

This file contained the implementation responsible for evaluating whether generated AI responses were supported by retrieved context.

Before making any code changes, I reviewed the surrounding modules to understand:

- how context chunks were created,
- how they were passed into the evaluator,
- how evaluation results were returned,
- and whether other components relied on the current behavior.

This helped establish that the safest solution would likely involve improving input handling inside the evaluator rather than changing upstream retrieval behavior.

---

# Understanding the Component

The `FaithfulnessChecker` is part of PathReview's Retrieval-Augmented Generation evaluation system.

In a typical RAG workflow:

1. A user provides a question or request.
2. The system retrieves relevant documents or context chunks.
3. A language model generates a response using that retrieved information.
4. The evaluator checks whether the generated response is supported by the retrieved evidence.

The purpose of the `FaithfulnessChecker` is to prevent unsupported claims from receiving a high confidence evaluation score.

The evaluator performs several important operations:

1. Receives generated text from the AI model.
2. Receives retrieved context chunks from the retrieval layer.
3. Extracts important claim statements from the generated response.
4. Combines retrieved context into a searchable text representation.
5. Compares generated claims against available evidence.
6. Calculates a faithfulness score.
7. Returns evaluation results.

The failure occurred during step four.

The system was unable to safely prepare the retrieved context before beginning the actual evaluation process.

---

# Phase 2 — Reproducing the Failure

After understanding the component's responsibility, I attempted to reproduce the issue locally instead of immediately modifying the implementation.

The issue description indicated that the evaluator crashed when a context chunk contained:

```python
{
    "text": None
}
```

I reviewed the existing regression test:

```text
test_none_context_chunk_text
```

and used it as the starting point for reproduction.

Running the test confirmed that the failure was reproducible and that the exception occurred before any faithfulness scoring logic executed.

The traceback pointed back to the context preparation step inside the `check()` method.

The failing operation was:

```python
context_text = " ".join(
    [chunk.get("text", "") for chunk in context_chunks]
)
```

At first glance, this implementation appeared safe because it provided a default empty string value.

However, reproducing the failure revealed that the assumption behind this logic was incomplete.

---

# Phase 3 — Tracing the Failure Path

To understand why the exception occurred, I traced the data flow through the failing operation.

The evaluator receives context chunks in the form of dictionaries.

A normal context chunk looks similar to:

```python
{
    "text": "The retrieved document contains supporting information."
}
```

For this input:

```python
chunk.get("text", "")
```

correctly returns:

```python
"The retrieved document contains supporting information."
```

The issue appears when the chunk contains:

```python
{
    "text": None
}
```

The original code assumes that the fallback value will be used. However, Python's `dict.get()` behavior is different.

The fallback value is only returned when the key does not exist.

Example:

```python
chunk = {}
chunk.get("text", "")
```

Result:

```python
""
```

However:

```python
chunk = {"text": None}
chunk.get("text", "")
```

Result:

```python
None
```

This difference was the key discovery during debugging.

The code was correctly handling missing fields, but it was not handling fields that existed with invalid values.

---

# Investigation Finding

The failure was not caused by:

- the claim extraction logic,
- the keyword matching process,
- the faithfulness scoring calculation,
- or the retrieval algorithm itself.

The failure happened earlier in the pipeline during input normalization.

The evaluator expected every context chunk's `text` field to contain a string, but that expectation was never enforced before the data reached the string concatenation step.

As a result, a single malformed context chunk could prevent the entire evaluation process from completing.

This investigation changed the direction of the fix. Instead of modifying the scoring algorithm, the correct solution was to make the evaluator more defensive at the point where it receives external data.
# Root Cause Analysis

After reproducing the issue and tracing the execution path, I identified that the failure was caused by an incorrect assumption about how Python dictionary defaults behave.

The existing implementation attempted to protect against missing context values by using:

```python
chunk.get("text", "")
```

At first inspection, this appears to guarantee that the evaluator will always receive a string. However, the behavior of `dict.get()` is more specific:

- If the key does not exist, the provided default value is returned.
- If the key exists but contains `None`, the value remains `None`.

This distinction created an edge case where malformed retrieval data could bypass the intended protection.

---

# Technical Explanation of the Failure

The original context-building logic was:

```python
context_text = " ".join(
    [chunk.get("text", "") for chunk in context_chunks]
)
```

The intended behavior was:

```text
Missing "text" field
        |
        v
Use empty string
        |
        v
Continue evaluation
```

However, the actual behavior was:

```text
"text": None
        |
        v
dict.get() returns None
        |
        v
None enters join()
        |
        v
TypeError raised
        |
        v
Evaluation pipeline crashes
```

The error produced:

```text
TypeError: sequence item 0: expected str instance, NoneType found
```

The exception occurred because Python's `str.join()` method requires every item in the sequence to already be a string.

A single invalid chunk was therefore capable of stopping the entire faithfulness evaluation process.

---

# Why This Bug Was Easy to Miss

This issue was an example of a subtle reliability problem rather than an obvious implementation mistake.

The original code followed a common Python pattern:

```python
dictionary.get(key, default_value)
```

Many developers use this pattern to safely access optional values. In most situations, it works exactly as expected.

The hidden problem is that there are multiple forms of "missing data":

## Case 1 — Missing Key

Example:

```python
{
}
```

The key does not exist.

Result:

```python
chunk.get("text", "")
```

returns:

```python
""
```

---

## Case 2 — Existing Key With Empty Value

Example:

```python
{
    "text": ""
}
```

The key exists but contains an empty string.

Result:

```python
chunk.get("text", "")
```

returns:

```python
""
```

---

## Case 3 — Existing Key With None Value

Example:

```python
{
    "text": None
}
```

The key exists, but its value is invalid for string operations.

Result:

```python
chunk.get("text", "")
```

returns:

```python
None
```

This third case was the source of the crash.

The evaluator handled missing fields, but it did not handle malformed values.

---

# Design Goal

Once the root cause was identified, I established several requirements for the fix.

The solution needed to:

- Prevent malformed context chunks from crashing evaluation.
- Preserve existing behavior for valid context.
- Avoid changing the scoring algorithm.
- Avoid requiring every caller to sanitize data manually.
- Keep the change small and easy to review.
- Improve reliability without introducing unnecessary complexity.

The key engineering decision was to handle invalid values at the evaluator boundary.

---

# Design Decision

## Chosen Approach: Normalize Context Inside `FaithfulnessChecker`

The final approach was to sanitize context values immediately before they are combined into the evaluation context.

The evaluator already acts as a boundary between external retrieval data and internal scoring logic. This made it the correct location to validate incoming values.

The implementation ensures that:

- valid strings pass through unchanged,
- missing values become empty strings,
- explicit `None` values become empty strings,
- the downstream scoring logic continues receiving predictable input.

This keeps the rest of the evaluator simple because the scoring logic can continue assuming it receives valid text.

---

# Alternative Solutions Considered

During investigation, I considered multiple approaches before choosing the final implementation.

---

## Option 1 — Validate Context Before Calling the Evaluator

One possible solution was to sanitize retrieved chunks before they reached `FaithfulnessChecker`.

Example:

```text
Retriever
    |
    v
Validation Layer
    |
    v
FaithfulnessChecker
```

### Advantages

- Keeps the evaluator focused only on scoring.
- Prevents invalid data from entering downstream components.

### Disadvantages

- Requires every caller to remember to perform validation.
- Duplicates logic across the codebase.
- Future contributors could introduce new callers without the same protection.

Because the evaluator can potentially receive data from multiple sources, this approach would not provide complete protection.

---

## Option 2 — Normalize Data Inside the Evaluator (Selected)

The chosen approach was to sanitize context inside `FaithfulnessChecker`.

Flow:

```text
Retrieved Context
        |
        v
FaithfulnessChecker
        |
        v
Normalize Input
        |
        v
Run Evaluation
```

### Advantages

- Creates a single source of truth.
- Protects all current and future callers.
- Requires a minimal code change.
- Keeps the existing evaluation algorithm unchanged.
- Improves reliability at the correct system boundary.

This approach provided the best balance between maintainability and simplicity.

---

# Implementation Details

The final implementation focused only on context normalization.

The previous behavior:

```python
context_text = " ".join(
    chunk.get("text", "")
    for chunk in context_chunks
)
```

was replaced with logic that ensures every value passed into `join()` is a valid string.

Conceptually:

```python
clean_text = chunk.get("text") or ""
```

This handles both:

```python
{}
```

and:

```python
{
    "text": None
}
```

while preserving normal values:

```python
{
    "text": "valid content"
}
```

The faithfulness scoring algorithm itself was intentionally left unchanged.

This was important because the issue was related to input handling, not scoring behavior.

---

# Impact of the Change

After this improvement:

Before:

```text
Malformed context chunk
        |
        v
TypeError
        |
        v
Evaluation stops
```

After:

```text
Malformed context chunk
        |
        v
Converted to safe empty value
        |
        v
Evaluation continues
```

The result is a more resilient evaluation pipeline that can tolerate imperfect retrieval data without changing the behavior of valid evaluations.

---

# Code Review Considerations

When reviewing this change, the main considerations were:

- Does this alter existing scoring behavior?
- Does it hide important errors?
- Does it introduce unnecessary complexity?
- Is the fix placed at the correct layer?

The answer to each was:

- Existing valid evaluations remain unchanged.
- The evaluator continues functioning safely with malformed input.
- The implementation is small and localized.
- Input normalization belongs at the evaluation boundary.

This made the change low-risk and appropriate for a Tier 1 issue.
# Testing and Verification

After implementing the fix, I focused on verifying two things:

1. The original failure described in Issue #153 was resolved.
2. Existing faithfulness evaluation behavior remained unchanged.

Because this was a reliability issue, the goal of testing was not only to prove that the error disappeared, but also to confirm that valid evaluation scenarios continued working exactly as before.

---

# Regression Testing

The first verification step was confirming that the regression scenario no longer caused the evaluator to crash.

The original failure condition:

```python
{
    "text": None
}
```

previously caused:

```text
TypeError: sequence item 0: expected str instance, NoneType found
```

After the fix, the evaluator safely processes the input and continues through the normal evaluation flow.

The regression test:

```text
test_none_context_chunk_text
```

now verifies that malformed context data does not interrupt execution.

This test acts as permanent protection against future changes accidentally reintroducing the same bug.

---

# Test Cases Considered

During validation, I considered multiple context scenarios to ensure the fix handled different data conditions correctly.

## Valid Context

Example:

```python
{
    "text": "The document contains supporting information."
}
```

Expected behavior:

- Context is processed normally.
- Faithfulness scoring remains unchanged.

---

## Missing Text Field

Example:

```python
{
}
```

Expected behavior:

- Missing values are treated safely.
- Evaluation continues without failure.

---

## Explicit None Value

Example:

```python
{
    "text": None
}
```

Expected behavior:

- `None` is converted into a safe empty value.
- No exception is raised.

---

## Empty String

Example:

```python
{
    "text": ""
}
```

Expected behavior:

- Existing behavior remains unchanged.
- Empty content does not interrupt evaluation.

---

## Mixed Context Data

Example:

```python
[
    {
        "text": "Valid document content."
    },
    {
        "text": None
    },
    {
        "text": "Additional supporting information."
    }
]
```

Expected behavior:

- Valid content remains available.
- Invalid chunks do not break processing.
- The evaluator completes successfully.

---

# Verification Results

The final verification confirmed:

- ✅ The original crash no longer occurs.
- ✅ `test_none_context_chunk_text` passes.
- ✅ Valid context continues producing expected evaluation results.
- ✅ Malformed context is handled safely.
- ✅ Existing scoring behavior remains unchanged.
- ✅ No additional regressions were introduced.

The final implementation improved reliability while keeping the scope of the change intentionally small.

---

# Git Workflow

I followed a standard feature-branch workflow to keep the change isolated and easy to review.

## Development Branch

```text
fix/153-faithfulness-none-text
```

---

## Development Process

The workflow followed these stages:

```text
Investigate
    |
    v
Reproduce Failure
    |
    v
Identify Root Cause
    |
    v
Implement Minimal Fix
    |
    v
Run Regression Tests
    |
    v
Document Changes
    |
    v
Prepare Pull Request
```

Each step helped reduce the chance of introducing unrelated changes.

---

# Commit Organization

The changes were organized around clear development milestones:

## Bug Fix

Purpose:

- Resolve the `None` handling issue.
- Prevent evaluator crashes.
- Preserve existing scoring behavior.

Example commit message:

```text
fix: handle None context chunk text in faithfulness checker
```

---

## Regression Coverage

Purpose:

- Protect against future regressions.
- Document expected behavior for malformed context.

Example commit message:

```text
test: add regression coverage for None context chunks
```

---

## Documentation Update

Purpose:

- Document investigation process.
- Explain technical reasoning.
- Provide future contributors with context.

Example commit message:

```text
docs: update issue 153 engineering journal
```

---

# Remaining Work and Future Improvements

Although Issue #153 resolves the immediate crash, the investigation identified additional opportunities to improve the reliability of the RAG evaluation pipeline.

These improvements are outside the scope of the current issue but could provide additional long-term value.

---

## Stronger Input Validation

Currently, the evaluator receives context chunks as dictionaries.

A future improvement would be introducing stronger validation through typed models.

Potential benefits:

- Detect invalid data earlier.
- Provide clearer error messages.
- Reduce assumptions throughout the codebase.
- Improve developer experience.

For example, a validated context model could guarantee that every chunk entering the evaluator has a predictable structure.

---

## Expand Automated Test Coverage

The current regression test protects against the discovered failure case.

Additional tests could improve coverage by validating:

- missing keys,
- empty strings,
- non-string values,
- empty context lists,
- multiple malformed chunks,
- unexpected dictionary structures.

This would provide stronger confidence that the evaluator remains stable as the application evolves.

---

## Improve Logging and Observability

The current fix prevents malformed data from crashing evaluation.

However, silently ignoring malformed values may make debugging upstream retrieval problems more difficult.

A future enhancement could:

- log when malformed chunks are detected,
- include metadata about the affected retrieval result,
- provide visibility into retrieval quality issues.

This would maintain reliability while improving system observability.

---

## Repository-Wide Audit

During this investigation, I identified a common pattern where developers may assume:

```python
dictionary.get(key, default)
```

handles all missing-data scenarios.

A future improvement would be auditing similar patterns throughout the repository to identify places where explicit `None` values could create similar failures.

---

# Challenges Encountered

The most challenging part of this issue was not writing the final code change. The more difficult part was identifying why the existing implementation failed despite appearing defensive.

The original code used a common Python pattern:

```python
dict.get(key, default)
```

At first glance, this suggested that missing values were already handled.

The investigation required understanding the difference between:

- a missing dictionary key,
- an existing key containing `None`,
- and a valid empty string.

This distinction was the key to finding the real root cause.

The experience reinforced the importance of reproducing issues, examining actual runtime data, and verifying assumptions before changing production code.

---

# Lessons Learned

## Defensive Programming

This issue reinforced that components interacting with external or generated data should assume inputs may not always match expectations.

Retrieval pipelines, APIs, and machine learning systems frequently encounter incomplete or malformed information. Handling these cases at system boundaries improves reliability and reduces unexpected failures.

---

## Investigation Before Implementation

One of the biggest lessons from this issue was the value of understanding the system before changing it.

By tracing the execution path first, I was able to avoid unnecessary changes and implement a focused solution that addressed the actual cause.

---

## Python Data Handling

This issue strengthened my understanding of Python dictionary behavior.

The difference between:

```python
{}
```

and:

```python
{
    "text": None
}
```

may appear small, but it has important consequences when data moves through operations that expect specific types.

---

## Value of Regression Tests

The regression test created for this issue provides long-term protection for the codebase.

Future contributors can now modify the evaluator with confidence that this specific failure mode will be detected automatically.

---

# Engineering Reflection

Although the final code change was relatively small, the investigation required careful reasoning about data flow, component boundaries, and assumptions within existing code.

This issue provided valuable experience working inside an unfamiliar production-style repository and reinforced several important engineering practices:

- reproduce failures before implementing fixes,
- understand the architecture before changing behavior,
- place validation at the correct boundary,
- minimize changes when solving reliability issues,
- and document decisions so future contributors understand the reasoning behind the implementation.

The completed fix improves the stability of the RAG evaluation pipeline while preserving existing functionality. More importantly, the process demonstrated that effective engineering is not only about writing code—it is about understanding systems, identifying assumptions, and making changes that improve long-term maintainability.

---

# References

**GitHub Issue**

- Issue #153 — Faithfulness checker crashes when a context chunk has `text: None`

**Repository Component**

```text
rag/evaluator/faithfulness_checker.py
```

**Related Regression Test**

```text
test_none_context_chunk_text
```

**Development Branch**

```text
fix/153-faithfulness-none-text
```

**Pull Request**

(Add PR number after submission)