class SynthesisStrategy:
    def synthesize(self, results):
        successful = [result for result in results if result.error is None]
        return {"summary": "Multi-agent investigation completed", "completed_agents": [result.agent_id for result in successful], "failed_agents": [result.agent_id for result in results if result.error], "findings": {result.agent_id: result.result for result in successful}}
