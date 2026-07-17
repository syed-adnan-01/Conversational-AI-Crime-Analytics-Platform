// ─── Reports Mock Data ────────────────────────────────────────────────────────

export type ReportType    = "fir-summary" | "crime-analytics" | "network-analysis" | "monthly-digest" | "incident-brief" | "investigation-status";
export type ReportStatus  = "ready" | "generating" | "failed" | "scheduled";

export interface GeneratedReport {
  id: string;
  title: string;
  type: ReportType;
  generatedBy: string;
  generatedAt: string;
  status: ReportStatus;
  sizeMb: number;
  pages: number;
  district: string;
  period: string;
  classification: "Confidential" | "Secret" | "Top Secret" | "Restricted";
  summary: string;
  sections: { heading: string; content: string }[];
}

export interface ReportTemplate {
  id: string;
  type: ReportType;
  name: string;
  description: string;
  icon: string;
  color: string;
  avgPages: string;
  estTime: string;
}

// ─── Templates ────────────────────────────────────────────────────────────────

export const REPORT_TEMPLATES: ReportTemplate[] = [
  { id: "tpl-1", type: "fir-summary",          name: "FIR Summary Report",        description: "Comprehensive list of all FIRs with risk scores and status",           icon: "FileText",    color: "#0070f3", avgPages: "12–18", estTime: "~30s" },
  { id: "tpl-2", type: "crime-analytics",       name: "Crime Analytics Report",    description: "Statistical crime analysis with charts and trend comparison",          icon: "BarChart3",   color: "#bf5af2", avgPages: "8–14",  estTime: "~45s" },
  { id: "tpl-3", type: "network-analysis",      name: "Criminal Network Report",   description: "Criminal association maps and threat actor profiles",                  icon: "Network",     color: "#ff2d55", avgPages: "16–24", estTime: "~60s" },
  { id: "tpl-4", type: "monthly-digest",        name: "Monthly Intelligence Digest","description": "Executive summary of monthly crime patterns and AI predictions",    icon: "Calendar",    color: "#30d158", avgPages: "6–10",  estTime: "~20s" },
  { id: "tpl-5", type: "incident-brief",        name: "Incident Brief",            description: "Detailed report on a single incident or FIR",                        icon: "AlertTriangle",color: "#ff8c00", avgPages: "4–6",   estTime: "~15s" },
  { id: "tpl-6", type: "investigation-status",  name: "Investigation Status Report","description": "Current status of all active investigations and open tasks",        icon: "FolderOpen",  color: "#ffd60a", avgPages: "10–16", estTime: "~35s" },
];

// ─── Generated Reports ────────────────────────────────────────────────────────

