"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Folder, FileText, Camera, Video, FlaskConical, Monitor,
  Package, User, Clock, Shield, Brain, CheckCircle2,
  Circle, Loader2, ChevronRight, AlertTriangle, Search,
  Users, Paperclip, ListChecks, CalendarClock, Star,
} from "lucide-react";
import { INVESTIGATION_CASES, type InvestigationCase, type EvidenceItem, type TimelineEvent, type CaseSuspect, type InvestigationTask } from "@/lib/mock-data/investigation";
import { formatRelativeTime, formatDate } from "@/lib/utils";

// ─── Config ───────────────────────────────────────────────────────────────────

const PRIORITY_CFG = {
  critical: { color: "#ff2d55", bg: "rgba(255,45,85,0.12)", label: "Critical" },
  high:     { color: "#ff8c00", bg: "rgba(255,140,0,0.12)",  label: "High" },
  medium:   { color: "#ffd60a", bg: "rgba(255,214,10,0.12)", label: "Medium" },
  low:      { color: "#30d158", bg: "rgba(48,209,88,0.12)",  label: "Low" },
};

const EVIDENCE_ICONS: Record<EvidenceItem["type"], React.ElementType> = {
  document: FileText, photo: Camera, video: Video, forensics: FlaskConical,
  digital: Monitor, physical: Package, witness: User,
};

const EVIDENCE_COLORS: Record<EvidenceItem["type"], string> = {
  document: "#0070f3", photo: "#bf5af2", video: "#ff8c00", forensics: "#30d158",
  digital: "#ffd60a", physical: "#526080", witness: "#ff2d55",
};

const EV_STATUS_CFG = {
  analysed:    { color: "#30d158", label: "Analysed" },
  pending:     { color: "#ffd60a", label: "Pending" },
  contaminated:{ color: "#ff2d55", label: "Contaminated" },
  sealed:      { color: "#0070f3", label: "Sealed" },
};

const EVENT_CFG: Record<TimelineEvent["type"], { color: string; icon: React.ElementType }> = {
  discovery:  { color: "#ff2d55", icon: AlertTriangle },
  arrest:     { color: "#30d158", icon: Shield },
  forensics:  { color: "#bf5af2", icon: FlaskConical },
  lead:       { color: "#0070f3", icon: Brain },
  court:      { color: "#ffd60a", icon: FileText },
  operation:  { color: "#ff8c00", icon: Star },
  witness:    { color: "#526080", icon: User },
};

const SUSPECT_STATUS = {
  wanted:   { color: "#ff2d55", label: "Wanted" },
  arrested: { color: "#30d158", label: "Arrested" },
  released: { color: "#ff8c00", label: "Released" },
  unknown:  { color: "#ffd60a", label: "Unknown" },
};

const TASK_STATUS = {
  "done":        { icon: CheckCircle2, color: "#30d158" },
  "in-progress": { icon: Loader2,      color: "#ffd60a" },
  "pending":     { icon: Circle,       color: "#526080" },
};

function initials(name: string) {
  return name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2);
}

// ─── Sub-tabs ─────────────────────────────────────────────────────────────────

