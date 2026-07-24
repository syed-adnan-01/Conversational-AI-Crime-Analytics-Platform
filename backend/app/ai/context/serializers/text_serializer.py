"""
============================================================
Text Serializer Strategy
============================================================

Module  : AI Context Builder
Purpose : Formats InvestigationContext into dense plain text optimized
          for vector embeddings and semantic search.
"""

from app.ai.context.context_models import DetailLevel, InvestigationContext
from app.ai.context.exceptions import AIContextSerializationException
from app.ai.context.serializers.base import BaseSerializer


class TextSerializer(BaseSerializer):
    """
    Serializes InvestigationContext into dense plain text for embedding models.
    """

    def serialize(
        self,
        context: InvestigationContext,
        level: DetailLevel = DetailLevel.STANDARD,
    ) -> str:
        try:
            chunks: list[str] = []

            # Basic Summary Chunk
            summary_chunk = (
                f"INVESTIGATION SUMMARY: {context.summary.case_title}. "
                f"Status: {context.summary.status}. "
                f"Registered Date: {context.summary.registered_date or 'Unknown'}. "
                f"Lead Officer: {context.summary.lead_officer or 'Unassigned'}. "
                f"Counts: {context.summary.total_accused} accused, {context.summary.total_victims} victims, "
                f"{context.summary.total_evidence} evidence items, {context.summary.total_sections} sections."
            )
            chunks.append(summary_chunk)

            if level == DetailLevel.SUMMARY:
                return "\n".join(chunks)

            # Complainant Chunk
            if context.complainant:
                c = context.complainant
                complainant_chunk = (
                    f"COMPLAINANT: Name: {c.name}. Gender: {getattr(c.gender, 'value', c.gender) or 'N/A'}. "
                    f"Age: {c.age or 'N/A'}. Address: {c.address or 'N/A'}. Contact: {c.mobile_no or 'N/A'}."
                )
                chunks.append(complainant_chunk)

            # Victims Chunk
            if context.victims:
                v_str = "; ".join(
                    f"{v.name} (Age: {v.age or 'N/A'}, Gender: {getattr(v.gender, 'value', v.gender) or 'N/A'})"
                    for v in context.victims
                )
                chunks.append(f"VICTIMS: {v_str}.")

            # Accused Chunk
            if context.accused:
                a_str = "; ".join(
                    f"{a.name} (Mobile: {getattr(a, 'mobile_no', None) or 'N/A'})"
                    for a in context.accused
                )
                chunks.append(f"ACCUSED PERSONS: {a_str}.")

            # Sections Chunk
            if context.sections:
                s_str = "; ".join(
                    f"Section {s.section_number}: {s.title} ({s.description or 'No desc'})"
                    for s in context.sections
                )
                chunks.append(f"APPLIED SECTIONS: {s_str}.")

            # Evidence Chunk
            if context.evidence:
                e_str = "; ".join(
                    f"[{e.evidence_number}] {e.title} ({getattr(e.evidence_type, 'value', e.evidence_type) or 'N/A'})"
                    for e in context.evidence
                )
                chunks.append(f"EVIDENCE: {e_str}.")

            # Timeline Chunk
            if context.timeline_events:
                t_str = "; ".join(
                    f"[{te.event_time}] {te.title}: {te.description}"
                    for te in context.timeline_events
                )
                chunks.append(f"TIMELINE: {t_str}.")

            if level == DetailLevel.DETAILED:
                meta_chunk = (
                    f"METADATA: CaseID: {context.metadata.case_id}. Hash: {context.metadata.context_hash}. "
                    f"BuildDuration: {context.metadata.build_duration_ms}ms. AI Ready: {context.metadata.is_ai_ready}."
                )
                chunks.append(meta_chunk)

            return "\n\n".join(chunks)
        except Exception as exc:
            raise AIContextSerializationException("Text", str(exc)) from exc
