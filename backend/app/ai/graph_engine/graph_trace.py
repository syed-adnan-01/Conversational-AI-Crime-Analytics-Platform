from .graph_models import GraphTrace

class GraphTracer:
    def __init__(self): self.traces: list[GraphTrace] = []
    def record(self, trace: GraphTrace): self.traces.append(trace); return trace