function OverviewTab({ c }: { c: InvestigationCase }) {
  const p = PRIORITY_CFG[c.priority];
  const done  = c.tasks.filter((t) => t.status === "done").length;
  const total = c.tasks.length;

  return (
    <div className="space-y-5">
      {/* AI Score banner */}
      <div className="rounded-xl p-4" style={{ background: "rgba(191,90,242,0.07)", border: "1px solid rgba(191,90,242,0.2)" }}>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Brain className="w-3.5 h-3.5" style={{ color: "#bf5af2" }} />
            <span className="text-xs font-bold" style={{ color: "#bf5af2" }}>AI Case Score</span>
          </div>
          <span className="text-2xl font-bold" style={{ color: c.aiScore >= 80 ? "#ff2d55" : "#ff8c00" }}>
            {c.aiScore}<span className="text-xs font-normal text-gray-500">/100</span>
          </span>
        </div>
        <div className="w-full h-1.5 rounded-full overflow-hidden mb-2" style={{ background: "rgba(255,255,255,0.08)" }}>
          <motion.div className="h-full rounded-full" initial={{ width: 0 }} animate={{ width: `${c.aiScore}%` }}
            transition={{ duration: 0.8 }}
            style={{ background: c.aiScore >= 80 ? "linear-gradient(90deg,#ff8c00,#ff2d55)" : "#ff8c00" }} />
        </div>
        <p className="text-xs" style={{ color: "#526080" }}>High urgency — immediate investigative action recommended by CrimeSphere AI.</p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { icon: Paperclip,   label: "Evidence",  value: c.evidenceCount, color: "#0070f3" },
          { icon: Users,       label: "Suspects",  value: c.suspectCount,  color: "#ff2d55" },
          { icon: User,        label: "Witnesses", value: c.witnessCount,  color: "#bf5af2" },
          { icon: CalendarClock,label:"Days Active",value: c.daysActive,   color: "#ffd60a" },
        ].map(({ icon: Icon, label, value, color }) => (
          <div key={label} className="rounded-lg p-3 text-center"
            style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }}>
            <Icon className="w-4 h-4 mx-auto mb-1" style={{ color }} />
            <div className="text-lg font-bold text-white">{value}</div>
            <div className="text-[10px]" style={{ color: "#526080" }}>{label}</div>
          </div>
        ))}
      </div>

      {/* Description */}
      <div>
        <p className="text-[10px] uppercase tracking-widest font-semibold mb-2" style={{ color: "#2a3a55" }}>Case Description</p>
        <p className="text-xs leading-relaxed" style={{ color: "#94a3c0" }}>{c.description}</p>
      </div>

      {/* Lead officer + team */}
      <div>
        <p className="text-[10px] uppercase tracking-widest font-semibold mb-2" style={{ color: "#2a3a55" }}>Assigned Team</p>
        <div className="space-y-2">
          {[{ name: c.leadOfficer, role: c.leadRank, lead: true }, ...c.teamMembers.map((m) => ({ name: m, role: "Investigating Officer", lead: false }))].map((o) => (
            <div key={o.name} className="flex items-center gap-2.5 rounded-lg px-3 py-2"
              style={{ background: "rgba(255,255,255,0.025)", border: "1px solid rgba(255,255,255,0.06)" }}>
              <div className="w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-bold text-white shrink-0"
                style={{ background: o.lead ? "linear-gradient(135deg,#0070f3,#bf5af2)" : "rgba(255,255,255,0.1)" }}>
                {initials(o.name)}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-white truncate">{o.name}</p>
                <p className="text-[10px] truncate" style={{ color: "#526080" }}>{o.role}</p>
              </div>
              {o.lead && <span className="text-[9px] px-1.5 py-0.5 rounded-full font-bold" style={{ background: "rgba(0,112,243,0.15)", color: "#2b91ff" }}>Lead</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Task progress */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <p className="text-[10px] uppercase tracking-widest font-semibold" style={{ color: "#2a3a55" }}>Task Progress</p>
          <span className="text-xs font-bold text-white">{done}/{total} done</span>
        </div>
        <div className="w-full h-2 rounded-full overflow-hidden mb-3" style={{ background: "rgba(255,255,255,0.07)" }}>
          <motion.div className="h-full rounded-full bg-green-400" initial={{ width: 0 }}
            animate={{ width: `${(done / total) * 100}%` }} transition={{ duration: 0.8 }} />
        </div>
        <div className="space-y-2">
          {c.tasks.map((task) => {
            const cfg = TASK_STATUS[task.status];
            const Icon = cfg.icon;
            return (
              <div key={task.id} className="flex items-start gap-2.5">
                <Icon className="w-3.5 h-3.5 shrink-0 mt-0.5" style={{ color: cfg.color }} />
                <div className="flex-1 min-w-0">
                  <p className="text-xs text-white" style={{ textDecoration: task.status === "done" ? "line-through" : "none", opacity: task.status === "done" ? 0.5 : 1 }}>
                    {task.title}
                  </p>
                  <p className="text-[10px]" style={{ color: "#2a3a55" }}>{task.assignedTo} · Due {formatRelativeTime(task.due)}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function EvidenceTab({ items }: { items: EvidenceItem[] }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {items.map((ev, i) => {
        const Icon  = EVIDENCE_ICONS[ev.type];
        const color = EVIDENCE_COLORS[ev.type];
        const sc    = EV_STATUS_CFG[ev.status];
        return (
          <motion.div key={ev.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="rounded-xl p-4" style={{ background: "rgba(255,255,255,0.025)", border: "1px solid rgba(255,255,255,0.07)" }}>
            <div className="flex items-start gap-3 mb-3">
              <div className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                style={{ background: `${color}18`, border: `1px solid ${color}35` }}>
                <Icon className="w-4 h-4" style={{ color }} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-bold text-white truncate">{ev.name}</p>
                <p className="text-[10px] truncate" style={{ color: "#526080" }}>{ev.collectedFrom}</p>
              </div>
              <span className="text-[9px] font-bold px-2 py-0.5 rounded-full shrink-0"
                style={{ background: `${sc.color}18`, color: sc.color }}>
                {sc.label}
              </span>
            </div>
            <p className="text-[11px] leading-relaxed mb-2" style={{ color: "#94a3c0" }}>{ev.notes}</p>
            <div className="flex items-center justify-between text-[10px]" style={{ color: "#2a3a55" }}>
              <span>{ev.addedBy}</span>
              <span>{formatRelativeTime(ev.collectedAt)}</span>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}

function TimelineTab({ events }: { events: TimelineEvent[] }) {
  const sorted = [...events].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
  return (
    <div className="relative">
      {/* Vertical line */}
      <div className="absolute left-4 top-2 bottom-2 w-px" style={{ background: "rgba(255,255,255,0.07)" }} />
      <div className="space-y-4 pl-12">
        {sorted.map((ev, i) => {
          const cfg  = EVENT_CFG[ev.type];
          const Icon = cfg.icon;
          return (
            <motion.div key={ev.id} initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.06 }}
              className="relative">
              {/* Dot */}
              <div className="absolute -left-[2.2rem] top-1 w-5 h-5 rounded-full flex items-center justify-center z-10"
                style={{ background: `${cfg.color}20`, border: `2px solid ${cfg.color}` }}>
                <Icon className="w-2.5 h-2.5" style={{ color: cfg.color }} />
              </div>
              <div className="rounded-xl p-3.5" style={{ background: "rgba(255,255,255,0.025)", border: "1px solid rgba(255,255,255,0.07)" }}>
                <div className="flex items-center justify-between mb-1.5">
                  <p className="text-xs font-bold text-white">{ev.title}</p>
                  <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full uppercase tracking-widest shrink-0"
                    style={{ background: `${cfg.color}18`, color: cfg.color }}>
                    {ev.type}
                  </span>
                </div>
                <p className="text-xs leading-relaxed mb-2" style={{ color: "#94a3c0" }}>{ev.description}</p>
                <div className="flex items-center justify-between text-[10px]" style={{ color: "#2a3a55" }}>
                  <span>{ev.addedBy}</span>
                  <span>{formatDate(ev.date)}</span>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

function SuspectsTab({ suspects }: { suspects: CaseSuspect[] }) {
  return (
    <div className="space-y-4">
      {suspects.map((s, i) => {
        const st = SUSPECT_STATUS[s.status];
        return (
          <motion.div key={s.id} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.07 }}
            className="rounded-xl p-4" style={{ background: "rgba(255,255,255,0.025)", border: "1px solid rgba(255,255,255,0.07)" }}>
            <div className="flex items-start gap-3 mb-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xs font-bold text-white shrink-0"
                style={{ background: `${st.color}20`, border: `2px solid ${st.color}50`, color: st.color }}>
                {initials(s.name)}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <p className="text-sm font-bold text-white">{s.name}</p>
                  <p className="text-xs" style={{ color: "#526080" }}>{s.alias}</p>
                  <span className="text-[9px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1"
                    style={{ background: `${st.color}15`, color: st.color }}>
                    <span className="w-1.5 h-1.5 rounded-full" style={{ background: st.color }} />
                    {st.label}
                  </span>
                </div>
                <p className="text-xs mt-0.5" style={{ color: "#526080" }}>{s.role}</p>
              </div>
              <div className="text-right shrink-0">
                <p className="text-lg font-bold" style={{ color: s.threatScore >= 80 ? "#ff2d55" : "#ff8c00" }}>{s.threatScore}</p>
                <p className="text-[10px]" style={{ color: "#2a3a55" }}>Threat</p>
              </div>
            </div>
            <div className="w-full h-1.5 rounded-full overflow-hidden mb-3" style={{ background: "rgba(255,255,255,0.07)" }}>
              <div className="h-full rounded-full" style={{ width: `${s.threatScore}%`, background: s.threatScore >= 80 ? "#ff2d55" : "#ff8c00" }} />
            </div>
            <p className="text-xs leading-relaxed" style={{ color: "#94a3c0" }}>{s.notes}</p>
          </motion.div>
        );
      })}
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

const TABS = [
  { key: "overview",  label: "Overview",  icon: Folder },
  { key: "evidence",  label: "Evidence",  icon: Paperclip },
  { key: "timeline",  label: "Timeline",  icon: CalendarClock },
  { key: "suspects",  label: "Suspects",  icon: Users },
] as const;

type TabKey = typeof TABS[number]["key"];

export default function InvestigationWorkspace() {
  const [selectedId, setSelectedId] = useState(INVESTIGATION_CASES[0].id);
  const [activeTab,  setActiveTab]  = useState<TabKey>("overview");
  const [search,     setSearch]     = useState("");

  const selected = INVESTIGATION_CASES.find((c) => c.id === selectedId)!;
  const filtered = INVESTIGATION_CASES.filter((c) =>
    !search || c.title.toLowerCase().includes(search.toLowerCase()) || c.firNumber.toLowerCase().includes(search.toLowerCase())
  );

  const p = PRIORITY_CFG[selected.priority];

  return (
    <div className="flex h-[calc(100vh-4rem)] -m-6 overflow-hidden">

      {/* ═══ LEFT: Case List ═══ */}
      <div className="hidden lg:flex w-[280px] shrink-0 flex-col"
        style={{ background: "#0a0f1e", borderRight: "1px solid rgba(255,255,255,0.06)" }}>
        <div className="px-4 py-4 shrink-0" style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
          <p className="text-sm font-bold text-white mb-3">Active Cases</p>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none" style={{ color: "#526080" }} />
            <input type="text" value={search} onChange={(e) => setSearch(e.target.value)}
              placeholder="Search cases…"
              className="w-full h-9 pl-9 pr-3 rounded-lg text-xs text-white outline-none"
              style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)" }} />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto py-2 px-2 space-y-1.5">
          {filtered.map((c) => {
            const cp = PRIORITY_CFG[c.priority];
            const isActive = c.id === selectedId;
            return (
              <button key={c.id} onClick={() => { setSelectedId(c.id); setActiveTab("overview"); }}
                className="w-full text-left rounded-xl p-3.5 transition-all"
                style={{ background: isActive ? "rgba(0,112,243,0.12)" : "transparent", border: isActive ? "1px solid rgba(0,112,243,0.22)" : "1px solid transparent" }}>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <span className="text-[10px] font-mono" style={{ color: "#2b91ff" }}>{c.firNumber}</span>
                  <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full shrink-0"
                    style={{ background: cp.bg, color: cp.color }}>{cp.label}</span>
                </div>
                <p className="text-xs font-semibold text-white mb-1.5 leading-snug line-clamp-2">{c.title}</p>
                <div className="flex items-center justify-between text-[10px]" style={{ color: "#2a3a55" }}>
                  <span>{c.district}</span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-2.5 h-2.5" />
                    {c.daysActive}d
                  </span>
                </div>
                {/* Mini progress */}
                <div className="mt-2 w-full h-0.5 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.07)" }}>
                  <div className="h-full rounded-full bg-green-400"
                    style={{ width: `${(c.tasks.filter((t) => t.status === "done").length / c.tasks.length) * 100}%` }} />
                </div>
              </button>
            );
          })}
        </div>

        <div className="px-4 py-3 shrink-0 text-center" style={{ borderTop: "1px solid rgba(255,255,255,0.05)" }}>
          <p className="text-[10px]" style={{ color: "#2a3a55" }}>
            {INVESTIGATION_CASES.length} active cases · {INVESTIGATION_CASES.filter((c) => c.priority === "critical").length} critical
          </p>
        </div>
      </div>

      {/* ═══ RIGHT: Workspace ═══ */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden" style={{ background: "#080b12" }}>

        {/* Case header */}
        <div className="px-6 py-4 shrink-0"
          style={{ background: "rgba(10,15,30,0.95)", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1 flex-wrap">
                <span className="text-xs font-mono font-bold" style={{ color: "#2b91ff" }}>{selected.firNumber}</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full" style={{ background: p.bg, color: p.color }}>{p.label} Priority</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ background: "rgba(255,140,0,0.1)", color: "#ff8c00" }}>Active</span>
                <span className="flex items-center gap-1 text-[10px]" style={{ color: "#2a3a55" }}>
                  <Clock className="w-3 h-3" /> {selected.daysActive} days active
                </span>
              </div>
              <h2 className="text-base font-bold text-white">{selected.title}</h2>
              <p className="text-xs mt-0.5" style={{ color: "#526080" }}>
                {selected.crimeType} · {selected.district} · Lead: {selected.leadOfficer}
              </p>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <button className="text-xs px-3 py-1.5 rounded-lg transition-colors"
                style={{ background: "rgba(255,45,85,0.1)", border: "1px solid rgba(255,45,85,0.2)", color: "#ff2d55" }}>
                Escalate
              </button>
              <button className="text-xs px-3 py-1.5 rounded-lg transition-colors"
                style={{ background: "rgba(0,112,243,0.1)", border: "1px solid rgba(0,112,243,0.2)", color: "#2b91ff" }}>
                Export Report
              </button>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex gap-1 mt-4">
            {TABS.map(({ key, label, icon: Icon }) => (
              <button key={key} onClick={() => setActiveTab(key)}
                className="flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all"
                style={{
                  background: activeTab === key ? "rgba(0,112,243,0.15)" : "transparent",
                  border: activeTab === key ? "1px solid rgba(0,112,243,0.3)" : "1px solid transparent",
                  color: activeTab === key ? "#2b91ff" : "#526080",
                }}>
                <Icon className="w-3.5 h-3.5" />
                {label}
                {key === "evidence" && <span className="text-[10px] px-1.5 py-0.5 rounded-full"
                  style={{ background: "rgba(255,255,255,0.08)", color: "#94a3c0" }}>{selected.evidenceCount}</span>}
                {key === "suspects" && <span className="text-[10px] px-1.5 py-0.5 rounded-full"
                  style={{ background: "rgba(255,255,255,0.08)", color: "#94a3c0" }}>{selected.suspectCount}</span>}
              </button>
            ))}
          </div>
        </div>

        {/* Tab content */}
        <div className="flex-1 overflow-y-auto p-6">
          <AnimatePresence mode="wait">
            <motion.div key={`${selectedId}-${activeTab}`}
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.2 }}>
              {activeTab === "overview"  && <OverviewTab  c={selected} />}
              {activeTab === "evidence"  && <EvidenceTab  items={selected.evidence} />}
              {activeTab === "timeline"  && <TimelineTab  events={selected.timeline} />}
              {activeTab === "suspects"  && <SuspectsTab  suspects={selected.suspects} />}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
