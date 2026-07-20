"""Check if generated feedback is supported by retrieved context."""

import re
import unicodedata
from typing import Any

import structlog

logger = structlog.get_logger()

# Preserve the original implementation's function-word filter. Material
# predicates and qualifiers deliberately stay out of this set: removing
# "expert", "developer", or "uses" would turn ordinary two-token claims
# into unsafe one-token claims.
_STOP_WORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "and",
        "or",
        "but",
        "in",
        "of",
        "to",
        "for",
        "that",
    }
)

# Issue #152's short-claim exception is limited to a reporting construction
# ("[The candidate] knows Python") or an actually bare one-token claim. Only
# these words are removed while deciding whether that exception applies.
_SHORT_CLAIM_REPORTERS = frozenset({"know", "knows"})
_SHORT_CLAIM_SUBJECTS = frozenset({"candidate"})

# If a claim contains a concrete token, generic matches cannot substitute for
# that missing anchor. All-generic multi-token claims still follow the original
# rule. This is a guard, not an entailment vocabulary: unknown multiword
# descriptors retain the lexical heuristic's limitations.
_GENERIC_TOKENS = frozenset(
    {
        "know",
        "knows",
        "understand",
        "understands",
        "show",
        "shows",
        "demonstrate",
        "demonstrates",
        "use",
        "uses",
        "using",
        "write",
        "writes",
        "build",
        "builds",
        "displays",
        "exhibits",
        "developer",
        "developers",
        "engineer",
        "engineers",
        "candidate",
        "portfolio",
        "skill",
        "skills",
        "skilled",
        "expertise",
        "expert",
        "experts",
        "experience",
        "experienced",
        "knowledge",
        "background",
        "proficiency",
        "proficient",
        "familiarity",
        "familiar",
        "ability",
        "abilities",
        "strong",
        "solid",
        "good",
        "great",
        "excellent",
        "impressive",
        "project",
        "projects",
        "work",
        "code",
        "coding",
        "programming",
        "development",
        "framework",
        "frameworks",
        "tool",
        "tools",
        "technology",
        "technologies",
        "language",
        "languages",
        "library",
        "libraries",
        "stack",
        "mastery",
        "professional",
        "professionals",
        "specialist",
        "specialists",
        "competent",
        "competency",
        "qualified",
        "certified",
    }
)

_TOKEN_TRANSLATION = str.maketrans(
    {
        # Apostrophes inside contractions.
        "\u2018": "'",
        "\u2019": "'",
        "\u02bc": "'",
        "\uff07": "'",
        # A soft hyphen is a display hint, not part of the word.
        "\u00ad": "",
        # Hyphen and dash variants. Spaced dashes remain token boundaries;
        # unspaced forms stay compounds (the conservative polarity).
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2015": "-",
        "\u2212": "-",
        "\ufe63": "-",
        "\uff0d": "-",
    }
)

# Unicode-aware word runs; strips punctuation so "Python," matches "python"
# while preserving compounds ("Node.js"/"go-to-market"/"R&D"), accented
# words ("résumé"), contractions, and language names ("c++", "c#").
_TOKEN_RE = re.compile(r"[^\W_]+(?:[-.'&_][^\W_]+)*(?:\+\+|#)?")

# A claim counts as fully grounded once this many of its meaningful tokens
# appear in the context; longer claims never need more than this.
_FULL_SUPPORT_TOKENS = 3

# Per-claim score at or above which a claim is considered supported.
_SUPPORT_THRESHOLD = 0.5

# Ceiling (strictly below _SUPPORT_THRESHOLD) for claims that do not meet
# the support rule: partial overlap contributes to the graded score but can
# never classify a claim as supported.
_PARTIAL_SUPPORT_CAP = 0.4


