def score(output, expected):
    recommendations = output.get('recommendations', []); explained = sum(bool(item.get('explanation') and item.get('supporting_evidence')) for item in recommendations if isinstance(item, dict)); count = len(recommendations)
    return {'recommendation_quality': explained / count if count else 0.0, 'evidence_coverage': float(bool(output.get('provenance') or output.get('evidence_references'))), 'explainability_completeness': explained / count if count else 0.0}
