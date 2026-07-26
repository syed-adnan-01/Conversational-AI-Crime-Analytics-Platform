"""
Pipeline stages execution logic for AI Orchestrator.
"""

import time
import uuid
from sqlalchemy.orm import Session

from app.ai.llm.llm_models import LLMRequest
from app.ai.llm.llm_service import LLMService
from app.ai.orchestrator.workflow import OrchestrationRequest, OrchestrationResult
from app.ai.prompting.prompt_models import PromptRequest
from app.ai.prompting.prompt_service import PromptService
from app.ai.retrieval.retrieval_models import SearchQuery
from app.ai.retrieval.retrieval_pipeline import RetrievalPipeline


class OrchestrationPipeline:
    """Executes Retrieval -> Prompt Builder -> LLM Gateway sequence."""

    @classmethod
    def execute(cls, db: Session, request: OrchestrationRequest) -> OrchestrationResult:
        start = time.time()
        orchestration_id = f"ORCH-{uuid.uuid4().hex[:8]}"

        # Step 1: Retrieval Engine
        retrieval_query = SearchQuery(query_text=request.query, top_k=5)
        retrieval_ctx = RetrievalPipeline.run(
            db=db, case_id=request.case_id, query=retrieval_query
        )

        # Step 2: Prompt Engine
        prompt_req = PromptRequest(
            retrieval_context=retrieval_ctx,
            user_query=request.query,
            persona=request.persona,
            conversation_id=request.conversation_id,
            output_schema=request.output_schema,
        )
        prompt_resp = PromptService.build_prompt(prompt_req)

        # Step 3: LLM Gateway
        llm_req = LLMRequest(
            prompt_response=prompt_resp,
            prompt=prompt_resp.assembled_prompt,
            provider=request.provider,
            response_schema=request.output_schema or prompt_resp.output_schema,
            conversation_id=request.conversation_id,
        )
        llm_resp = LLMService.generate(llm_req)

        latency = round((time.time() - start) * 1000, 2)

        return OrchestrationResult(
            orchestration_id=orchestration_id,
            case_id=request.case_id,
            query=request.query,
            prompt_response=prompt_resp,
            llm_response=llm_resp,
            parsed_output=llm_resp.parsed_output,
            execution_time_ms=latency,
        )
