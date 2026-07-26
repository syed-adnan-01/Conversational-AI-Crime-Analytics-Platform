from collections import deque

def bfs(graph, start_id, max_depth=2, relationship_types=()):
    allowed = set(relationship_types); visited = {start_id}; queue = deque([(start_id, 0)]); edge_ids = set()
    adjacency = {}
    for edge in graph.edges:
        if allowed and edge.relationship_type.value not in allowed: continue
        adjacency.setdefault(edge.source_id, []).append(edge); adjacency.setdefault(edge.target_id, []).append(edge)
    while queue:
        node_id, depth = queue.popleft()
        if depth >= max_depth: continue
        for edge in adjacency.get(node_id, []):
            edge_ids.add(edge.id); other = edge.target_id if edge.source_id == node_id else edge.source_id
            if other not in visited: visited.add(other); queue.append((other, depth + 1))
    return visited, edge_ids
