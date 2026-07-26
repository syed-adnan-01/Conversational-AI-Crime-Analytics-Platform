"""
Conversation Summarizer — condenses long conversation history for long-term memory.
"""

from typing import List

from app.ai.copilot.copilot_models import ConversationMessage


class ConversationSummarizer:
    """
    Produces a compact natural-language summary of a conversation window.
    In production this would call the LLM Gateway; here we provide a
    deterministic extractive fallback for offline/test environments.
    """

    @staticmethod
    def summarize(messages: List[ConversationMessage], max_sentences: int = 5) -> str:
        if not messages:
            return "No conversation history to summarize."

        user_turns = [m.content for m in messages if m.role == "user"]
        assistant_turns = [m.content for m in messages if m.role == "assistant"]

        lines = []
        if user_turns:
            lines.append(f"The user asked {len(user_turns)} question(s).")
            lines.append(f"Last question: \"{user_turns[-1][:120]}\"")
        if assistant_turns:
            lines.append(f"The assistant provided {len(assistant_turns)} response(s).")
            lines.append(f"Last response excerpt: \"{assistant_turns[-1][:120]}\"")

        return " ".join(lines[:max_sentences])
