"""Core investigation engine."""

from __future__ import annotations

from collections import defaultdict
from time import perf_counter

from app.ai.copilot.copilot_service import CopilotService
from app.ai.investigation.analysis.case_similarity import analyze_case_similarity, _load_case_bundle
from app.ai.investigation.analysis.completeness import analyze_completeness
from app.ai.investigation.analysis.contradiction_detection import detect_contradictions
from app.ai.investigation.analysis.evidence_analysis import analyze_evidence
from app.ai.investigation.analysis.explainability import build_reasoning_trace
from app.ai.investigation.analysis.legal_analysis import analyze_legal
from app.ai.investigation.analysis.recommendation_engine import build_recommendations
from app.ai.investigation.analysis.timeline_analysis import analyze_timeline
from app.ai.investigation.analysis.confidence import blend_confidence, clamp_score, level_from_score
from app.ai.investigation.graph.relationship_builder import build_relationship_graph
from app.ai.investigation.intelligence.investigation_audit import InvestigationAudit
from app.ai.investigation.intelligence.investigation_cache import InvestigationCache
from app.ai.investigation.intelligence.investigation_metrics import InvestigationMetricsCollector
from app.ai.investigation.intelligence.investigation_models import (
    InvestigationRequest,
    InvestigationResponse,
    RelationshipGraph,
)
from app.ai.prompting.prompt_models import PromptPersona, PromptRequest, PromptType
from app.ai.prompting.prompt_service import PromptService
from app.ai.llm.llm_models import LLMRequest
from app.ai.llm.llm_service import LLMService
from app.models.act import Act
from app.models.case_master import CaseMaster
from app.models.case_section import CaseSectionAssociation
from app.models.section import Section
from app.repository.act_repository import ActRepository
from app.repository.case_section_repository import CaseSectionRepository
from app.repository.complainant_repository import ComplainantRepository
from app.repository.officer_repository import OfficerRepository


