"""
============================================================
Context Plugin Abstract Base Class
============================================================

Module  : AI Context Builder
Purpose : Provides the plugin interface for context enrichment.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.ai.context.context_models import InvestigationContext


class ContextPlugin(ABC):
    """
    Abstract plugin interface for extending InvestigationContext without
    modifying the core ContextBuilder.
    """

    @abstractmethod
    def enrich(self, context: "InvestigationContext") -> None:
        """
        Enrich the given investigation context in-place.
        
        Args:
            context: The InvestigationContext instance to modify or enrich.
        """
        pass
