import api from "@/lib/api";

export interface DashboardSummary {
  total_cases: number;
  open_cases: number;
  closed_cases: number;
  pending_cases: number;
  investigation_completion_percent: number;
  evidence_uploaded: number;
  officers_assigned: number;
}

export interface RecentCase {
  case_id: string;
  case_number: string;
  fir: string;
  district?: string;
  officer?: string;
  priority?: string;
  status?: string;
  created_date?: string;
  risk_score?: number;
}

export interface TrendData {
  month: string;
  active: number;
  resolved: number;
}

export interface AlertData {
  id: string;
  title: string;
  description: string;
  severity: "critical" | "high" | "medium" | "low";
  time: string;
  read: boolean;
}

export interface AIInsight {
  id: string;
  title: string;
  description: string;
  confidence: number;
  type: "pattern" | "anomaly" | "prediction";
}

export async function getDashboardSummary() {
  const { data } = await api.get<DashboardSummary>("/dashboard/summary");
  return data;
}

export async function getRecentCases() {
  const { data } = await api.get<RecentCase[]>("/dashboard/recent-cases");
  return data;
}

export async function getTrends() {
  const { data } = await api.get<TrendData[]>("/dashboard/trends");
  return data;
}

export async function getAlerts() {
  const { data } = await api.get<AlertData[]>("/dashboard/alerts");
  return data;
}

export async function getAIInsights() {
  const { data } = await api.get<AIInsight[]>("/dashboard/ai");
  return data;
}
