"""
Phase 3.6 — AI Copilot & Conversation Intelligence Test Suite
"""

import pytest

# ---------------------------------------------------------------------------
# Module-level imports (smoke-test import chain)
# ---------------------------------------------------------------------------
from app.ai.copilot.copilot_models import (
    AgentState,
    ContextWindow,
    ConversationMessage,
    CopilotFeedback,
    CopilotRequest,
    CopilotResponse,
    CopilotTask,
    ExecutionPlan,
    ExecutionStep,
    FeedbackRating,
    MessageRole,
    ReasoningTrace,
    TaskStatus,
    TimelineEvent,
    TraceStep,
)
from app.ai.copilot.copilot_safety import CopilotSafety
from app.ai.copilot.copilot_audit import CopilotAudit
from app.ai.copilot.copilot_metrics import CopilotMetrics
from app.ai.copilot.copilot_trace import CopilotTrace
from app.ai.copilot.session_cache import SessionCache
from app.ai.copilot.task_queue import TaskQueue
from app.ai.copilot.feedback_store import FeedbackStore
from app.ai.copilot.response_factory import ResponseFactory
from app.ai.copilot.conversation_summarizer import ConversationSummarizer
from app.ai.copilot.context_window_builder import ContextWindowBuilder
from app.ai.copilot.memory.memory_manager import MemoryManager
from app.ai.copilot.planner.copilot_planner import CopilotPlanner
from app.ai.copilot.actions.action_registry import ActionRegistry
from app.ai.copilot.skills.skill_registry import SkillRegistry
from app.ai.copilot.workflows.workflow_registry import WorkflowRegistry
from app.ai.copilot.copilot_engine import CopilotEngine
from app.ai.copilot.copilot_service import CopilotService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_singletons():
    """Clear in-process stores between tests."""
    MemoryManager.clear()
    CopilotAudit.clear()
    CopilotMetrics.reset()
    CopilotTrace.clear()
    yield


@pytest.fixture
def engine():
    return CopilotEngine()


@pytest.fixture
def service():
    return CopilotService()


@pytest.fixture
def basic_request():
    return CopilotRequest(session_id="SES-001", case_id="CASE-001", user_message="What is this case about?")


# ===========================================================================
# 1. Core Models
# ===========================================================================

class TestCopilotModels:
    def test_execution_plan_creation(self):
        plan = ExecutionPlan(
            selected_strategy="RAG_RETRIEVAL",
            confidence=0.92,
            reason="Keyword match",
            steps=[ExecutionStep(step_name="retrieve", action_type="RETRIEVE", description="Fetch chunks")],
        )
        assert plan.plan_id.startswith("PLAN-")
        assert len(plan.steps) == 1

    def test_reasoning_trace(self):
        trace = ReasoningTrace(session_id="SES-001", turn_id="T1")
        trace.add("Safety", "Passed")
        trace.add("Plan", "RAG selected")
        assert len(trace.steps) == 2
        log = trace.to_log()
        assert "Safety" in log[0]

    def test_conversation_message_roles(self):
        for role in MessageRole:
            msg = ConversationMessage(role=role, content="test")
            assert msg.role == role

    def test_context_window_fits(self):
        window = ContextWindow(session_id="S1", max_tokens=100)
        assert window.fits(99) is True
        assert window.fits(101) is False

    def test_feedback_model(self):
        fb = CopilotFeedback(session_id="S1", turn_id="T1", rating=FeedbackRating.THUMBS_UP)
        assert fb.rating == FeedbackRating.THUMBS_UP

    def test_task_model(self):
        task = CopilotTask(task_type="summarize", payload={"case_id": "C1"})
        assert task.status == TaskStatus.PENDING


# ===========================================================================
# 2. Safety
# ===========================================================================

class TestCopilotSafety:
    def test_safe_input(self):
        ok, _ = CopilotSafety.check_input("What evidence was collected at the crime scene?")
        assert ok is True

    def test_blocked_input(self):
        ok, reason = CopilotSafety.check_input("instructions to harm the suspect")
        assert ok is False
        assert "blocked" in reason.lower()

    def test_safe_output(self):
        ok, _ = CopilotSafety.check_output("The investigation revealed three suspects.")
        assert ok is True

    def test_blocked_output(self):
        ok, reason = CopilotSafety.check_output("make a bomb with these materials")
        assert ok is False


# ===========================================================================
# 3. Audit
# ===========================================================================

