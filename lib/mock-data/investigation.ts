// ─── Investigation Workspace Mock Data ───────────────────────────────────────

export type CasePriority = "critical" | "high" | "medium" | "low";
export type EvidenceStatus = "analysed" | "pending" | "contaminated" | "sealed";
export type EventType = "discovery" | "arrest" | "forensics" | "lead" | "court" | "operation" | "witness";
export type TaskStatus = "done" | "in-progress" | "pending";

export interface EvidenceItem {
  id: string;
  type: "document" | "photo" | "video" | "forensics" | "digital" | "physical" | "witness";
  name: string;
  collectedAt: string;
  collectedFrom: string;
  status: EvidenceStatus;
  addedBy: string;
  notes: string;
}

export interface TimelineEvent {
  id: string;
  date: string;
  type: EventType;
  title: string;
  description: string;
  addedBy: string;
}

export interface CaseSuspect {
  id: string;
  name: string;
  alias: string;
  status: "arrested" | "wanted" | "released" | "unknown";
  threatScore: number;
  role: string;
  notes: string;
}

export interface InvestigationTask {
  id: string;
  title: string;
  status: TaskStatus;
  assignedTo: string;
  due: string;
}

export interface InvestigationCase {
  id: string;
  firNumber: string;
  title: string;
  description: string;
  priority: CasePriority;
  status: "active" | "escalated" | "stalled" | "closed";
  openedAt: string;
  lastUpdated: string;
  daysActive: number;
  leadOfficer: string;
  leadRank: string;
  teamMembers: string[];
  district: string;
  crimeType: string;
  evidenceCount: number;
  suspectCount: number;
  witnessCount: number;
  aiScore: number;
  evidence: EvidenceItem[];
  timeline: TimelineEvent[];
  suspects: CaseSuspect[];
  tasks: InvestigationTask[];
}

// ─── Cases ────────────────────────────────────────────────────────────────────

