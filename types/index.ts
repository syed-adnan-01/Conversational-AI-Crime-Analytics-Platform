// ─── Shared Types for CrimeSphere AI ────────────────────────────────────────

export type RiskLevel = "low" | "medium" | "high" | "critical";

export type CrimeStatus =
  | "open"
  | "investigating"
  | "closed"
  | "escalated"
  | "pending";

export type Department =
  | "cyber-crime"
  | "homicide"
  | "narcotics"
  | "anti-terrorism"
  | "financial-crime"
  | "organized-crime"
  | "traffic"
  | "special-branch"
  | "state-police"
  | "central-bureau";

export type ClearanceLevel = 1 | 2 | 3 | 4 | 5;

// ─── Officer / User ──────────────────────────────────────────────────────────

export interface Officer {
  id: string;
  name: string;
  badgeNumber: string;
  rank: string;
  department: Department;
  station: string;
  district: string;
  state: string;
  email: string;
  phone: string;
  avatar?: string;
  clearanceLevel: ClearanceLevel;
  isActive: boolean;
  lastLogin: string;
  createdAt: string;
}

// ─── FIR (First Information Report) ─────────────────────────────────────────

export interface FIR {
  id: string;
  firNumber: string;
  title: string;
  description: string;
  crimeType: string;
  riskLevel: RiskLevel;
  status: CrimeStatus;
  reportedAt: string;
  updatedAt: string;
  location: string;
  district: string;
  state: string;
  ps: string; // Police Station
  assignedTo: string;
  assignedOfficerId: string;
  suspects: string[];
  victims: string[];
  witnesses: string[];
  evidence: EvidenceItem[];
  aiScore: number; // 0-100 AI risk score
  tags: string[];
}

// ─── Evidence ────────────────────────────────────────────────────────────────

export interface EvidenceItem {
  id: string;
  type: "document" | "image" | "video" | "physical" | "digital" | "testimony";
  description: string;
  collectedAt: string;
  collectedBy: string;
  location: string;
  chainOfCustody: string[];
}

// ─── Criminal Profile ────────────────────────────────────────────────────────

export interface CriminalProfile {
  id: string;
  name: string;
  aliases: string[];
  age: number;
  gender: "male" | "female" | "other";
  nationality: string;
  photo?: string;
  riskLevel: RiskLevel;
  status: "wanted" | "arrested" | "released" | "deceased" | "unknown";
  crimeHistory: string[];
  linkedFIRs: string[];
  associates: string[];
  lastKnownLocation: string;
  biometrics?: {
    fingerprints: boolean;
    faceId: boolean;
    dna: boolean;
  };
  aiThreatScore: number;
  notes: string;
  createdAt: string;
  updatedAt: string;
}

// ─── Alert ───────────────────────────────────────────────────────────────────

export interface Alert {
  id: string;
  type: "critical" | "warning" | "info" | "success";
  category: "crime" | "system" | "ai" | "network" | "officer";
  title: string;
  message: string;
  timestamp: string;
  isRead: boolean;
  source: string;
  linkedFIR?: string;
  actionRequired: boolean;
}

// ─── Crime Analytics ─────────────────────────────────────────────────────────

export interface CrimeStats {
  month: string;
  violent: number;
  property: number;
  cyber: number;
  narcotics: number;
  total: number;
}

export interface HeatmapPoint {
  lat: number;
  lng: number;
  weight: number;
  crimeType: string;
  district: string;
}

// ─── Investigation ───────────────────────────────────────────────────────────

export interface Investigation {
  id: string;
  title: string;
  description: string;
  status: "active" | "cold" | "closed" | "suspended";
  priority: RiskLevel;
  linkedFIRs: string[];
  team: string[];
  leadOfficer: string;
  createdAt: string;
  updatedAt: string;
  deadline?: string;
  notes: InvestigationNote[];
  aiInsights: string[];
  progress: number; // 0-100
}

export interface InvestigationNote {
  id: string;
  content: string;
  authorId: string;
  authorName: string;
  createdAt: string;
  isAI: boolean;
}

// ─── AI Chat ─────────────────────────────────────────────────────────────────

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
  tokens?: number;
  sources?: string[];
}

// ─── Report ──────────────────────────────────────────────────────────────────

export interface Report {
  id: string;
  title: string;
  type: "daily" | "weekly" | "monthly" | "incident" | "analytics" | "custom";
  status: "draft" | "pending" | "approved" | "published";
  createdBy: string;
  createdAt: string;
  approvedBy?: string;
  approvedAt?: string;
  district: string;
  dateRange: { from: string; to: string };
  summary: string;
  fileUrl?: string;
}

// ─── Nav / Sidebar ───────────────────────────────────────────────────────────

export interface NavItem {
  label: string;
  href: string;
  icon: string;
  badge?: number;
  children?: NavItem[];
  requiredClearance?: ClearanceLevel;
}
