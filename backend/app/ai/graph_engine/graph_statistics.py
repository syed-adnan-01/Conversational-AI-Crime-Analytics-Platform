from collections import Counter
from .graph_models import GraphStatistics

def calculate_statistics(nodes, edges):
    return GraphStatistics(node_count=len(nodes), edge_count=len(edges), entity_counts=dict(Counter(n.entity_type.value for n in nodes)), relationship_counts=dict(Counter(e.relationship_type.value for e in edges)))
