"""
Long-Term Memory storing summarized facts and weighted items.
"""

from typing import List
from pydantic import BaseModel, Field
from app.ai.copilot.memory.memory_models import MemoryImportance, MemoryItem


class LongTermMemory(BaseModel):
    """Stores high-importance facts and historical session summaries."""

    items: List[MemoryItem] = Field(default_factory=list)
    summary_text: str = ""

    def add_fact(self, content: str, importance: MemoryImportance = MemoryImportance.HIGH, category: str = "FACT") -> None:
        item = MemoryItem(
            item_id=f"MEM-{len(self.items)+1}",
            content=content,
            importance=importance,
            category=category,
        )
        self.items.append(item)

    def get_important_facts(self) -> List[MemoryItem]:
        """Returns facts weighted as HIGH or CRITICAL."""
        return [i for i in self.items if i.importance in (MemoryImportance.HIGH, MemoryImportance.CRITICAL)]
