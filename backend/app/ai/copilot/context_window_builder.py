"""
Context Window Builder — assembles the token-bounded conversation window
from the three-tier memory manager before prompt construction.
"""

from typing import List

from app.ai.copilot.copilot_models import ContextWindow, ConversationMessage, MessageRole
from app.ai.copilot.memory.memory_manager import MemoryManager


class ContextWindowBuilder:
    """Builds a bounded ContextWindow from session memory for prompt assembly."""

    def __init__(self, max_tokens: int = 32768) -> None:
        self.max_tokens = max_tokens

    def build(self, session_id: str, system_prompt: str = "") -> ContextWindow:
        """Retrieve recent messages from memory and fit them within max_tokens."""
        window = ContextWindow(session_id=session_id, max_tokens=self.max_tokens)

        if system_prompt:
            sys_msg = ConversationMessage(
                role=MessageRole.SYSTEM,
                content=system_prompt,
            )
            # Rough token approximation: 1 token ≈ 4 characters
            tokens = len(system_prompt) // 4 + 1
            if window.fits(tokens):
                window.messages.append(sys_msg)
                window.total_tokens += tokens

        recent: List[ConversationMessage] = MemoryManager.get_recent(session_id)
        for msg in recent:
            tokens = len(msg.content) // 4 + 1
            if window.fits(tokens):
                window.messages.append(msg)
                window.total_tokens += tokens
            else:
                break  # Stop adding once window is full

        return window
