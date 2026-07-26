from .workflow_models import WorkflowResult
class WorkflowEngine:
    def __init__(self, coordinator, registry=None): self.coordinator = coordinator; from .workflow_registry import WorkflowRegistry; self.registry = registry or WorkflowRegistry(); self.history = []
    def execute(self, workflow):
        self.registry.add(workflow); plan, responses, context = self.coordinator.execute(workflow.request); workflow.plan = plan
        result = WorkflowResult(workflow_id=workflow.workflow_id, responses=responses, cancelled=context.cancelled); self.history.append(result); return result
