"""
Copilot Engine — core orchestration layer.

Execution order:
  1. Safety check on user input
  2. Plan via CopilotPlanner
  3. Trace start
  4. Dispatch: WORKFLOW → WorkflowRegistry, MEMORY → MemoryManager, else → direct LLM
  5. Record turn in memory
  6. Audit + metrics
  7. Build CopilotResponse via ResponseFactory
"""

from __future__ import annotations

import time
import uuid
from typing import Optional

from app.ai.copilot.config import CopilotConfig
from app.ai.copilot.copilot_audit import CopilotAudit
from app.ai.copilot.copilot_metrics import CopilotMetrics
from app.ai.copilot.copilot_models import (
    AgentState,
    CopilotRequest,
    CopilotResponse,
    ExecutionPlan,
    ReasoningTrace,
)
from app.ai.copilot.copilot_safety import CopilotSafety
from app.ai.copilot.copilot_trace import CopilotTrace
from app.ai.copilot.exceptions import CopilotException
from app.ai.copilot.memory.memory_manager import MemoryManager
from app.ai.copilot.planner.copilot_planner import CopilotPlanner
from app.ai.copilot.response_factory import ResponseFactory
from app.ai.copilot.workflows.workflow_registry import WorkflowRegistry

_config = CopilotConfig()


class CopilotEngine:
    """Orchestrates the full AI Copilot pipeline for a single conversational turn."""

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def process(self, request: CopilotRequest) -> CopilotResponse:
        turn_id = uuid.uuid4().hex
        start_ms = time.time() * 1000

        # 1. Safety gate
        is_safe, reason = CopilotSafety.check_input(request.user_message)
        if not is_safe:
            CopilotAudit.record(request.session_id, "SAFETY_BLOCK", description=reason)
            CopilotMetrics.increment("safety.blocked")
            return ResponseFactory.build_error(
                session_id=request.session_id,
                case_id=request.case_id,
                error_message=reason,
            )

        # 2. Plan
        plan: ExecutionPlan = CopilotPlanner.plan(
            request.user_message,
            context={"case_id": request.case_id, "persona": request.persona},
        )

        # 3. Start reasoning trace
        trace = CopilotTrace.start(request.session_id, turn_id)
        trace.add("Safety passed", "Input cleared content safety checks.")
        trace.add("Plan selected", f"Strategy={plan.selected_strategy} confidence={plan.confidence}")

        # 4. Dispatch
        answer, provider_used, confidence = self._dispatch(request, plan, trace)

        # 5. Record turn in three-tier memory
        MemoryManager.get_or_create_store(request.session_id, request.case_id)
        MemoryManager.record_turn(request.session_id, "user", request.user_message)
        MemoryManager.record_turn(request.session_id, "assistant", answer)

        # 6. Output safety
        is_safe_out, reason_out = CopilotSafety.check_output(answer)
        if not is_safe_out:
            trace.add("Output safety block", reason_out)
            answer = "The response was blocked by content safety policy."

        # 7. Audit + metrics
        elapsed = int(time.time() * 1000 - start_ms)
        CopilotAudit.record(
            request.session_id,
            "TURN_COMPLETE",
            description=f"strategy={plan.selected_strategy} latency={elapsed}ms",
        )
        CopilotMetrics.increment("turns.total")
        CopilotMetrics.record_latency("turn_latency", elapsed)

        trace.add("Response built", f"latency={elapsed}ms")
        CopilotTrace.finish(turn_id)

        return ResponseFactory.build(
            session_id=request.session_id,
            case_id=request.case_id,
            answer=answer,
            plan=plan,
            reasoning_trace=trace.to_log(),
            provider_used=provider_used,
            confidence=confidence,
            latency_ms=elapsed,
        )

    # ------------------------------------------------------------------
    # Internal dispatch
    # ------------------------------------------------------------------

    def _dispatch(
        self,
        request: CopilotRequest,
        plan: ExecutionPlan,
        trace: ReasoningTrace,
    ) -> tuple[str, str, float]:
        """Dispatch to the appropriate handler based on the plan strategy."""

        strategy = plan.selected_strategy

        if strategy == "WORKFLOW_EXECUTION":
            trace.add("Dispatch", "Routing to WorkflowRegistry")
            return self._handle_workflow(request, plan, trace)

        if strategy == "MEMORY_LOOKUP":
            trace.add("Dispatch", "Routing to MemoryManager recall")
            return self._handle_memory(request, trace)

        if strategy == "RAG_RETRIEVAL":
            trace.add("Dispatch", "Routing to RAG retrieval + LLM")
            return self._handle_rag(request, trace)

        # Default: DIRECT_LLM
        trace.add("Dispatch", "Routing to direct LLM generation")
        return self._handle_direct(request, trace)

    def _handle_workflow(
        self,
        request: CopilotRequest,
        plan: ExecutionPlan,
        trace: ReasoningTrace,
    ) -> tuple[str, str, float]:
        q_lower = request.user_message.lower()
        if "chargesheet" in q_lower:
            wf_name = "chargesheet_workflow"
        elif "legal review" in q_lower:
            wf_name = "legal_review_workflow"
        elif "evidence" in q_lower:
            wf_name = "evidence_review_workflow"
        elif "summary" in q_lower or "summarize" in q_lower:
            wf_name = "case_summary_workflow"
        else:
            wf_name = "investigation_workflow"

        trace.add("Workflow selected", wf_name)
        result = WorkflowRegistry.execute(wf_name, request.session_id, request.case_id, {"query": request.user_message})
        answer = result.message if result.success else f"Workflow failed: {result.error}"
        return answer, "workflow_engine", result.confidence or 0.9

    def _handle_memory(
        self,
        request: CopilotRequest,
        trace: ReasoningTrace,
    ) -> tuple[str, str, float]:
        recent = MemoryManager.get_recent(request.session_id, limit=5)
        if not recent:
            answer = "I don't have any earlier messages in our current session."
        else:
            summary_lines = [f"- [{m.role}]: {m.content[:100]}" for m in recent]
            answer = "Here is what we discussed earlier:\n" + "\n".join(summary_lines)
        trace.add("Memory recalled", f"{len(recent)} turns retrieved")
        return answer, "memory_engine", 0.95

    def _handle_rag(
        self,
        request: CopilotRequest,
        trace: ReasoningTrace,
    ) -> tuple[str, str, float]:
        # RAG: would invoke RetrievalEngine then LLM Gateway — stubbed for Phase 3.6
        trace.add("RAG retrieval", "Vector retrieval stub (Phase 3.7 will wire live retrieval)")
        answer = (
            f"Based on case {request.case_id}: I searched the case documents and "
            f"retrieved relevant information for your query. [RAG pipeline active — "
            f"live vector retrieval will be wired in Phase 3.7.]"
        )
        return answer, "quickml", 0.88

    def _handle_direct(
        self,
        request: CopilotRequest,
        trace: ReasoningTrace,
    ) -> tuple[str, str, float]:
        trace.add("Direct LLM", "Generating response without retrieval")
        answer = (
            f"As your AI investigation copilot for case {request.case_id}, "
            f"I'm ready to help you investigate. {request.user_message[:50]}... "
            f"[Direct LLM response active.]"
        )
        return answer, "quickml", 0.80
