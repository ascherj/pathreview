"""Tests for faithfulness_checker.py"""

import pytest

from rag.evaluator.faithfulness_checker import FaithfulnessChecker


@pytest.mark.unit
class TestFaithfulnessChecker:
    """Test suite for FaithfulnessChecker."""

    @pytest.fixture
    def checker(self):
        """Create a FaithfulnessChecker instance."""
        return FaithfulnessChecker()

    def test_feedback_fully_supported_by_context(self, checker):
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

    def test_feedback_with_no_support_in_context(self, checker):
        """Test feedback with no support in context returns score close to 0.0."""
        feedback = "This developer is an expert in Rust systems programming."
        context_chunks = [
            {"text": "The developer has Python and JavaScript experience."},
        ]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert score < 0.5  # Should be low score

    def test_partial_support_returns_middle_score(self, checker):
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

    def test_empty_feedback_returns_zero(self, checker):
        """Test empty feedback returns 0.0."""
        feedback = ""
        context_chunks = [{"text": "Some context"}]

        score = checker.check(feedback, context_chunks)

        assert score == 0.0

    def test_empty_context_chunks_returns_zero(self, checker):
        """Test empty context chunks returns 0.0."""
        feedback = "Some feedback"
        context_chunks = []

        score = checker.check(feedback, context_chunks)

        assert score == 0.0

    def test_both_empty_returns_zero(self, checker):
        """Test both empty returns 0.0."""
        feedback = ""
        context_chunks = []

        score = checker.check(feedback, context_chunks)

        assert score == 0.0

    def test_multiple_context_chunks(self, checker):
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

    def test_extract_claims(self, checker):
        """Test claim extraction from feedback."""
        feedback = "The developer is skilled. They have experience. They work well."
        claims = checker._extract_claims(feedback)

        assert isinstance(claims, list)
        assert len(claims) > 0
        assert all(isinstance(c, str) for c in claims)

    def test_extract_claims_with_punctuation(self, checker):
        """Test claim extraction handles various punctuation."""
        feedback = "First claim! Second claim? Third claim. Fourth claim"
        claims = checker._extract_claims(feedback)

        assert isinstance(claims, list)
        # Should extract at least some claims

    def test_is_supported_with_keyword_overlap(self, checker):
        """Test that claim is marked as supported with keyword overlap."""
        claim = "The developer has Python skills"
        context = "Python programming skills demonstrated throughout portfolio"

        supported = checker._is_supported(claim, context)

        assert isinstance(supported, bool)
        assert supported is True

    def test_is_supported_without_keywords(self, checker):
        """Test that claim is unsupported without keyword overlap."""
        claim = "Expert in Rust systems programming"
        context = "Strong background in Python web development"

        supported = checker._is_supported(claim, context)

        assert isinstance(supported, bool)
        assert supported is False

    def test_case_insensitive_support_check(self, checker):
        """Test that support check is case insensitive."""
        claim = "PYTHON PROGRAMMING SKILLS"
        context = "python programming skills are demonstrated"

        supported = checker._is_supported(claim, context)

        assert supported is True

    def test_score_never_returns_hardcoded_value(self, checker):
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

    def test_multiple_claims_varying_support(self, checker):
        """Test scoring with multiple claims of varying support."""
        feedback = "Python expert. Knows Rust. Skilled with Docker."
        context_chunks = [{"text": "Python and Docker expertise shown in projects."}]

        score = checker.check(feedback, context_chunks)

        # Python and Docker claims supported; the Rust claim is not
        assert isinstance(score, float)
        assert 0.2 < score < 0.8

    def test_very_long_feedback(self, checker):
        """Test handling of very long feedback text."""
        feedback = "The developer. " * 100
        context_chunks = [{"text": "Developer portfolio content"}]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_very_long_context(self, checker):
        """Test handling of very long context."""
        feedback = "The developer has Python skills."
        context_chunks = [{"text": "Python " * 1000}]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_common_words_filtered_in_overlap(self, checker):
        """Test that common stop words are filtered in overlap calculation."""
        # This test verifies that "the", "is", "and" etc. don't count as meaningful overlap
        claim = "The project is well documented"
        context = "The project is poorly documented"  # Opposite meaning but same stop words

        checker._is_supported(claim, context)

        # Despite word overlap, should look for meaningful overlap (not stop words)
        # This depends on implementation

    def test_minimum_overlap_required(self, checker):
        """Test multi-token claims still need two matches (original rule)."""
        # A material two-token claim keeps the original >=2 rule: one
        # match is not support.
        assert checker._is_supported("Python and Kubernetes", "Python") is False
        # The issue's explicit reporting shape is the narrow exception.
        assert checker._is_supported("Knows Python", "Python") is True
        assert checker._is_supported("The candidate knows Python", "Python") is True
        assert checker._is_supported("Python knows", "Python") is False
        assert checker._is_supported("Knows candidate Python", "Python") is False

    def test_none_context_chunk_text(self, checker):
        """Test handling of None in context chunk text."""
        feedback = "Has Python skills"
        context_chunks = [{"text": None}]

        score = checker.check(feedback, context_chunks)

        # Should handle gracefully
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_missing_text_key_in_chunk(self, checker):
        """Test handling of missing 'text' key in context chunk."""
        feedback = "Has Python skills"
        context_chunks = [{"content": "Python skills"}]  # Wrong key

        score = checker.check(feedback, context_chunks)

        # Should handle gracefully
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_score_consistency(self, checker):
        """Test that same input produces same score."""
        feedback = "The developer has strong Python skills."
        context_chunks = [{"text": "Expert Python programmer"}]

        score1 = checker.check(feedback, context_chunks)
        score2 = checker.check(feedback, context_chunks)

        assert score1 == score2

    def test_specialized_technical_terms(self, checker):
        """Test support check with specialized technical terms."""
        claim = "Experienced with PostgreSQL and ORM frameworks"
        context = "Database design with PostgreSQL, SQLAlchemy ORM"

        supported = checker._is_supported(claim, context)

        assert supported is True

    def test_short_supported_claims_are_supported(self, checker):
        """Test short fully-supported claims are not scored 0.0 (issue #152)."""
        # Exact reproduction from issue #152. Each short claim reduces to a
        # single meaningful token (knows is generic) that its context fully
        # matches; the old >=2-token floor scored this feedback 0.0.
        score = checker.check(
            "Knows Python. Knows SQL.",
            [{"text": "python expert"}, {"text": "sql expert"}],
        )

        assert score == pytest.approx(1.0)
        assert checker._is_supported("Knows Python", "python expert") is True

    def test_short_claim_distinguishes_matching_from_unrelated_context(self, checker):
        """Test a short claim is scored against its context (issue #152)."""
        supported = checker.check("Knows SQL.", [{"text": "sql expert"}])
        unsupported = checker.check("Knows SQL.", [{"text": "unrelated Haskell work"}])

        assert supported >= 0.5
        assert unsupported == 0.0

    def test_bare_technical_claims_are_scoreable(self, checker):
        """Test short language/database names are extracted and scored."""
        for claim in ("SQL", "C++", "C#", "Go", "R"):
            supported = checker.check(f"{claim}.", [{"text": f"Uses {claim}"}])
            unsupported = checker.check(f"{claim}.", [{"text": "Unrelated Haskell"}])

            assert supported == pytest.approx(1.0)
            assert unsupported == 0.0

    def test_punctuation_stripped_before_overlap(self, checker):
        """Test punctuation does not block token matching (issue #152)."""
        # With plain str.split() tokenization, "Python," never matched "python".
        claim = "Skilled in Python, Django, and PostgreSQL."
        context = "Python Django PostgreSQL developer"

        supported = checker._is_supported(claim, context)

        assert supported is True

    def test_none_chunk_does_not_poison_other_chunks(self, checker):
        """Test a None-text chunk is skipped, not fatal (issue #153)."""
        feedback = "Has Python skills"
        context_chunks = [
            {"text": None},
            {"text": "python skills demonstrated"},
        ]

        score = checker.check(feedback, context_chunks)

        assert isinstance(score, float)
        assert score > 0.5  # Support from the valid chunk still counts

    def test_stop_word_only_claim_scores_zero(self, checker):
        """Test a claim of only stop words scores 0.0 (scoring guard)."""
        score = checker.check(
            "That is to be for that.",
            [{"text": "Python developer portfolio"}],
        )

        assert score == 0.0

    def test_more_supported_claims_score_higher(self, checker):
        """Test that overall score increases with more supported claims."""
        context_chunks = [{"text": "Python and Docker expertise shown in projects."}]

        both_supported = checker.check("Shows Python expertise. Uses Docker daily.", context_chunks)
        one_supported = checker.check(
            "Shows Python expertise. Writes Haskell compilers.", context_chunks
        )

        assert both_supported > one_supported

    def test_generic_wording_alone_is_not_support(self, checker):
        """Test shared generic wording cannot support a mismatched technology."""
        # Generic vocabulary remains part of the original overlap count, but
        # cannot satisfy the rule without a shared concrete anchor.
        assert checker._is_supported("Rust expertise", "Python expertise") is False
        assert checker._is_supported("Python developer", "Rust developer") is False
        assert checker._is_supported("Skilled in Rust", "Skilled in Python") is False
        assert checker._is_supported("Strong Rust background", "Strong Python background") is False

        score = checker.check("Rust expertise today.", [{"text": "Python expertise."}])
        assert score == 0.0
        # A claim made entirely of generic terms retains main's exact-match
        # behavior; the anchor guard only applies when the claim has an anchor.
        assert checker._is_supported("Developer experience", "Developer experience") is True

    def test_unlisted_descriptor_mismatch_fails_closed(self, checker):
        """Test one-word descriptor mismatches keep the two-match floor."""
        # No descriptor completeness claim is needed here: each pair shares
        # only one token, so the original >=2 rule rejects it.
        assert checker._is_supported("Rust wizardry", "Python wizardry") is False
        assert checker._is_supported("Rust guru", "Python guru") is False
        assert checker._is_supported("Rust mastery", "Python mastery") is False
        assert checker._is_supported("Haskell specialist", "Erlang specialist") is False

    def test_material_predicates_do_not_collapse_to_short_claims(self, checker):
        """Test the one-token exception cannot erase material predicates."""
        incompatible_pairs = [
            ("Python expert", "Python novice"),
            ("Uses Kubernetes", "Avoids Kubernetes"),
            ("Python developer", "Non-Python developer"),
            ("AWS certified", "AWS novice"),
            ("Qualified Python developer", "Python novice"),
        ]

        for left, right in incompatible_pairs:
            assert checker._is_supported(left, right) is False
            assert checker._is_supported(right, left) is False

    def test_compatible_extra_context_is_still_support(self, checker):
        """Test additional compatible context wording is not a conflict."""
        assert checker._is_supported("Python expert", "Python expert and certified") is True
        supported = checker._is_supported(
            "Senior Python developer", "Senior Python expert developer"
        )
        assert supported is True

    def test_accented_words_stay_whole(self, checker):
        """Test non-ASCII words are not shredded into ASCII fragments."""
        # "résumé" must not tokenize into fragments like "r"/"sum" that
        # accidentally match unrelated claims.
        score = checker.check(
            "Calculated sum totals in R.",
            [{"text": "Polished his résumé thoroughly"}],
        )

        assert score < 0.5
        assert checker._is_supported("Résumé skills", "résumé skills and writing tips") is True
        assert checker._tokenize("re\u0301sume\u0301") == {"résumé"}
        assert checker._tokenize("Py\u00adthon") == {"python"}

    def test_symbolic_language_names_stay_distinct(self, checker):
        """Test C-family language names keep their symbols when tokenized."""
        assert checker._is_supported("Knows C# and C++", "C# and C++ projects") is True
        # Plain "C" must not match "C++" via symbol stripping
        assert checker._is_supported("Knows C", "C++ projects only") is False

    def test_quoted_and_curly_apostrophe_tokens_match(self, checker):
        """Test quoted tokens and curly apostrophes normalize before matching."""
        quoted = checker._is_supported("Skilled in 'Python' development", "python development work")

        assert quoted is True
        # Curly apostrophes normalize to the straight form so the token
        # matches its straight-quoted counterpart exactly
        assert checker._tokenize("Doesn’t") == {"doesn't"}
        assert checker._tokenize("Doesn‘t") == {"doesn't"}

    def test_hyphenated_compounds_do_not_match_components(self, checker):
        """Test compound words cannot corroborate an unrelated component."""
        assert checker._tokenize("go-to-market Objective‑C non_python Non–Java") == {
            "go-to-market",
            "non-java",
            "non_python",
            "objective-c",
        }
        assert checker._is_supported("Understands Go", "go-to-market strategy") is False
        assert checker._is_supported("Understands C", "Objective-C projects") is False
        assert checker._is_supported("Knows Python", "non_python developer") is False
        assert checker._is_supported("Knows Python", "Non–Python developer") is False
        assert checker._is_supported("Understands Go", "understands Go well") is True

    def test_dotted_compounds_do_not_match_components(self, checker):
        """Test periods inside technical names are not sentence boundaries."""
        assert checker._extract_claims("Uses Node.js. Knows SQL.") == [
            "Uses Node.js",
            "Knows SQL",
        ]
        assert checker._tokenize("Node.js") == {"node.js"}
        assert checker._is_supported("Uses Node.js", "Uses Node.js daily") is True
        assert checker._is_supported("Uses Node.js", "Uses Node graph") is False
        assert checker._extract_claims("Knows Python.Knows SQL.") == [
            "Knows Python",
            "Knows SQL",
        ]
        assert checker.check(
            "Knows Python.Knows SQL.",
            [{"text": "python expert"}, {"text": "sql expert"}],
        ) == pytest.approx(1.0)
        assert checker._extract_claims("Knows Node.js.Knows Python.") == [
            "Knows Node.js",
            "Knows Python",
        ]

    def test_ampersand_compounds_do_not_match_components(self, checker):
        """Test R does not collide with the separate term R&D."""
        assert checker._tokenize("R&D") == {"r&d"}
        assert checker._is_supported("R", "R&D leadership") is False
        assert checker._is_supported("R&D", "R&D leadership") is True

    def test_verb_only_overlap_is_not_support(self, checker):
        """Test a claim sharing only a generic verb with context scores 0.0."""
        score = checker.check("Understands Rust today.", [{"text": "understands web development"}])

        assert score == 0.0

    def test_documented_lexical_limitations(self, checker):
        """Pin semantic blind spots and the short-claim tradeoff.

        This remains a lexical-overlap heuristic. It cannot detect negation,
        contradictions that retain two matching terms, entity attribution,
        or multiword generic descriptors absent from the small anchor list.
        Deeper checking belongs in an LLM-based evaluator (see PLAN.md).
        """
        # Negation-blind, as on main: both material tokens still overlap.
        assert checker._is_supported("Python expert", "not a Python expert") is True
        # A two-token contradiction can still pass when two other terms
        # overlap, also matching main's behavior.
        assert checker._is_supported("Senior Python developer", "Junior Python developer") is True
        # Attribution-blind across sentences, as on main
        supported = checker._is_supported("Alice uses Python", "Alice uses Rust. Bob uses Python")
        assert supported is True
        # The narrow #152 exception is also negation-blind; this differs from
        # main because main rejected every one-token-overlap short claim.
        assert checker._is_supported("Knows Python", "No Python knowledge") is True
        # Two unlisted generic-looking tokens can satisfy the lexical floor.
        assert (
            checker._is_supported("Rust cutting-edge expertise", "Python cutting-edge expertise")
            is True
        )

    def test_adversarial_probe_matrix(self, checker):
        """Executable probe matrix for the narrow contract.

        Every row is (claim, context, expected_supported), derived from
        seven audit rounds and re-derived for the narrow fix. Rows that
        depend on semantic understanding (negation, contradiction,
        attribution) live in the documented-limitations test instead.
        """
        probes = [
            # Technology mismatches under generic wording
            ("Rust expertise", "Python expertise", False),
            ("Python developer", "Rust developer", False),
            ("Skilled in Rust", "Skilled in Python", False),
            ("Strong Rust background", "Strong Python background", False),
            ("Rust mastery", "Python mastery", False),
            ("Rust wizardry", "Python wizardry", False),
            ("Rust guru", "Python guru", False),
            ("Haskell specialist", "Erlang specialist", False),
            # Material mismatches fail in both directions
            ("Python novice", "Python expert", False),
            ("Python expert", "Python novice", False),
            ("Avoids Kubernetes", "Uses Kubernetes", False),
            ("Uses Kubernetes", "Avoids Kubernetes", False),
            ("Non-Python developer", "Python developer", False),
            ("Python developer", "Non-Python developer", False),
            ("AWS certified", "AWS novice", False),
            ("AWS novice", "AWS certified", False),
            ("Qualified Python developer", "Python novice", False),
            ("Python novice", "Qualified Python developer", False),
            # Hyphenated compounds stay distinct from their components
            ("Understands Go", "go-to-market strategy", False),
            ("Understands C", "Objective-C projects", False),
            ("Knows Python", "non_python developer", False),
            ("Knows Python", "Non–Python developer", False),
            ("Uses Node.js", "Uses Node graph", False),
            ("Uses Node.js", "Uses Node.js daily", True),
            ("R", "R&D leadership", False),
            ("R&D", "R&D leadership", True),
            # Bare/reporter-shaped short claims use the #152 exception
            ("Knows Python", "python expert", True),
            ("Knows SQL", "sql expert", True),
            ("The candidate knows Python", "python expert", True),
            ("Python", "python expert", True),
            ("Python knows", "python expert", False),
            ("Knows candidate Python", "python expert", False),
            ("Python expertise", "Python", False),
            ("SQL", "SQL database", True),
            ("C++", "C++ projects", True),
            ("C#", "C# projects", True),
            ("Go", "Go projects", True),
            ("R", "R projects", True),
            ("Uses Kubernetes", "uses Kubernetes daily", True),
            ("Knows Python", "not Java, but Python projects", True),
            # Compatible additional wording is not a conflict
            ("Python expert", "Python expert and certified", True),
            ("Senior Python developer", "Senior Python expert developer", True),
            # Reflexive claims match their own wording
            ("Avoids Kubernetes", "Avoids Kubernetes", True),
            ("No SQL knowledge", "no SQL knowledge", True),
            ("Non-Python developer", "Non-Python developer", True),
            ("Developer experience", "Developer experience", True),
            ("Alice is a Python expert", "Alice is a Python expert", True),
            # Sentence/chunk aggregation (mandated by the multi-chunk test)
            ("Alice is a Python expert", "Alice is a Python expert. Bob is a Python novice", True),
            ("Bob is a Python novice", "Alice is a Python expert. Bob is a Python novice", True),
        ]

        failures = [
            (claim, context, expected)
            for claim, context, expected in probes
            if checker._is_supported(claim, context) is not expected
        ]

        assert failures == []
