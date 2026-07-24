"""
============================================================
Query Classifier
============================================================

Module  : AI Query Processing Subsystem
Purpose : Classifies user query intent and maps it to the optimal RetrievalPolicy.
"""

from app.ai.retrieval.retrieval_models import QueryIntent
from app.ai.retrieval.retrieval_policies import (
    BaseRetrievalPolicy,
    EvidencePolicy,
    InvestigationPolicy,
    LegalPolicy,
    TimelinePolicy,
)


class QueryClassifier:
    """
    Analyzes intent of investigative query strings and resolves matching RetrievalPolicy.
    """

    @classmethod
    def classify_intent(cls, query: str) -> QueryIntent:
        q = query.lower()

        if any(w in q for w in ["section", "ipc", "act", "legal", "charge", "bail", "bailable", "cognizable"]):
            return QueryIntent.LEGAL_QUERY
        if any(w in q for w in ["evidence", "proof", "recovered", "seized", "weapon", "phone", "custody", "dna"]):
            return QueryIntent.EVIDENCE_SEARCH
        if any(w in q for w in ["when", "date", "timeline", "event", "hearing", "proceeding", "court"]):
            return QueryIntent.TIMELINE_QUERY
        if any(w in q for w in ["officer", "assigned", "io", "investigator", "badge", "inspector"]):
            return QueryIntent.OFFICER_QUERY
        if any(w in q for w in ["case", "fir", "crime", "summary", "status"]):
            return QueryIntent.CASE_LOOKUP

        return QueryIntent.GENERAL

    @classmethod
    def resolve_policy(cls, intent: QueryIntent) -> BaseRetrievalPolicy:
        """Map intent to pre-packaged RetrievalPolicy."""
        if intent == QueryIntent.LEGAL_QUERY:
            return LegalPolicy()
        if intent == QueryIntent.EVIDENCE_SEARCH:
            return EvidencePolicy()
        if intent == QueryIntent.TIMELINE_QUERY:
            return TimelinePolicy()

        return InvestigationPolicy()
