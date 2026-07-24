"""
============================================================
Prompt Context Formatter
============================================================

Module  : AI Context Assembly Subsystem
Purpose : Formats chunks into structured PromptSections ready for LLM consumption.
"""

from app.ai.retrieval.retrieval_models import PromptSections, RetrievedChunk


class PromptContextFormatter:
    """
    Formats retrieved chunks into clean, structured prompt sections.
    """

    @classmethod
    def format_sections(cls, query: str, chunks: list[RetrievedChunk]) -> PromptSections:
        case_lines: list[str] = []
        victim_lines: list[str] = []
        accused_lines: list[str] = []
        evidence_lines: list[str] = []
        timeline_lines: list[str] = []
        legal_lines: list[str] = []

        for chunk in chunks:
            line = f"{chunk.citation.source_reference} {chunk.content}"
            ctype = chunk.chunk_type.upper()

            if ctype in ("CASE", "COMPLAINANT"):
                case_lines.append(line)
            elif ctype == "VICTIM":
                victim_lines.append(line)
            elif ctype in ("ACCUSED", "ARREST"):
                accused_lines.append(line)
            elif ctype == "EVIDENCE":
                evidence_lines.append(line)
            elif ctype in ("TIMELINE", "COURT", "OFFICER"):
                timeline_lines.append(line)
            elif ctype in ("SECTION", "CHARGESHEET"):
                legal_lines.append(line)

        system_text = (
            "You are CrimeSphere AI, an expert law enforcement intelligence copilot. "
            "Base your answer strictly on the verified investigation context below. "
            "Include source citations (e.g. [Evidence #ID]) for all statements."
        )

        return PromptSections(
            system_context=system_text,
            case_summary="\n".join(case_lines) if case_lines else "No specific case summary chunks retrieved.",
            victims="\n".join(victim_lines) if victim_lines else "No victim records retrieved.",
            accused="\n".join(accused_lines) if accused_lines else "No accused/arrest records retrieved.",
            evidence="\n".join(evidence_lines) if evidence_lines else "No evidence records retrieved.",
            timeline="\n".join(timeline_lines) if timeline_lines else "No timeline/court records retrieved.",
            legal="\n".join(legal_lines) if legal_lines else "No legal/chargesheet records retrieved.",
            question=query,
        )

    @classmethod
    def assemble_full_text(cls, sections: PromptSections) -> str:
        """Combine PromptSections into a single unified Markdown text block."""
        parts = [
            f"=== SYSTEM CONTEXT ===\n{sections.system_context}\n",
            f"=== CASE SUMMARY ===\n{sections.case_summary}\n",
            f"=== VICTIMS ===\n{sections.victims}\n",
            f"=== ACCUSED ===\n{sections.accused}\n",
            f"=== EVIDENCE ===\n{sections.evidence}\n",
            f"=== TIMELINE & PROCEEDINGS ===\n{sections.timeline}\n",
            f"=== LEGAL & CHARGESHEET ===\n{sections.legal}\n",
            f"=== INVESTIGATION QUESTION ===\n{sections.question}",
        ]
        return "\n".join(parts)
