"""
Token Budget Manager allocating token quotas per section and enforcing ceiling constraints.
"""

from typing import Dict


class TokenBudgetManager:
    """
    Allocates max token budgets across system prompt, context sections, and user query.
    Performs intelligent trimming if a section exceeds its allocated quota.
    """

    # Proportional allocation percentages when max_budget is given
    DEFAULT_RATIOS: Dict[str, float] = {
        "system": 0.15,
        "summary": 0.15,
        "evidence": 0.25,
        "timeline": 0.15,
        "victims": 0.05,
        "accused": 0.05,
        "legal": 0.10,
        "question": 0.10,
    }

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Heuristic token estimator (approx. 4 characters per token)."""
        if not text:
            return 0
        return max(1, len(text.strip()) // 4)

    @classmethod
    def allocate_budgets(cls, max_budget: int = 4096) -> Dict[str, int]:
        """Calculates token budget allowances for each section."""
        return {
            section: int(max_budget * ratio)
            for section, ratio in cls.DEFAULT_RATIOS.items()
        }

    @classmethod
    def trim_to_budget(cls, text: str, max_tokens: int) -> str:
        """Trims text to fit within max_tokens limit if necessary."""
        if not text:
            return ""
        current_tokens = cls.estimate_tokens(text)
        if current_tokens <= max_tokens:
            return text

        # Calculate target character length
        max_chars = max_tokens * 4
        trimmed = text[:max_chars].rsplit(" ", 1)[0]
        return trimmed + "\n... [Truncated due to token budget]"
