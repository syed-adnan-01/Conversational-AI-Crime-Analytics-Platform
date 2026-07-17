// ─── Admin Panel Mock Data ────────────────────────────────────────────────────

export type UserStatus   = "active" | "inactive" | "suspended";
export type ClearanceLevel = 1 | 2 | 3 | 4 | 5;
export type AuditAction  = "login" | "logout" | "report" | "case-update" | "user-mgmt" | "config" | "alert" | "export" | "failed-login";

export interface OfficerUser {
  id: string;
  name: string;
  email: string;
  badgeNumber: string;
  rank: string;
  role: string;
  district: string;
  state: string;
  clearanceLevel: ClearanceLevel;
  status: UserStatus;
  lastLogin: string;
  joinedAt: string;
  mfaEnabled: boolean;
  avatar: string; // initials
}

export interface Role {
  id: string;
  name: string;
  level: ClearanceLevel;
  userCount: number;
  color: string;
  description: string;
  permissions: { module: string; read: boolean; write: boolean; admin: boolean }[];
}

export interface AuditLog {
  id: string;
  timestamp: string;
  userId: string;
  userName: string;
  action: AuditAction;
  description: string;
  module: string;
  ip: string;
  success: boolean;
}

export interface SystemMetric {
  id: string;
  label: string;
  value: string;
  unit: string;
  status: "healthy" | "warning" | "critical" | "offline";
  detail: string;
  icon: string;
  trend?: string;
}

// ─── Officers ─────────────────────────────────────────────────────────────────

