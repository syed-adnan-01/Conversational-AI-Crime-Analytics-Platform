from .bfs_search import bfs

def neighborhood(graph, entity_id, depth=1):
    node_ids, edge_ids = bfs(graph, entity_id, depth)
    return [node for node in graph.nodes if node.id in node_ids], [edge for edge in graph.edges if edge.id in edge_ids]
