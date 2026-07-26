from .decision_models import Recommendation
from .recommendation_ranking import rank
class RecommendationEngine:
    def generate(self, request, provenance, confidence, reasoning):
        outputs = request.source_outputs; recommendations = []
        missing = []
        for module, output in outputs.items():
            if isinstance(output, dict): missing.extend(str(value) for key in ('missing_evidence', 'evidence_gaps', 'missing_documents', 'large_gaps') for value in output.get(key, []) or [])
        if missing:
            recommendations.append(Recommendation(title='Address identified investigation gaps', priority=1, explanation='One or more supplied analysis modules identified missing evidence or documentation.', supporting_evidence=provenance, confidence=confidence, recommended_next_step='Collect or document: ' + '; '.join(sorted(set(missing))), originating_modules=list(outputs), originating_agents=list((outputs.get('agents') or {}).keys()) if isinstance(outputs.get('agents'), dict) else [], reasoning_chain=reasoning, uncertainty_indicators=['Confidence is limited to supplied evidence and module outputs.'], status=request.status))
        if not recommendations:
            recommendations.append(Recommendation(title='Review available investigation analysis', priority=3, explanation='No evidence-backed gap was supplied; human review is recommended before any operational action.', supporting_evidence=provenance, confidence=confidence, recommended_next_step='Review source analyses and add corroborated evidence.', originating_modules=list(outputs), reasoning_chain=reasoning, uncertainty_indicators=['No actionable gap was found in the submitted outputs.'], status=request.status))
        return rank(recommendations)
