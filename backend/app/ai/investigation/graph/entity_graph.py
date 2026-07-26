"""Entity graph builder."""

from __future__ import annotations

from app.ai.investigation.analysis.confidence import clamp_score
from app.ai.investigation.intelligence.investigation_models import RelationshipEdge, RelationshipGraph, RelationshipNode


def add_node(nodes: list[RelationshipNode], node_id: str, node_type: str, label: str, case_id: str | None = None, **attributes) -> None:
    if any(node.node_id == node_id for node in nodes):
        return
    nodes.append(RelationshipNode(node_id=node_id, node_type=node_type, label=label, case_id=case_id, attributes=attributes))


def add_edge(
    edges: list[RelationshipEdge],
    edge_id: str,
    source_id: str,
    target_id: str,
    relation: str,
    confidence: float,
    **attributes,
) -> None:
    if any(edge.edge_id == edge_id for edge in edges):
        return
    edges.append(
        RelationshipEdge(
            edge_id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            confidence=clamp_score(confidence),
            attributes=attributes,
        )
    )