export const INVESTIGATION_CASES: InvestigationCase[] = [
  {
    id: "case-001",
    firNumber: "FIR-2024-00847",
    title: "Armed Robbery — Sadar Bazar Jewellery Shop",
    description:
      "Armed robbery involving 3–4 suspects at Ratan Jewellers. Gold jewellery worth ₹48 Lakhs stolen. One security guard injured. Suspects fled in a white Fortuner (DL-01-XX-4782). Cross-linked to 2 prior North Delhi robberies and the Sadar Gang network.",
    priority: "critical",
    status: "active",
    openedAt: new Date(Date.now() - 2 * 86400000).toISOString(),
    lastUpdated: new Date(Date.now() - 3600000).toISOString(),
    daysActive: 2,
    leadOfficer: "SP Rajesh Kumar",
    leadRank: "Superintendent of Police",
    teamMembers: ["SI Priya Mehta", "ASI Ramesh Gupta", "HC Sanjay Yadav"],
    district: "Central Delhi",
    crimeType: "Violent Crime",
    evidenceCount: 6,
    suspectCount: 3,
    witnessCount: 4,
    aiScore: 94,
    evidence: [
      { id: "ev-001", type: "photo",   name: "CCTV — Entry Camera (Shop)",    collectedAt: new Date(Date.now() - 44 * 3600000).toISOString(), collectedFrom: "Ratan Jewellers, Camera 1",  status: "analysed",  addedBy: "SI Priya Mehta",   notes: "3 suspects clearly visible entering shop. Face 1 & 2 partially masked." },
      { id: "ev-002", type: "photo",   name: "CCTV — Street View Camera",     collectedAt: new Date(Date.now() - 44 * 3600000).toISOString(), collectedFrom: "Sadar Bazar Traffic Cam", status: "analysed",  addedBy: "SI Priya Mehta",   notes: "White Fortuner registration DL-01-XX-4782 captured at 11:22 AM approaching shop." },
      { id: "ev-003", type: "forensics",name: "Fingerprints — Partial Set",   collectedAt: new Date(Date.now() - 40 * 3600000).toISOString(), collectedFrom: "Shop Counter (glass)",    status: "pending",   addedBy: "ASI Ramesh Gupta", notes: "3 partial prints collected. Awaiting AFIS match." },
      { id: "ev-004", type: "physical", name: "Tyre Mark Impressions",        collectedAt: new Date(Date.now() - 38 * 3600000).toISOString(), collectedFrom: "Outside Ratan Jewellers", status: "analysed",  addedBy: "ASI Ramesh Gupta", notes: "Confirmed Fortuner tyre profile match. Wheel width consistent with 2020–2023 model." },
      { id: "ev-005", type: "witness",  name: "Witness Statement — Shopkeeper",collectedAt: new Date(Date.now() - 36 * 3600000).toISOString(), collectedFrom: "PS Sadar Bazar",         status: "sealed",    addedBy: "SI Priya Mehta",   notes: "Suresh Gupta identified one suspect as matching Rajan Mehta profile (70% confidence)." },
      { id: "ev-006", type: "digital",  name: "Vehicle Toll Records (NH-44)", collectedAt: new Date(Date.now() - 20 * 3600000).toISOString(), collectedFrom: "NHAI Database",          status: "analysed",  addedBy: "HC Sanjay Yadav",  notes: "DL-01-XX-4782 detected at NH-44 toll (Muradabad direction) at 1:47 PM. Likely escape route confirmed." },
    ],
    timeline: [
      { id: "tl-001", date: new Date(Date.now() - 46 * 3600000).toISOString(), type: "discovery",  title: "Robbery Reported",            description: "Security guard Ramesh raised alarm at 11:35 AM. PCR reached in 8 minutes.", addedBy: "System" },
      { id: "tl-002", date: new Date(Date.now() - 44 * 3600000).toISOString(), type: "forensics",  title: "Forensics Team Deployed",     description: "FSL team collected 3 partial fingerprints and 2 tyre mark impressions.", addedBy: "ASI Ramesh Gupta" },
      { id: "tl-003", date: new Date(Date.now() - 40 * 3600000).toISOString(), type: "lead",       title: "Vehicle Identified via CCTV", description: "White Fortuner DL-01-XX-4782 captured on traffic cam. APB issued to all checkpoints.", addedBy: "SI Priya Mehta" },
      { id: "tl-004", date: new Date(Date.now() - 28 * 3600000).toISOString(), type: "lead",       title: "Rajan Mehta Link Established","description": "Witness statement + CCTV analysis suggests Rajan Mehta (CR-2019-04821) is Suspect #1.", addedBy: "SP Rajesh Kumar" },
      { id: "tl-005", date: new Date(Date.now() - 20 * 3600000).toISOString(), type: "lead",       title: "Escape Route Confirmed",      description: "Toll data confirms vehicle headed towards Muradabad via NH-44 at 1:47 PM.", addedBy: "HC Sanjay Yadav" },
      { id: "tl-006", date: new Date(Date.now() - 8  * 3600000).toISOString(), type: "operation",  title: "Joint Operation Launched",    description: "UP STF coordination request sent. Checkpoints activated at Ghaziabad, Hapur, and Muradabad.", addedBy: "SP Rajesh Kumar" },
    ],
    suspects: [
      { id: "sp-001", name: "Rajan Mehta", alias: '"Shadow"', status: "wanted", threatScore: 87, role: "Primary Suspect — Robbery Lead", notes: "Witness ID + CCTV match 70% confidence. Active NB warrant. Last tower: Vaishali, Ghaziabad." },
      { id: "sp-002", name: "Unknown Male #2", alias: "N/A",   status: "unknown", threatScore: 60, role: "Armed Accomplice", notes: "Partial face visible on Camera 3. 5'8, heavy build, black jacket." },
      { id: "sp-003", name: "Vehicle Owner",   alias: "N/A",   status: "unknown", threatScore: 45, role: "Getaway Driver / Vehicle Procurer", notes: "DL-01-XX-4782 registered to shell company in Noida. RTO records subpoenaed." },
    ],
    tasks: [
      { id: "t-001", title: "AFIS fingerprint match report",             status: "in-progress", assignedTo: "ASI Ramesh Gupta", due: new Date(Date.now() + 12 * 3600000).toISOString() },
      { id: "t-002", title: "RTO vehicle registration investigation",    status: "in-progress", assignedTo: "HC Sanjay Yadav",  due: new Date(Date.now() + 6  * 3600000).toISOString() },
      { id: "t-003", title: "Coordinate with UP STF on Rajan Mehta",    status: "done",        assignedTo: "SP Rajesh Kumar",  due: new Date(Date.now() - 6  * 3600000).toISOString() },
      { id: "t-004", title: "Victim hospital visit & statement",         status: "done",        assignedTo: "SI Priya Mehta",   due: new Date(Date.now() - 24 * 3600000).toISOString() },
      { id: "t-005", title: "CCTV retrieval from 3 additional cameras", status: "pending",     assignedTo: "HC Sanjay Yadav",  due: new Date(Date.now() + 24 * 3600000).toISOString() },
    ],
  },
  {
    id: "case-002",
    firNumber: "FIR-2024-00844",
    title: "Missing Child — AMBER Alert Active",
    description:
      "8-year-old Ananya Singh missing from Vasant Kunj park since 3 days. AMBER alert active. Suspect vehicle (white car, partial plate DL-9C) identified on CCTV. No ransom demand. Human trafficking route cross-checked.",
    priority: "critical",
    status: "active",
    openedAt: new Date(Date.now() - 3 * 86400000).toISOString(),
    lastUpdated: new Date(Date.now() - 4 * 3600000).toISOString(),
    daysActive: 3,
    leadOfficer: "SI Meena Rawat",
    leadRank: "Sub Inspector",
    teamMembers: ["HC Rakesh Sharma", "W-SI Pooja Nair", "SHO Deepak Verma"],
    district: "South Delhi",
    crimeType: "Missing Person",
    evidenceCount: 5,
    suspectCount: 1,
    witnessCount: 3,
    aiScore: 91,
    evidence: [
      { id: "ev-007", type: "photo",    name: "CCTV — Park Entrance Gate 2",  collectedAt: new Date(Date.now() - 72 * 3600000).toISOString(), collectedFrom: "Vasant Kunj Park Camera", status: "analysed",  addedBy: "HC Rakesh Sharma", notes: "Child seen with unknown male at 4:12 PM. Male 30–35 yrs, grey shirt, sunglasses." },
      { id: "ev-008", type: "photo",    name: "Suspect Vehicle — White Sedan", collectedAt: new Date(Date.now() - 70 * 3600000).toISOString(), collectedFrom: "Vasant Marg Traffic Cam", status: "analysed",  addedBy: "HC Rakesh Sharma", notes: "Partial plate DL-9C-XX. Vehicle type: Honda City or Hyundai Verna (white, 2019–2022)." },
      { id: "ev-009", type: "witness",  name: "Witness Statement — Mother 1", collectedAt: new Date(Date.now() - 68 * 3600000).toISOString(), collectedFrom: "Park Eyewitness",         status: "sealed",    addedBy: "W-SI Pooja Nair",  notes: "Saw child talking to male near park gate. Child seemed frightened. Male held her hand and walked quickly." },
      { id: "ev-010", type: "digital",  name: "Railway Station CCTV Sweep",   collectedAt: new Date(Date.now() - 48 * 3600000).toISOString(), collectedFrom: "Hazrat Nizamuddin Stn",  status: "pending",   addedBy: "HC Rakesh Sharma", notes: "48-hr footage under review. AI facial scan in progress." },
      { id: "ev-011", type: "document", name: "AMBER Alert Broadcast Record", collectedAt: new Date(Date.now() - 70 * 3600000).toISOString(), collectedFrom: "Delhi Police HQ",         status: "sealed",    addedBy: "SHO Deepak Verma", notes: "Alert broadcast across Delhi NCR, Haryana, UP border checkpoints." },
    ],
    timeline: [
      { id: "tl-007", date: new Date(Date.now() - 72 * 3600000).toISOString(), type: "discovery",  title: "Child Reported Missing",        description: "Father Arvind Singh reported Ananya missing at 5:45 PM. FIR registered immediately.", addedBy: "SHO Deepak Verma" },
      { id: "tl-008", date: new Date(Date.now() - 70 * 3600000).toISOString(), type: "operation",  title: "AMBER Alert Activated",         description: "State-wide AMBER alert issued. All district SPs alerted. Border checkpoints activated.", addedBy: "SI Meena Rawat" },
      { id: "tl-009", date: new Date(Date.now() - 68 * 3600000).toISOString(), type: "witness",    title: "Eyewitness Account Recorded",   description: "Two mothers at park provided description of suspect and partial vehicle plate.", addedBy: "W-SI Pooja Nair" },
      { id: "tl-010", date: new Date(Date.now() - 48 * 3600000).toISOString(), type: "lead",       title: "AI Trafficking Route Analysis", description: "CrimeSphere AI flagged 3 known trafficking routes. Agra, Jaipur checkpoints prioritised.", addedBy: "SI Meena Rawat" },
      { id: "tl-011", date: new Date(Date.now() - 24 * 3600000).toISOString(), type: "forensics",  title: "Facial Scan Initiated",         description: "AI facial recognition initiated across CCTV feeds at 12 Delhi railway and bus stations.", addedBy: "HC Rakesh Sharma" },
    ],
    suspects: [
      { id: "sp-004", name: "Unknown Male", alias: "N/A", status: "unknown", threatScore: 72, role: "Primary Suspect — Abductor", notes: "Male 30–35 yrs, grey shirt, black sunglasses. White Honda City/Verna. Plate partial DL-9C." },
    ],
    tasks: [
      { id: "t-006", title: "AI facial scan — railway CCTV",            status: "in-progress", assignedTo: "HC Rakesh Sharma", due: new Date(Date.now() + 6 * 3600000).toISOString() },
      { id: "t-007", title: "RTO lookup for partial plate DL-9C",       status: "in-progress", assignedTo: "W-SI Pooja Nair",  due: new Date(Date.now() + 3 * 3600000).toISOString() },
      { id: "t-008", title: "Check NGO shelters across Delhi-NCR",      status: "done",        assignedTo: "SI Meena Rawat",   due: new Date(Date.now() - 24 * 3600000).toISOString() },
      { id: "t-009", title: "Coordinate with UP Anti-Trafficking Cell", status: "pending",     assignedTo: "SHO Deepak Verma", due: new Date(Date.now() + 12 * 3600000).toISOString() },
    ],
  },
  {
    id: "case-003",
    firNumber: "FIR-2024-00798",
    title: "Drug Network — Pune Micro-Delivery Operation",
    description:
      "Multi-month intelligence-led operation targeting Arun Singh's Pune drug distribution cell. 12 arrested, 4 kg MDMA + cannabis seized. Kingpin Arun Singh still at large. Cross-state operations active.",
    priority: "high",
    status: "active",
    openedAt: new Date(Date.now() - 5 * 86400000).toISOString(),
    lastUpdated: new Date(Date.now() - 8 * 3600000).toISOString(),
    daysActive: 5,
    leadOfficer: "DSP Ravi Patil",
    leadRank: "Deputy Superintendent of Police",
    teamMembers: ["PI Anjali Deshmukh", "SI Aman Khan", "NCB Agent Pradeep"],
    district: "Pune",
    crimeType: "Narcotics",
    evidenceCount: 7,
    suspectCount: 4,
    witnessCount: 2,
    aiScore: 88,
    evidence: [
      { id: "ev-012", type: "physical", name: "MDMA — 2.8 kg (sealed)",         collectedAt: new Date(Date.now() - 120 * 3600000).toISOString(), collectedFrom: "Koregaon Park Flat 4B", status: "sealed",    addedBy: "NCB Agent Pradeep", notes: "Lab confirmed MDMA. Street value ₹4.2 Cr." },
      { id: "ev-013", type: "physical", name: "Cannabis — 1.2 kg (sealed)",     collectedAt: new Date(Date.now() - 120 * 3600000).toISOString(), collectedFrom: "Koregaon Park Flat 4B", status: "sealed",    addedBy: "NCB Agent Pradeep", notes: "Lab confirmed cannabis indica. Compressed bricks, interstate transport suspected." },
      { id: "ev-014", type: "digital",  name: "Encrypted Chat — 14 Phones",     collectedAt: new Date(Date.now() - 118 * 3600000).toISOString(), collectedFrom: "Arrested suspects",     status: "pending",   addedBy: "PI Anjali Deshmukh", notes: "Forensic lab extracting data. Signal and Telegram encrypted messages identified." },
      { id: "ev-015", type: "document", name: "Drug Ledger — Physical Record",  collectedAt: new Date(Date.now() - 118 * 3600000).toISOString(), collectedFrom: "Flat 4B hidden drawer", status: "analysed",  addedBy: "SI Aman Khan",       notes: "Ledger shows weekly deliveries, customer codes, and amounts. 43 customers identified." },
      { id: "ev-016", type: "physical", name: "Cash — ₹3.2 Lakh (seized)",     collectedAt: new Date(Date.now() - 118 * 3600000).toISOString(), collectedFrom: "Koregaon Park Flat 4B", status: "sealed",    addedBy: "NCB Agent Pradeep", notes: "Denominations consistent with drug sale proceeds." },
      { id: "ev-017", type: "digital",  name: "Network Map (AI Generated)",     collectedAt: new Date(Date.now() - 96  * 3600000).toISOString(), collectedFrom: "CrimeSphere AI Engine",  status: "analysed",  addedBy: "DSP Ravi Patil",     notes: "AI-generated network showing connections to Mumbai, Goa, and Bengaluru distribution nodes." },
      { id: "ev-018", type: "witness",  name: "Informant Statement (Protected)",collectedAt: new Date(Date.now() - 80  * 3600000).toISOString(), collectedFrom: "Protected Location",    status: "sealed",    addedBy: "DSP Ravi Patil",     notes: "Identity protected. Confirms Arun Singh visits Pune monthly. Last visit 3 weeks ago." },
    ],
    timeline: [
      { id: "tl-012", date: new Date(Date.now() - 130 * 3600000).toISOString(), type: "operation", title: "Raid Executed — Koregaon Park", description: "Joint NCB-Pune Police raid. 12 arrested. ₹4 kg drugs + ₹3.2 lakh cash seized.", addedBy: "DSP Ravi Patil" },
      { id: "tl-013", date: new Date(Date.now() - 118 * 3600000).toISOString(), type: "forensics", title: "Lab Analysis Dispatched",       description: "Drug samples and 14 phones sent to FSL Pune. Encrypted data extraction in progress.", addedBy: "PI Anjali Deshmukh" },
      { id: "tl-014", date: new Date(Date.now() - 96  * 3600000).toISOString(), type: "lead",      title: "AI Network Analysis Complete",  description: "CrimeSphere mapped 23-node criminal network. Arun Singh confirmed as kingpin.", addedBy: "System" },
      { id: "tl-015", date: new Date(Date.now() - 72  * 3600000).toISOString(), type: "court",     title: "Remand Obtained — 14 days",     description: "All 12 accused remanded to judicial custody for 14 days.", addedBy: "DSP Ravi Patil" },
      { id: "tl-016", date: new Date(Date.now() - 48  * 3600000).toISOString(), type: "operation", title: "Arun Singh Lookout Notice",     description: "Red Corner Notice issued. Border alerts active. Interpol coordination initiated.", addedBy: "DSP Ravi Patil" },
    ],
    suspects: [
      { id: "sp-005", name: "Arun Singh",  alias: '"The Director"', status: "wanted",   threatScore: 96, role: "Kingpin — Absconding",         notes: "Interpol Red Notice issued. Believed to be in Pune or Mumbai. Network leader." },
      { id: "sp-006", name: "Manoj Yadav", alias: '"Street Boss"',  status: "arrested", threatScore: 52, role: "Street Distribution",           notes: "In custody, Arthur Road Jail. Providing partial cooperation." },
      { id: "sp-007", name: "Karan Desai", alias: "N/A",            status: "arrested", threatScore: 48, role: "Encrypted Communications Mgr",  notes: "Phone forensics in progress. Likely holds key network contact data." },
      { id: "sp-008", name: "Unknown Goa Contact", alias: "N/A",    status: "unknown",  threatScore: 55, role: "Goa Distribution Node",          notes: "Referenced in ledger as 'GC'. Identity unknown. Goa Police alerted." },
    ],
    tasks: [
      { id: "t-010", title: "FSL phone data extraction report",         status: "in-progress", assignedTo: "PI Anjali Deshmukh", due: new Date(Date.now() + 48 * 3600000).toISOString() },
      { id: "t-011", title: "Identify 43 customers from ledger",        status: "in-progress", assignedTo: "SI Aman Khan",        due: new Date(Date.now() + 72 * 3600000).toISOString() },
      { id: "t-012", title: "Interpol coordination for Arun Singh",     status: "done",        assignedTo: "DSP Ravi Patil",      due: new Date(Date.now() - 24 * 3600000).toISOString() },
      { id: "t-013", title: "Goa Police coordination re: GC contact",   status: "pending",     assignedTo: "NCB Agent Pradeep",   due: new Date(Date.now() + 24 * 3600000).toISOString() },
    ],
  },
];
