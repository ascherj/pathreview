"""Bias detection in generated feedback."""

import re
import structlog

logger = structlog.get_logger()


class BiasDetector:
    """Detect biased language in feedback."""

    # Genuinely dismissive phrases about educational background
    DISMISSIVE_PATTERNS = [
        r"(?:bootcamp|self-taught|online\s+course|coding\s+bootcamp|online\s+training|self\s+taught).*(?:can't|cannot|won't|will\s+not|lack|lacks|missing|inadequate|insufficient|not\s+prepare|not\s+equal|never\s+comparable|not\s+comparable|means\s+inadequate|lacking)"
    ]

    # Demographic assumptions (about age, background, identity)
    DEMOGRAPHIC_PATTERNS = [
        r"(?:young|old|aged|age).*(?:can't|cannot|won't|will\s+not|struggle|keep\s+up|learn)",
        r"(?:poor|rich|working[\s-]?class).*(?:can't|cannot|won't|will\s+not|struggle|succeed|afford)",
        r"(?:immigrant|international|foreign).*(?:can't|cannot|won't|will\s+not|struggle|communicate)"
    ]

    @staticmethod
    def detect_bias(text: str) -> tuple[bool, str]:
        """Detect biased language in feedback.

        Args:
            text: Feedback text

        Returns:
            Tuple of (is_biased, reason)
        """
        # Check for dismissive language about education
        for pattern in BiasDetector.DISMISSIVE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                reason = "Dismissive language about educational background"
                logger.warning("bias_detected", reason=reason)
                return True, reason

        # Check for demographic assumptions
        for pattern in BiasDetector.DEMOGRAPHIC_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                reason = "Demographic assumptions detected"
                logger.warning("bias_detected", reason=reason)
                return True, reason

        return False, ""
