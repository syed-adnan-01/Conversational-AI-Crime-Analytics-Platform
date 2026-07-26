"""
Standardized safety guardrails and anti-hallucination rules injected into prompts.
"""


class SafetyGuardrails:
    """Provides isolated, standardized safety instructions for AI generation."""

    RULES: list[str] = [
        "1. Never fabricate or hallucinate facts not present in the supplied context.",
        "2. Ground all claims and analyses strictly in the provided evidence and case records.",
        "3. Explicitly state uncertainty when evidence is incomplete or inconclusive.",
        "4. Cite retrieved document evidence or section numbers when making factual claims.",
        "5. Do not infer legal guilt; maintain objective investigative analysis.",
        "6. Limit statutory interpretation to the explicit text of the supplied Acts and Sections.",
    ]

    @classmethod
    def get_guardrails_text(cls) -> str:
        """Returns formatted safety rules text for injection into system or user prompts."""
        return "### SAFETY & COMPLIANCE GUARDRAILS\n" + "\n".join(cls.RULES)
