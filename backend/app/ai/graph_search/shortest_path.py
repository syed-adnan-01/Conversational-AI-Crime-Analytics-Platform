from collections import deque
from app.ai.graph_engine.graph_models import ShortestPath

def shortest_path(graph, start_id, end_id):
    queue = deque([start_id]); prior = {start_id: (None, None)}
    while queue and end_id not in prior:
        current = queue.popleft()
        for edge in graph.edges:
            if edge.source_id != current and edge.target_id != current: continue
            other = edge.target_id if edge.source_id == current else edge.source_id
            if other not in prior: prior[other] = (current, edge); queue.append(other)
    if end_id not in prior: return ShortestPath()
    nodes, edges, current = [], [], end_id
    while current is not None:
        nodes.append(current); parent, edge = prior[current]
        if edge: edges.append(edge)
        current = parent
    return ShortestPath(node_ids=list(reversed(nodes)), edges=list(reversed(edges)), found=True)
