// ─── Mock data for the Dashboard ────────────────────────────────────────────

import type { RiskLevel, CrimeStatus } from "@/types";

// ── KPI Stats ──────────────────────────────────────────────────────────────
export const kpiStats = [
  {
    id: "total-firs",
    label: "Total Active FIRs",
    value: "2,847",
    change: "+12.4%",
    changeLabel: "vs last month",
    trend: "up" as const,
    color: "#0070f3",
    glowColor: "rgba(0,112,243,0.18)",
    borderColor: "rgba(0,112,243,0.3)",
    icon: "FileText",
    description: "Active cases across all districts",
  },
  {
    id: "critical-alerts",
    label: "Critical Alerts",
    value: "18",
    change: "+3",
    changeLabel: "since yesterday",
    trend: "up" as const,
    color: "#ff2d55",
    glowColor: "rgba(255,45,85,0.15)",
    borderColor: "rgba(255,45,85,0.3)",
    icon: "AlertTriangle",
    description: "Require immediate attention",
  },
  {
    id: "resolved",
    label: "Resolved Cases",
    value: "1,203",
    change: "+8.1%",
    changeLabel: "this month",
    trend: "up" as const,
    color: "#30d158",
    glowColor: "rgba(48,209,88,0.12)",
    borderColor: "rgba(48,209,88,0.3)",
    icon: "CheckCircle2",
    description: "Closed in last 30 days",
  },
  {
    id: "ai-accuracy",
    label: "AI Prediction Score",
    value: "94.7%",
    change: "+0.3%",
    changeLabel: "model improvement",
    trend: "up" as const,
    color: "#bf5af2",
    glowColor: "rgba(191,90,242,0.12)",
    borderColor: "rgba(191,90,242,0.3)",
    icon: "Brain",
    description: "Crime prediction accuracy",
  },
];

// ── Crime Monthly Trend ────────────────────────────────────────────────────
export const crimeMonthlyData = [
  { month: "Feb", violent: 245, property: 320, cyber: 180, narcotics: 95 },
  { month: "Mar", violent: 268, property: 298, cyber: 220, narcotics: 112 },
  { month: "Apr", violent: 230, property: 310, cyber: 250, narcotics: 98 },
  { month: "May", violent: 290, property: 280, cyber: 195, narcotics: 130 },
  { month: "Jun", violent: 275, property: 340, cyber: 280, narcotics: 115 },
  { month: "Jul", violent: 310, property: 315, cyber: 320, narcotics: 142 },
];

// ── Crime Type Distribution ────────────────────────────────────────────────
export const crimeTypeDistribution = [
  { name: "Property Crime", value: 35, color: "#0070f3" },
  { name: "Violent Crime",  value: 28, color: "#ff2d55" },
  { name: "Cyber Crime",    value: 22, color: "#bf5af2" },
  { name: "Narcotics",      value: 15, color: "#ff8c00" },
];

// ── Recent Alerts ──────────────────────────────────────────────────────────
export const recentAlerts = [
  {
    id: "alert-001",
    type: "critical" as const,
    title: "Armed Robbery in Progress",
    message: "Multiple armed suspects at Sadar Bazar. Units dispatched. Perimeter set.",
    timestamp: new Date(Date.now() - 5 * 60000).toISOString(),
    source: "PCR Control Room",
    district: "Central Delhi",
    actionRequired: true,
    linkedFIR: "FIR-2024-00847",
  },
  {
    id: "alert-002",
    type: "warning" as const,
    title: "Wanted Suspect Flagged",
    message: "Rajan Mehta flagged by AI face-recognition at Ghaziabad NH-9 toll plaza.",
    timestamp: new Date(Date.now() - 18 * 60000).toISOString(),
    source: "AI Recognition Engine",
    district: "Ghaziabad",
    actionRequired: true,
    linkedFIR: "FIR-2024-00312",
  },
  {
    id: "alert-003",
    type: "critical" as const,
    title: "Missing Child — AMBER Alert",
    message: "8-year-old missing from Vasant Kunj. All units on lookout. AMBER active.",
    timestamp: new Date(Date.now() - 72 * 60000).toISOString(),
    source: "PS Vasant Kunj",
    district: "South Delhi",
    actionRequired: true,
    linkedFIR: "FIR-2024-00844",
  },
  {
    id: "alert-004",
    type: "info" as const,
    title: "Cyber Attack on Banking Portal",
    message: "Coordinated phishing targeting HDFC customers. 2,300 accounts at risk.",
    timestamp: new Date(Date.now() - 45 * 60000).toISOString(),
    source: "Cyber Crime Division",
    district: "Mumbai",
    actionRequired: false,
    linkedFIR: "FIR-2024-00841",
  },
  {
    id: "alert-005",
    type: "warning" as const,
    title: "Drug Network Activity",
    message: "AI detected unusual comms in Arun Singh narcotics network. 3 new nodes.",
    timestamp: new Date(Date.now() - 120 * 60000).toISOString(),
    source: "CrimeSphere AI",
    district: "Pune",
    actionRequired: false,
    linkedFIR: "FIR-2024-00798",
  },
];

