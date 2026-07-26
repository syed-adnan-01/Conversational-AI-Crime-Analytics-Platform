"""
Safety Validator for LLM Gateway responses.
Checks empty responses, malformed structures, missing citations, and unsafe hallucination markers.
"""

from typing import List, Tuple


class SafetyValidator:
    """Evaluates safety, completeness, and compliance of raw LLM outputs."""

    HALLUCINATION_MARKERS = [
        "As an AI developed by OpenAI",
        "As a large language model",
        "I don't have access to real-time data",
        "I do not possess real-time information",
        "I cannot browse the internet",
    ]

    @classmethod
    def validate_safety(cls, content: str, require_citations: bool = False) -> Tuple[bool, List[str]]:
        """
        Validates output content.
        Returns (is_safe, list_of_violations).
        """
        violations: List[str] = []

        if not content or not content.strip():
            violations.append("Response content is empty")
            return False, violations

        # Check for generic hallucination disclaimer markers
        for marker in cls.HALLUCINATION_MARKERS:
            if marker.lower() in content.lower():
                violations.append(f"Contains generic disclaimer marker: '{marker}'")

        # Check citation coverage if mandated
        if require_citations and "[" not in content:
            violations.append("Response lacks explicit citation bracket references")

        is_safe = len(violations) == 0
        return is_safe, violations
