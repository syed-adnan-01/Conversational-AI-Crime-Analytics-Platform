import api from "@/lib/api";

export interface CaseSearchParams {
  crime_no?: string;
  case_no?: string;
  page?: number;
  page_size?: number;
}

export function searchCases(params: CaseSearchParams) {
  return api.get("/cases/search", { params }).then((response) => response.data);
}

export function getCase(caseId: string) {
  return api.get(`/cases/${caseId}`).then((response) => response.data);
}

export function caseEvidence(caseId: string) {
  return api.get(`/cases/${caseId}/evidence`).then((response) => response.data);
}

export function caseVictims(caseId: string) {
  return api.get(`/cases/${caseId}/victims`).then((response) => response.data);
}

export function caseAccused(caseId: string) {
  return api.get(`/cases/${caseId}/accused`).then((response) => response.data);
}

export function caseWitnesses(caseId: string) {
  return api.get(`/cases/${caseId}/witnesses`).then((response) => response.data);
}

export function caseTimeline(caseId: string) {
  return api.get(`/cases/${caseId}/timeline`).then((response) => response.data);
}
