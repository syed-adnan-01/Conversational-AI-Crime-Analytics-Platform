"""
Working Memory tracking active case entities discussed in session.
"""

from typing import List, Set
from pydantic import BaseModel, Field


class WorkingMemory(BaseModel):
    """Tracks active entities and context referenced during current session."""

    case_id: str = ""
    referenced_evidence: Set[str] = Field(default_factory=set)
    referenced_witnesses: Set[str] = Field(default_factory=set)
    referenced_accused: Set[str] = Field(default_factory=set)
    referenced_sections: Set[str] = Field(default_factory=set)

    def track_evidence(self, evidence_id: str) -> None:
        self.referenced_evidence.add(evidence_id)

    def track_witness(self, witness_id: str) -> None:
        self.referenced_witnesses.add(witness_id)

    def track_accused(self, accused_id: str) -> None:
        self.referenced_accused.add(accused_id)

    def track_section(self, section_name: str) -> None:
        self.referenced_sections.add(section_name)
