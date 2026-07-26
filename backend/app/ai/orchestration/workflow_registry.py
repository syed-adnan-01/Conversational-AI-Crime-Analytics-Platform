class WorkflowRegistry:
    def __init__(self): self._workflows = {}
    def add(self, workflow): self._workflows[workflow.workflow_id] = workflow
    def all(self): return list(self._workflows.values())
