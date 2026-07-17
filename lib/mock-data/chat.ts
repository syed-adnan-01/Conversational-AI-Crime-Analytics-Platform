// ─── Mock data + response engine for AI Crime Chat ──────────────────────────

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  sources?: string[];
}

export interface ChatSession {
  id: string;
  title: string;
  preview: string;
  timestamp: string;
  messageCount: number;
}

// ── Sessions ──────────────────────────────────────────────────────────────

export const mockSessions: ChatSession[] = [
  {
    id: "s1",
    title: "FIR Analysis — Sadar Bazar",
    preview: "Risk score for FIR-2024-00847 is 94/100 — critical...",
    timestamp: new Date(Date.now() - 2 * 3600000).toISOString(),
    messageCount: 8,
  },
  {
    id: "s2",
    title: "Narcotics Network Query",
    preview: "The Arun Singh network now spans 4 states...",
    timestamp: new Date(Date.now() - 5 * 3600000).toISOString(),
    messageCount: 14,
  },
  {
    id: "s3",
    title: "Suspect Profile: Rajan Mehta",
    preview: "High recidivism risk — 89% probability within 12 months...",
    timestamp: new Date(Date.now() - 26 * 3600000).toISOString(),
    messageCount: 6,
  },
  {
    id: "s4",
    title: "Cyber Crime Pattern Analysis",
    preview: "ATM skimming pattern across 7 locations — single gang...",
    timestamp: new Date(Date.now() - 28 * 3600000).toISOString(),
    messageCount: 11,
  },
  {
    id: "s5",
    title: "Crime Hotspot Prediction",
    preview: "Dharavi zone 78% probability of violent incidents...",
    timestamp: new Date(Date.now() - 50 * 3600000).toISOString(),
    messageCount: 9,
  },
];

// ── Quick Prompts ─────────────────────────────────────────────────────────

export const quickPrompts = [
  {
    id: "q1",
    icon: "FileText",
    label: "Analyse FIR-2024-00847",
    description: "Full AI risk assessment & recommendations",
    query: "Analyse FIR-2024-00847 and provide a complete risk assessment with recommended actions.",
  },
  {
    id: "q2",
    icon: "MapPin",
    label: "Today's crime hotspots",
    description: "High-risk zones across all districts",
    query: "Show me the current crime hotspots across all districts for today.",
  },
  {
    id: "q3",
    icon: "Network",
    label: "Map criminal network",
    description: "Rajan Mehta's known associates",
    query: "Map the full criminal network connected to Rajan Mehta and identify key associates.",
  },
  {
    id: "q4",
    icon: "TrendingUp",
    label: "Predict tomorrow's risks",
    description: "AI-powered crime forecast",
    query: "Predict crime risk areas for tomorrow based on current patterns and historical data.",
  },
];

// ── Initial Welcome Message ───────────────────────────────────────────────

export const initialMessages: ChatMessage[] = [
  {
    id: "init-001",
    role: "assistant",
    content: `**Welcome, SP Rajesh Kumar.**

I am **CrimeSphere Intelligence** — your AI-powered crime analysis assistant with real-time access to:
- **2,847** active FIRs across 36 jurisdictions
- **12,400+** criminal profiles in the national registry
- **Real-time alerts** and predictive hotspot analytics
- **Pattern recognition** trained on 10 years of crime data

How can I assist your investigation today?`,
    timestamp: new Date(Date.now() - 5 * 60000).toISOString(),
    sources: [],
  },
];

// ── Mock Response Engine ──────────────────────────────────────────────────

const FIR_RESPONSE = `**FIR-2024-00847 — Complete Risk Assessment**

📍 **Location:** Sadar Bazar, Central Delhi
🕐 **Reported:** 2 hours ago · PS Sadar Bazar
⚠️ **AI Risk Score:** 94 / 100 — CRITICAL

---

**Incident Summary**
Armed robbery at a jewellery shop involving 3–4 suspects. One victim (male, 35) sustained minor injuries. Suspects fled in a white Fortuner (DL-01-XX-4782).

**Key Intelligence Findings:**
- Suspect vehicle matches **2 prior robberies** in North Delhi (Dec 2023 · Jan 2024)
- MO is consistent with the tracked **"Sadar Gang"** — active since Q3 2023
- At least 2 suspects have narcotics priors linked to **FIR-2023-00621**
- Time of operation (11:30 AM weekday) matches gang's known pattern

**Recommended Actions:**
- Issue APB for vehicle DL-01-XX-4782 at all checkpoints
- Cross-reference suspects from FIR-2023-00621 immediately
- Deploy CCTV retrieval team at Sadar Bazar market
- Coordinate Narcotics Cell for cross-linked suspects

**Linked FIRs:** FIR-2023-00621 · FIR-2024-00312 · FIR-2024-00291`;

const SUSPECT_RESPONSE = `**Suspect Profile — Rajan Mehta**

🆔 **Registry ID:** CR-2019-04821
⚠️ **AI Threat Score:** 87 / 100 — HIGH RISK
📍 **Last Known Location:** Ghaziabad, UP (3 hrs ago — tower data)

---

**Personal Details**
Age: 34 · Male · Indian National
Status: **Wanted** — Non-bailable warrant active since March 2024

**Criminal History (7 offences):**
- Armed robbery (2019) — Convicted, 3 years, released 2022
- Narcotics possession (2020) — Acquitted on technicality
- Vehicle theft x2 (2022–23) — Cases ongoing
- Assault with weapon (2023) — Case ongoing

**Known Associates:**
- Suresh Pandey (finance/hawala) · Score 79
- Karan Tiwari (logistics) · Score 68
- Arun Singh (kingpin) · Score 96

**AI Assessment:**
Recidivism probability **89%** within 12 months. Operational between Delhi-NCR and western UP. Rotates SIM cards every 48 hours. Last active tower: Vaishali, Ghaziabad.

**Active Warrants:** 2 non-bailable · 1 anticipatory bail rejected`;

