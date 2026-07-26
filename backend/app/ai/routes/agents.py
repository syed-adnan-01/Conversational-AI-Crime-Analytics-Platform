"""Additive REST API for the Coordinator-based investigation system."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.ai.base.agent_models import AgentRequest
from app.ai.base.registry import AgentRegistry
from app.ai.communication.message_bus import MessageBus
from app.ai.coordinator.coordinator import AgentCoordinator
from app.ai.supervisor.supervisor_agent import SupervisorAgent
from app.ai.orchestration.workflow_engine import WorkflowEngine
from app.ai.orchestration.workflow_models import Workflow
from app.ai.evidence.evidence_agent import EvidenceAgent
from app.ai.timeline.timeline_agent import TimelineAgent
from app.ai.legal.legal_agent import LegalAgent
from app.ai.search.search_agent import SearchAgent
from app.ai.graph.graph_agent import KnowledgeGraphAgent
from app.ai.prediction.prediction_agent import PredictionAgent
from app.ai.reporting.report_agent import ReportAgent
from app.ai.analytics.analytics_agent import AnalyticsAgent

router = APIRouter()
_bus = MessageBus(); _registry = AgentRegistry()
for _agent in (EvidenceAgent(bus=_bus), TimelineAgent(bus=_bus), LegalAgent(bus=_bus), SearchAgent(bus=_bus), KnowledgeGraphAgent(bus=_bus), PredictionAgent(bus=_bus), ReportAgent(bus=_bus), AnalyticsAgent(bus=_bus)): _registry.register(_agent)
_coordinator = AgentCoordinator(_registry, bus=_bus); _supervisor = SupervisorAgent(_coordinator); _workflows = WorkflowEngine(_coordinator)
class WorkflowRequest(BaseModel): name: str = 'investigation'; request: AgentRequest
@router.post('/execute')
def execute(body: AgentRequest, current_user: User = Depends(get_current_user)): return _supervisor.investigate(body)
@router.post('/workflow')
def workflow(body: WorkflowRequest, current_user: User = Depends(get_current_user)): return _workflows.execute(Workflow(name=body.name, request=body.request))
@router.get('/agents')
def agents(current_user: User = Depends(get_current_user)): return [agent.health() for agent in _registry.all()]
@router.get('/capabilities')
def capabilities(current_user: User = Depends(get_current_user)): return _registry.capabilities()
@router.get('/health')
def health(): return {'status': 'healthy', 'agents': [agent.health() for agent in _registry.all()]}
@router.get('/metrics')
def metrics(current_user: User = Depends(get_current_user)): return _coordinator.metrics.snapshot()
@router.get('/workflows')
def workflows(current_user: User = Depends(get_current_user)): return _workflows.registry.all()