export const OFFICERS: OfficerUser[] = [
  { id: "u1", name: "SP Rajesh Kumar",     email: "rajesh.kumar@crimesphere.gov.in",    badgeNumber: "IPS-2024-0042", rank: "Superintendent of Police",          role: "Senior Investigator", district: "Central Delhi",   state: "Delhi",          clearanceLevel: 3, status: "active",    lastLogin: new Date(Date.now() - 30  * 60000).toISOString(), joinedAt: "2024-01-15", mfaEnabled: true,  avatar: "RK" },
  { id: "u2", name: "DySP Priya Sharma",   email: "priya.sharma@crimesphere.gov.in",    badgeNumber: "IPS-2023-0189", rank: "Deputy Superintendent of Police",    role: "Cyber Crime Lead",    district: "Mumbai Suburban", state: "Maharashtra",    clearanceLevel: 3, status: "active",    lastLogin: new Date(Date.now() - 2   * 3600000).toISOString(), joinedAt: "2023-06-10", mfaEnabled: true,  avatar: "PS" },
  { id: "u3", name: "DSP Ravi Patil",      email: "ravi.patil@crimesphere.gov.in",      badgeNumber: "MH-2021-0334",  rank: "Deputy Superintendent of Police",    role: "Narcotics Lead",      district: "Pune",            state: "Maharashtra",    clearanceLevel: 3, status: "active",    lastLogin: new Date(Date.now() - 6   * 3600000).toISOString(), joinedAt: "2021-03-22", mfaEnabled: true,  avatar: "RP" },
  { id: "u4", name: "PI Anjali Deshmukh",  email: "anjali.deshmukh@crimesphere.gov.in", badgeNumber: "MH-2022-0512",  rank: "Police Inspector",                   role: "Investigator",        district: "Pune",            state: "Maharashtra",    clearanceLevel: 2, status: "active",    lastLogin: new Date(Date.now() - 1   * 3600000).toISOString(), joinedAt: "2022-07-01", mfaEnabled: true,  avatar: "AD" },
  { id: "u5", name: "SI Meena Rawat",      email: "meena.rawat@crimesphere.gov.in",     badgeNumber: "DL-2023-0671",  rank: "Sub Inspector",                      role: "Field Officer",       district: "South Delhi",     state: "Delhi",          clearanceLevel: 1, status: "active",    lastLogin: new Date(Date.now() - 4   * 3600000).toISOString(), joinedAt: "2023-09-15", mfaEnabled: false, avatar: "MR" },
  { id: "u6", name: "DSP Kavitha Nair",    email: "kavitha.nair@crimesphere.gov.in",    badgeNumber: "KA-2020-0112",  rank: "Deputy Superintendent of Police",    role: "Financial Crime Lead",district: "Bengaluru Urban", state: "Karnataka",      clearanceLevel: 3, status: "active",    lastLogin: new Date(Date.now() - 8   * 3600000).toISOString(), joinedAt: "2020-11-30", mfaEnabled: true,  avatar: "KN" },
  { id: "u7", name: "ASI Ramesh Gupta",    email: "ramesh.gupta@crimesphere.gov.in",    badgeNumber: "DL-2019-0891",  rank: "Assistant Sub Inspector",            role: "Forensics",           district: "Central Delhi",   state: "Delhi",          clearanceLevel: 1, status: "active",    lastLogin: new Date(Date.now() - 12  * 3600000).toISOString(), joinedAt: "2019-04-18", mfaEnabled: false, avatar: "RG" },
  { id: "u8", name: "SP Vikram Singh",     email: "vikram.singh@crimesphere.gov.in",    badgeNumber: "JK-2022-0047",  rank: "Superintendent of Police",          role: "Counter-Terrorism",   district: "Jammu",           state: "J&K",            clearanceLevel: 4, status: "active",    lastLogin: new Date(Date.now() - 24  * 3600000).toISOString(), joinedAt: "2022-01-01", mfaEnabled: true,  avatar: "VS" },
  { id: "u9", name: "Analyst Siddharth",   email: "siddharth.m@crimesphere.gov.in",     badgeNumber: "SYS-2024-0008", rank: "Data Analyst",                       role: "Crime Analyst",       district: "HQ — New Delhi",  state: "Delhi",          clearanceLevel: 2, status: "active",    lastLogin: new Date(Date.now() - 3   * 3600000).toISOString(), joinedAt: "2024-03-01", mfaEnabled: true,  avatar: "SM" },
  { id: "u10",name: "HC Sanjay Yadav",     email: "sanjay.yadav@crimesphere.gov.in",    badgeNumber: "DL-2018-1102",  rank: "Head Constable",                     role: "Field Officer",       district: "Central Delhi",   state: "Delhi",          clearanceLevel: 1, status: "inactive",  lastLogin: new Date(Date.now() - 72  * 3600000).toISOString(), joinedAt: "2018-09-05", mfaEnabled: false, avatar: "SY" },
  { id: "u11",name: "PI Fatima Sheikh",    email: "fatima.sheikh@crimesphere.gov.in",   badgeNumber: "MH-2020-0744",  rank: "Police Inspector",                   role: "Investigator",        district: "Mumbai City",     state: "Maharashtra",    clearanceLevel: 2, status: "suspended", lastLogin: new Date(Date.now() - 120 * 3600000).toISOString(), joinedAt: "2020-05-20", mfaEnabled: false, avatar: "FS" },
  { id: "u12",name: "Admin Sys",           email: "admin@crimesphere.gov.in",           badgeNumber: "SYS-0000-0001", rank: "System Administrator",               role: "Administrator",       district: "HQ — New Delhi",  state: "Delhi",          clearanceLevel: 5, status: "active",    lastLogin: new Date(Date.now() - 1   * 3600000).toISOString(), joinedAt: "2023-01-01", mfaEnabled: true,  avatar: "AS" },
];

// ─── Roles ────────────────────────────────────────────────────────────────────

