def health(service): return {'status': 'healthy', 'audit_entries': len(service.audit.entries)}
