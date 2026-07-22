"""Tests for faithfulness_checker.py"""

import pytest

from rag.evaluator.faithfulness_checker import FaithfulnessChecker


@pytest.mark.unit
class TestFaithfulnessChecker:
    """Test suite for FaithfulnessChecker."""

    @pytest.fixture
    def checker(self) -> FaithfulnessChecker:
        """Create a FaithfulnessChecker instance."""
        return FaithfulnessChecker()

    def test_feedback_fully_supported_by_context(self, checker: FaithfulnessChecker) -> None:
        """Test feedback fully supported by context returns score close to 1.0."""
        feedback = "The developer has strong Python skills and experience with Django."
        context_chunks = [
            {"text": "The portfolio shows Python expertise and Django framework experience."},
        ]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        # Should be high score due to support
        assert score > 0.5

    def test_feedback_with_no_support_in_context(self, checker: FaithfulnessChecker) -> None:
        """Test feedback with no support in context returns score close to 0.0."""
        feedback = "This developer is an expert in Rust systems programming."
        context_chunks = [
            {"text": "The developer has Python and JavaScript experience."},
        ]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert score < 0.5  # Should be low score

    def test_partial_support_returns_middle_score(self, checker: FaithfulnessChecker) -> None:
        """Test partial support returns score between 0 and 1."""
        feedback = "The developer shows Python expertise and Kubernetes knowledge."
        context_chunks = [
            {"text": "Strong Python programming skills demonstrated in projects."},
        ]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        # Partial support should be middle range
        assert 0.2 < score < 0.8

    def test_empty_feedback_returns_zero(self, checker: FaithfulnessChecker) -> None:
        """Test empty feedback returns 0.0."""
        feedback = ""
        context_chunks = [{"text": "Some context"}]

        score = checker.check(feedback, context_chunks)

        assert score == 0.0

    def test_empty_context_chunks_returns_zero(self, checker: FaithfulnessChecker) -> None:
        """Test empty context chunks returns 0.0."""
        feedback = "Some feedback"
        context_chunks: list[dict[str, str]] = []

        score = checker.check(feedback, context_chunks)

        assert score == 0.0

    def test_both_empty_returns_zero(self, checker: FaithfulnessChecker) -> None:
        """Test both empty returns 0.0."""
        feedback = ""
        context_chunks: list[dict[str, str]] = []

        score = checker.check(feedback, context_chunks)

        assert score == 0.0

    def test_multiple_context_chunks(self, checker: FaithfulnessChecker) -> None:
        """Test multiple context chunks contribute to score."""
        feedback = "The developer has Python, JavaScript, and Docker experience."
        context_chunks = [
            {"text": "Python expertise shown in backend projects."},
            {"text": "JavaScript skills demonstrated in frontend development."},
            {"text": "Docker and containerization knowledge evident in CI/CD pipelines."},
        ]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
        # All three claims supported
        assert score > 0.5

    def test_extract_claims(self, checker: FaithfulnessChecker) -> None:
        """Test claim extraction from feedback."""
        feedback = "The developer is skilled. They have experience. They work well."
        claims = checker._extract_claims(feedback)

        assert isinstance(claims, list)
        assert len(claims) > 0
        assert all(isinstance(c, str) for c in claims)

    def test_extract_claims_with_punctuation(self, checker: FaithfulnessChecker) -> None:
        """Test claim extraction handles various punctuation."""
        feedback = "First claim! Second claim? Third claim. Fourth claim"
        claims = checker._extract_claims(feedback)

        assert isinstance(claims, list)
        # Should extract at least some claims

    def test_is_supported_with_keyword_overlap(self, checker: FaithfulnessChecker) -> None:
        """Test that claim is marked as supported with keyword overlap."""
        claim = "The developer has Python skills"
        context = "Python programming skills demonstrated throughout portfolio"

        supported = checker._is_supported(claim, context)

        assert isinstance(supported, bool)
        assert supported is True

    def test_is_supported_without_keywords(self, checker: FaithfulnessChecker) -> None:
        """Test that claim is unsupported without keyword overlap."""
        claim = "Expert in Rust systems programming"
        context = "Strong background in Python web development"

        supported = checker._is_supported(claim, context)

        assert isinstance(supported, bool)
        assert supported is False

    def test_case_insensitive_support_check(self, checker: FaithfulnessChecker) -> None:
        """Test that support check is case insensitive."""
        claim = "PYTHON PROGRAMMING SKILLS"
        context = "python programming skills are demonstrated"

        supported = checker._is_supported(claim, context)

        assert supported is True

    def test_score_never_returns_hardcoded_value(self, checker: FaithfulnessChecker) -> None:
        """Test that score varies with input, never hardcoded 1.0 or 0.0."""
        # First test: fully supported
        score1 = checker.check(
            "Python and JavaScript skills", [{"text": "Expert in Python and JavaScript"}]
        )

        # Second test: no support
        score2 = checker.check("Rust expertise", [{"text": "Java programming background"}])

        # Scores should be different
        assert score1 != score2
        # First should be higher
        assert score1 > score2

    def test_multiple_claims_varying_support(self, checker: FaithfulnessChecker) -> None:
        """Test scoring with multiple claims of varying support."""
        feedback = "Python expert. Knows Rust. Skilled with Docker."
        context_chunks = [{"text": "Python and Docker expertise shown in projects."}]

        score = checker.check(feedback, context_chunks)

        # Two claims supported, one not
        assert isinstance(score, float)
        assert 0.2 < score < 0.8

    def test_very_long_feedback(self, checker: FaithfulnessChecker) -> None:
        """Test handling of very long feedback text."""
        feedback = "The developer. " * 100
        context_chunks = [{"text": "Developer portfolio content"}]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_very_long_context(self, checker: FaithfulnessChecker) -> None:
        """Test handling of very long context."""
        feedback = "The developer has Python skills."
        context_chunks = [{"text": "Python " * 1000}]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_common_words_filtered_in_overlap(self, checker: FaithfulnessChecker) -> None:
        """Test that common stop words are filtered in overlap calculation."""
        claim = "The project is well documented"
        context = "The team is available"

        supported = checker._is_supported(claim, context)

        assert supported is False

    def test_minimum_overlap_required(self, checker: FaithfulnessChecker) -> None:
        """Test longer claims require more than one ambiguous matching token."""
        claim = "Strong API design"
        context = "API routes are configured"

        supported = checker._is_supported(claim, context)

        assert supported is False

    def test_exact_issue_152_example_returns_partial_support(
        self, checker: FaithfulnessChecker
    ) -> None:
        """Test the exact short-claim issue example returns partial support."""
        feedback = "Knows Python. Knows SQL."
        context_chunks = [{"text": "Python development experience shown in backend projects."}]

        score = checker.check(feedback, context_chunks)

        assert score == 0.5

    def test_short_claim_supported_by_one_meaningful_term(
        self, checker: FaithfulnessChecker
    ) -> None:
        """Test short factual claims can be supported by one meaningful term."""
        claim = "Knows Python."
        context = "Python development experience shown in backend projects."

        supported = checker._is_supported(claim, context)

        assert supported is True

    def test_multi_skill_short_claim_not_supported_by_one_skill(
        self, checker: FaithfulnessChecker
    ) -> None:
        """Test one matching skill does not support a multi-skill claim."""
        claim = "Knows Python and SQL."
        context = "Python development experience shown in backend projects."

        supported = checker._is_supported(claim, context)

        assert supported is False

    def test_generic_short_claim_not_supported_by_ambiguous_overlap(
        self, checker: FaithfulnessChecker
    ) -> None:
        """Test generic one-token overlap does not support a short claim."""
        claim = "Strong API design."
        context = "API routes are configured."

        supported = checker._is_supported(claim, context)

        assert supported is False

    def test_single_word_claim_supported_by_one_meaningful_term(
        self, checker: FaithfulnessChecker
    ) -> None:
        """Test one-word competency claims can be supported by one term."""
        claim = "Docker."
        context = "Docker and containerization knowledge evident in CI/CD pipelines."

        supported = checker._is_supported(claim, context)

        assert supported is True

    def test_verb_phrase_with_and_remains_one_claim(self, checker: FaithfulnessChecker) -> None:
        """Test general verb phrases joined by and are not split into fragments."""
        feedback = "Designed and deployed a scalable backend."

        claims = checker._extract_claims(feedback)

        assert claims == ["Designed and deployed a scalable backend"]

    def test_none_context_chunk_text(self, checker: FaithfulnessChecker) -> None:
        """Test handling of None in context chunk text."""
        feedback = "Has Python skills"
        context_chunks = [{"text": None}]

        score = checker.check(feedback, context_chunks)

        # Should handle gracefully
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_missing_text_key_in_chunk(self, checker: FaithfulnessChecker) -> None:
        """Test handling of missing 'text' key in context chunk."""
        feedback = "Has Python skills"
        context_chunks = [{"content": "Python skills"}]  # Wrong key

        score = checker.check(feedback, context_chunks)

        # Should handle gracefully
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_score_consistency(self, checker: FaithfulnessChecker) -> None:
        """Test that same input produces same score."""
        feedback = "The developer has strong Python skills."
        context_chunks = [{"text": "Expert Python programmer"}]

        score1 = checker.check(feedback, context_chunks)
        score2 = checker.check(feedback, context_chunks)

        assert score1 == score2

    def test_specialized_technical_terms(self, checker: FaithfulnessChecker) -> None:
        """Test support check with specialized technical terms."""
        claim = "Experienced with PostgreSQL and ORM frameworks"
        context = "Database design with PostgreSQL, SQLAlchemy ORM"

        supported = checker._is_supported(claim, context)

        assert supported is True
