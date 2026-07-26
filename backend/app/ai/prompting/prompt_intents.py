"""
Prompt Intents for task orientation.
"""

from enum import Enum


class PromptIntent(str, Enum):
    """
    Intended action for the model execution.
    """
    QUESTION = "question"
    SUMMARIZE = "summarize"
    GENERATE = "generate"
    COMPARE = "compare"
    ANALYZE = "analyze"
    RECOMMEND = "recommend"
    EXPLAIN = "explain"
    VERIFY = "verify"

    @classmethod
    def get_default(cls) -> "PromptIntent":
        return cls.QUESTION
