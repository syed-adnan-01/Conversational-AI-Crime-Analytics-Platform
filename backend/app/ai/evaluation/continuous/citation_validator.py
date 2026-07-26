from .models import QualityIssue
class CitationValidator:
    def validate(self, output, expected):
        actual = set(output.get('citations', [])); known = set(expected.get('citations', [])); issues = []
        if output.get('claims') and not actual: issues.append(QualityIssue(category='missing_citations', description='Claims were supplied without citations.', severity='high'))
        for citation in actual - known: issues.append(QualityIssue(category='evidence_mismatch', description='Citation is absent from supplied references.', reference=str(citation), severity='high'))
        return issues
