"""REST endpoints for the additive Crime Knowledge Graph."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.ai.entities.entity_models import EntityRecord
from app.ai.graph_engine.graph_models import GraphSearchRequest
from app.ai.graph_engine.graph_service import GraphService
from app.ai.visualization.graph_export import GraphExporter

router = APIRouter()
_service = GraphService()
_exporter = GraphExporter()

class BuildRequest(BaseModel): case_id: str; refresh: bool = False
class CaseRequest(BaseModel): case_id: str
class ExpandRequest(CaseRequest): entity_id: str; depth: int = Field(default=1, ge=0, le=10)
class SearchRequest(CaseRequest): search: GraphSearchRequest
class ResolveRequest(BaseModel): entities: list[EntityRecord]

@router.post('/build')
def build(body: BuildRequest, current_user: User = Depends(get_current_user)): return _service.build(body.case_id, body.refresh)
@router.post('/search')
def search(body: SearchRequest, current_user: User = Depends(get_current_user)): return _service.search(body.case_id, body.search)
@router.post('/resolve')
def resolve(body: ResolveRequest, current_user: User = Depends(get_current_user)): return _service.resolve(body.entities)
@router.post('/community')
def community(body: CaseRequest, current_user: User = Depends(get_current_user)): return _service.community(body.case_id)
@router.post('/link-prediction')
def link_prediction(body: CaseRequest, current_user: User = Depends(get_current_user)): return _service.link_predictions(body.case_id)
@router.post('/expand')
def expand(body: ExpandRequest, current_user: User = Depends(get_current_user)): return _service.expand(body.case_id, body.entity_id, body.depth)
@router.get('/case/{case_id}')
def case_graph(case_id: str, format: str | None = None, current_user: User = Depends(get_current_user)):
    graph = _service.build(case_id)
    return _exporter.cytoscape(graph) if format == 'cytoscape' else _exporter.reactflow(graph) if format == 'reactflow' else graph
@router.get('/entity/{entity_id}')
def entity(entity_id: str, current_user: User = Depends(get_current_user)):
    result = _service.entity(entity_id)
    if not result: raise HTTPException(404, 'Entity not found; build its case graph first')
    return result
@router.get('/statistics')
def statistics(case_id: str | None = None, current_user: User = Depends(get_current_user)): return _service.statistics(case_id)
@router.get('/health')
def health(): return _service.health()
