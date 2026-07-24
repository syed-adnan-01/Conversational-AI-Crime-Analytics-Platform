"""
============================================================
Section Chunk Strategy
============================================================

Module  : AI Chunking Engine
Purpose : Chunks InvestigationContext by domain entity boundaries
          (Case, Complainant, Victims, Accused, Sections, Evidence, etc.).
"""

from app.ai.chunking.chunk_models import ChunkMetadata, ChunkType, ContextChunk
from app.ai.chunking.strategies.base import BaseChunkStrategy
from app.ai.context.context_models import InvestigationContext


class SectionChunkStrategy(BaseChunkStrategy):
    """
    Entity-boundary chunking strategy. Creates distinct, structured chunks
    for each domain entity within an InvestigationContext while maintaining
    parent entity relationships and metadata.
    """

    def build_chunks(self, context: InvestigationContext) -> list[ContextChunk]:
        chunks: list[ContextChunk] = []
        case_id = context.metadata.case_id
        context_hash = context.metadata.context_hash
        chunk_idx = 0

        # 1. CASE HEADER CHUNK
        c_case = context.case
        case_text = (
            f"CASE MASTER: FIR No. {c_case.crime_no}. "
            f"Case No: {c_case.case_no or 'N/A'}. "
            f"Registered Date: {c_case.crime_registered_date}. "
            f"Status: {context.summary.status}. "
            f"Lead Officer: {context.summary.lead_officer or 'Unassigned'}."
        )
        case_chunk = ContextChunk(
            chunk_id=f"CHUNK-{case_id}-CASE-{chunk_idx}",
            case_id=case_id,
            context_hash=context_hash,
            chunk_index=chunk_idx,
            chunk_type=ChunkType.CASE,
            parent_entity_id=case_id,
            parent_chunk_id=None,
            content=case_text,
            token_estimate=len(case_text.split()),
            metadata=ChunkMetadata(
                entity_type="CaseMaster",
                entity_id=case_id,
                created_at=c_case.crime_registered_date,
            ),
        )
        chunks.append(case_chunk)
        parent_case_chunk_id = case_chunk.chunk_id
        chunk_idx += 1

        # 2. COMPLAINANT CHUNK
        if context.complainant:
            comp = context.complainant
            comp_text = (
                f"COMPLAINANT: Name: {comp.name}. "
                f"Gender: {getattr(comp.gender, 'value', comp.gender) or 'N/A'}. "
                f"Age: {comp.age or 'N/A'}. Mobile: {comp.mobile_no or 'N/A'}. "
                f"Address: {comp.address or 'N/A'}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-COMP-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.COMPLAINANT,
                    parent_entity_id=comp.complainant_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=comp_text,
                    token_estimate=len(comp_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="Complainant",
                        entity_id=comp.complainant_id,
                        created_at=comp.created_at,
                    ),
                )
            )
            chunk_idx += 1

        # 3. VICTIMS CHUNKS
        for v in context.victims:
            vic_text = (
                f"VICTIM: Name: {v.name}. "
                f"Gender: {getattr(v.gender, 'value', v.gender) or 'N/A'}. "
                f"Age: {v.age or 'N/A'}. Mobile: {getattr(v, 'mobile_no', None) or 'N/A'}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-VIC-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.VICTIM,
                    parent_entity_id=v.victim_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=vic_text,
                    token_estimate=len(vic_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="Victim",
                        entity_id=v.victim_id,
                        created_at=v.created_at,
                    ),
                )
            )
            chunk_idx += 1

        # 4. ACCUSED CHUNKS
        for a in context.accused:
            acc_text = (
                f"ACCUSED: Name: {a.name}. "
                f"Alias: {getattr(a, 'alias', None) or 'N/A'}. "
                f"Mobile: {getattr(a, 'mobile_no', None) or 'N/A'}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-ACC-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.ACCUSED,
                    parent_entity_id=a.accused_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=acc_text,
                    token_estimate=len(acc_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="Accused",
                        entity_id=a.accused_id,
                        created_at=a.created_at,
                    ),
                )
            )
            chunk_idx += 1

        # 5. WITNESSES CHUNKS
        for w in context.witnesses:
            wit_text = (
                f"WITNESS: Name: {w.name}. "
                f"Gender: {getattr(w.gender, 'value', w.gender) or 'N/A'}. "
                f"Mobile: {w.mobile_no or 'N/A'}. "
                f"Statement: {getattr(w, 'statement', None) or 'N/A'}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-WIT-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.WITNESS,
                    parent_entity_id=w.witness_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=wit_text,
                    token_estimate=len(wit_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="Witness",
                        entity_id=w.witness_id,
                        created_at=w.created_at,
                    ),
                )
            )
            chunk_idx += 1

        # 6. SECTIONS CHUNKS
        for s in context.sections:
            sec_text = (
                f"APPLIED SECTION {s.section_number}: Title: {s.title}. "
                f"Description: {s.description or 'N/A'}. "
                f"Cognizable: {s.is_cognizable}. Bailable: {s.is_bailable}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-SEC-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.SECTION,
                    parent_entity_id=s.section_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=sec_text,
                    token_estimate=len(sec_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="Section",
                        entity_id=s.section_id,
                        section_number=s.section_number,
                        is_cognizable=s.is_cognizable,
                        is_bailable=s.is_bailable,
                        created_at=s.created_at,
                    ),
                )
            )
            chunk_idx += 1

        # 7. EVIDENCE CHUNKS
        for e in context.evidence:
            evi_text = (
                f"EVIDENCE [{e.evidence_number}]: Title: {e.title}. "
                f"Type: {getattr(e.evidence_type, 'value', e.evidence_type) or 'N/A'}. "
                f"Custody Status: {getattr(e, 'custody_status', None) or 'N/A'}. "
                f"Collected By: {e.collected_by}. Location: {e.storage_location}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-EVI-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.EVIDENCE,
                    parent_entity_id=e.evidence_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=evi_text,
                    token_estimate=len(evi_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="Evidence",
                        entity_id=e.evidence_id,
                        custody_status=str(getattr(e, 'custody_status', None) or 'N/A'),
                        created_at=e.created_at,
                    ),
                )
            )
            chunk_idx += 1

        # 8. ARREST CHUNKS
        for arr in context.arrests:
            arr_text = (
                f"ARREST: Accused ID: {arr.accused_id}. "
                f"Arrest Date: {arr.arrest_date}. Location: {getattr(arr, 'arrest_location', 'N/A')}. "
                f"Status: {getattr(arr.status, 'value', arr.status) or 'N/A'}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-ARR-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.ARREST,
                    parent_entity_id=arr.arrest_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=arr_text,
                    token_estimate=len(arr_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="Arrest",
                        entity_id=arr.arrest_id,
                        created_at=arr.created_at,
                    ),
                )
            )
            chunk_idx += 1

        # 9. CHARGESHEET CHUNKS
        for cs in context.chargesheets:
            cs_text = (
                f"CHARGESHEET [{cs.chargesheet_number}]: Filing Date: {cs.filing_date}. "
                f"Officer: {cs.investigating_officer}. Summary: {cs.summary}. "
                f"Status: {getattr(cs.status, 'value', cs.status) or 'N/A'}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-CS-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.CHARGESHEET,
                    parent_entity_id=cs.chargesheet_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=cs_text,
                    token_estimate=len(cs_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="Chargesheet",
                        entity_id=cs.chargesheet_id,
                        created_at=cs.created_at,
                    ),
                )
            )
            chunk_idx += 1

        # 10. COURT PROCEEDINGS CHUNKS
        for cp in context.court_proceedings:
            cp_text = (
                f"COURT PROCEEDING: Court: {cp.court_name}. Hearing Date: {cp.hearing_date}. "
                f"Stage: {getattr(cp.stage, 'value', cp.stage) or 'N/A'}. Summary: {cp.summary}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-CP-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.COURT,
                    parent_entity_id=cp.proceeding_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=cp_text,
                    token_estimate=len(cp_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="CourtProceeding",
                        entity_id=cp.proceeding_id,
                        hearing_date=cp.hearing_date,
                        created_at=cp.created_at,
                    ),
                )
            )
            chunk_idx += 1

        # 11. TIMELINE CHUNKS
        for te in context.timeline_events:
            te_text = (
                f"TIMELINE EVENT [{te.event_time}]: Title: {te.title}. "
                f"Type: {getattr(te.event_type, 'value', te.event_type) or 'N/A'}. Description: {te.description}."
            )
            chunks.append(
                ContextChunk(
                    chunk_id=f"CHUNK-{case_id}-TE-{chunk_idx}",
                    case_id=case_id,
                    context_hash=context_hash,
                    chunk_index=chunk_idx,
                    chunk_type=ChunkType.TIMELINE,
                    parent_entity_id=te.event_id,
                    parent_chunk_id=parent_case_chunk_id,
                    content=te_text,
                    token_estimate=len(te_text.split()),
                    metadata=ChunkMetadata(
                        entity_type="TimelineEvent",
                        entity_id=te.event_id,
                        created_at=te.created_at,
                    ),
                )
            )
            chunk_idx += 1

        return chunks