class FaithfulnessChecker:
    """Verify that feedback claims are supported by context."""

    def check(self, feedback: str, context_chunks: list[dict[str, Any]]) -> float:
        """Check faithfulness of feedback to context.

        Args:
            feedback: Generated feedback text
            context_chunks: Retrieved context chunks

        Returns:
            Faithfulness score 0.0-1.0 (mean per-claim support)
        """
        if not feedback or not context_chunks:
            logger.info(
                "faithfulness_empty_input",
                has_feedback=bool(feedback),
                has_chunks=bool(context_chunks),
            )
            return 0.0

        # Extract key claims from feedback (sentences)
        claims = self._extract_claims(feedback)
        if not claims:
            logger.info("faithfulness_no_claims_extracted")
            return 0.5  # Default to neutral if no extractable claims

        # Aggregate context tokens across chunks; a chunk may carry
        # text=None (issue #153)
        context_tokens: set[str] = set()
        for chunk in context_chunks:
            context_tokens |= self._tokenize(chunk.get("text") or "")

        # Score each claim by how much of it is grounded in the context
        claim_scores = [self._support_score(claim, context_tokens) for claim in claims]
        score = sum(claim_scores) / len(claim_scores)

        logger.info(
            "faithfulness_checked",
            claims_count=len(claims),
            supported_count=sum(1 for s in claim_scores if s >= _SUPPORT_THRESHOLD),
            score=score,
        )

        return score

    @classmethod
    def _extract_claims(cls, text: str) -> list[str]:
        """Extract key claims from feedback text.

        Args:
            text: Feedback text

        Returns:
            List of claims (sentences)
        """
        # A period inside a word (for example Node.js) is not a sentence
        # boundary. Keep every nonempty tokenizable fragment so bare technical
        # claims such as SQL, C++, C#, Go, and R are scoreable (issue #152).
        sentences = re.split(r"\.(?!\w)|\.(?=[A-Z][a-z])|[!?;]+", text)
        claims = [s.strip() for s in sentences if s.strip() and cls._tokenize(s)]
        return claims[:10]  # Limit to 10 claims for scoring

    @staticmethod
    def _token_sequence(text: str) -> list[str]:
        """Normalize text and return its tokens in source order."""
        normalized = unicodedata.normalize("NFC", text).translate(_TOKEN_TRANSLATION)
        return _TOKEN_RE.findall(normalized.casefold())

    @classmethod
    def _tokenize(cls, text: str) -> set[str]:
        """Tokenize text into a lowercase, punctuation-free token set.

        Canonically equivalent Unicode spellings, curly apostrophes, and
        word-internal hyphens are normalized before tokenization.

        Args:
            text: Text to tokenize

        Returns:
            Set of lowercase tokens with punctuation stripped
        """
        return set(cls._token_sequence(text))

    @classmethod
    def _claim_terms(cls, claim: str) -> tuple[set[str], bool]:
        """Return claim terms and whether one matched term may support it.

        The one-token exception applies only to a genuinely bare claim or
        issue #152's reporting shape ("[The candidate] knows Python").
        Material predicates and qualifiers remain terms and therefore keep
        the original two-match floor.
        """
        ordered_terms = [token for token in cls._token_sequence(claim) if token not in _STOP_WORDS]
        reporter_shape = False
        content_terms = ordered_terms

        if ordered_terms[:1] and ordered_terms[0] in _SHORT_CLAIM_REPORTERS:
            reporter_shape = True
            content_terms = ordered_terms[1:]
        elif (
            len(ordered_terms) >= 2
            and ordered_terms[0] in _SHORT_CLAIM_SUBJECTS
            and ordered_terms[1] in _SHORT_CLAIM_REPORTERS
        ):
            reporter_shape = True
            content_terms = ordered_terms[2:]

        original_terms = set(ordered_terms)
        terms = set(content_terms)
        one_token_exception = len(terms) == 1 and (reporter_shape or len(original_terms) == 1)
        return terms, one_token_exception

    @classmethod
    def _support_score(cls, claim: str, context_tokens: set[str]) -> float:
        """Score how well a claim is grounded in the context tokens.

        A claim is supported when at least two of its terms appear in the
        context — the original rule — or when one matched concrete term is
        eligible for the narrowly scoped issue #152 exception. Unsupported
        claims keep a graded partial score capped below the threshold.

        This is deliberately a narrow lexical-overlap heuristic with the
        original implementation's semantic blind spots: it does not detect
        negation, contradiction, or entity attribution. The short-claim
        exception adds one explicit tradeoff: a negated context that repeats
        its single concrete term can still appear supported. Deeper checking
        belongs in an LLM-based evaluator, not here.

        Args:
            claim: Claim text
            context_tokens: Tokenized context

        Returns:
            Support score 0.0-1.0
        """
        terms, one_token_exception = cls._claim_terms(claim)
        if not terms:
            return 0.0

        matched = terms & context_tokens
        anchors = terms - _GENERIC_TOKENS
        if anchors and not matched & anchors:
            return 0.0

        short_supported = (
            one_token_exception and len(matched) == 1 and bool(matched - _GENERIC_TOKENS)
        )
        supported = len(matched) >= 2 or short_supported

        raw = len(matched) / min(len(terms), _FULL_SUPPORT_TOKENS)
        if supported:
            return min(1.0, max(raw, _SUPPORT_THRESHOLD))
        return min(raw, _PARTIAL_SUPPORT_CAP)

    @classmethod
    def _is_supported(cls, claim: str, context: str) -> bool:
        """Check if a claim is supported by context.

        Args:
            claim: Claim text
            context: Context text

        Returns:
            True if claim is supported
        """
        return cls._support_score(claim, cls._tokenize(context)) >= _SUPPORT_THRESHOLD
