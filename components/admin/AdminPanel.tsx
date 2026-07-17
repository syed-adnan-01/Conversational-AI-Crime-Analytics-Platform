"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Users, Shield, ScrollText, Activity, Lock,
  CheckCircle2, XCircle, AlertTriangle, Wifi,
  Database, Brain, HardDrive, Zap, Search,
  Plus, Edit2, Ban, Check, X,
  ChevronRight, Clock, LogIn, LogOut,
  FileText, Settings, RefreshCcw,
} from "lucide-react";
import {
  OFFICERS, ROLES, AUDIT_LOGS, SYSTEM_METRICS,
  AUDIT_CFG, type OfficerUser,
} from "@/lib/mock-data/admin";
import { formatRelativeTime, formatDate } from "@/lib/utils";

// ─── Config ───────────────────────────────────────────────────────────────────
const USER_STATUS_CFG = {
  active:    { color: "#30d158", bg: "rgba(48,209,88,0.1)",  label: "Active"    },
  inactive:  { color: "#526080", bg: "rgba(82,96,128,0.1)",  label: "Inactive"  },
  suspended: { color: "#ff2d55", bg: "rgba(255,45,85,0.1)",  label: "Suspended" },
};

const CLEARANCE_COLOR: Record<number, string> = {
  1: "#30d158", 2: "#0070f3", 3: "#ff8c00", 4: "#bf5af2", 5: "#ff2d55",
};

const METRIC_ICONS: Record<string, React.ElementType> = {
  Wifi, Database, Brain, HardDrive, Users, Zap, Shield,
};

const METRIC_STATUS_CFG = {
  healthy:  { color: "#30d158", bg: "rgba(48,209,88,0.1)"  },
  warning:  { color: "#ffd60a", bg: "rgba(255,214,10,0.1)" },
  critical: { color: "#ff2d55", bg: "rgba(255,45,85,0.1)"  },
  offline:  { color: "#526080", bg: "rgba(82,96,128,0.1)"  },
};

type AdminSection = "users" | "roles" | "audit" | "system" | "security";

const SECTIONS: { key: AdminSection; label: string; icon: React.ElementType; badge?: number }[] = [
  { key: "users",    label: "User Management",      icon: Users,       badge: OFFICERS.length },
  { key: "roles",    label: "Roles & Permissions",  icon: Shield,      badge: ROLES.length },
  { key: "audit",    label: "Audit Logs",           icon: ScrollText,  badge: AUDIT_LOGS.length },
  { key: "system",   label: "System Health",        icon: Activity     },
  { key: "security", label: "Security Settings",    icon: Lock         },
];

function initials(name: string) {
  return name.split(" ").slice(-2).map((n) => n[0]).join("").toUpperCase();
}

