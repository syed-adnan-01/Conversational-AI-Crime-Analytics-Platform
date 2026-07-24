"""
AI Routes Subpackage.
"""

from app.ai.routes.context import router as context_router
from app.ai.routes.indexing import router as indexing_router
from app.ai.routes.retrieval import router as retrieval_router

__all__ = [
    "context_router",
    "indexing_router",
    "retrieval_router",
]
