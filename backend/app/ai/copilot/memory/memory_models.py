"""
Three-Tier Memory Data Models.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class MemoryImportance(str, Enum):
    """Importance classification for weighted memory retention."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class MemoryItem(BaseModel):
    """Single remembered fact item."""
    model_config = ConfigDict(from_attributes=True)

    item_id: str
    content: str
    importance: MemoryImportance = MemoryImportance.MEDIUM
    category: str = "GENERAL"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
