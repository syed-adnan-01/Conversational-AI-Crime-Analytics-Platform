from concurrent.futures import ThreadPoolExecutor
class Scheduler:
    def execute(self, plan, registry, context):
        steps = plan.steps; results = []
        groups = {}
        for step in steps: groups.setdefault(step.parallel_group, []).append(step)
        for group in sorted(groups):
            if context.cancelled: break
            with ThreadPoolExecutor(max_workers=len(groups[group])) as pool:
                futures = [pool.submit(registry.get(step.task.agent_id).execute, step.task, context) for step in groups[group]]
                results.extend(future.result() for future in futures)
        return results
