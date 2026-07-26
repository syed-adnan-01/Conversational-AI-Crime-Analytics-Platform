"""
Action Registry for dynamic action lookup and execution dispatch.
"""

from typing import Any, Dict, List, Optional
from app.ai.copilot.actions.action_models import ActionMetadata, ActionResult
from app.ai.copilot.actions.analyze_evidence import AnalyzeEvidenceAction
from app.ai.copilot.actions.base import BaseAction
from app.ai.copilot.actions.compare_statements import CompareStatementsAction
from app.ai.copilot.actions.generate_report import GenerateReportAction
from app.ai.copilot.actions.legal_analysis import LegalAnalysisAction
from app.ai.copilot.actions.semantic_search import SemanticSearchAction
from app.ai.copilot.actions.suggest_next_steps import SuggestNextStepsAction
from app.ai.copilot.actions.summarize_case import SummarizeCaseAction
from app.ai.copilot.actions.timeline_analysis import TimelineAnalysisAction


class ActionRegistry:
    """Dynamic registry for discovering and executing registered BaseAction instances."""

    _actions: Dict[str, BaseAction] = {}

    @classmethod
    def _initialize(cls) -> None:
        if not cls._actions:
            cls.register(SummarizeCaseAction())
            cls.register(AnalyzeEvidenceAction())
            cls.register(CompareStatementsAction())
            cls.register(LegalAnalysisAction())
            cls.register(SuggestNextStepsAction())
            cls.register(GenerateReportAction())
            cls.register(TimelineAnalysisAction())
            cls.register(SemanticSearchAction())

    @classmethod
    def register(cls, action: BaseAction) -> None:
        cls._actions[action.metadata.name.lower()] = action

    @classmethod
    def find(cls, name: str) -> Optional[BaseAction]:
        cls._initialize()
        return cls._actions.get(name.lower())

    @classmethod
    def execute(cls, name: str, session_id: str, case_id: str, payload: Dict[str, Any]) -> ActionResult:
        cls._initialize()
        action = cls.find(name)
        if not action:
            return ActionResult(
                action_name=name,
                success=False,
                error=f"Action '{name}' is not registered.",
            )
        return action.execute(session_id, case_id, payload)

    @classmethod
    def list_actions(cls) -> List[ActionMetadata]:
        cls._initialize()
        return [act.metadata for act in cls._actions.values()]
