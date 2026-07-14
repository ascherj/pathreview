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

        # Concatenate context text
        context_text = " ".join([chunk.get("text", "") for chunk in context_chunks])

        # Check each claim for support
        supported = 0
        for claim in claims:
            if self._is_supported(claim, context_text):
                supported += 1

        score = supported / len(claims) if claims else 0.0

        logger.info(
            "faithfulness_checked", claims_count=len(claims), supported_count=supported, score=score
        )

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
        sentences = re.split(r"[.!?]+", text)
        claims = []
        skill_nouns = {"experience", "expertise", "knowledge", "skill", "skills"}
        for sentence in sentences:
            sentence = sentence.strip()
            tokens = FaithfulnessChecker._tokenize(sentence)
            if not tokens:
                continue
            if "," in sentence and tokens[-1] in skill_nouns:
                shared_noun = tokens[-1]
                for part in [p.strip() for p in sentence.split(",") if p.strip()]:
                    part_tokens = FaithfulnessChecker._tokenize(
                        re.sub(r"^\s*and\s+", "", part, flags=re.IGNORECASE)
                    )
                    claims.append(
                        " ".join(part_tokens[-2:])
                        if part_tokens[-1] == shared_noun
                        else f"{part_tokens[-1]} {shared_noun}"
                    )
                continue
            parts = [
                p.strip() for p in re.split(r"\band\b", sentence, flags=re.IGNORECASE) if p.strip()
            ]
            if len(parts) == 2:
                left_tokens = FaithfulnessChecker._tokenize(parts[0])
                right_tokens = FaithfulnessChecker._tokenize(parts[1])
                if (
                    left_tokens
                    and right_tokens
                    and left_tokens[-1] in skill_nouns
                    and right_tokens[-1] in skill_nouns
                ):
                    claims.extend([" ".join(left_tokens[-2:]), " ".join(right_tokens[-2:])])
                    continue
            claims.append(sentence)
        claims = [s for s in claims if len(s) > 3]
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
        stop_words = {
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
            "this",
            "has",
            "have",
            "with",
        }
        claim_tokens = set(FaithfulnessChecker._tokenize(claim)) - stop_words
        context_tokens = set(FaithfulnessChecker._tokenize(context)) - stop_words

        # Require at least some meaningful overlap
        meaningful_overlap = claim_tokens & context_tokens

        if len(claim_tokens) <= 3:
            return len(meaningful_overlap) >= 1

        return len(meaningful_overlap) >= 2

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Return lowercase word tokens without surrounding punctuation."""
        return re.findall(r"\b\w+\b", text.lower())
