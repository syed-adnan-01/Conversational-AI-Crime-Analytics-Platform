from .graph_builder import GraphBuilder

class GraphEngine:
    def __init__(self, builder=None): self.builder = builder or GraphBuilder()
    def build(self, case_id): return self.builder.build(case_id)
