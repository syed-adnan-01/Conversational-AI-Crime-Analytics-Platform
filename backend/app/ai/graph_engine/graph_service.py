from __future__ import annotations
from time import perf_counter
from app.ai.community_detection.network_analysis import CommunityDetector
from app.ai.entity_resolution.resolver import EntityResolutionService
from app.ai.graph_search.graph_queries import GraphQueries
from .graph_builder import GraphBuilder
from .graph_cache import GraphCache
from .graph_metrics import GraphMetricsTracker
from .graph_models import LinkPrediction

class GraphService:
    """Application facade. Dependencies are injectable; source repositories remain untouched."""
    def __init__(self, builder=None, cache=None, queries=None, resolver=None, communities=None, metrics=None):
        self.builder = builder or GraphBuilder(); self.cache = cache or GraphCache(); self.queries = queries or GraphQueries()
        self.resolver = resolver or EntityResolutionService(); self.communities = communities or CommunityDetector(); self.metrics = metrics or GraphMetricsTracker()
    def build(self, case_id: str, refresh=False):
        if not refresh:
            graph = self.cache.get(case_id)
            if graph: return graph
        started = perf_counter(); graph = self.builder.build(case_id); elapsed = (perf_counter()-started)*1000
        self.cache.put(case_id, graph); self.metrics.record_graph(graph, elapsed); self.metrics.value.cache_hit_rate = self.cache.hit_rate
        return graph
    def search(self, case_id, request):
        answer = self.queries.search(self.build(case_id), request); self.metrics.value.query_latency_ms = answer.query_latency_ms; return answer
    def expand(self, case_id, entity_id, depth=1): return self.queries.neighborhood(self.build(case_id), entity_id, depth)
    def shortest_path(self, case_id, source_id, target_id): return self.queries.shortest_path(self.build(case_id), source_id, target_id)
    def entity(self, entity_id):
        for graph in self.cache._values.values():
            for node in graph.nodes:
                if node.id == entity_id: return node
        return None
    def community(self, case_id): return self.communities.detect(self.build(case_id))
    def resolve(self, entities):
        outcome = self.resolver.resolve(entities); self.metrics.value.resolution_accuracy = outcome.resolution_score; return outcome
    def link_predictions(self, case_id):
        graph = self.build(case_id); predictions = []
        neighbours = {node.id: set() for node in graph.nodes}
        for edge in graph.edges: neighbours.setdefault(edge.source_id, set()).add(edge.target_id); neighbours.setdefault(edge.target_id, set()).add(edge.source_id)
        ids = sorted(neighbours)
        for index, source_id in enumerate(ids):
            for target_id in ids[index + 1:]:
                if target_id in neighbours[source_id]: continue
                shared = neighbours[source_id] & neighbours[target_id]
                if len(shared) >= 2:
                    predictions.append(LinkPrediction(source_id=source_id, target_id=target_id, relationship_type="ASSOCIATED_WITH", confidence=min(.9, .4 + .15 * len(shared)), supporting_evidence=sorted(shared), reasoning="Both entities have recorded relationships to the listed supporting entities; this is a suggestion, not a discovered fact."))
        return predictions
    def statistics(self, case_id=None):
        return self.build(case_id).statistics if case_id else self.metrics.value
    def health(self): return {"status": "healthy", "cache_hit_rate": self.cache.hit_rate, "cached_graphs": len(self.cache._values)}
