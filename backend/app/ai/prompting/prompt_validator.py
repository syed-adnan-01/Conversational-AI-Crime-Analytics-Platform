"""
Prompt Validator enforcing budget limits, placeholder resolution, and non-empty prompt constraints.
"""

from app.ai.prompting.exceptions import PromptValidationException, TokenBudgetExceededException
from app.ai.prompting.prompt_metrics import PromptMetrics
from app.ai.prompting.prompt_templates import TemplateEngine
from app.ai.prompting.token_budget_manager import TokenBudgetManager


class PromptValidator:
    """Validates constructed prompts prior to downstream LLM response building."""

    @classmethod
    def validate(
        cls,
        system_prompt: str,
        user_prompt: str,
        max_budget: int = 4096,
        raise_on_error: bool = True,
    ) -> bool:
        """
        Validates system_prompt and user_prompt.
        Raises PromptValidationException or TokenBudgetExceededException if raise_on_error is True.
        """
        try:
            if not system_prompt and not user_prompt:
                raise PromptValidationException("Both system_prompt and user_prompt are empty.")

            # Check unresolved placeholders
            full_text = system_prompt + "\n" + user_prompt
            unresolved = TemplateEngine.find_unresolved_placeholders(full_text)
            if unresolved:
                raise PromptValidationException(
                    f"Prompt contains unresolved placeholders: {', '.join(unresolved)}"
                )

            # Check token budget
            est_tokens = TokenBudgetManager.estimate_tokens(full_text)
            if max_budget > 0 and est_tokens > max_budget:
                raise TokenBudgetExceededException(
                    f"Estimated token count ({est_tokens}) exceeds max_token_budget ({max_budget})."
                )

            return True
        except Exception:
            PromptMetrics.record_validation_error()
            if raise_on_error:
                raise
            return False
