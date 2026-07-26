class ComplianceReports:
    def build(self, results): return {'checks': len(results), 'compliant': sum(item.compliant for item in results), 'non_compliant': sum(not item.compliant for item in results)}