// ── Recent FIRs ────────────────────────────────────────────────────────────
export const recentFIRs: {
  id: string;
  firNumber: string;
  title: string;
  crimeType: string;
  riskLevel: RiskLevel;
  status: CrimeStatus;
  district: string;
  assignedTo: string;
  reportedAt: string;
  aiScore: number;
}[] = [
  {
    id: "fir-001",
    firNumber: "FIR-2024-00847",
    title: "Armed Robbery — Sadar Bazar",
    crimeType: "Violent Crime",
    riskLevel: "critical",
    status: "investigating",
    district: "Central Delhi",
    assignedTo: "SP Rajesh Kumar",
    reportedAt: new Date(Date.now() - 2 * 3600000).toISOString(),
    aiScore: 94,
  },
  {
    id: "fir-002",
    firNumber: "FIR-2024-00841",
    title: "Cyber Fraud — Banking Phishing",
    crimeType: "Cyber Crime",
    riskLevel: "high",
    status: "investigating",
    district: "Mumbai Suburban",
    assignedTo: "DySP Priya Sharma",
    reportedAt: new Date(Date.now() - 5 * 3600000).toISOString(),
    aiScore: 87,
  },
  {
    id: "fir-003",
    firNumber: "FIR-2024-00835",
    title: "Narcotics Seizure — NH-48",
    crimeType: "Narcotics",
    riskLevel: "high",
    status: "open",
    district: "Gurugram",
    assignedTo: "SI Amit Verma",
    reportedAt: new Date(Date.now() - 8 * 3600000).toISOString(),
    aiScore: 79,
  },
  {
    id: "fir-004",
    firNumber: "FIR-2024-00829",
    title: "Financial Fraud — Shell Company",
    crimeType: "Financial Crime",
    riskLevel: "medium",
    status: "investigating",
    district: "Bengaluru Urban",
    assignedTo: "DSP Kavitha Nair",
    reportedAt: new Date(Date.now() - 12 * 3600000).toISOString(),
    aiScore: 71,
  },
  {
    id: "fir-005",
    firNumber: "FIR-2024-00821",
    title: "Chain Snatching — Brigade Road",
    crimeType: "Property Crime",
    riskLevel: "medium",
    status: "open",
    district: "Bengaluru Central",
    assignedTo: "ASI Suresh Babu",
    reportedAt: new Date(Date.now() - 18 * 3600000).toISOString(),
    aiScore: 55,
  },
  {
    id: "fir-006",
    firNumber: "FIR-2024-00814",
    title: "Vehicle Theft — Parking Complex",
    crimeType: "Property Crime",
    riskLevel: "low",
    status: "open",
    district: "Hyderabad",
    assignedTo: "HC Ramesh Rao",
    reportedAt: new Date(Date.now() - 24 * 3600000).toISOString(),
    aiScore: 32,
  },
];

// ── AI Insights ────────────────────────────────────────────────────────────
export const aiInsights = [
  {
    id: "insight-001",
    type: "prediction",
    title: "Crime Hotspot Predicted",
    description:
      "78% probability of violent incidents in Dharavi, Mumbai within 48 hrs based on historical + weather + event data.",
    confidence: 78,
    timestamp: new Date(Date.now() - 30 * 60000).toISOString(),
    actionable: true,
    color: "#ff2d55",
  },
  {
    id: "insight-002",
    type: "network",
    title: "Network Expansion Detected",
    description:
      "3 new nodes joined the Arun Singh narcotics network. Network now spans Maharashtra, MP, UP & Rajasthan.",
    confidence: 91,
    timestamp: new Date(Date.now() - 2 * 3600000).toISOString(),
    actionable: true,
    color: "#ff8c00",
  },
  {
    id: "insight-003",
    type: "pattern",
    title: "ATM Skimming Gang",
    description:
      "Identical skimming devices at 7 ATMs across Pune. MO & timing strongly suggests a single organised gang.",
    confidence: 85,
    timestamp: new Date(Date.now() - 4 * 3600000).toISOString(),
    actionable: true,
    color: "#bf5af2",
  },
  {
    id: "insight-004",
    type: "alert",
    title: "High Recidivism Risk",
    description:
      "4 recently released convicts have >80% reoffending probability score within the next 90 days.",
    confidence: 83,
    timestamp: new Date(Date.now() - 6 * 3600000).toISOString(),
    actionable: false,
    color: "#ffd60a",
  },
];
