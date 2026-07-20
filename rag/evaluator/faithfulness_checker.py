"""Check if generated feedback is supported by retrieved context."""

import re
import structlog

logger = structlog.get_logger()


class FaithfulnessChecker:
    """Verify that feedback claims are supported by context."""

    def check(self, feedback: str, context_chunks: list[dict]) -> float:
        """Check faithfulness of feedback to context.

        Args:
            feedback: Generated feedback text
            context_chunks: Retrieved context chunks

        Returns:
            Faithfulness score 0.0-1.0 (ratio of supported claims)
        """
        if not feedback or not context_chunks:
            logger.info("faithfulness_empty_input", has_feedback=bool(feedback),
                       has_chunks=bool(context_chunks))
            return 0.0

        # Extract key claims from feedback (sentences)
        claims = self._extract_claims(feedback)
        if not claims:
            logger.info("faithfulness_no_claims_extracted")
            return 0.5  # Default to neutral if no extractable claims

        # Concatenate context text (ignore chunks with missing/None text)
        context_text = " ".join([
            str(chunk.get("text") or "") for chunk in context_chunks
        ])

        # Check each claim for support
        supported = 0
        for claim in claims:
            if self._is_supported(claim, context_text):
                supported += 1

        score = supported / len(claims) if claims else 0.0

        logger.info("faithfulness_checked", claims_count=len(claims),
                   supported_count=supported, score=score)

        return score

    @staticmethod
    def _extract_claims(text: str) -> list[str]:
        """Extract key claims from feedback text.

        Args:
            text: Feedback text

        Returns:
            List of claims (sentences)
        """
        # Split by sentence (simple regex)
        sentences = re.split(r'[.!?]+', text)
        claims = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        return claims[:10]  # Limit to 10 claims for scoring

    @staticmethod
    def _is_supported(claim: str, context: str) -> bool:
        """Check if a claim is supported by context.

        Args:
            claim: Claim text
            context: Context text

        Returns:
            True if claim is supported
        """
        # Tokenize and check for keyword overlap
        claim_tokens = set(claim.lower().split())
        context_tokens = set(context.lower().split())

        # Require at least some meaningful overlap
        overlap = claim_tokens & context_tokens
        # Filter out common stop words
        stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
                     'and', 'or', 'but', 'in', 'of', 'to', 'for', 'that'}
        meaningful_overlap = overlap - stop_words

        # Short factual claims may only share one meaningful token with the
        # supporting context (e.g. "Knows Python." vs "python expert"). Treat
        # single-token overlaps as supported for short claims; keep the
        # stricter two-token rule for longer, more specific claims.
        claim_word_count = len([t for t in claim.lower().split() if t not in stop_words])
        required_overlap = 1 if claim_word_count <= 3 else 2
        return len(meaningful_overlap) >= required_overlap