class InvestigationEngine:
    """Deterministic application service that orchestrates investigation analysis."""

    def __init__(
        self,
        retrieval_service=None,
        prompt_service: PromptService | None = None,
        llm_service=None,
        copilot_service: CopilotService | None = None,
        cache: InvestigationCache | None = None,
        audit: InvestigationAudit | None = None,
        metrics: InvestigationMetricsCollector | None = None,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.prompt_service = prompt_service or PromptService()
        self.llm_service = llm_service or LLMService
        self.copilot_service = copilot_service or CopilotService()
        self.cache = cache or InvestigationCache()
        self.audit = audit or InvestigationAudit()
        self.metrics = metrics or InvestigationMetricsCollector()

    def _bundle_for_case(self, case_id: str):
        return _load_case_bundle(case_id)

    def _sections_and_acts(self, case_id: str) -> tuple[list[Section], list[Act], list[CaseSectionAssociation]]:
        case_sections = CaseSectionRepository.get_case_sections(case_id)
        sections: list[Section] = []
        for association in case_sections:
            section = __import__("app.repository.section_repository", fromlist=["SectionRepository"]).SectionRepository.get_section_by_id(association.section_id)
            if section:
                sections.append(section)
        acts = ActRepository.get_acts_by_ids([section.act_id for section in sections if section.act_id])
        return sections, acts, case_sections

    def _case_text(self, case: CaseMaster) -> str:
        bundle = self._bundle_for_case(case.case_master_id)
        if not bundle:
            return case.brief_facts or case.crime_no
        return " ".join([
            case.crime_no,
            case.case_no or "",
            case.brief_facts or "",
            *(item.title for item in bundle.evidence),
            *(item.description for item in bundle.evidence),
            *(item.name for item in bundle.accused),
            *(item.name for item in bundle.victims),
            *(item.name for item in bundle.witnesses),
        ])

    def analyze(self, request: InvestigationRequest, user_id: str | None = None) -> InvestigationResponse:
        cache_key = f"analyze:{request.case_id}:{request.query}:{request.top_k}:{request.include_graph}"
        cached = self.cache.get(cache_key)
        if cached:
            self.metrics.update(cache_hit=True)
            return cached

        started = perf_counter()
        case_id = request.case_id
        bundle = self._bundle_for_case(case_id) if case_id else None
        query = request.query or (self._case_text(bundle.case) if bundle else "")

        similar_cases = analyze_case_similarity(case_id, query, top_k=request.top_k)
        evidence_insights = analyze_evidence(bundle.evidence if bundle else []) if bundle else []
        timeline_insight = analyze_timeline(
            bundle.timeline_events if bundle else [],
            bundle.evidence if bundle else [],
            bundle.witnesses if bundle else [],
            bundle.arrests if bundle else [],
            bundle.chargesheets if bundle else [],
            bundle.court_proceedings if bundle else [],
        )
        officer_assignments = OfficerRepository.query_assignments(type("Q", (), {"case_master_id": case_id})())[0] if case_id else []
        contradictions = detect_contradictions(bundle.witnesses if bundle else [], bundle.evidence if bundle else [], bundle.timeline_events if bundle else [], officer_assignments)
        sections = bundle.sections if bundle else []
        completeness = analyze_completeness(
            bundle.evidence if bundle else [],
            bundle.witnesses if bundle else [],
            bundle.timeline_events if bundle else [],
            bundle.arrests if bundle else [],
            bundle.chargesheets if bundle else [],
            bundle.court_proceedings if bundle else [],
            sections,
            bundle.victims if bundle else [],
        )
        legal_insight = analyze_legal(
            sections,
            bundle.evidence if bundle else [],
            bundle.arrests if bundle else [],
            bundle.chargesheets if bundle else [],
            bundle.court_proceedings if bundle else [],
        )
        recommendations = build_recommendations(completeness, evidence_insights, timeline_insight, contradictions, legal_insight, similar_cases)

        graph = None
        graph_start = perf_counter()
        if request.include_graph and bundle and case_id:
            sections, acts, case_sections = self._sections_and_acts(case_id)
            graph = build_relationship_graph(
                case=bundle.case,
                complainants=ComplainantRepository.get_complainants_by_case_id(case_id),
                victims=bundle.victims,
                accused=bundle.accused,
                evidence=bundle.evidence,
                witnesses=bundle.witnesses,
                arrests=bundle.arrests,
                chargesheets=bundle.chargesheets,
                court_proceedings=bundle.court_proceedings,
                officers=officer_assignments,
                timeline_events=bundle.timeline_events,
                sections=sections,
                case_sections=case_sections,
                acts=acts,
            )
        graph_time_ms = (perf_counter() - graph_start) * 1000.0

        if request.include_llm_reasoning and request.case_id:
            try:
                prompt_request = PromptRequest(
                    query=query,
                    prompt_type=PromptType.CASE_ANALYSIS,
                    persona=PromptPersona.INVESTIGATOR,
                    output_format="json",
                    max_token_budget=4096,
                )
                prompt_response = self.prompt_service.build_prompt(prompt_request)
                self.llm_service.generate(LLMRequest(prompt_response=prompt_response, provider="mock"))
            except Exception:
                pass

        reasoning_trace = build_reasoning_trace(case_id, evidence_insights, timeline_insight, contradictions, recommendations, similar_cases)
        overall_confidence = clamp_score(
            blend_confidence(
                [
                    max((item.confidence for item in similar_cases), default=0.0),
                    max((item.confidence for item in evidence_insights), default=0.0),
                    timeline_insight.confidence,
                    max((item.confidence for item in contradictions), default=0.0),
                    max((item.confidence for item in recommendations), default=0.0),
                    legal_insight.confidence,
                ]
            )
        )
        metrics = self.metrics.update(
            retrieval_confidence=max((item.confidence for item in similar_cases), default=0.0),
            evidence_confidence=max((item.confidence for item in evidence_insights), default=0.0),
            recommendation_confidence=max((item.confidence for item in recommendations), default=0.0),
            overall_confidence=overall_confidence,
            retrieval_time_ms=0.0,
            analysis_time_ms=(perf_counter() - started) * 1000.0,
            graph_time_ms=graph_time_ms,
            total_time_ms=(perf_counter() - started) * 1000.0,
            cache_hit=False,
            audits_recorded=self.audit.count(),
        )

        response = InvestigationResponse(
            case_id=case_id,
            query=query,
            similar_cases=similar_cases,
            evidence_insights=evidence_insights,
            timeline_insight=timeline_insight,
            contradictions=contradictions,
            completeness=completeness,
            legal_insight=legal_insight,
            recommendations=recommendations,
            graph=graph,
            reasoning_trace=reasoning_trace,
            metrics=metrics,
            confidence=overall_confidence,
            confidence_level=level_from_score(overall_confidence),
        )
        self.audit.record("analyze", case_id, f"Generated investigation response with confidence {overall_confidence:.2f}")
        self.cache.set(cache_key, response)
        return response

    def similar(self, request: InvestigationRequest, user_id: str | None = None):
        return analyze_case_similarity(request.case_id, request.query, top_k=request.top_k)

    def evidence(self, request: InvestigationRequest, user_id: str | None = None):
        bundle = self._bundle_for_case(request.case_id) if request.case_id else None
        return analyze_evidence(bundle.evidence if bundle else [])

    def timeline(self, request: InvestigationRequest, user_id: str | None = None):
        bundle = self._bundle_for_case(request.case_id) if request.case_id else None
        return analyze_timeline(
            bundle.timeline_events if bundle else [],
            bundle.evidence if bundle else [],
            bundle.witnesses if bundle else [],
            bundle.arrests if bundle else [],
            bundle.chargesheets if bundle else [],
            bundle.court_proceedings if bundle else [],
        )

    def contradictions(self, request: InvestigationRequest, user_id: str | None = None):
        bundle = self._bundle_for_case(request.case_id) if request.case_id else None
        officer_assignments = OfficerRepository.query_assignments(type("Q", (), {"case_master_id": request.case_id})())[0] if request.case_id else []
        return detect_contradictions(bundle.witnesses if bundle else [], bundle.evidence if bundle else [], bundle.timeline_events if bundle else [], officer_assignments)

    def recommend(self, request: InvestigationRequest, user_id: str | None = None):
        bundle = self._bundle_for_case(request.case_id) if request.case_id else None
        similar_cases = analyze_case_similarity(request.case_id, request.query, top_k=request.top_k)
        evidence_insights = analyze_evidence(bundle.evidence if bundle else []) if bundle else []
        timeline_insight = self.timeline(request, user_id=user_id)
        contradictions = self.contradictions(request, user_id=user_id)
        legal_insight = self.legal(request, user_id=user_id)
        completeness = self.completeness(request, user_id=user_id)
        return build_recommendations(completeness, evidence_insights, timeline_insight, contradictions, legal_insight, similar_cases)

    def completeness(self, request: InvestigationRequest, user_id: str | None = None):
        bundle = self._bundle_for_case(request.case_id) if request.case_id else None
        return analyze_completeness(
            bundle.evidence if bundle else [],
            bundle.witnesses if bundle else [],
            bundle.timeline_events if bundle else [],
            bundle.arrests if bundle else [],
            bundle.chargesheets if bundle else [],
            bundle.court_proceedings if bundle else [],
            bundle.sections if bundle else [],
            bundle.victims if bundle else [],
        )

    def legal(self, request: InvestigationRequest, user_id: str | None = None):
        bundle = self._bundle_for_case(request.case_id) if request.case_id else None
        return analyze_legal(
            bundle.sections if bundle else [],
            bundle.evidence if bundle else [],
            bundle.arrests if bundle else [],
            bundle.chargesheets if bundle else [],
            bundle.court_proceedings if bundle else [],
        )

    def build_graph(self, case_id: str) -> RelationshipGraph:
        bundle = self._bundle_for_case(case_id)
        if not bundle:
            return RelationshipGraph(case_id=case_id)
        sections, acts, case_sections = self._sections_and_acts(case_id)
        return build_relationship_graph(
            case=bundle.case,
            complainants=ComplainantRepository.get_complainants_by_case_id(case_id),
            victims=bundle.victims,
            accused=bundle.accused,
            evidence=bundle.evidence,
            witnesses=bundle.witnesses,
            arrests=bundle.arrests,
            chargesheets=bundle.chargesheets,
            court_proceedings=bundle.court_proceedings,
            officers=OfficerRepository.query_assignments(type("Q", (), {"case_master_id": case_id})())[0] if case_id else [],
            timeline_events=bundle.timeline_events,
            sections=sections,
            case_sections=case_sections,
            acts=acts,
        )

    def metrics_snapshot(self):
        return self.metrics.snapshot()

    def health(self) -> dict[str, object]:
        return {
            "status": "ok",
            "cache_size": self.cache.size(),
            "audits": self.audit.count(),
            "metrics": self.metrics.snapshot().model_dump(mode="json"),
        }
