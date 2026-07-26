def connected_components(graph):
    remaining = {node.id for node in graph.nodes}; groups = []
    while remaining:
        component = {remaining.pop()}; changed = True
        while changed:
            changed = False
            for edge in graph.edges:
                if edge.source_id in component and edge.target_id not in component: component.add(edge.target_id); remaining.discard(edge.target_id); changed = True
                if edge.target_id in component and edge.source_id not in component: component.add(edge.source_id); remaining.discard(edge.source_id); changed = True
        groups.append(component)
    return groups