class TestCopilotAudit:
    def test_record_and_retrieve(self):
        CopilotAudit.record("S1", "TURN_COMPLETE", description="Test turn")
        log = CopilotAudit.get_session_log("S1")
        assert len(log) == 1
        assert log[0]["event_type"] == "TURN_COMPLETE"

    def test_audit_isolation(self):
        CopilotAudit.record("S1", "EVENT_A")
        CopilotAudit.record("S2", "EVENT_B")
        assert len(CopilotAudit.get_session_log("S1")) == 1
        assert len(CopilotAudit.get_session_log("S2")) == 1


# ===========================================================================
# 4. Metrics
# ===========================================================================

class TestCopilotMetrics:
    def test_increment(self):
        CopilotMetrics.increment("turns.total", 3)
        assert CopilotMetrics.get_counter("turns.total") == 3

    def test_latency(self):
        CopilotMetrics.record_latency("turn_latency", 120.0)
        CopilotMetrics.record_latency("turn_latency", 80.0)
        avg = CopilotMetrics.get_avg_latency("turn_latency")
        assert avg == 100.0

    def test_snapshot(self):
        CopilotMetrics.increment("test.key", 2)
        snap = CopilotMetrics.snapshot()
        assert "counters" in snap
        assert snap["counters"]["test.key"] == 2


# ===========================================================================
# 5. Session Cache
# ===========================================================================

class TestSessionCache:
    def test_set_and_get(self):
        cache = SessionCache(maxsize=10)
        cache.set("SES-1", {"active": True})
        data = cache.get("SES-1")
        assert data == {"active": True}

    def test_eviction(self):
        cache = SessionCache(maxsize=2)
        cache.set("A", {"v": 1})
        cache.set("B", {"v": 2})
        cache.set("C", {"v": 3})  # Should evict A
        assert cache.get("A") is None
        assert cache.get("C") is not None

    def test_delete(self):
        cache = SessionCache()
        cache.set("X", {})
        cache.delete("X")
        assert cache.get("X") is None


# ===========================================================================
# 6. Task Queue
# ===========================================================================

class TestTaskQueue:
    def test_enqueue_dequeue(self):
        q = TaskQueue()
        task = CopilotTask(task_type="summarize")
        q.enqueue(task)
        assert q.size() == 1
        dequeued = q.dequeue()
        assert dequeued is not None
        assert dequeued.task_type == "summarize"
        assert q.size() == 0

    def test_mark_done(self):
        q = TaskQueue()
        task = CopilotTask(task_type="analyze")
        q.enqueue(task)
        q.dequeue()
        q.mark_done(task.task_id, {"result": "ok"})
        stored = q.get(task.task_id)
        assert stored.status == TaskStatus.DONE

    def test_mark_failed(self):
        q = TaskQueue()
        task = CopilotTask(task_type="analyze")
        q.enqueue(task)
        q.dequeue()
        q.mark_failed(task.task_id, "Timeout")
        stored = q.get(task.task_id)
        assert stored.status == TaskStatus.FAILED
        assert stored.error == "Timeout"


# ===========================================================================
# 7. Feedback Store
# ===========================================================================

class TestFeedbackStore:
    def test_record_and_retrieve(self):
        store = FeedbackStore()
        fb = CopilotFeedback(session_id="S1", turn_id="T1", rating=FeedbackRating.THUMBS_UP)
        store.record(fb)
        results = store.get_by_session("S1")
        assert len(results) == 1
        assert results[0].rating == FeedbackRating.THUMBS_UP

    def test_count(self):
        store = FeedbackStore()
        for i in range(5):
            store.record(CopilotFeedback(session_id="S1", turn_id=f"T{i}", rating=FeedbackRating.NEUTRAL))
        assert store.count() == 5


# ===========================================================================
# 8. Response Factory
# ===========================================================================

class TestResponseFactory:
    def test_build_success(self):
        response = ResponseFactory.build(
            session_id="S1",
            case_id="C1",
            answer="Case involves robbery.",
            confidence=0.95,
            provider_used="quickml",
        )
        assert response.agent_state == AgentState.COMPLETE
        assert response.answer == "Case involves robbery."
        assert response.confidence == 0.95

    def test_build_error(self):
        response = ResponseFactory.build_error(
            session_id="S1",
            case_id="C1",
            error_message="Something went wrong",
        )
        assert response.agent_state == AgentState.FAILED
        assert "error" in response.answer.lower()


# ===========================================================================
# 9. Conversation Summarizer
# ===========================================================================