export const ROLES: Role[] = [
  {
    id: "role-1", name: "System Administrator", level: 5, userCount: 1, color: "#ff2d55",
    description: "Full system access. Can manage users, roles, configuration, and audit logs.",
    permissions: [
      { module: "Dashboard",       read: true,  write: true,  admin: true },
      { module: "FIR Search",      read: true,  write: true,  admin: true },
      { module: "AI Crime Chat",   read: true,  write: true,  admin: true },
      { module: "Investigation",   read: true,  write: true,  admin: true },
      { module: "Analytics",       read: true,  write: true,  admin: true },
      { module: "Reports",         read: true,  write: true,  admin: true },
      { module: "Criminal Network",read: true,  write: true,  admin: true },
      { module: "Admin Panel",     read: true,  write: true,  admin: true },
    ],
  },
  {
    id: "role-2", name: "Senior Investigator (L3)", level: 3, userCount: 4, color: "#ff8c00",
    description: "Full investigative access. Can create reports, manage cases, and access network data.",
    permissions: [
      { module: "Dashboard",       read: true,  write: true,  admin: false },
      { module: "FIR Search",      read: true,  write: true,  admin: false },
      { module: "AI Crime Chat",   read: true,  write: true,  admin: false },
      { module: "Investigation",   read: true,  write: true,  admin: false },
      { module: "Analytics",       read: true,  write: false, admin: false },
      { module: "Reports",         read: true,  write: true,  admin: false },
      { module: "Criminal Network",read: true,  write: true,  admin: false },
      { module: "Admin Panel",     read: false, write: false, admin: false },
    ],
  },
  {
    id: "role-3", name: "Investigator (L2)", level: 2, userCount: 3, color: "#0070f3",
    description: "Standard investigative access. Can update cases and generate reports.",
    permissions: [
      { module: "Dashboard",       read: true,  write: false, admin: false },
      { module: "FIR Search",      read: true,  write: true,  admin: false },
      { module: "AI Crime Chat",   read: true,  write: true,  admin: false },
      { module: "Investigation",   read: true,  write: true,  admin: false },
      { module: "Analytics",       read: true,  write: false, admin: false },
      { module: "Reports",         read: true,  write: false, admin: false },
      { module: "Criminal Network",read: true,  write: false, admin: false },
      { module: "Admin Panel",     read: false, write: false, admin: false },
    ],
  },
  {
    id: "role-4", name: "Field Officer (L1)", level: 1, userCount: 3, color: "#30d158",
    description: "Limited access. Can view dashboards and update assigned cases only.",
    permissions: [
      { module: "Dashboard",       read: true,  write: false, admin: false },
      { module: "FIR Search",      read: true,  write: false, admin: false },
      { module: "AI Crime Chat",   read: true,  write: false, admin: false },
      { module: "Investigation",   read: true,  write: false, admin: false },
      { module: "Analytics",       read: false, write: false, admin: false },
      { module: "Reports",         read: false, write: false, admin: false },
      { module: "Criminal Network",read: false, write: false, admin: false },
      { module: "Admin Panel",     read: false, write: false, admin: false },
    ],
  },
];

// ─── Audit Logs ───────────────────────────────────────────────────────────────

export const AUDIT_LOGS: AuditLog[] = [
  { id: "al-01", timestamp: new Date(Date.now() - 5   * 60000).toISOString(),  userId: "u1",  userName: "SP Rajesh Kumar",   action: "case-update",  description: "Updated status of FIR-2024-00847 — suspect identified",          module: "Investigation",    ip: "10.2.14.88",  success: true  },
  { id: "al-02", timestamp: new Date(Date.now() - 15  * 60000).toISOString(),  userId: "u2",  userName: "DySP Priya Sharma", action: "report",       description: "Generated Q2 2024 Crime Analytics Report (22 pages)",            module: "Reports",          ip: "10.2.14.91",  success: true  },
  { id: "al-03", timestamp: new Date(Date.now() - 28  * 60000).toISOString(),  userId: "u9",  userName: "Analyst Siddharth", action: "login",        description: "Successful login via MFA — device: Windows PC",                  module: "Auth",             ip: "10.2.14.55",  success: true  },
  { id: "al-04", timestamp: new Date(Date.now() - 45  * 60000).toISOString(),  userId: "u3",  userName: "DSP Ravi Patil",    action: "export",       description: "Exported Criminal Network Report for Arun Singh (PDF)",          module: "Reports",          ip: "10.5.12.44",  success: true  },
  { id: "al-05", timestamp: new Date(Date.now() - 62  * 60000).toISOString(),  userId: "u4",  userName: "PI Anjali Deshmukh",action: "case-update",  description: "Added 2 evidence items to FIR-2024-00798",                       module: "Investigation",    ip: "10.5.12.51",  success: true  },
  { id: "al-06", timestamp: new Date(Date.now() - 80  * 60000).toISOString(),  userId: "?",   userName: "Unknown",           action: "failed-login", description: "Failed login attempt for rajesh.kumar@crimesphere.gov.in — IP blocked after 3 tries", module: "Auth", ip: "192.168.2.99", success: false },
  { id: "al-07", timestamp: new Date(Date.now() - 95  * 60000).toISOString(),  userId: "u12", userName: "Admin Sys",         action: "user-mgmt",    description: "Suspended account for PI Fatima Sheikh — reason: policy violation", module: "Admin",           ip: "10.2.14.10",  success: true  },
  { id: "al-08", timestamp: new Date(Date.now() - 110 * 60000).toISOString(),  userId: "u6",  userName: "DSP Kavitha Nair",  action: "alert",        description: "Acknowledged critical alert — FIR-2024-00847 armed robbery",     module: "Dashboard",        ip: "10.3.11.77",  success: true  },
  { id: "al-09", timestamp: new Date(Date.now() - 130 * 60000).toISOString(),  userId: "u8",  userName: "SP Vikram Singh",   action: "config",       description: "Updated district alert thresholds — Jammu zone to HIGH",         module: "Admin",            ip: "10.7.14.22",  success: true  },
  { id: "al-10", timestamp: new Date(Date.now() - 150 * 60000).toISOString(),  userId: "u1",  userName: "SP Rajesh Kumar",   action: "login",        description: "Successful login via MFA — device: Windows PC",                  module: "Auth",             ip: "10.2.14.88",  success: true  },
  { id: "al-11", timestamp: new Date(Date.now() - 180 * 60000).toISOString(),  userId: "u5",  userName: "SI Meena Rawat",    action: "case-update",  description: "Updated FIR-2024-00844 — AMBER alert status extended 72 hours",  module: "Investigation",    ip: "10.2.15.10",  success: true  },
  { id: "al-12", timestamp: new Date(Date.now() - 200 * 60000).toISOString(),  userId: "u2",  userName: "DySP Priya Sharma", action: "logout",       description: "Session terminated — idle timeout (30 min)",                     module: "Auth",             ip: "10.2.14.91",  success: true  },
];

