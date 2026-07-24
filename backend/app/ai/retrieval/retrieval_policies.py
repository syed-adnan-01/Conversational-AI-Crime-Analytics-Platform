"""
============================================================
Retrieval Policies
============================================================

Module  : AI Retrieval Engine
Purpose : Pre-packaged domain retrieval policies (Legal, Evidence, Timeline, Investigation)
          specifying retriever settings, token budgets, and section priorities.
"""

from abc import ABC, abstractmethod


class BaseRetrievalPolicy(ABC):
    """
    Abstract Retrieval Policy defining configuration defaults for specific LLM tasks.
    """

    @property
    @abstractmethod
    def policy_name(self) -> str:
        """Name of the policy."""
        pass

    @property
    @abstractmethod
    def max_token_budget(self) -> int:
        """Maximum prompt token limit for this policy."""
        pass

    @property
    @abstractmethod
    def default_top_k(self) -> int:
        """Default top-k candidate chunks to retrieve."""
        pass

    @property
    def section_priorities(self) -> dict[str, int]:
        """Priority weights for different sections (higher = kept first)."""
        return {
            "CASE": 100,
            "SECTION": 95,
            "EVIDENCE": 90,
            "CHARGESHEET": 85,
            "ARREST": 80,
            "COURT": 75,
            "TIMELINE": 70,
            "COMPLAINANT": 65,
            "ACCUSED": 60,
            "VICTIM": 55,
            "WITNESS": 50,
            "OFFICER": 40,
        }


class InvestigationPolicy(BaseRetrievalPolicy):
    """General investigation overview policy."""

    @property
    def policy_name(self) -> str:
        return "InvestigationPolicy"

    @property
    def max_token_budget(self) -> int:
        return 4096

    @property
    def default_top_k(self) -> int:
        return 15


class LegalPolicy(BaseRetrievalPolicy):
    """Legal sections & IPC penal code focus policy."""

    @property
    def policy_name(self) -> str:
        return "LegalPolicy"

    @property
    def max_token_budget(self) -> int:
        return 4096

    @property
    def default_top_k(self) -> int:
        return 15

    @property
    def section_priorities(self) -> dict[str, int]:
        return {
            "SECTION": 100,
            "CHARGESHEET": 95,
            "CASE": 90,
            "COURT": 85,
            "EVIDENCE": 70,
            "ARREST": 65,
            "ACCUSED": 60,
            "TIMELINE": 50,
        }


class EvidencePolicy(BaseRetrievalPolicy):
    """Evidence & custody chain focus policy."""

    @property
    def policy_name(self) -> str:
        return "EvidencePolicy"

    @property
    def max_token_budget(self) -> int:
        return 3072

    @property
    def default_top_k(self) -> int:
        return 12

    @property
    def section_priorities(self) -> dict[str, int]:
        return {
            "EVIDENCE": 100,
            "CHARGESHEET": 90,
            "CASE": 85,
            "ARREST": 80,
            "SECTION": 75,
            "WITNESS": 70,
            "TIMELINE": 60,
        }


class TimelinePolicy(BaseRetrievalPolicy):
    """Chronological event & court proceeding focus policy."""

    @property
    def policy_name(self) -> str:
        return "TimelinePolicy"

    @property
    def max_token_budget(self) -> int:
        return 2048

    @property
    def default_top_k(self) -> int:
        return 10

    @property
    def section_priorities(self) -> dict[str, int]:
        return {
            "TIMELINE": 100,
            "COURT": 95,
            "ARREST": 90,
            "CASE": 85,
            "CHARGESHEET": 80,
            "EVIDENCE": 70,
        }
