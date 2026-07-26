"""
Prompt Profiles defining workflow objectives.
While Personas answer "Who is speaking?", Profiles answer "What are we trying to accomplish?".
"""

from enum import Enum


class PromptProfile(str, Enum):
    """
    Workflow profile defining the target objective of the generated prompt.
    """
    POLICE_INVESTIGATION = "police_investigation"
    COURT_PREPARATION = "court_preparation"
    EVIDENCE_REVIEW = "evidence_review"
    LEGAL_OPINION = "legal_opinion"
    EXECUTIVE_SUMMARY = "executive_summary"
    CITIZEN_EXPLANATION = "citizen_explanation"

    @classmethod
    def get_default(cls) -> "PromptProfile":
        return cls.POLICE_INVESTIGATION
