def rank(recommendations): return sorted(recommendations, key=lambda item: (item.priority, -item.confidence.overall_confidence))
