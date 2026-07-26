def score(output, expected):
    tokens = output.get('token_count', 0); budget = expected.get('token_budget', 0)
    return {'token_efficiency': min(1.0, budget / tokens) if tokens and budget else 0.0, 'template_utilization': float(bool(output.get('template_id'))), 'context_utilization': min(1.0, output.get('context_tokens', 0) / expected.get('context_budget', 1))}
