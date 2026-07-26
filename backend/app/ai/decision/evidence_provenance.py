from .decision_models import EvidenceProvenance
class EvidenceProvenanceBuilder:
    def build(self, outputs):
        records = []
        for module, payload in outputs.items():
            if not isinstance(payload, dict): continue
            for key in ('evidence_references', 'retrieved_chunk_references', 'citations', 'supporting_facts', 'source_records'):
                for reference in payload.get(key, []) or []: records.append(EvidenceProvenance(source_type=key, source_id=str(reference), description=f'Referenced by {module}', module=module, confidence=payload.get('confidence')))
        return records
