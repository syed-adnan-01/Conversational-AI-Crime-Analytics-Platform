from .alternative_hypothesis_builder import AlternativeHypothesisBuilder
class HypothesisEngine:
    def __init__(self, builder=None): self.builder = builder or AlternativeHypothesisBuilder()
    def generate(self, provenance, confidence): return self.builder.build(provenance, confidence)
