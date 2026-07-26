from pydantic import BaseModel, Field
from uuid import uuid4
from app.ai.base.agent_models import AgentRequest, ExecutionPlan, AgentResponse
class Workflow(BaseModel): workflow_id: str = Field(default_factory=lambda: f'workflow-{uuid4().hex}'); name: str; request: AgentRequest; plan: ExecutionPlan | None = None
class WorkflowResult(BaseModel): workflow_id: str; responses: list[AgentResponse] = Field(default_factory=list); cancelled: bool = False