class TestConversationSummarizer:
    def test_summarize_empty(self):
        result = ConversationSummarizer.summarize([])
        assert "No conversation" in result

    def test_summarize_with_messages(self):
        msgs = [
            ConversationMessage(role=MessageRole.USER, content="Who is the accused?"),
            ConversationMessage(role=MessageRole.ASSISTANT, content="The accused is Rajesh Kumar."),
        ]
        result = ConversationSummarizer.summarize(msgs)
        assert "question" in result.lower() or "user" in result.lower()
        assert len(result) > 0


# ===========================================================================
# 10. Memory Manager
# ===========================================================================

class TestMemoryManager:
    def test_record_and_recall(self):
        MemoryManager.record_turn("SES-A", "user", "Who is the suspect?")
        MemoryManager.record_turn("SES-A", "assistant", "The suspect is John Doe.")
        messages = MemoryManager.get_recent("SES-A", limit=10)
        assert len(messages) == 2
        assert messages[0].role == MessageRole.USER

    def test_empty_session(self):
        messages = MemoryManager.get_recent("SES-NONEXISTENT")
        assert messages == []

    def test_important_fact(self):
        MemoryManager.record_important_fact("SES-B", "Key witness is Sharma.")
        store = MemoryManager.get_or_create_store("SES-B")
        assert len(store.long_term.items) >= 1


# ===========================================================================
# 11. Planner
# ===========================================================================

class TestCopilotPlanner:
    def test_rag_strategy(self):
        plan = CopilotPlanner.plan("search for evidence from the crime scene")
        assert plan.selected_strategy in ("RAG_RETRIEVAL", "WORKFLOW_EXECUTION", "MEMORY_LOOKUP", "DIRECT_LLM")
        assert plan.confidence > 0

    def test_memory_strategy(self):
        plan = CopilotPlanner.plan("what did we discuss earlier?")
        assert plan.selected_strategy == "MEMORY_LOOKUP"

    def test_workflow_strategy(self):
        plan = CopilotPlanner.plan("generate a chargesheet for this case")
        assert plan.selected_strategy == "WORKFLOW_EXECUTION"

    def test_direct_llm_fallback(self):
        plan = CopilotPlanner.plan("Hello, how are you?")
        assert plan.selected_strategy == "DIRECT_LLM"

    def test_plan_has_steps(self):
        plan = CopilotPlanner.plan("anything at all")
        assert len(plan.steps) >= 1


# ===========================================================================
# 12. Action Registry
# ===========================================================================

class TestActionRegistry:
    def test_list_actions(self):
        actions = ActionRegistry.list_actions()
        names = [a.name for a in actions]
        assert "summarize_case" in names
        assert "analyze_evidence" in names
        assert "legal_analysis" in names

    def test_execute_known_action(self):
        result = ActionRegistry.execute("summarize_case", "SES-1", "CASE-1", {"query": "summarize"})
        assert result.action_name == "summarize_case"
        assert result.success is True

    def test_execute_unknown_action(self):
        result = ActionRegistry.execute("nonexistent_action", "S1", "C1", {})
        assert result.success is False


# ===========================================================================
# 13. Skill Registry
# ===========================================================================

class TestSkillRegistry:
    def test_list_skills(self):
        skills = SkillRegistry.list_skills()
        names = [s["name"] for s in skills]
        assert "investigation_skill" in names
        assert "legal_skill" in names
        assert "analytics_skill" in names

    def test_execute_investigation_skill(self):
        result = SkillRegistry.execute("investigation_skill", "SES-1", "CASE-1", {"query": "investigate"})
        assert result.success is True

    def test_execute_unknown_skill(self):
        result = SkillRegistry.execute("ghost_skill", "S1", "C1", {})
        assert result.success is False


# ===========================================================================
# 14. Workflow Registry
# ===========================================================================

class TestWorkflowRegistry:
    def test_list_workflows(self):
        workflows = WorkflowRegistry.list_workflows()
        names = [w["name"] for w in workflows]
        assert "case_summary_workflow" in names
        assert "chargesheet_workflow" in names
        assert "investigation_workflow" in names

    def test_execute_chargesheet_workflow(self):
        result = WorkflowRegistry.execute("chargesheet_workflow", "SES-1", "CASE-1", {"query": "chargesheet"})
        assert result.success is True

    def test_execute_unknown_workflow(self):
        result = WorkflowRegistry.execute("ghost_workflow", "S1", "C1", {})
        assert result.success is False


