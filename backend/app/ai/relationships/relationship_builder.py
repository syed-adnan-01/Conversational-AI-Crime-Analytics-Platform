from __future__ import annotations
from app.ai.entities.entity_models import EntityRecord, EntityType
from .relationship_models import Relationship, RelationshipType
from .relationship_rules import CASE_RELATIONSHIPS


class RelationshipBuilder:
    """Creates only relationships backed by fields present in source records."""
    def build(self, entities: list[EntityRecord]) -> list[Relationship]:
        by_source = {entity.source_id: entity for entity in entities if entity.source_id}
        relationships: list[Relationship] = []
        for entity in entities:
            case_id = entity.metadata.get("case_master_id")
            case = by_source.get(str(case_id)) if case_id is not None else None
            kind = CASE_RELATIONSHIPS.get(entity.entity_type.value)
            if case and kind:
                relationships.append(Relationship(source_id=entity.id, target_id=case.id, relationship_type=kind, confidence=1.0, source="repository", reason=f"{entity.entity_type.value} record is linked to case {case.source_id}", source_records=[str(entity.source_id), str(case.source_id)], supporting_entities=[entity.id, case.id]))
            for field, relation in (("victim_id", RelationshipType.REFERENCES), ("accused_id", RelationshipType.REFERENCES)):
                target = by_source.get(str(entity.metadata.get(field))) if entity.metadata.get(field) else None
                if target:
                    relationships.append(Relationship(source_id=entity.id, target_id=target.id, relationship_type=relation, confidence=1.0, source="repository", reason=f"{field} is recorded on the source record", source_records=[str(entity.source_id), str(target.source_id)], supporting_entities=[entity.id, target.id]))
        return relationships