const HOTSPOT_RESPONSE = `**Crime Hotspot Analysis — Live**

📅 **${new Date().toLocaleDateString("en-IN", { weekday: "long", day: "2-digit", month: "long" })}** · Model Confidence: 91%

---

**🔴 Critical Risk Zones (Next 12 Hours)**
- Dharavi, Mumbai — Violent crime · **78% probability**
- Sadar Bazar, Delhi — Robbery · **71% probability**
- Whitefield, Bengaluru — Cyber crime · **65% probability**

**🟠 High Risk Zones**
- Sector 14, Gurugram — Property crime · 58%
- Koregaon Park, Pune — Narcotics · 54%
- Anna Nagar, Chennai — Financial fraud · 49%

**Pattern Drivers:**
- Friday effect — weekend approach increases street crime by ~22%
- Post-festival cash withdrawals still elevated in metro corridors
- 3 active gang operations detected in Mumbai–Delhi–Agra axis

**Recommended Deployments:**
Increase patrol density **+40%** in Dharavi and Sadar Bazar. Coordinate with local PS for rapid response. Issue advisory to commercial establishments in high-risk zones.`;

const NETWORK_RESPONSE = `**Criminal Network Map — Rajan Mehta**

🕸️ **Network Size:** 23 confirmed nodes · Threat: HIGH
🌐 **States Covered:** Maharashtra · Delhi · UP · Rajasthan

---

**Network Hierarchy:**
Arun Singh (Kingpin · Pune) ← Core
  → Rajan Mehta (Operations · Delhi-NCR) — **WANTED**
    → Suresh Pandey (Finance · Agra)
    → Karan Tiwari (Transport · Noida)
  → Mumbai Cell (6 members · 2 wanted)
  → UP Cell (8 members · 3 wanted)

**Key Intelligence:**
- Financial flows via hawala networks in Agra and Pune
- Communication: Encrypted apps + physical drop-boxes
- SIM rotation every 48–72 hours across all members
- Estimated monthly illicit turnover: ₹2.4 Cr

**Weakest Link:** Karan Tiwari (logistics) — 2 prior convictions, possible informant leverage

**Recommended Action:**
Joint operation with NCB and Organised Crime Cell. Simultaneous strikes across Delhi, Pune, and Agra nodes recommended for maximum disruption.`;

const PREDICTION_RESPONSE = `**Crime Risk Forecast — Next 24 Hours**

🤖 **Model:** CrimeSphere GPT-L v2.4 · Accuracy: 94.7%
📊 **Signals analysed:** 1,847 | **Data points:** 2.3M

---

**High-Confidence Predictions:**

**1. Narcotics Consignment — Mumbai Port (82%)**
Sea cargo pattern + network comms suggest a shipment between 02:00–06:00 IST. Recommend Customs + NCB alert immediately.

**2. Coordinated Cyber Attack — Banking Sector (76%)**
14 phishing domains registered in last 48 hrs targeting SBI and HDFC. Coordinated attack likely within 18 hours.

**3. Gang Confrontation — Pune East (69%)**
Territorial dispute between two rival factions detected via intercept analysis. Possible violent escalation at Kondhwa or Wanowrie.

**Preventive Actions:**
- Deploy Cyber Crime rapid-response on standby
- Issue banking fraud alert to RBI + major banks
- Increase armed patrol density in Pune East (Kondhwa/Wanowrie)
- Alert Mumbai Port Trust Security for overnight vigil`;

const DEFAULT_RESPONSE = `**CrimeSphere Intelligence Response**

I have cross-referenced your query against the live intelligence database.

**Current System Status:**
- Active FIRs: **2,847** across 36 jurisdictions
- Critical alerts pending: **18**
- Model confidence today: **94.7%**

I can provide detailed intelligence on specific topics. Try asking me:
- **"Analyse FIR-2024-00847"** — Case risk assessment
- **"Show profile of Rajan Mehta"** — Suspect deep-dive
- **"What are today's crime hotspots?"** — Live risk zones
- **"Map the Arun Singh network"** — Criminal network graph
- **"Predict tomorrow's crime risks"** — AI forecasting
- **"Analyse cyber crime patterns this month"** — Trend analysis

Please provide more specific details and I'll generate a precise intelligence report.`;

export function getMockResponse(query: string): string {
  const q = query.toLowerCase();
  if (q.includes("fir") || q.includes("00847") || q.includes("case") || q.includes("analyse") || q.includes("analyze")) return FIR_RESPONSE;
  if (q.includes("rajan") || q.includes("mehta") || q.includes("suspect") || q.includes("profile") || q.includes("wanted")) return SUSPECT_RESPONSE;
  if (q.includes("hotspot") || q.includes("zone") || q.includes("map") || q.includes("today") || q.includes("location")) return HOTSPOT_RESPONSE;
  if (q.includes("network") || q.includes("gang") || q.includes("arun") || q.includes("associate") || q.includes("narcotics")) return NETWORK_RESPONSE;
  if (q.includes("predict") || q.includes("forecast") || q.includes("tomorrow") || q.includes("risk") || q.includes("future")) return PREDICTION_RESPONSE;
  return DEFAULT_RESPONSE;
}
