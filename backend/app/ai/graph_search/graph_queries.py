from time import perf_counter
from app.ai.graph_engine.graph_models import GraphSearchResponse
from .bfs_search import bfs
from .shortest_path import shortest_path
from .neighborhood import neighborhood

class GraphQueries:
    def search(self, graph, request):
        started = perf_counter(); nodes, edge_ids = bfs(graph, request.start_entity_id, request.max_depth, request.relationship_types)
        return GraphSearchResponse(nodes=[node for node in graph.nodes if node.id in nodes], edges=[edge for edge in graph.edges if edge.id in edge_ids], depth=request.max_depth, query_latency_ms=(perf_counter()-started)*1000)
    def shortest_path(self, graph, start_id, end_id): return shortest_path(graph, start_id, end_id)
    def neighborhood(self, graph, entity_id, depth):
        nodes, edges = neighborhood(graph, entity_id, depth); return GraphSearchResponse(nodes=nodes, edges=edges, depth=depth)
