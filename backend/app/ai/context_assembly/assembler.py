"""
============================================================
Context Assembler
============================================================

Module  : AI Context Assembly Subsystem
Purpose : Orchestrates prompt context formatting, token budgeting,
          provenance generation, and final RetrievalContext assembly.
"""

import hashlib
import uuid
from datetime import datetime
from typing import Optional

from app.ai.context_assembly.context_window import ContextWindow
from app.ai.context_assembly.prompt_budget_manager import PromptBudgetManager
from app.ai.context_assembly.prompt_context import PromptContextFormatter
from app.ai.retrieval.exceptions import ContextAssemblyException
from app.ai.retrieval.retrieval_models import (
    PromptProvenance,
    RetrievalContext,
    RetrievalStatistics,
    RetrievedChunk,
)


class ContextAssembler:
    """
    Assembler merging retrieved chunks into versioned, token-budgeted RetrievalContext objects.
    """

    @classmethod
    def assemble(
        cls,
        query: str,
        chunks: list[RetrievedChunk],
        max_token_budget: int = 4096,
        statistics: Optional[RetrievalStatistics] = None,
        query_id: Optional[str] = None,
        retrieval_id: Optional[str] = None,
    ) -> RetrievalContext:
        try:
            q_id = query_id or f"Q-{uuid.uuid4().hex[:8]}"
            r_id = retrieval_id or f"RET-{uuid.uuid4().hex[:8]}"

            # 1. Allocate token budget
            budgeted_chunks, _, _ = PromptBudgetManager.allocate_budget(chunks, max_token_budget)

            # 2. Format sections
            sections = PromptContextFormatter.format_sections(query, budgeted_chunks)

            # 3. Assemble full text
            full_text = PromptContextFormatter.assemble_full_text(sections)
            total_tokens = ContextWindow.estimate_tokens(full_text)

            # 4. Generate context hash
            context_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()

            # 5. Create provenance metadata
            provenance = PromptProvenance(
                query_id=q_id,
                retrieval_id=r_id,
                chunk_ids=[c.chunk_id for c in budgeted_chunks],
                generated_at=datetime.now(),
                context_hash=context_hash,
            )

            # Update statistics if provided
            stats = statistics or RetrievalStatistics()
            stats.token_count = total_tokens
            stats.chunks_returned = len(budgeted_chunks)

            return RetrievalContext(
                version="1.0.0",
                query=query,
                assembled_text=full_text,
                sections=sections,
                chunks=budgeted_chunks,
                token_count=total_tokens,
                max_token_budget=max_token_budget,
                provenance=provenance,
                statistics=stats,
            )

        except Exception as exc:
            raise ContextAssemblyException(str(exc)) from exc
