"""
============================================================
Markdown Serializer Strategy
============================================================

Module  : AI Context Builder
Purpose : Formats InvestigationContext into structured Markdown reports
          optimized for LLM prompt contexts.
"""

from app.ai.context.context_models import DetailLevel, InvestigationContext
from app.ai.context.exceptions import AIContextSerializationException
from app.ai.context.serializers.base import BaseSerializer


class MarkdownSerializer(BaseSerializer):
    """
    Serializes InvestigationContext into structured Markdown optimized for LLM prompts.
    """

    def serialize(
        self,
        context: InvestigationContext,
        level: DetailLevel = DetailLevel.STANDARD,
    ) -> str:
        try:
            lines: list[str] = []

            # ----------------------------------------------------------
            # Header & Summary Section
            # ----------------------------------------------------------
            lines.append(f"# INVESTIGATION CONTEXT REPORT: {context.summary.case_title}")
            lines.append(f"**Status:** {context.summary.status}")
            lines.append(f"**Registered Date:** {context.summary.registered_date or 'N/A'}")
            lines.append(f"**Lead Officer:** {context.summary.lead_officer or 'Unassigned'}")
            lines.append(f"**AI Readiness:** {'🟢 Ready' if context.summary.is_ai_ready else '🟡 Incomplete'}")
            lines.append("")

            lines.append("## CONTEXT SUMMARY & STATISTICS")
            lines.append(f"- **Total Entities:** {context.metadata.total_entities}")
            lines.append(f"- **Victims:** {context.summary.total_victims}")
            lines.append(f"- **Accused:** {context.summary.total_accused}")
            lines.append(f"- **Evidence Items:** {context.summary.total_evidence}")
            lines.append(f"- **Sections Applied:** {context.summary.total_sections}")
            lines.append("")

            if level == DetailLevel.SUMMARY:
                return "\n".join(lines)

            # ----------------------------------------------------------
            # Standard Case Details
            # ----------------------------------------------------------
            case = context.case
            lines.append("## CASE DETAILS")
            lines.append(f"- **Crime Number:** {case.crime_no}")
            if case.case_no:
                lines.append(f"- **Court Case Number:** {case.case_no}")
            lines.append(f"- **Registration Date:** {case.crime_registered_date}")
            lines.append("")

            # Complainant
            lines.append("## COMPLAINANT")
            if context.complainant:
                c = context.complainant
                lines.append(f"- **Name:** {c.name}")
                lines.append(f"- **Gender/Age:** {getattr(c.gender, 'value', c.gender) or 'N/A'}, {c.age or 'N/A'} yrs")
                lines.append(f"- **Contact:** {c.mobile_no or 'N/A'} | Email: {c.email or 'N/A'}")
                lines.append(f"- **Address:** {c.address or 'N/A'}")
            else:
                lines.append("No complainant registered.")
            lines.append("")

            # Victims
            lines.append("## VICTIMS")
            if context.victims:
                for v in context.victims:
                    lines.append(f"- **{v.name}** (Age: {v.age or 'N/A'}, Gender: {getattr(v.gender, 'value', v.gender) or 'N/A'}, Mobile: {getattr(v, 'mobile_no', None) or 'N/A'})")
            else:
                lines.append("No victims registered.")
            lines.append("")

            # Accused
            lines.append("## ACCUSED")
            if context.accused:
                for a in context.accused:
                    alias_str = getattr(a, 'alias', None) or 'N/A'
                    lines.append(f"- **{a.name}** (Alias: {alias_str}, Mobile: {getattr(a, 'mobile_no', None) or 'N/A'})")
            else:
                lines.append("No accused persons registered.")
            lines.append("")

            # Sections
            lines.append("## LAW SECTIONS APPLIED")
            if context.sections:
                for s in context.sections:
                    lines.append(f"- **Section {s.section_number}:** {s.title} (Cognizable: {s.is_cognizable}, Bailable: {s.is_bailable})")
            else:
                lines.append("No legal sections assigned.")
            lines.append("")

            # Evidence
            lines.append("## EVIDENCE REGISTERED")
            if context.evidence:
                for e in context.evidence:
                    e_type = getattr(e.evidence_type, 'value', e.evidence_type) or 'N/A'
                    c_status = getattr(e, 'custody_status', None) or 'N/A'
                    lines.append(f"- **[{e.evidence_number}] {e.title}** ({e_type}) - Custody: {c_status}")
            else:
                lines.append("No evidence registered.")
            lines.append("")

            # Arrests
            lines.append("## ARRESTS")
            if context.arrests:
                for arr in context.arrests:
                    arr_status = getattr(arr.status, 'value', arr.status) or 'N/A'
                    arr_loc = getattr(arr, 'arrest_location', None) or 'N/A'
                    lines.append(f"- **Arrest Date:** {arr.arrest_date} | Status: {arr_status} | Location: {arr_loc}")
            else:
                lines.append("No arrests recorded.")
            lines.append("")

            # Chargesheets
            lines.append("## CHARGESHEETS")
            if context.chargesheets:
                for cs in context.chargesheets:
                    cs_status = getattr(cs.status, 'value', cs.status) or 'N/A'
                    lines.append(f"- **Chargesheet No:** {cs.chargesheet_number} | Filed Date: {cs.filing_date} | Status: {cs_status}")
            else:
                lines.append("No chargesheets filed.")
            lines.append("")

            # Court Proceedings
            lines.append("## COURT PROCEEDINGS")
            if context.court_proceedings:
                for cp in context.court_proceedings:
                    cp_stage = getattr(cp.stage, 'value', cp.stage) or 'N/A'
                    lines.append(f"- **Hearing Date:** {cp.hearing_date} | Court: {cp.court_name} | Stage: {cp_stage} | Next Date: {cp.next_hearing_date or 'N/A'}")
            else:
                lines.append("No court proceedings recorded.")
            lines.append("")

            # Timeline
            lines.append("## INVESTIGATION TIMELINE")
            if context.timeline_events:
                for te in context.timeline_events:
                    te_type = getattr(te.event_type, 'value', te.event_type) or 'N/A'
                    lines.append(f"- **[{te.event_time}] {te.title}** ({te_type}): {te.description}")
            else:
                lines.append("No timeline events recorded.")
            lines.append("")

            # ----------------------------------------------------------
            # Detailed View Extras
            # ----------------------------------------------------------
            if level == DetailLevel.DETAILED:
                lines.append("## METADATA & SYSTEM FINGERPRINT")
                lines.append(f"- **Case ID:** {context.metadata.case_id}")
                lines.append(f"- **Context Version:** {context.metadata.context_version}")
                lines.append(f"- **Build Duration:** {context.metadata.build_duration_ms} ms")
                lines.append(f"- **Context Hash (SHA-256):** `{context.metadata.context_hash}`")
                lines.append("- **AI Readiness Checklist:**")
                for reason in context.metadata.ai_readiness_reasons:
                    lines.append(f"  - {reason}")
                lines.append("")

            return "\n".join(lines)
        except Exception as exc:
            raise AIContextSerializationException("Markdown", str(exc)) from exc
