"""
============================================================
Embedding Models
============================================================

Module  : AI Embeddings Layer
Purpose : Defines the EmbeddingRecord model representing generated vector embeddings.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EmbeddingRecord(BaseModel):
    """
    Domain model holding a generated vector embedding for a specific chunk.
    """
    model_config = ConfigDict(from_attributes=True)

    embedding_id: str
    chunk_id: str
    vector: list[float]
    model_name: str
    dimensions: int
    created_at: datetime
