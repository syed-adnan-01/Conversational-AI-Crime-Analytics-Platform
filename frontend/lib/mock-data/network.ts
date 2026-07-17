// ─── Criminal Network Mock Data ──────────────────────────────────────────────

export type NodeStatus = "wanted" | "arrested" | "released" | "deceased" | "unknown";
export type NodeTier   = 1 | 2 | 3;
export type EdgeType   = "operational" | "financial" | "communication" | "family";
export type EdgeStrength = "strong" | "medium" | "weak";

export interface NetworkNode {
  id: string;
  name: string;
  alias: string;
  role: string;
  threatScore: number;
  status: NodeStatus;
  crimeTypes: string[];
  lastLocation: string;
  state: string;
  tier: NodeTier;
  linkedFIRs: string[];
  bio: string;
  // SVG positions (out of 900 x 560)
  x: number;
  y: number;
}

export interface NetworkEdge {
  id: string;
  source: string;
  target: string;
  type: EdgeType;
  strength: EdgeStrength;
  description: string;
}

// ─── Nodes ────────────────────────────────────────────────────────────────────

export const NETWORK_NODES: NetworkNode[] = [
  {
    id: "n1",
    name: "Arun Singh",
    alias: '"The Director"',
    role: "Network Kingpin",
    threatScore: 96,
    status: "wanted",
    crimeTypes: ["Narcotics", "Extortion", "Money Laundering"],
    lastLocation: "Pune, Maharashtra",
    state: "Maharashtra",
    tier: 1,
    linkedFIRs: ["FIR-2024-00798", "FIR-2023-00621"],
    bio: "Top-tier organised crime syndicate leader. Operates across 4 states. Evaded arrest 3 times. Red Notice issued with Interpol.",
    x: 450, y: 270,
  },
  {
    id: "n2",
    name: "Rajan Mehta",
    alias: '"Shadow"',
    role: "Operations Head — Delhi",
    threatScore: 87,
    status: "wanted",
    crimeTypes: ["Armed Robbery", "Narcotics", "Vehicle Theft"],
    lastLocation: "Ghaziabad, UP",
    state: "Uttar Pradesh",
    tier: 2,
    linkedFIRs: ["FIR-2024-00847", "FIR-2024-00312"],
    bio: "Primary enforcer for Arun Singh's Delhi-NCR operations. 7 prior offences. Non-bailable warrant active.",
    x: 210, y: 160,
  },
  {
    id: "n3",
    name: "Suresh Pandey",
    alias: '"The Accountant"',
    role: "Finance & Hawala Controller",
    threatScore: 79,
    status: "wanted",
    crimeTypes: ["Money Laundering", "Hawala", "Financial Fraud"],
    lastLocation: "Agra, UP",
    state: "Uttar Pradesh",
    tier: 2,
    linkedFIRs: ["FIR-2024-00829"],
    bio: "Handles all financial flows for the Singh network via hawala channels. CAs in Agra and Pune implicated.",
    x: 700, y: 160,
  },
  {
    id: "n4",
    name: "Deepak Nair",
    alias: '"The Fixer"',
    role: "Mumbai Cell Commander",
    threatScore: 74,
    status: "wanted",
    crimeTypes: ["Extortion", "Narcotics Distribution", "Violent Crime"],
    lastLocation: "Dharavi, Mumbai",
    state: "Maharashtra",
    tier: 2,
    linkedFIRs: ["FIR-2024-00751"],
    bio: "Controls Mumbai operations. Suspected link to Salim Qureshi extortion network. Runs 6-member cell.",
    x: 185, y: 400,
  },
  {
    id: "n5",
    name: "Manish Rai",
    alias: '"Coordinator"',
    role: "Delhi Logistics Coordinator",
    threatScore: 68,
    status: "arrested",
    crimeTypes: ["Narcotics Transport", "Extortion"],
    lastLocation: "Custody — Tihar Jail, Delhi",
    state: "Delhi",
    tier: 2,
    linkedFIRs: ["FIR-2024-00835"],
    bio: "Arrested during NH-48 narcotics seizure operation. In custody. Providing partial information under interrogation.",
    x: 720, y: 400,
  },
  {
    id: "n6",
    name: "Karan Tiwari",
    alias: '"Wheels"',
    role: "Transport & Logistics",
    threatScore: 64,
    status: "wanted",
    crimeTypes: ["Drug Trafficking", "Vehicle Smuggling"],
    lastLocation: "Noida, UP",
    state: "Uttar Pradesh",
    tier: 3,
    linkedFIRs: ["FIR-2024-00835"],
    bio: "Manages inter-state vehicle and narcotics transport. Known to use legitimate trucking firms as cover.",
    x: 75, y: 270,
  },
  {
    id: "n7",
    name: "Vikram Joshi",
    alias: '"Ghost"',
    role: "Intelligence Gatherer",
    threatScore: 58,
    status: "unknown",
    crimeTypes: ["Surveillance", "Information Brokering"],
    lastLocation: "Unknown — last seen Lucknow",
    state: "Uttar Pradesh",
    tier: 3,
    linkedFIRs: [],
    bio: "Suspected intelligence operative for Rajan Mehta. Gathers information on law enforcement operations. No confirmed identity.",
    x: 330, y: 80,
  },
  {
    id: "n8",
    name: "Ravi Sharma",
    alias: '"The Collector"',
    role: "Hawala Channel Operative",
    threatScore: 55,
    status: "arrested",
    crimeTypes: ["Hawala", "Money Laundering"],
    lastLocation: "Custody — Manesar PS",
    state: "Haryana",
    tier: 3,
    linkedFIRs: ["FIR-2024-00835"],
    bio: "Arrested at NH-48 checkpoint. Low-level hawala operative linking Suresh Pandey's Agra network to Punjab routes.",
    x: 590, y: 80,
  },
  {
    id: "n9",
    name: "Pradeep Waghmare",
    alias: '"Banker"',
    role: "Shell Company Operator",
    threatScore: 61,
    status: "wanted",
    crimeTypes: ["Financial Fraud", "Shell Companies", "Tax Evasion"],
    lastLocation: "Bengaluru, Karnataka",
    state: "Karnataka",
    tier: 3,
    linkedFIRs: ["FIR-2024-00829"],
    bio: "Operates 4 shell companies channelling funds for Suresh Pandey. CA background. Currently absconding.",
    x: 820, y: 270,
  },
  {
    id: "n10",
    name: "Manoj Yadav",
    alias: '"Street Boss"',
    role: "Mumbai Street Network",
    threatScore: 52,
    status: "arrested",
    crimeTypes: ["Drug Peddling", "Assault"],
    lastLocation: "Custody — Arthur Road Jail",
    state: "Maharashtra",
    tier: 3,
    linkedFIRs: ["FIR-2024-00798"],
    bio: "Arrested during Pune drug raid. Low-level peddler in Deepak Nair's Mumbai cell. 12 kg MDMA linked to his supply chain.",
    x: 80, y: 490,
  },
  {
    id: "n11",
    name: "Salim Qureshi",
    alias: '"Voice"',
    role: "Extortion Operative",
    threatScore: 70,
    status: "wanted",
    crimeTypes: ["Extortion", "Threat", "Underworld Links"],
    lastLocation: "Unknown — Dubai suspected",
    state: "Unknown",
    tier: 3,
    linkedFIRs: ["FIR-2024-00751"],
    bio: "Primary extortionist linked to Mumbai underworld. Voice analysis confirms identity in Dharavi extortion case. May be operating from Dubai.",
    x: 370, y: 480,
  },
  {
    id: "n12",
    name: "Kavya Desai",
    alias: '"Source"',
    role: "Suspected Police Informant",
    threatScore: 30,
    status: "unknown",
    crimeTypes: ["Information Leaking", "Bribery"],
    lastLocation: "Pune, Maharashtra",
    state: "Maharashtra",
    tier: 3,
    linkedFIRs: [],
    bio: "Suspected of leaking intelligence to the Arun Singh network. Under surveillance. Identity not confirmed to network operatives.",
    x: 645, y: 480,
  },
];

