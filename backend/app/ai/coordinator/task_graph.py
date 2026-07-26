class TaskGraph:
    def __init__(self, tasks): self.tasks = {task.task_id: task for task in tasks}
    def ready(self, complete): return [task for task in self.tasks.values() if task.task_id not in complete and all(dep in complete for dep in task.depends_on)]
