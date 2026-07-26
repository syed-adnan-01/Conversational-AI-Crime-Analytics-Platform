def calibration(output, expected):
    confidence = float(output.get('confidence', output.get('overall_confidence', 0))); outcome = expected.get('outcome')
    return abs(confidence - float(outcome)) if outcome is not None else 0.0
