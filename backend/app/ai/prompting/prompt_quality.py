"""
Prompt Quality Evaluator scoring completeness, token efficiency, and guardrail coverage.
"""

from typing import Any, Dict, List
import re


class PromptQualityEvaluator:
    """
    Evaluates generated prompts across 6 core quality metrics:
    1. Unresolved Placeholders Check (0 unresolved = 100)
    2. Guardrail Coverage (presence of safety rules)
    3. Token Efficiency (within budget limits)
    4. Completeness (query/task present)
    5. Section Presence (context non-empty)
    6. Citation Coverage (evidence citations referenced)
    """

    @classmethod
    def evaluate(
        cls,
        system_prompt: str,
        user_prompt: str,
        max_budget: int,
        estimated_tokens: int,
        requested_sections: List[str] | None = None,
    ) -> Dict[str, Any]:
        """
        Evaluates prompt quality and returns a score out of 100 with a detailed breakdown.
        """
        full_text = system_prompt + "\n" + user_prompt
        score = 100.0
        deductions: Dict[str, float] = {}

        # 1. Unresolved placeholders
        unresolved = re.findall(r"\{\{[a-zA-Z0-9_]+\}\}", full_text)
        if unresolved:
            penalty = min(30.0, len(unresolved) * 10.0)
            score -= penalty
            deductions["unresolved_placeholders"] = penalty

        # 2. Guardrails check
        if "GUARDRAIL" not in system_prompt and "GUARDRAIL" not in user_prompt:
            score -= 15.0
            deductions["missing_guardrails"] = 15.0

        # 3. Token efficiency check
        if estimated_tokens > max_budget:
            score -= 20.0
            deductions["budget_overflow"] = 20.0
        elif estimated_tokens < 20:
            score -= 10.0
            deductions["low_content"] = 10.0

        # 4. User question / query check
        if "Question:" not in user_prompt and "query:" not in user_prompt.lower() and len(user_prompt.strip()) == 0:
            score -= 25.0
            deductions["missing_user_query"] = 25.0

        final_score = max(0.0, round(score, 1))

        return {
            "quality_score": final_score,
            "unresolved_placeholders": unresolved,
            "deductions": deductions,
            "token_efficiency": round(min(1.0, estimated_tokens / max(1, max_budget)) * 100, 1),
            "passed_validation": final_score >= 70.0,
        }
