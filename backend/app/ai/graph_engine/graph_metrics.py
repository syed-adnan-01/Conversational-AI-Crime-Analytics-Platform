from .graph_models import GraphMetrics

class GraphMetricsTracker:
    def __init__(self): self.value = GraphMetrics()
    def record_graph(self, graph, build_time_ms=0):
        self.value.node_count = len(graph.nodes); self.value.edge_count = len(graph.edges); self.value.graph_build_time_ms = build_time_ms
