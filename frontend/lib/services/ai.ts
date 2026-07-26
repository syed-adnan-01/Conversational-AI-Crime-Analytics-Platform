import api from "@/lib/api";

export const ai = {
  copilotChat: (payload: { session_id: string; case_id: string; message: string; persona?: string }) =>
    api.post("/ai/copilot/chat", payload).then((response) => response.data),
  copilotHistory: (sessionId: string) => api.get(`/ai/copilot/history/${sessionId}`).then((response) => response.data),
  investigate: (payload: { case_id: string; query?: string }) => api.post("/ai/investigation/analyze", payload).then((response) => response.data),
  graph: (caseId: string) => api.get(`/ai/graph/case/${caseId}`).then((response) => response.data),
  agents: (payload: { case_id: string; query?: string }) => api.post("/ai/agents/execute", payload).then((response) => response.data),
  decision: (payload: { case_id: string; source_outputs: Record<string, unknown> }) => api.post("/ai/decision/analyze", payload).then((response) => response.data),
  evaluate: (payload: Record<string, unknown>) => api.post("/ai/evaluation/evaluate", payload).then((response) => response.data),
};