export const GENERATED_REPORTS: GeneratedReport[] = [
  {
    id: "rpt-001",
    title: "Delhi District — FIR Summary Report",
    type: "fir-summary",
    generatedBy: "SP Rajesh Kumar",
    generatedAt: new Date(Date.now() - 2 * 3600000).toISOString(),
    status: "ready",
    sizeMb: 4.2,
    pages: 14,
    district: "Central Delhi",
    period: "Jul 2024",
    classification: "Confidential",
    summary: "This report provides a comprehensive summary of all 247 FIRs registered in Central Delhi during July 2024. 18 cases are classified as Critical, 43 as High Risk. AI-assisted prioritisation has been applied to all active cases. Detection rate stands at 73.2%.",
    sections: [
      { heading: "Executive Summary",         content: "Central Delhi registered 247 FIRs in July 2024 — a 6.2% increase over June 2024 (232 FIRs). Violent crimes constitute 31% of all cases, followed by property crimes at 28%. AI risk scoring has been applied to all 247 cases, with 18 rated Critical and 43 rated High." },
      { heading: "Critical Cases",            content: "FIR-2024-00847 (Armed Robbery, Sadar Bazar) — AI Score: 94\nFIR-2024-00844 (Missing Child, AMBER Alert) — AI Score: 91\nFIR-2024-00771 (Terror Threat, Railway Station) — AI Score: 76" },
      { heading: "Case Status Breakdown",     content: "Open: 89 cases (36%)\nInvestigating: 124 cases (50%)\nClosed: 28 cases (11%)\nEscalated: 6 cases (2.4%)" },
      { heading: "AI Recommendations",        content: "1. Immediate resource reallocation to Sadar Bazar zone — robbery pattern escalating.\n2. Joint operation with UP STF recommended for Rajan Mehta apprehension.\n3. AMBER Alert to remain active for FIR-2024-00844 for additional 72 hours." },
    ],
  },
  {
    id: "rpt-002",
    title: "Q2 2024 Crime Analytics Report — All Districts",
    type: "crime-analytics",
    generatedBy: "DySP Priya Sharma",
    generatedAt: new Date(Date.now() - 12 * 3600000).toISOString(),
    status: "ready",
    sizeMb: 8.7,
    pages: 22,
    district: "All Districts",
    period: "Apr–Jun 2024",
    classification: "Secret",
    summary: "Quarter 2 2024 shows a 12% rise in cyber crimes and a 7% reduction in violent crimes compared to Q1. Narcotics seizures increased by 34%. AI prediction accuracy for Q2 was 94.7%.",
    sections: [
      { heading: "Q2 2024 Overview",          content: "Total crimes registered: 7,167 (up 4.6% from Q1 2024 — 6,854). The most significant trend is a 34% increase in narcotics seizures, attributed to successful intelligence-led operations." },
      { heading: "Category Analysis",         content: "Property crimes: 2,341 (▲6.5%)\nViolent crimes: 1,847 (▲11.7%)\nCyber crimes: 1,403 (▲42.2%)\nNarcotics: 743 (▼9.5%)\nFinancial crimes: 621 (▲14.4%)" },
      { heading: "Hotspot Districts",         content: "Top 3 high-crime districts:\n1. Central Delhi (421 cases)\n2. Mumbai City (389 cases)\n3. Bengaluru Urban (312 cases)" },
      { heading: "AI Model Performance",      content: "Detection Rate: 94.7%\nFalse Positive Rate: 2.3%\nNew pattern signatures identified: 14\nPredictive accuracy (30-day hotspot): 91.2%" },
    ],
  },
  {
    id: "rpt-003",
    title: "Arun Singh Criminal Network — Analysis Report",
    type: "network-analysis",
    generatedBy: "SP Rajesh Kumar",
    generatedAt: new Date(Date.now() - 26 * 3600000).toISOString(),
    status: "ready",
    sizeMb: 12.4,
    pages: 28,
    district: "Multi-District",
    period: "Jan–Jul 2024",
    classification: "Top Secret",
    summary: "Comprehensive analysis of the Arun Singh organised crime network spanning 4 states. Network comprises 23 confirmed members, 8 wanted, 3 arrested. Financial intelligence estimates monthly illicit turnover at ₹2.4 Crore.",
    sections: [
      { heading: "Network Overview",          content: "The Arun Singh network is an organised crime syndicate operating across Maharashtra, Delhi, Uttar Pradesh, and Rajasthan. Core leadership consists of 4 individuals (Tier 1 and Tier 2). Network has been active since 2019." },
      { heading: "Key Actors",               content: "Arun Singh (Kingpin, Threat: 96) — WANTED\nRajan Mehta (Operations, Threat: 87) — WANTED\nSuresh Pandey (Finance, Threat: 79) — WANTED\nDeepak Nair (Mumbai Cell, Threat: 74) — WANTED" },
      { heading: "Financial Intelligence",   content: "Estimated monthly illicit revenue: ₹2.4 Crore\nHawala network nodes: 3 (Agra, Pune, Jaipur)\nShell companies identified: 4\nEDR referral: Recommended" },
      { heading: "Recommendations",          content: "1. Joint NCB-State Police coordinated strike across all 4 states simultaneously.\n2. Interpol Red Notice for Arun Singh — ISSUED.\n3. Financial freeze on identified shell companies via ED." },
    ],
  },
  {
    id: "rpt-004",
    title: "June 2024 Monthly Intelligence Digest",
    type: "monthly-digest",
    generatedBy: "System — Auto-Generated",
    generatedAt: new Date(Date.now() - 48 * 3600000).toISOString(),
    status: "ready",
    sizeMb: 2.1,
    pages: 8,
    district: "All Districts",
    period: "Jun 2024",
    classification: "Restricted",
    summary: "Monthly executive digest for June 2024. Key highlights: Cyber crimes up 22%, narcotics seizures record high, 3 major gang operations disrupted. AI predictions for July 2024 attached.",
    sections: [
      { heading: "Month in Brief",            content: "June 2024 recorded 1,203 total crimes across monitored districts — a 3.2% decrease from May 2024. Three major gang operations were successfully disrupted by joint police teams." },
      { heading: "Key Achievements",         content: "- Narcotics Raid, Koregaon Park: 12 arrested, ₹6 Cr contraband seized\n- ATM Skimming Gang: Network dismantled, ₹18 Lakh recovered\n- NH-48 Checkpoint: 2 drug carriers arrested" },
      { heading: "July 2024 AI Predictions", content: "Expected crime hotspots:\n1. Dharavi, Mumbai — Violent crime (78% probability)\n2. Sadar Bazar, Delhi — Robbery (71% probability)\n3. Whitefield, Bengaluru — Cyber crime (65% probability)" },
    ],
  },
  {
    id: "rpt-005",
    title: "Incident Brief — FIR-2024-00847",
    type: "incident-brief",
    generatedBy: "SI Priya Mehta",
    generatedAt: new Date(Date.now() - 1 * 3600000).toISOString(),
    status: "generating",
    sizeMb: 0,
    pages: 0,
    district: "Central Delhi",
    period: "Jul 2024",
    classification: "Confidential",
    summary: "Report currently being generated by the system. Estimated completion in 30 seconds.",
    sections: [],
  },
  {
    id: "rpt-006",
    title: "Active Investigation Status — All Cases",
    type: "investigation-status",
    generatedBy: "System — Scheduled",
    generatedAt: new Date(Date.now() - 72 * 3600000).toISOString(),
    status: "ready",
    sizeMb: 5.8,
    pages: 16,
    district: "All Districts",
    period: "Jul 2024",
    classification: "Confidential",
    summary: "Status report for all 3 active high-priority investigations. Task completion rates, pending evidence, and officer assignments reviewed.",
    sections: [
      { heading: "Case FIR-2024-00847",      content: "Status: Investigating | Priority: Critical | Days Active: 2\nTask completion: 2/5 (40%)\nPending: AFIS match, additional CCTV retrieval, vehicle registration\nNext milestone: UP STF coordination meeting" },
      { heading: "Case FIR-2024-00844",      content: "Status: Investigating | Priority: Critical | Days Active: 3\nTask completion: 1/4 (25%)\nPending: RTO lookup, railway CCTV AI scan, UP ATF coordination\nNext milestone: AI facial scan results (ETA 6 hours)" },
      { heading: "Case FIR-2024-00798",      content: "Status: Investigating | Priority: High | Days Active: 5\nTask completion: 1/4 (25%)\nPending: FSL phone data, ledger customer identification\nNext milestone: Interpol response on Arun Singh" },
    ],
  },
  {
    id: "rpt-007",
    title: "Narcotics Trend Analysis — Q2 2024",
    type: "crime-analytics",
    generatedBy: "DSP Ravi Patil",
    generatedAt: new Date(Date.now() - 96 * 3600000).toISOString(),
    status: "failed",
    sizeMb: 0,
    pages: 0,
    district: "All Districts",
    period: "Apr–Jun 2024",
    classification: "Secret",
    summary: "Report generation failed due to insufficient data access permissions. Request elevated clearance or regenerate.",
    sections: [],
  },
];

// ─── Type config map ──────────────────────────────────────────────────────────

export const TYPE_CFG: Record<ReportType, { label: string; color: string }> = {
  "fir-summary":          { label: "FIR Summary",        color: "#0070f3" },
  "crime-analytics":      { label: "Crime Analytics",    color: "#bf5af2" },
  "network-analysis":     { label: "Network Analysis",   color: "#ff2d55" },
  "monthly-digest":       { label: "Monthly Digest",     color: "#30d158" },
  "incident-brief":       { label: "Incident Brief",     color: "#ff8c00" },
  "investigation-status": { label: "Investigation",      color: "#ffd60a" },
};

export const CLASS_CFG: Record<GeneratedReport["classification"], { color: string; bg: string }> = {
  "Restricted":  { color: "#30d158", bg: "rgba(48,209,88,0.1)" },
  "Confidential":{ color: "#0070f3", bg: "rgba(0,112,243,0.1)" },
  "Secret":      { color: "#ff8c00", bg: "rgba(255,140,0,0.1)" },
  "Top Secret":  { color: "#ff2d55", bg: "rgba(255,45,85,0.1)" },
};
