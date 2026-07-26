from .graph_export import GraphExporter
def export(graph): return GraphExporter().cytoscape(graph)
