from .relationship_builder import RelationshipBuilder

class RelationshipService:
    def __init__(self, builder: RelationshipBuilder | None = None): self.builder = builder or RelationshipBuilder()
    def discover(self, entities): return self.builder.build(entities)
