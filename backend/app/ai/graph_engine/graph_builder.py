from __future__ import annotations
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Protocol
from app.ai.entities.entity_models import EntityType
from app.ai.entities.entity_registry import EntityRegistry
from app.ai.relationships.relationship_builder import RelationshipBuilder
from .graph_models import GraphEdge, GraphNode, RelationshipGraph
from .graph_statistics import calculate_statistics


class CaseDataProvider(Protocol):
    def case_data(self, case_id: str) -> dict[str, object]: ...

class RepositoryCaseDataProvider:
    """Read-only adapter around the existing repositories; injectable in tests/providers."""
    def case_data(self, case_id: str) -> dict[str, object]:
        from app.repository.case_repository import CaseRepository
        from app.repository.accused_repository import AccusedRepository
        from app.repository.victim_repository import VictimRepository
        from app.repository.witness_repository import WitnessRepository
        from app.repository.evidence_repository import EvidenceRepository
        from app.repository.timeline_repository import TimelineRepository
        return {"case": CaseRepository.get_case_by_id(case_id), "accused": AccusedRepository.get_accused_by_case_id(case_id), "victims": VictimRepository.get_victims_by_case_id(case_id), "witnesses": WitnessRepository.get_witnesses_by_case_id(case_id), "evidence": EvidenceRepository.get_case_evidence(case_id), "timeline": TimelineRepository.get_case_timeline(case_id)}

class GraphBuilder:
    def __init__(self, provider: CaseDataProvider | None = None, registry: EntityRegistry | None = None, relationship_builder: RelationshipBuilder | None = None):
        self.provider = provider or RepositoryCaseDataProvider(); self.registry = registry or EntityRegistry(); self.relationship_builder = relationship_builder or RelationshipBuilder()
    @staticmethod
    def _data(item):
        raw = item.model_dump() if hasattr(item, "model_dump") else asdict(item) if is_dataclass(item) else dict(item)
        return {key: (value.value if isinstance(value, Enum) else value) for key, value in raw.items()}
    def _add(self, result, entity_type, source_id, label, data):
        if source_id is None: return
        result.append(self.registry.register(entity_type, source_id, label or str(source_id), data))
    def build(self, case_id: str) -> RelationshipGraph:
        source = self.provider.case_data(case_id); entities = []
        case = source.get("case")
        if case:
            data = self._data(case); self._add(entities, EntityType.CASE, data.get("case_master_id", case_id), data.get("crime_no") or data.get("case_no"), data)
        for key, entity_type, id_field, label_field in (("accused", EntityType.ACCUSED, "accused_id", "name"), ("victims", EntityType.VICTIM, "victim_id", "name"), ("witnesses", EntityType.WITNESS, "witness_id", "name"), ("evidence", EntityType.EVIDENCE, "evidence_id", "title"), ("timeline", EntityType.TIMELINE, "event_id", "title")):
            for item in source.get(key, []) or []:
                data = self._data(item); self._add(entities, entity_type, data.get(id_field), data.get(label_field), data)
        nodes = [GraphNode(**entity.model_dump(), group=entity.entity_type.value) for entity in entities]
        edges = [GraphEdge(**edge.model_dump(), id=f"KG-EDGE-{index}") for index, edge in enumerate(self.relationship_builder.build(entities), 1)]
        return RelationshipGraph(nodes=nodes, edges=edges, metadata={"case_id": case_id, "source": "repositories"}, statistics=calculate_statistics(nodes, edges))
