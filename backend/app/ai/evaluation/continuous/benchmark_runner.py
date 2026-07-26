from .models import BenchmarkReport
class BenchmarkRunner:
    def __init__(self, service): self.service = service
    def run(self, suite):
        results = [self.service.evaluate(case) for case in suite.cases]
        return BenchmarkReport(suite=suite.name, total=len(results), average_score=sum(item.scores.overall for item in results) / len(results) if results else 0, evaluations=results)
