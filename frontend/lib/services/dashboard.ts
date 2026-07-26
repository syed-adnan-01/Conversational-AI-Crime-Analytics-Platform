import api from "@/lib/api";

export interface DashboardData {
  total_cases: number;
  status_counts: Record<string, number>;
  recent_cases: Array<Record<string, unknown>>;
  alerts: unknown[];
  trends: unknown[];
}

/** Uses only currently available backend data; alerts and trends are intentionally empty until their sources exist. */
export function getDashboard() {
  return api.get<DashboardData>("/analytics/dashboard").then((response) => response.data);
}
