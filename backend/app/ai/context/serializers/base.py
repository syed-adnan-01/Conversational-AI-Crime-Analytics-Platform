"""
============================================================
Base Serializer Interface
============================================================

Module  : AI Context Builder
Purpose : Defines abstract strategy interface for context serializers.
"""

from abc import ABC, abstractmethod

from app.ai.context.context_models import DetailLevel, InvestigationContext


class BaseSerializer(ABC):
    """
    Abstract Base Class for InvestigationContext Serializers.
    """

    @abstractmethod
    def serialize(
        self,
        context: InvestigationContext,
        level: DetailLevel = DetailLevel.STANDARD,
    ) -> str:
        """
        Serialize InvestigationContext to string representation according to detail level.
        """
        pass
