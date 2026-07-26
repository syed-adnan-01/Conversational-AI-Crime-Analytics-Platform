class ReportGenerator:
    def summary(self, evaluations):
        scores = [item.scores.overall for item in evaluations]; return {'count': len(evaluations), 'average_quality': sum(scores) / len(scores) if scores else 0.0, 'model_comparison': {}, 'regression': {'regressed': False}}
