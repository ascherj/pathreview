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
        # Split by sentence and by coordinating conjunctions so compound
        # feedback ("Python expertise and Kubernetes knowledge") yields
        # independently supported claims instead of one all-or-nothing claim.
        sentences = re.split(r'[.!?]+', text)
        claims = []
        for sentence in sentences:
            # Split coordinated clauses first
            for clause in re.split(r'\s+(?:and|or|but)\s+', sentence, flags=re.IGNORECASE):
                clause = clause.strip()
                if not clause or len(clause) < 5:
                    continue
                # Split comma-separated technology lists into individual claims
                if "," in clause:
                    head, *rest = [c.strip() for c in clause.split(",")]
                    if head and len(head) > 10:
                        claims.append(head)
                    for part in rest:
                        # keep only substantial fragments
                        if len(part) > 3 and not part.lower().startswith(("and ", "or ")):
                            claims.append(part)
                        elif part.lower().startswith(("and ", "or ")):
                            part = part[4:].strip()
                            if len(part) > 3:
                                claims.append(part)
                else:
                    claims.append(clause)
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
        meaningful_claim = {t for t in claim_tokens if t not in stop_words}

        # A claim is supported when it shares at least one meaningful token
        # with the context. Longer claims need proportionally more overlap so
        # vague feedback doesn't score fully supported.
        if not meaningful_claim:
            return False
        if len(meaningful_claim) <= 3:
            return len(meaningful_overlap) >= 1
        return len(meaningful_overlap) / len(meaningful_claim) >= 0.2
