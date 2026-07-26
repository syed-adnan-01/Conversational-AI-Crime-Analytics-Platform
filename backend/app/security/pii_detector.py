import re
class PIIDetector:
    patterns = {'email': r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b', 'phone': r'\b(?:\+91[- ]?)?[6-9]\d{9}\b', 'aadhaar': r'\b\d{4}[ -]?\d{4}[ -]?\d{4}\b', 'pan': r'\b[A-Z]{5}\d{4}[A-Z]\b', 'passport': r'\b[A-Z][0-9]{7}\b'}
    def detect(self, text): return [(kind, match.group(0)) for kind, pattern in self.patterns.items() for match in re.finditer(pattern, text or '')]
