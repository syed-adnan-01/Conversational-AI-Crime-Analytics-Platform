from app.ai.graph_engine.graph_builder import GraphBuilder
from app.ai.graph_engine.graph_service import GraphService
from app.ai.graph_engine.graph_models import GraphSearchRequest

class Provider:
    def case_data(self, case_id):
        return {"case": {"case_master_id": case_id, "crime_no": "42/2026"}, "accused": [{"accused_id": "A1", "case_master_id": case_id, "name": "Ravi"}], "victims": [{"victim_id": "V1", "case_master_id": case_id, "name": "Sam"}], "witnesses": [], "evidence": [{"evidence_id": "E1", "case_master_id": case_id, "title": "CCTV", "accused_id": "A1"}], "timeline": []}

def test_build_and_search_graph():
    service = GraphService(builder=GraphBuilder(provider=Provider()))
    graph = service.build("C1")
    assert graph.statistics.node_count == 4
    accused = next(node for node in graph.nodes if node.source_id == "A1")
    result = service.search("C1", GraphSearchRequest(start_entity_id=accused.id, max_depth=2))
    assert len(result.nodes) >= 2
    assert all(edge.reason and edge.source_records for edge in graph.edges)
