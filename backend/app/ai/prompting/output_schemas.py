"""
Pydantic models representing structured JSON output schemas expected from LLMs.
"""

from typing import Optional
from pydantic import BaseModel, Field


class CaseSummaryOutput(BaseModel):
    """Structured output schema for Case Summaries."""
    fir_number: str = Field(..., description="FIR registration number")
    crime_type: str = Field(..., description="Primary classification of the crime")
    summary: str = Field(..., description="Executive summary of the case")
    key_facts: list[str] = Field(default_factory=list, description="Bullet points of key factual elements")
    victim_count: int = Field(0, description="Total number of victims involved")
    accused_count: int = Field(0, description="Total number of accused persons")
    status: str = Field("UNDER_INVESTIGATION", description="Current investigation status")


class LegalOpinionOutput(BaseModel):
    """Structured output schema for Legal Opinions."""
    applicable_acts: list[str] = Field(default_factory=list, description="Relevant statutory Acts (e.g. IPC, BNS)")
    applicable_sections: list[str] = Field(default_factory=list, description="Relevant statutory Sections (e.g. Sec 302)")
    legal_reasoning: str = Field(..., description="Detailed legal reasoning and statutory compliance analysis")
    evidentiary_requirements: list[str] = Field(default_factory=list, description="Legal proof required for court prosecution")
    prosecution_viability: str = Field("HIGH", description="Assessment of prosecution viability (HIGH, MEDIUM, LOW)")


class EvidenceAnalysisOutput(BaseModel):
    """Structured output schema for Evidence Analysis."""
    evidence_inventory: list[dict[str, str]] = Field(default_factory=list, description="List of physical/digital evidence items")
    chain_of_custody_intact: bool = Field(True, description="Whether chain of custody is established")
    forensic_findings: list[str] = Field(default_factory=list, description="Key findings from forensic lab reports")
    gaps_identified: list[str] = Field(default_factory=list, description="Missing evidence or evidentiary gaps")
    strength_score: float = Field(8.5, description="Evidentiary strength score out of 10")


class TimelineOutput(BaseModel):
    """Structured output schema for Case Timelines."""
    chronological_events: list[dict[str, str]] = Field(default_factory=list, description="Ordered list of events with timestamp and description")
    incriminating_sequence: list[str] = Field(default_factory=list, description="Key sequence of events demonstrating intent/execution")
    inconsistencies: list[str] = Field(default_factory=list, description="Timeline contradictions or alibi discrepancies")


class ChargesheetOutput(BaseModel):
    """Structured output schema for Chargesheet drafting."""
    chargesheet_number: str = Field(..., description="Draft Chargesheet filing number")
    accused_details: list[dict[str, str]] = Field(default_factory=list, description="Details of accused charged")
    offences_charged: list[str] = Field(default_factory=list, description="Specific offences and sections charged")
    brief_facts_of_case: str = Field(..., description="Formal factual recitation for court filing")
    witness_list: list[str] = Field(default_factory=list, description="List of prosecution witnesses (PWs)")
    evidence_list: list[str] = Field(default_factory=list, description="List of prosecution evidence exhibits")


class InvestigationRecommendationOutput(BaseModel):
    """Structured output schema for Next Steps and Recommendations."""
    immediate_actions: list[str] = Field(default_factory=list, description="Urgent investigation tasks required")
    pending_verifications: list[str] = Field(default_factory=list, description="Statements or evidence requiring verification")
    witnesses_to_examine: list[str] = Field(default_factory=list, description="Persons to be interviewed or re-examined")
    risk_assessment: str = Field("MEDIUM", description="Risk level (HIGH, MEDIUM, LOW)")
