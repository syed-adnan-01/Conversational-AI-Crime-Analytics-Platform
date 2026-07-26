from .models import MaskingLevel
class RedactionEngine:
    def redact(self, text, detections, level=MaskingLevel.PARTIAL):
        if level == MaskingLevel.NONE: return text
        result = text
        for _, value in detections:
            replacement = '[REDACTED]' if level == MaskingLevel.FULL else value[:2] + '*' * max(0, len(value)-4) + value[-2:]
            result = result.replace(value, replacement)
        return result
