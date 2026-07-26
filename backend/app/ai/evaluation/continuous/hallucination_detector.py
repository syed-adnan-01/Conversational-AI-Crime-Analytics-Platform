from .models import QualityIssue
class HallucinationDetector:
    def detect(self, output, expected):
        issues = []; claims = set(output.get('claims', [])); supported = set(expected.get('supported_claims', []))
        for claim in claims - supported: issues.append(QualityIssue(category='unsupported_claim', description='Claim is not present in supplied supporting claims.', reference=str(claim), severity='high'))
        for entity in set(output.get('entities', [])) - set(expected.get('entities', [])): issues.append(QualityIssue(category='fabricated_entity', description='Entity is absent from supplied reference entities.', reference=str(entity), severity='high'))
        for section in set(output.get('legal_sections', [])) - set(expected.get('legal_sections', [])): issues.append(QualityIssue(category='fabricated_legal_section', description='Legal section is absent from supplied legal references.', reference=str(section), severity='high'))
        return issues
