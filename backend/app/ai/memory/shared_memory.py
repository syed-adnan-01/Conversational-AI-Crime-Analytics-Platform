from pydantic import BaseModel, Field
from typing import Any
class SharedMemory(BaseModel): values: dict[str, Any] = Field(default_factory=dict)
