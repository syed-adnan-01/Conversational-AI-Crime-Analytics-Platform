import api from "@/lib/api";

export interface ReportSummary {
  report_id: string;
  report_type: string;
  title: string;
  case_id?: string;
  generated_by: string;
  generated_at: string;
  status: string;
}

export interface ReportTypeInfo {
  type: string;
  name: string;
  description: string;
  requires_case_id: boolean;
  supported_formats: string[];
}

export interface ReportTypeResponse {
  types: ReportTypeInfo[];
}

export interface ReportListResponse {
  reports: ReportSummary[];
}

export interface ReportDetail extends ReportSummary {
  content?: Record<string, unknown>;
  metadata?: Record<string, unknown>;
  sections?: { title?: string; content?: unknown }[];
}

// ─── Normalizer: maps raw API fields → ReportSummary shape ──────────────────
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function normalizeReport(raw: any): ReportSummary {
  return {
    report_id:    raw.report_id   ?? raw.id ?? "",
    report_type:  raw.report_type ?? "",
    title:        raw.title       ?? "Untitled Report",
    case_id:      raw.case_id,
    generated_by: raw.generated_by ?? "system",
    generated_at: raw.generated_at ?? raw.created_at ?? new Date().toISOString(),
    status:       raw.status       ?? "READY",
  };
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function normalizeDetail(raw: any): ReportDetail {
  return {
    ...normalizeReport(raw),
    content:  raw.content  ?? raw.data    ?? {},
    metadata: raw.metadata ?? { summary: raw.description ?? "", classification: "Restricted" },
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    sections: (raw.sections ?? []).map((s: any) => ({
      title:   s.title ?? "Section",
      content: Array.isArray(s.items) && s.items.length > 0
        ? s.items.map((i: unknown) => JSON.stringify(i)).join("\n")
        : (s.content ?? s.todo?.join("\n") ?? ""),
    })),
  };
}

export const reportsService = {
  listReports: (): Promise<ReportListResponse> =>
    api.get("/reports").then((res) => {
      // Backend returns { items: [...], total: N } — normalize to { reports: [...] }
      const raw = res.data ?? {};
      const items: ReportSummary[] = (raw.items ?? raw.reports ?? []).map(normalizeReport);
      return { reports: items };
    }),

  listTypes: (): Promise<ReportTypeResponse> =>
    api.get("/reports/types").then((res) => {
      const raw = res.data ?? {};
      const items = raw.items ?? raw.types ?? [];
      return {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        types: items.map((t: any) => ({
          type:              t.report_type ?? t.type ?? "",
          name:              t.title ?? t.name ?? "",
          description:       t.description ?? "",
          requires_case_id:  t.requires_case_id ?? false,
          supported_formats: (t.export_formats ?? t.supported_formats ?? []).map(String),
        })),
      };
    }),

  generateReport: (payload: { report_type: string; case_id?: string }): Promise<ReportSummary> =>
    api.post("/reports/generate", payload).then((res) => normalizeReport(res.data ?? {})),

  getReport: (reportId: string): Promise<ReportDetail> =>
    api.get(`/reports/${reportId}`).then((res) => normalizeDetail(res.data ?? {})),

  exportReport: (reportId: string, format: string = "json"): Promise<Blob | Record<string, unknown>> =>
    api.get(`/reports/${reportId}/export?format=${format}`).then((res) => res.data),
};
