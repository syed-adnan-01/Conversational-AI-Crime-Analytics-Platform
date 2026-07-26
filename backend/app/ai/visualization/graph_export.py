COLORS = {"Case": "#2563eb", "Accused": "#dc2626", "Victim": "#7c3aed", "Witness": "#059669", "Evidence": "#d97706", "Timeline": "#64748b"}
class GraphExporter:
    def cytoscape(self, graph):
        return {"elements": {"nodes": [{"data": {"id": node.id, "label": node.label, "type": node.entity_type.value, "color": COLORS.get(node.entity_type.value, "#64748b"), "group": node.group}} for node in graph.nodes], "edges": [{"data": {"id": edge.id, "source": edge.source_id, "target": edge.target_id, "label": edge.relationship_type.value, "confidence": edge.confidence}} for edge in graph.edges]}}
    def reactflow(self, graph):
        return {"nodes": [{"id": node.id, "type": "default", "data": {"label": node.label, "entityType": node.entity_type.value, "color": COLORS.get(node.entity_type.value, "#64748b")}, "position": {"x": i * 180, "y": (i % 3) * 120}} for i, node in enumerate(graph.nodes)], "edges": [{"id": edge.id, "source": edge.source_id, "target": edge.target_id, "label": edge.relationship_type.value} for edge in graph.edges]}