// ─── Edges ────────────────────────────────────────────────────────────────────

export const NETWORK_EDGES: NetworkEdge[] = [
  { id: "e1",  source: "n1", target: "n2", type: "operational",    strength: "strong",  description: "Core operational command chain" },
  { id: "e2",  source: "n1", target: "n3", type: "financial",      strength: "strong",  description: "Primary financial control flow" },
  { id: "e3",  source: "n1", target: "n4", type: "operational",    strength: "strong",  description: "Mumbai cell direct command" },
  { id: "e4",  source: "n1", target: "n5", type: "operational",    strength: "medium",  description: "Delhi logistics coordination" },
  { id: "e5",  source: "n2", target: "n6", type: "operational",    strength: "medium",  description: "Transport network access" },
  { id: "e6",  source: "n2", target: "n7", type: "communication",  strength: "medium",  description: "Intelligence sharing" },
  { id: "e7",  source: "n3", target: "n8", type: "financial",      strength: "medium",  description: "Hawala channel link" },
  { id: "e8",  source: "n3", target: "n9", type: "financial",      strength: "strong",  description: "Shell company control" },
  { id: "e9",  source: "n4", target: "n10",type: "operational",    strength: "medium",  description: "Street distribution chain" },
  { id: "e10", source: "n4", target: "n11",type: "operational",    strength: "weak",    description: "Extortion subcontracting" },
  { id: "e11", source: "n5", target: "n12",type: "communication",  strength: "weak",    description: "Suspected leak channel" },
  { id: "e12", source: "n1", target: "n11",type: "operational",    strength: "weak",    description: "Direct extortion oversight" },
];

// ─── Helpers ──────────────────────────────────────────────────────────────────

export const TIER_CONFIG: Record<NodeTier, { radius: number; label: string; color: string }> = {
  1: { radius: 38, label: "Kingpin",    color: "#ff2d55" },
  2: { radius: 28, label: "Lieutenant", color: "#ff8c00" },
  3: { radius: 20, label: "Operative",  color: "#ffd60a" },
};

export const STATUS_CONFIG: Record<NodeStatus, { color: string; label: string; dot: string }> = {
  wanted:   { color: "#ff2d55", label: "Wanted",   dot: "#ff2d55" },
  arrested: { color: "#30d158", label: "Arrested", dot: "#30d158" },
  released: { color: "#ff8c00", label: "Released", dot: "#ff8c00" },
  deceased: { color: "#526080", label: "Deceased", dot: "#526080" },
  unknown:  { color: "#ffd60a", label: "Unknown",  dot: "#ffd60a" },
};

export const EDGE_CONFIG: Record<EdgeStrength, { width: number; opacity: number; dash: string }> = {
  strong: { width: 2.5, opacity: 0.6, dash: "none" },
  medium: { width: 1.5, opacity: 0.4, dash: "6 4" },
  weak:   { width: 1,   opacity: 0.25, dash: "3 5" },
};