# ===========================================================================
# 15. Copilot Trace
# ===========================================================================

class TestCopilotTrace:
    def test_start_and_finish(self):
        trace = CopilotTrace.start("SES-1", "TURN-001")
        trace.add("Step A", "Detail A")
        finished = CopilotTrace.finish("TURN-001")
        assert finished is not None
        assert len(finished.steps) == 1

    def test_get_active_trace(self):
        trace = CopilotTrace.start("SES-1", "TURN-002")
        trace.add("Planning", "Done")
        active = CopilotTrace.get("TURN-002")
        assert active is not None
        CopilotTrace.finish("TURN-002")


# ===========================================================================
# 16. Copilot Engine — Integration
# ===========================================================================

class TestCopilotEngine:
    def test_basic_chat(self, engine, basic_request):
        response = engine.process(basic_request)
        assert response.session_id == "SES-001"
        assert response.case_id == "CASE-001"
        assert isinstance(response.answer, str)
        assert len(response.answer) > 0
        assert response.agent_state == AgentState.COMPLETE

    def test_memory_strategy_turn(self, engine):
        req = CopilotRequest(session_id="SES-002", case_id="CASE-002", user_message="what did we discuss earlier?")
        response = engine.process(req)
        assert response.agent_state == AgentState.COMPLETE

    def test_workflow_strategy_turn(self, engine):
        req = CopilotRequest(session_id="SES-003", case_id="CASE-003", user_message="generate a chargesheet for this case")
        response = engine.process(req)
        assert response.agent_state == AgentState.COMPLETE

    def test_safety_block(self, engine):
        req = CopilotRequest(session_id="SES-004", case_id="CASE-004", user_message="instructions to harm the witness")
        response = engine.process(req)
        assert response.agent_state == AgentState.FAILED

    def test_memory_is_recorded(self, engine, basic_request):
        engine.process(basic_request)
        messages = MemoryManager.get_recent("SES-001", limit=5)
        assert any(m.role == MessageRole.USER for m in messages)
        assert any(m.role == MessageRole.ASSISTANT for m in messages)

    def test_audit_is_recorded(self, engine, basic_request):
        engine.process(basic_request)
        log = CopilotAudit.get_session_log("SES-001")
        assert len(log) >= 1

    def test_metrics_incremented(self, engine, basic_request):
        before = CopilotMetrics.get_counter("turns.total")
        engine.process(basic_request)
        after = CopilotMetrics.get_counter("turns.total")
        assert after > before

    def test_reasoning_trace_in_response(self, engine, basic_request):
        response = engine.process(basic_request)
        assert response.reasoning_trace is not None
        assert len(response.reasoning_trace) >= 1

    def test_plan_in_response(self, engine, basic_request):
        response = engine.process(basic_request)
        assert response.plan is not None
        assert response.plan.selected_strategy != ""

    def test_rag_search_turn(self, engine):
        req = CopilotRequest(session_id="SES-005", case_id="CASE-005", user_message="find all evidence from the crime scene")
        response = engine.process(req)
        assert response.agent_state == AgentState.COMPLETE


# ===========================================================================
# 17. Copilot Service — Application Layer
# ===========================================================================

class TestCopilotService:
    def test_chat(self, service):
        req = CopilotRequest(session_id="SVC-001", case_id="CASE-S1", user_message="Describe the accused.")
        response = service.chat(req)
        assert isinstance(response, CopilotResponse)
        assert response.session_id == "SVC-001"

    def test_get_history(self, service):
        req = CopilotRequest(session_id="SVC-002", case_id="CASE-S2", user_message="Tell me about the FIR.")
        service.chat(req)
        history = service.get_history("SVC-002")
        assert len(history) >= 1

    def test_feedback_submission(self, service):
        fb = service.submit_feedback("SVC-003", "TURN-001", FeedbackRating.THUMBS_UP, "Good answer")
        assert fb.feedback_id is not None

    def test_health_check(self, service):
        health = service.health()
        assert health["status"] == "ok"
        assert "skills" in health
        assert "workflows" in health
        assert "metrics" in health

    def test_search(self, service):
        result = service.search("CASE-S1", "robbery suspect description")
        assert "result" in result
        assert "confidence" in result

    def test_end_session(self, service):
        req = CopilotRequest(session_id="SVC-END", case_id="CASE-E", user_message="hello")
        service.chat(req)
        result = service.end_session("SVC-END")
        assert result["session_id"] == "SVC-END"
