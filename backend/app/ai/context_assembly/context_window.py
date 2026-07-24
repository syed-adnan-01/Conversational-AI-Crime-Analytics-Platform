"""
============================================================
Context Window Manager
============================================================

Module  : AI Context Assembly Subsystem
Purpose : Manages token window limits and token estimations.
"""

from typing import Iterable


class ContextWindow:
    """
    Utility for tracking token counts against configured window budgets.
    """

    @classmethod
    def estimate_tokens(cls, text: str) -> int:
        """Estimate token count (word count approximation)."""
        if not text:
            return 0
        return len(text.split())

    @classmethod
    def fit_within_budget(
        cls, items: Iterable[tuple[int, str]], max_tokens: int
    ) -> list[str]:
        """Return list of text strings that fit within max_tokens budget."""
        result: list[str] = []
        accumulated = 0

        for tokens, text in items:
            if accumulated + tokens <= max_tokens:
                result.append(text)
                accumulated += tokens
            else:
                break

        return result
