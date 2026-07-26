from app.ai.graph_engine.graph_models import Community
from .connected_components import connected_components

class CommunityDetector:
    def detect(self, graph):
        return [Community(id=f"community-{i}", node_ids=sorted(group), reason="Connected by recorded case relationships", confidence=1.0) for i, group in enumerate(connected_components(graph), 1) if len(group) > 1]
