"""Build relationship graphs for a case."""

from __future__ import annotations

from app.ai.investigation.analysis.confidence import blend_confidence, clamp_score
from app.ai.investigation.graph.entity_graph import add_edge, add_node
from app.ai.investigation.intelligence.investigation_models import RelationshipGraph
from app.models.act import Act
from app.models.accused import Accused
from app.models.arrest import Arrest
from app.models.case_master import CaseMaster
from app.models.case_section import CaseSectionAssociation
from app.models.chargesheet import Chargesheet
from app.models.complainant import Complainant
from app.models.court_proceeding import CourtProceeding
from app.models.evidence import Evidence
from app.models.officer import OfficerAssignment
from app.models.section import Section
from app.models.timeline import TimelineEvent
from app.models.victim import Victim
from app.models.witness import Witness


def build_relationship_graph(
    case: CaseMaster,
    complainants: list[Complainant],
    victims: list[Victim],
    accused: list[Accused],
    evidence: list[Evidence],
    witnesses: list[Witness],
    arrests: list[Arrest],
    chargesheets: list[Chargesheet],
    court_proceedings: list[CourtProceeding],
    officers: list[OfficerAssignment],
    timeline_events: list[TimelineEvent],
    sections: list[Section],
    case_sections: list[CaseSectionAssociation],
    acts: list[Act],
) -> RelationshipGraph:
    nodes = []
    edges = []

    add_node(nodes, case.case_master_id, "case", case.crime_no, case.case_master_id, crime_no=case.crime_no, brief_facts=case.brief_facts)

    for complainant in complainants:
        node_id = complainant.complainant_id or complainant.name
        add_node(nodes, node_id, "complainant", complainant.name, case.case_master_id)
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "has_complainant", 0.9)

    for victim in victims:
        node_id = victim.victim_id or victim.name
        add_node(nodes, node_id, "victim", victim.name, case.case_master_id)
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "has_victim", 0.95)

    for accused_item in accused:
        node_id = accused_item.accused_id or accused_item.name
        add_node(nodes, node_id, "accused", accused_item.name, case.case_master_id)
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "has_accused", 0.95)

    for item in evidence:
        node_id = item.evidence_id or item.evidence_number
        add_node(nodes, node_id, "evidence", item.title, case.case_master_id, evidence_type=item.evidence_type.value if hasattr(item.evidence_type, 'value') else str(item.evidence_type))
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "has_evidence", 0.92)
        if item.accused_id:
            add_edge(edges, f"EDGE-{node_id}-{item.accused_id}", node_id, item.accused_id, "linked_to_accused", 0.82)
        if item.victim_id:
            add_edge(edges, f"EDGE-{node_id}-{item.victim_id}", node_id, item.victim_id, "linked_to_victim", 0.82)

    for witness in witnesses:
        node_id = witness.witness_id or witness.name
        add_node(nodes, node_id, "witness", witness.name, case.case_master_id)
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "has_witness", 0.9)

    for arrest in arrests:
        node_id = arrest.arrest_id or f"{arrest.accused_id}-{arrest.arrest_date.isoformat()}"
        add_node(nodes, node_id, "arrest", arrest.grounds_for_arrest, case.case_master_id)
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "has_arrest", 0.86)
        add_edge(edges, f"EDGE-{node_id}-{arrest.accused_id}", node_id, arrest.accused_id, "arrests", 0.9)

    for chargesheet in chargesheets:
        node_id = chargesheet.chargesheet_id or chargesheet.chargesheet_number
        add_node(nodes, node_id, "chargesheet", chargesheet.chargesheet_number, case.case_master_id)
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "has_chargesheet", 0.9)

    for proceeding in court_proceedings:
        node_id = proceeding.proceeding_id or proceeding.court_name
        add_node(nodes, node_id, "court_proceeding", proceeding.stage.value if hasattr(proceeding.stage, 'value') else str(proceeding.stage), case.case_master_id)
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "has_court_proceeding", 0.85)

    for officer in officers:
        node_id = officer.officer_id or officer.assignment_id or (officer.role.value if hasattr(officer.role, 'value') else str(officer.role))
        add_node(nodes, node_id, "officer", getattr(officer.role, 'value', str(officer.role)), case.case_master_id)
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "assigned_officer", 0.9)

    for timeline_event in timeline_events:
        node_id = timeline_event.event_id or timeline_event.title
        add_node(nodes, node_id, "timeline", timeline_event.title, case.case_master_id, event_type=timeline_event.event_type.value if hasattr(timeline_event.event_type, 'value') else str(timeline_event.event_type))
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "timeline_event", 0.88)

    for section in sections:
        node_id = section.section_id or section.section_number
        add_node(nodes, node_id, "section", section.section_number, case.case_master_id, title=section.title)
        add_edge(edges, f"EDGE-{case.case_master_id}-{node_id}", case.case_master_id, node_id, "charged_under", 0.9)
        for act in acts:
            if act.act_id == section.act_id:
                add_node(nodes, act.act_id or act.short_name, "act", act.short_name, case.case_master_id, name=act.name)
                add_edge(edges, f"EDGE-{act.act_id}-{node_id}", act.act_id or act.short_name, node_id, "contains_section", 0.92)

    confidence = clamp_score(
        blend_confidence(
            [
                1.0 if nodes else 0.0,
                1.0 if edges else 0.0,
                min(1.0, len(nodes) / 10.0),
                min(1.0, len(edges) / 15.0),
            ]
        )
    )

    return RelationshipGraph(
        case_id=case.case_master_id,
        nodes=nodes,
        edges=edges,
        summary=f"Graph built with {len(nodes)} nodes and {len(edges)} edges.",
        confidence=confidence,
    )
