import api from "@/lib/api";

export interface CaseSearchParams {
  crime_no?: string;
  case_no?: string;
  case_category_id?: number;
  crime_major_head_id?: number;
  case_status_id?: number;
  police_station_id?: number;
  gravity_offence_id?: number;
  page?: number;
  page_size?: number;
}

export interface CaseSummary {
  case_master_id: string;
  crime_no: string;
  case_no?: string;
  case_status_id?: number;
  crime_registered_date: string;
  police_station_id: number;
  crime_major_head_id?: number;
  police_person_id?: number;
}

export interface PaginationMeta {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface CaseListResponse {
  items: CaseSummary[];
  pagination: PaginationMeta;
}

export interface CaseResponse {
  case_master_id: string;
  crime_no: string;
  case_no?: string;
  crime_registered_date: string;
  police_station_id: number;
  created_at?: string;
  updated_at?: string;
  police_person_id?: number;
  case_category_id?: number;
  gravity_offence_id?: number;
  crime_major_head_id?: number;
  crime_minor_head_id?: number;
  case_status_id?: number;
  court_id?: number;
  incident_from_date?: string;
  incident_to_date?: string;
  info_received_ps_date?: string;
  latitude?: number;
  longitude?: number;
  brief_facts?: string;
}

export function searchCases(params: CaseSearchParams): Promise<CaseListResponse> {
  return api.get("/cases/search", { params }).then((response) => response.data);
}

export function getCase(caseId: string): Promise<CaseResponse> {
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