// ─── Users Tab ────────────────────────────────────────────────────────────────
function UsersTab() {
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("all");

  const filtered = OFFICERS.filter((o) => {
    const q = search.toLowerCase();
    const matchQ = !q || o.name.toLowerCase().includes(q) || o.badgeNumber.toLowerCase().includes(q) || o.district.toLowerCase().includes(q);
    const matchS = filterStatus === "all" || o.status === filterStatus;
    return matchQ && matchS;
  });

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="text-base font-bold text-white">Officer Accounts</h3>
          <p className="text-xs mt-0.5" style={{ color: "#526080" }}>
            {OFFICERS.filter((o) => o.status === "active").length} active · {OFFICERS.filter((o) => o.status === "suspended").length} suspended
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold"
          style={{ background: "#0070f3", color: "white" }}>
          <Plus className="w-4 h-4" /> Add Officer
        </button>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-3 mb-5">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none" style={{ color: "#526080" }} />
          <input type="text" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search by name, badge, district…"
            className="w-full h-9 pl-9 pr-3 rounded-lg text-xs text-white outline-none"
            style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.09)" }} />
        </div>
        <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}
          className="h-9 px-3 rounded-lg text-xs text-white outline-none"
          style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.09)" }}>
          <option value="all" style={{ background: "#0d1322" }}>All Status</option>
          {["active","inactive","suspended"].map((s) => (
            <option key={s} value={s} style={{ background: "#0d1322" }}>{s.charAt(0).toUpperCase()+s.slice(1)}</option>
          ))}
        </select>
      </div>

      {/* Table */}
      <div className="rounded-xl overflow-hidden" style={{ border: "1px solid rgba(255,255,255,0.07)" }}>
        <table className="w-full text-xs">
          <thead>
            <tr style={{ background: "#0a0f1e", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
              {["Officer", "Badge No.", "Role", "District", "Clearance", "MFA", "Status", "Last Login", "Actions"].map((h) => (
                <th key={h} className="px-4 py-3 text-left font-semibold uppercase tracking-wider whitespace-nowrap"
                  style={{ color: "#2a3a55" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((o, i) => {
              const sc = USER_STATUS_CFG[o.status];
              const isLast = i === filtered.length - 1;
              return (
                <motion.tr key={o.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: i * 0.03 }}
                  className="group transition-colors cursor-pointer"
                  style={{ borderBottom: isLast ? "none" : "1px solid rgba(255,255,255,0.04)" }}
                  onMouseEnter={(e) => (e.currentTarget as HTMLTableRowElement).style.background = "rgba(255,255,255,0.025)"}
                  onMouseLeave={(e) => (e.currentTarget as HTMLTableRowElement).style.background = "transparent"}>

                  {/* Officer */}
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2.5">
                      <div className="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-bold text-white shrink-0"
                        style={{ background: `linear-gradient(135deg, ${CLEARANCE_COLOR[o.clearanceLevel]}80, ${CLEARANCE_COLOR[o.clearanceLevel]}40)`, border: `1px solid ${CLEARANCE_COLOR[o.clearanceLevel]}50` }}>
                        {o.avatar}
                      </div>
                      <div>
                        <p className="font-semibold text-white">{o.name}</p>
                        <p className="text-[10px]" style={{ color: "#2a3a55" }}>{o.email}</p>
                      </div>
                    </div>
                  </td>
                  {/* Badge */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="font-mono text-[10px]" style={{ color: "#2b91ff" }}>{o.badgeNumber}</span>
                  </td>
                  {/* Role */}
                  <td className="px-4 py-3" style={{ color: "#526080" }}>{o.role}</td>
                  {/* District */}
                  <td className="px-4 py-3 whitespace-nowrap" style={{ color: "#526080" }}>{o.district}</td>
                  {/* Clearance */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full"
                      style={{ background: `${CLEARANCE_COLOR[o.clearanceLevel]}18`, color: CLEARANCE_COLOR[o.clearanceLevel] }}>
                      L-{o.clearanceLevel}
                    </span>
                  </td>
                  {/* MFA */}
                  <td className="px-4 py-3">
                    {o.mfaEnabled
                      ? <CheckCircle2 className="w-4 h-4" style={{ color: "#30d158" }} />
                      : <XCircle     className="w-4 h-4" style={{ color: "#ff2d55" }} />}
                  </td>
                  {/* Status */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full flex items-center gap-1 w-fit"
                      style={{ background: sc.bg, color: sc.color }}>
                      <span className="w-1.5 h-1.5 rounded-full" style={{ background: sc.color }} />
                      {sc.label}
                    </span>
                  </td>
                  {/* Last Login */}
                  <td className="px-4 py-3 whitespace-nowrap text-[10px]" style={{ color: "#2a3a55" }}>
                    {formatRelativeTime(o.lastLogin)}
                  </td>
                  {/* Actions */}
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button className="p-1.5 rounded-md hover:bg-white/5 transition-colors" title="Edit">
                        <Edit2 className="w-3 h-3" style={{ color: "#526080" }} />
                      </button>
                      <button className="p-1.5 rounded-md hover:bg-red-500/10 transition-colors" title="Suspend">
                        <Ban className="w-3 h-3" style={{ color: "#526080" }} />
                      </button>
                    </div>
                  </td>
                </motion.tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ─── Roles Tab ────────────────────────────────────────────────────────────────
function RolesTab() {
  const [selectedRole, setSelectedRole] = useState(ROLES[0]);

  return (
    <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
      {/* Left: Role list */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-white mb-1">Roles ({ROLES.length})</h3>
        {ROLES.map((role) => (
          <button key={role.id} onClick={() => setSelectedRole(role)}
            className="w-full text-left rounded-xl p-4 transition-all"
            style={{
              background: selectedRole.id === role.id ? `${role.color}10` : "rgba(255,255,255,0.025)",
              border: selectedRole.id === role.id ? `1.5px solid ${role.color}40` : "1px solid rgba(255,255,255,0.07)",
            }}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-bold text-white">{role.name}</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full"
                style={{ background: `${role.color}18`, color: role.color }}>L-{role.level}</span>
            </div>
            <p className="text-xs mb-2" style={{ color: "#526080" }}>{role.description}</p>
            <div className="flex items-center gap-1 text-[10px]" style={{ color: "#2a3a55" }}>
              <Users className="w-3 h-3" />
              {role.userCount} officer{role.userCount !== 1 ? "s" : ""}
            </div>
          </button>
        ))}
      </div>

      {/* Right: Permissions matrix */}
      <div className="xl:col-span-2">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-bold text-white">{selectedRole.name} — Permissions</h3>
          <button className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg"
            style={{ background: "rgba(0,112,243,0.1)", border: "1px solid rgba(0,112,243,0.2)", color: "#2b91ff" }}>
            <Edit2 className="w-3 h-3" /> Edit Role
          </button>
        </div>
        <div className="rounded-xl overflow-hidden" style={{ border: "1px solid rgba(255,255,255,0.07)" }}>
          <table className="w-full text-xs">
            <thead>
              <tr style={{ background: "#0a0f1e", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
                {["Module", "Read", "Write", "Admin"].map((h) => (
                  <th key={h} className="px-4 py-3 text-left font-semibold uppercase tracking-wider"
                    style={{ color: "#2a3a55" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {selectedRole.permissions.map((perm, i) => (
                <tr key={perm.module} style={{ borderBottom: i < selectedRole.permissions.length - 1 ? "1px solid rgba(255,255,255,0.04)" : "none" }}>
                  <td className="px-4 py-3 font-medium text-white">{perm.module}</td>
                  {[perm.read, perm.write, perm.admin].map((val, j) => (
                    <td key={j} className="px-4 py-3">
                      {val
                        ? <Check className="w-4 h-4" style={{ color: "#30d158" }} />
                        : <X    className="w-4 h-4" style={{ color: "#2a3a55" }} />}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// ─── Audit Tab ────────────────────────────────────────────────────────────────
function AuditTab() {
  return (
    <div>
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="text-base font-bold text-white">Audit Logs</h3>
          <p className="text-xs mt-0.5" style={{ color: "#526080" }}>
            All system events · {AUDIT_LOGS.filter((l) => !l.success).length} security events
          </p>
        </div>
        <button className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg"
          style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.09)", color: "#526080" }}>
          <RefreshCcw className="w-3 h-3" /> Refresh
        </button>
      </div>
      <div className="space-y-2">
        {AUDIT_LOGS.map((log, i) => {
          const cfg = AUDIT_CFG[log.action];
          return (
            <motion.div key={log.id} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }}
              className="flex items-start gap-3 rounded-xl p-3.5"
              style={{
                background: !log.success ? "rgba(255,45,85,0.05)" : "rgba(255,255,255,0.025)",
                border: `1px solid ${!log.success ? "rgba(255,45,85,0.2)" : "rgba(255,255,255,0.06)"}`,
              }}>
              {/* Status dot */}
              <span className="w-2 h-2 rounded-full mt-1.5 shrink-0"
                style={{ background: log.success ? cfg.color : "#ff2d55" }} />

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-0.5 flex-wrap">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full"
                    style={{ background: `${cfg.color}18`, color: cfg.color }}>{cfg.label}</span>
                  <span className="text-xs font-semibold text-white">{log.userName}</span>
                  <span className="text-[10px]" style={{ color: "#526080" }}>·</span>
                  <span className="text-[10px]" style={{ color: "#526080" }}>{log.module}</span>
                  {!log.success && (
                    <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full"
                      style={{ background: "rgba(255,45,85,0.15)", color: "#ff2d55" }}>SECURITY EVENT</span>
                  )}
                </div>
                <p className="text-xs leading-snug" style={{ color: "#94a3c0" }}>{log.description}</p>
                <div className="flex items-center gap-3 mt-1 text-[10px]" style={{ color: "#2a3a55" }}>
                  <span className="flex items-center gap-1"><Clock className="w-2.5 h-2.5" />{formatRelativeTime(log.timestamp)}</span>
                  <span>IP: {log.ip}</span>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

// ─── System Health Tab ────────────────────────────────────────────────────────
function SystemTab() {
  return (
    <div>
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="text-base font-bold text-white">System Health</h3>
          <p className="text-xs mt-0.5" style={{ color: "#526080" }}>
            Live monitoring · CrimeSphere AI Platform v2.4.1
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          <span className="text-xs" style={{ color: "#30d158" }}>All core systems nominal</span>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-6">
        {SYSTEM_METRICS.map((m, i) => {
          const Icon = METRIC_ICONS[m.icon] ?? Activity;
          const sc   = METRIC_STATUS_CFG[m.status];
          return (
            <motion.div key={m.id} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.06 }}
              className="rounded-xl p-4"
              style={{ background: "#0d1322", border: `1px solid ${m.status !== "healthy" ? sc.color + "40" : "rgba(255,255,255,0.07)"}` }}>
              <div className="flex items-start justify-between mb-3">
                <div className="w-9 h-9 rounded-lg flex items-center justify-center"
                  style={{ background: sc.bg, border: `1px solid ${sc.color}30` }}>
                  <Icon className="w-4 h-4" style={{ color: sc.color }} />
                </div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full"
                  style={{ background: sc.bg, color: sc.color }}>
                  {m.status.charAt(0).toUpperCase() + m.status.slice(1)}
                </span>
              </div>
              <div className="text-2xl font-bold text-white mb-0.5 tabular-nums">
                {m.value}<span className="text-xs font-normal text-gray-500 ml-0.5">{m.unit}</span>
              </div>
              <div className="text-xs font-semibold text-white mb-1">{m.label}</div>
              <div className="text-[10px]" style={{ color: "#2a3a55" }}>{m.detail}</div>
              {m.trend && <div className="text-[10px] mt-1" style={{ color: sc.color }}>{m.trend}</div>}
            </motion.div>
          );
        })}
      </div>

      {/* Server info table */}
      <div className="rounded-xl overflow-hidden" style={{ background: "#0d1322", border: "1px solid rgba(255,255,255,0.07)" }}>
        <div className="px-5 py-4" style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
          <h4 className="text-sm font-bold text-white">Infrastructure Details</h4>
        </div>
        <div className="p-5 grid grid-cols-2 md:grid-cols-3 gap-4">
          {[
            { label: "Platform",      value: "CrimeSphere AI v2.4.1" },
            { label: "Environment",   value: "Production — Tier 1" },
            { label: "Region",        value: "ap-south-1 (Mumbai)" },
            { label: "Node.js",       value: "v24.x LTS" },
            { label: "Next.js",       value: "16.2.10" },
            { label: "AI Runtime",    value: "CUDA 12.3 · A100 80GB" },
            { label: "Last Deploy",   value: "July 15, 2024 — 02:30 IST" },
            { label: "SSL Cert",      value: "Valid until Dec 2025" },
            { label: "Data Centre",   value: "NIC — New Delhi (Primary)" },
          ].map(({ label, value }) => (
            <div key={label}>
              <p className="text-[10px] uppercase tracking-widest mb-0.5" style={{ color: "#2a3a55" }}>{label}</p>
              <p className="text-xs text-white font-medium">{value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── Security Tab ─────────────────────────────────────────────────────────────
function SecurityTab() {
  const failedLogins = AUDIT_LOGS.filter((l) => l.action === "failed-login").length;
  const mfaEnabled   = OFFICERS.filter((o) => o.mfaEnabled).length;
  const mfaPct       = Math.round((mfaEnabled / OFFICERS.length) * 100);

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-base font-bold text-white mb-4">Security Overview</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { label: "Failed Logins (24h)", value: failedLogins, color: "#ff2d55", icon: XCircle,      note: "1 IP blocked" },
            { label: "MFA Coverage",        value: `${mfaPct}%`, color: mfaPct >= 80 ? "#30d158" : "#ff8c00", icon: Shield, note: `${mfaEnabled}/${OFFICERS.length} officers` },
            { label: "Active Sessions",     value: 9,            color: "#0070f3", icon: Users,         note: "Avg session: 2.4 hrs" },
          ].map(({ label, value, color, icon: Icon, note }) => (
            <div key={label} className="rounded-xl p-4" style={{ background: "#0d1322", border: "1px solid rgba(255,255,255,0.07)" }}>
              <div className="flex items-center gap-2 mb-2">
                <Icon className="w-4 h-4" style={{ color }} />
                <span className="text-xs" style={{ color: "#526080" }}>{label}</span>
              </div>
              <div className="text-2xl font-bold tabular-nums" style={{ color }}>{value}</div>
              <div className="text-[10px] mt-1" style={{ color: "#2a3a55" }}>{note}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Policy settings */}
      <div className="rounded-xl overflow-hidden" style={{ border: "1px solid rgba(255,255,255,0.07)" }}>
        <div className="px-5 py-4" style={{ background: "#0a0f1e", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
          <h4 className="text-sm font-bold text-white">Security Policy Configuration</h4>
        </div>
        <div className="divide-y" style={{ borderColor: "rgba(255,255,255,0.05)" }}>
          {[
            { label: "Multi-Factor Authentication",     desc: "Require MFA for all Level 3+ officers",      enabled: true  },
            { label: "Session Timeout",                 desc: "Auto-logout after 30 min idle",              enabled: true  },
            { label: "IP Allowlist",                    desc: "Restrict login to government network IPs",   enabled: true  },
            { label: "Password Complexity",             desc: "Min 12 chars with special characters",       enabled: true  },
            { label: "Audit Log Retention (365 days)",  desc: "All events logged and retained for 1 year",  enabled: true  },
            { label: "Auto-Lock Suspended Accounts",   desc: "Suspended accounts lose API token access",   enabled: true  },
            { label: "Geo-Restriction Login",          desc: "Block logins outside India",                 enabled: false },
            { label: "AI Anomaly Detection",           desc: "Flag unusual access patterns via AI",        enabled: true  },
          ].map(({ label, desc, enabled }) => (
            <div key={label} className="flex items-center justify-between px-5 py-3.5">
              <div>
                <p className="text-xs font-semibold text-white">{label}</p>
                <p className="text-[10px] mt-0.5" style={{ color: "#526080" }}>{desc}</p>
              </div>
              <div className="flex items-center gap-2 shrink-0 ml-4">
                {enabled
                  ? <CheckCircle2 className="w-4 h-4" style={{ color: "#30d158" }} />
                  : <XCircle      className="w-4 h-4" style={{ color: "#2a3a55" }} />}
                <span className="text-[10px] font-semibold" style={{ color: enabled ? "#30d158" : "#2a3a55" }}>
                  {enabled ? "Enabled" : "Disabled"}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Blocked IPs */}
      <div className="rounded-xl p-4" style={{ background: "rgba(255,45,85,0.05)", border: "1px solid rgba(255,45,85,0.2)" }}>
        <div className="flex items-center gap-2 mb-3">
          <AlertTriangle className="w-4 h-4" style={{ color: "#ff2d55" }} />
          <span className="text-xs font-bold" style={{ color: "#ff2d55" }}>Blocked IP Addresses (1)</span>
        </div>
        <div className="flex items-center justify-between text-xs rounded-lg px-3 py-2.5"
          style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
          <span className="font-mono text-white">192.168.2.99</span>
          <span style={{ color: "#526080" }}>3 failed logins · blocked 80 min ago</span>
          <button className="text-[10px] px-2 py-0.5 rounded" style={{ background: "rgba(255,45,85,0.15)", color: "#ff2d55" }}>
            Unblock
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────
export default function AdminPanel() {
  const [activeSection, setActiveSection] = useState<AdminSection>("users");

  const CONTENT: Record<AdminSection, React.ReactNode> = {
    users:    <UsersTab    />,
    roles:    <RolesTab    />,
    audit:    <AuditTab    />,
    system:   <SystemTab   />,
    security: <SecurityTab />,
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] -m-6 overflow-hidden">

      {/* ═══ LEFT: Admin nav ═══ */}
      <div className="hidden lg:flex w-[240px] shrink-0 flex-col"
        style={{ background: "#0a0f1e", borderRight: "1px solid rgba(255,255,255,0.06)" }}>
        <div className="px-4 py-5 shrink-0" style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
          <div className="flex items-center gap-2.5 mb-1">
            <div className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{ background: "rgba(255,45,85,0.12)", border: "1px solid rgba(255,45,85,0.25)" }}>
              <Settings className="w-4 h-4" style={{ color: "#ff2d55" }} />
            </div>
            <div>
              <p className="text-sm font-bold text-white">Admin Panel</p>
              <p className="text-[10px]" style={{ color: "#2a3a55" }}>Clearance Level 5</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1">
          {SECTIONS.map(({ key, label, icon: Icon, badge }) => {
            const isActive = activeSection === key;
            return (
              <button key={key} onClick={() => setActiveSection(key)}
                className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all text-left"
                style={{
                  background: isActive ? "rgba(255,45,85,0.1)" : "transparent",
                  border: isActive ? "1px solid rgba(255,45,85,0.22)" : "1px solid transparent",
                  color: isActive ? "white" : "#526080",
                }}>
                <Icon className="w-4 h-4 shrink-0" style={{ color: isActive ? "#ff2d55" : "inherit" }} />
                <span className="flex-1 truncate">{label}</span>
                {badge !== undefined && (
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full"
                    style={{ background: isActive ? "rgba(255,45,85,0.2)" : "rgba(255,255,255,0.07)", color: isActive ? "#ff2d55" : "#526080" }}>
                    {badge}
                  </span>
                )}
                {isActive && <ChevronRight className="w-3 h-3 shrink-0" style={{ color: "#ff2d55" }} />}
              </button>
            );
          })}
        </nav>

        {/* Admin badge */}
        <div className="mx-3 mb-3 rounded-xl p-3" style={{ background: "rgba(255,45,85,0.07)", border: "1px solid rgba(255,45,85,0.18)" }}>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-bold text-white"
              style={{ background: "linear-gradient(135deg, #ff2d55, #ff8c00)" }}>AS</div>
            <div>
              <p className="text-[11px] font-semibold text-white">Admin Sys</p>
              <p className="text-[10px]" style={{ color: "#2a3a55" }}>Level 5 — Top Secret</p>
            </div>
          </div>
          <div className="text-[9px] text-center py-1 rounded-md font-bold uppercase tracking-wider"
            style={{ background: "rgba(255,45,85,0.15)", color: "#ff2d55" }}>
            Administrator Access
          </div>
        </div>
      </div>

      {/* ═══ MAIN: Content ═══ */}
      <div className="flex-1 overflow-y-auto p-8 min-w-0" style={{ background: "#080b12" }}>
        <AnimatePresence mode="wait">
          <motion.div key={activeSection}
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.2 }}>
            {CONTENT[activeSection]}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
