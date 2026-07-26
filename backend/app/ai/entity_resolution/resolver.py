from app.ai.entities.entity_models import EntityRecord
from app.ai.graph_engine.graph_models import ResolutionResult
from .duplicate_detector import matching_fields

class EntityResolutionService:
    def resolve(self, entities: list[EntityRecord]) -> ResolutionResult:
        if not entities: return ResolutionResult(resolution_score=0, reasoning=["No entities supplied"])
        anchor = entities[0]; duplicates = []; reasons = []
        for candidate in entities[1:]:
            exact, name_score = matching_fields(anchor, candidate)
            if exact or name_score >= .92:
                duplicates.append(candidate.id); reasons.append(f"Matched {candidate.id} by {', '.join(exact) if exact else 'high name similarity'}")
        score = 1.0 if duplicates and reasons and 'by ' in reasons[0] else 0.0
        if duplicates:
            merged = anchor.model_copy(deep=True); merged.aliases.extend(alias for entity in entities[1:] for alias in entity.aliases); merged.metadata["merged_source_ids"] = [entity.source_id for entity in entities]
            return ResolutionResult(resolution_score=score, merged_entity=merged, duplicate_entity_ids=duplicates, reasoning=reasons)
        return ResolutionResult(resolution_score=0.0, merged_entity=anchor, reasoning=["No duplicate evidence met the threshold"])
