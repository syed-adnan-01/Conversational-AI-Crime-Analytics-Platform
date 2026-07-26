"""
Copilot Safety — content safety filter applied to user inputs and LLM outputs.
"""

from typing import Tuple

# Patterns that require safety intervention
_BLOCKED_PATTERNS = [
    "how to commit",
    "instructions to harm",
    "make a bomb",
    "kill someone",
    "illegal weapon",
]


class CopilotSafety:
    """Lightweight content safety filter for copilot I/O."""

    @staticmethod
    def check_input(user_message: str) -> Tuple[bool, str]:
        """
        Returns (is_safe, reason).
        is_safe=True means the message passed safety checks.
        """
        lower = user_message.lower()
        for pattern in _BLOCKED_PATTERNS:
            if pattern in lower:
                return False, f"Input blocked by content safety policy: '{pattern}' detected."
        return True, ""

    @staticmethod
    def check_output(response_text: str) -> Tuple[bool, str]:
        """
        Returns (is_safe, reason).
        Applies post-generation output safety checks.
        """
        lower = response_text.lower()
        for pattern in _BLOCKED_PATTERNS:
            if pattern in lower:
                return False, f"Output blocked by content safety policy: '{pattern}' detected."
        return True, ""
