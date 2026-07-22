"""Run the RAG evaluation suite against benchmark portfolios.

Week 8 reproduction (B-20) — feature gap, not a crash:
  $ python3 scripts/run_evals.py
  → prints "Evaluation complete. Results written to eval_results.json"
  → but eval_results.json is never created
  → tests/fixtures/sample_profiles/ is missing
  → EvalSuite/EvalResult has no actionability_score (despite the TODO below)

See PLAN.md and tests/unit/test_run_evals_reproduction.py.
"""


def main() -> None:
    """Execute the full evaluation pipeline and output results."""
    print("Running RAG evaluation suite...")
    # TODO: Implement eval runner
    # 1. Load benchmark portfolios from tests/fixtures/sample_profiles/
    # 2. Run each through the full RAG pipeline with mock LLM
    # 3. Score retrieval relevance, faithfulness, and actionability
    # 4. Output JSON report to eval_results.json
    print("Evaluation complete. Results written to eval_results.json")


if __name__ == "__main__":
    main()
