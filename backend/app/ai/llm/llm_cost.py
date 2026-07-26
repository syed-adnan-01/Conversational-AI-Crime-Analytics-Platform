"""
LLM Cost Calculator for tracking financial expenditure per request.
"""

from typing import Dict, Tuple


class LLMCostCalculator:
    """
    Calculates execution cost in USD based on provider pricing tables per 1k tokens.
    Pricing rate format: (input_cost_per_1k, output_cost_per_1k)
    """

    PRICING_TABLE: Dict[str, Tuple[float, float]] = {
        # QuickML rates
        "quickml": (0.0001, 0.0002),
        "quickml-rag": (0.0001, 0.0002),
        # Gemini rates
        "gemini": (0.000125, 0.000375),
        "gemini-2.5-pro": (0.00125, 0.0050),
        "gemini-2.5-flash": (0.000075, 0.00030),
        # OpenAI rates
        "openai": (0.0015, 0.0020),
        "gpt-4o": (0.0025, 0.0100),
        "gpt-4o-mini": (0.00015, 0.0006),
        # Claude rates
        "claude": (0.0030, 0.0150),
        "claude-3-5-sonnet": (0.0030, 0.0150),
        # Mock rate
        "mock": (0.0, 0.0),
    }

    @classmethod
    def calculate_cost(
        cls, provider_or_model: str, prompt_tokens: int, completion_tokens: int
    ) -> float:
        """Calculates total cost in USD."""
        key = provider_or_model.lower()
        rates = cls.PRICING_TABLE.get(key, (0.0001, 0.0002))
        in_cost = (prompt_tokens / 1000.0) * rates[0]
        out_cost = (completion_tokens / 1000.0) * rates[1]
        return round(in_cost + out_cost, 6)