// ─── System Metrics ───────────────────────────────────────────────────────────

export const SYSTEM_METRICS: SystemMetric[] = [
  { id: "m1", label: "API Gateway",       value: "45",     unit: "ms",    status: "healthy",  detail: "Avg response time · 99.98% uptime",       icon: "Wifi",         trend: "▼ 3ms from last hour" },
  { id: "m2", label: "Database",          value: "99.97",  unit: "%",     status: "healthy",  detail: "PostgreSQL 15 · 128 GB allocated",        icon: "Database",     trend: "12,400 active records" },
  { id: "m3", label: "AI Model",          value: "94.7",   unit: "%",     status: "healthy",  detail: "CrimeSphere GPT-L v2.4 · CUDA enabled",   icon: "Brain",        trend: "1,203 signals/min" },
  { id: "m4", label: "Active Sessions",   value: "9",      unit: "",      status: "healthy",  detail: "9 of 500 licensed seats in use",           icon: "Users",        trend: "Peak today: 14" },
  { id: "m5", label: "Storage",           value: "68",     unit: "%",     status: "warning",  detail: "2.7 TB used of 4 TB allocated",            icon: "HardDrive",    trend: "▲ 4% from last week" },
  { id: "m6", label: "Cache (Redis)",     value: "Online", unit: "",      status: "healthy",  detail: "Hit rate 98.4% · 0.1ms latency",           icon: "Zap",          trend: "12,847 keys cached" },
  { id: "m7", label: "Firewall",          value: "Active", unit: "",      status: "healthy",  detail: "47 blocked IPs · 0 active threats",        icon: "Shield",       trend: "Last threat blocked 6h ago" },
  { id: "m8", label: "Backup Status",     value: "Failed", unit: "",      status: "critical", detail: "Last successful backup: 26 hrs ago",       icon: "HardDrive",    trend: "⚠ Manual backup required" },
];

// ─── Action config for audit ──────────────────────────────────────────────────

export const AUDIT_CFG: Record<AuditLog["action"], { color: string; label: string }> = {
  "login":        { color: "#30d158", label: "Login"        },
  "logout":       { color: "#526080", label: "Logout"       },
  "report":       { color: "#bf5af2", label: "Report"       },
  "case-update":  { color: "#0070f3", label: "Case Update"  },
  "user-mgmt":    { color: "#ff8c00", label: "User Mgmt"    },
  "config":       { color: "#ffd60a", label: "Config"       },
  "alert":        { color: "#ff8c00", label: "Alert"        },
  "export":       { color: "#0070f3", label: "Export"       },
  "failed-login": { color: "#ff2d55", label: "Failed Login" },
};
