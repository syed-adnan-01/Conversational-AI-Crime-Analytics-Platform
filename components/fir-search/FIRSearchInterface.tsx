"use client";

import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  Filter,
  X,
  ChevronUp,
  ChevronDown,
  ChevronsUpDown,
  Eye,
  Brain,
  MapPin,
  User,
  Clock,
  Shield,
  AlertTriangle,
  FileText,
  Tag,
  ChevronRight,
} from "lucide-react";
import {
  MOCK_FIRS,
  CRIME_TYPES,
  DISTRICTS,
  type MockFIR,
} from "@/lib/mock-data/fir";
import { formatRelativeTime, formatDate } from "@/lib/utils";
import type { RiskLevel, CrimeStatus } from "@/types";

// ─── Config maps ─────────────────────────────────────────────────────────

const RISK_CFG: Record<RiskLevel, { label: string; color: string; bg: string }> = {
  critical: { label: "Critical", color: "#ff2d55", bg: "rgba(255,45,85,0.12)" },
  high:     { label: "High",     color: "#ff8c00", bg: "rgba(255,140,0,0.12)" },
  medium:   { label: "Medium",   color: "#ffd60a", bg: "rgba(255,214,10,0.12)" },
  low:      { label: "Low",      color: "#30d158", bg: "rgba(48,209,88,0.12)" },
};

const STATUS_CFG: Record<CrimeStatus, { label: string; color: string; bg: string }> = {
  open:          { label: "Open",          color: "#2b91ff", bg: "rgba(43,145,255,0.1)" },
  investigating: { label: "Investigating", color: "#ffd60a", bg: "rgba(255,214,10,0.1)" },
  closed:        { label: "Closed",        color: "#30d158", bg: "rgba(48,209,88,0.1)" },
  escalated:     { label: "Escalated",     color: "#ff2d55", bg: "rgba(255,45,85,0.1)" },
  pending:       { label: "Pending",       color: "#526080", bg: "rgba(82,96,128,0.1)" },
};

type SortKey = "firNumber" | "riskLevel" | "status" | "aiScore" | "reportedAt";
type SortDir = "asc" | "desc";

const RISK_ORDER: Record<RiskLevel, number> = { critical: 4, high: 3, medium: 2, low: 1 };

// ─── Sort icon ────────────────────────────────────────────────────────────

function SortIcon({ col, sortKey, sortDir }: { col: SortKey; sortKey: SortKey; sortDir: SortDir }) {
  if (col !== sortKey) return <ChevronsUpDown className="w-3 h-3 opacity-30" />;
  return sortDir === "asc"
    ? <ChevronUp className="w-3 h-3 text-blue-400" />
    : <ChevronDown className="w-3 h-3 text-blue-400" />;
}

// ─── Detail Panel ─────────────────────────────────────────────────────────

function FIRDetailPanel({ fir, onClose }: { fir: MockFIR; onClose: () => void }) {
  const risk   = RISK_CFG[fir.riskLevel];
  const status = STATUS_CFG[fir.status];

  return (
    <motion.div
      initial={{ x: "100%", opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: "100%", opacity: 0 }}
      transition={{ type: "spring", damping: 28, stiffness: 280 }}
      className="flex flex-col h-full overflow-hidden"
      style={{
        width: 400,
        background: "#0a0f1e",
        borderLeft: "1px solid rgba(255,255,255,0.07)",
      }}
    >
      {/* Header */}
      <div
        className="flex items-start justify-between p-5 shrink-0"
        style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}
      >
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span
              className="text-xs font-mono font-bold"
              style={{ color: "#2b91ff" }}
            >
              {fir.firNumber}
            </span>
            <span
              className="text-[10px] font-bold px-2 py-0.5 rounded-full"
              style={{ background: risk.bg, color: risk.color }}
            >
              {risk.label}
            </span>
            <span
              className="text-[10px] font-semibold px-2 py-0.5 rounded-full"
              style={{ background: status.bg, color: status.color }}
            >
              {status.label}
            </span>
          </div>
          <h3 className="text-sm font-bold text-white leading-snug">
            {fir.title}
          </h3>
        </div>
        <button
          onClick={onClose}
          className="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 ml-3 mt-0.5"
          style={{
            background: "rgba(255,255,255,0.05)",
            border: "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <X className="w-3.5 h-3.5" style={{ color: "#526080" }} />
        </button>
      </div>

      {/* Scrollable body */}
      <div className="flex-1 overflow-y-auto p-5 space-y-5">

        {/* AI Score */}
        <div
          className="rounded-xl p-4"
          style={{
            background: "rgba(191,90,242,0.06)",
            border: "1px solid rgba(191,90,242,0.18)",
          }}
        >
          <div className="flex items-center gap-2 mb-2">
            <Brain className="w-3.5 h-3.5" style={{ color: "#bf5af2" }} />
            <span className="text-xs font-bold" style={{ color: "#bf5af2" }}>
              AI Analysis
            </span>
            <span
              className="ml-auto text-sm font-bold tabular-nums"
              style={{
                color:
                  fir.aiScore >= 80 ? "#ff2d55" :
                  fir.aiScore >= 60 ? "#ff8c00" : "#30d158",
              }}
            >
              {fir.aiScore}/100
            </span>
          </div>
          <div
            className="w-full h-1.5 rounded-full mb-3"
            style={{ background: "rgba(255,255,255,0.08)" }}
          >
            <div
              className="h-full rounded-full"
              style={{
                width: `${fir.aiScore}%`,
                background:
                  fir.aiScore >= 80 ? "#ff2d55" :
                  fir.aiScore >= 60 ? "#ff8c00" : "#30d158",
              }}
            />
          </div>
          <p className="text-xs leading-relaxed" style={{ color: "#94a3c0" }}>
            {fir.aiSummary}
          </p>
        </div>

        {/* Description */}
        <Section title="Incident Description">
          <p className="text-xs leading-relaxed" style={{ color: "#94a3c0" }}>
            {fir.description}
          </p>
        </Section>

        {/* Details grid */}
        <Section title="Case Details">
          <div className="space-y-2">
            {[
              { icon: FileText, label: "Crime Type",  value: fir.crimeType },
              { icon: MapPin,   label: "Location",    value: fir.location },
              { icon: Shield,   label: "Police Stn.", value: fir.ps },
              { icon: User,     label: "Assigned To", value: `${fir.assignedTo} (${fir.rank})` },
              { icon: Clock,    label: "Reported",    value: formatDate(fir.reportedAt) },
              { icon: Clock,    label: "Updated",     value: formatRelativeTime(fir.updatedAt) },
            ].map(({ icon: Icon, label, value }) => (
              <div key={label} className="flex items-start gap-2">
                <Icon className="w-3 h-3 shrink-0 mt-0.5" style={{ color: "#2a3a55" }} />
                <span className="text-[11px] shrink-0 w-20" style={{ color: "#526080" }}>
                  {label}
                </span>
                <span className="text-[11px] text-white flex-1">{value}</span>
              </div>
            ))}
          </div>
        </Section>

        {/* Suspects */}
        {fir.suspects.length > 0 && (
          <Section title={`Suspects (${fir.suspects.length})`}>
            <ul className="space-y-1">
              {fir.suspects.map((s, i) => (
                <li key={i} className="flex items-center gap-2">
                  <span
                    className="w-1.5 h-1.5 rounded-full shrink-0"
                    style={{ background: "#ff2d55" }}
                  />
                  <span className="text-xs" style={{ color: "#94a3c0" }}>{s}</span>
                </li>
              ))}
            </ul>
          </Section>
        )}

        {/* Victims */}
        {fir.victims.length > 0 && (
          <Section title={`Victims (${fir.victims.length})`}>
            <ul className="space-y-1">
              {fir.victims.map((v, i) => (
                <li key={i} className="flex items-center gap-2">
                  <span
                    className="w-1.5 h-1.5 rounded-full shrink-0"
                    style={{ background: "#0070f3" }}
                  />
                  <span className="text-xs" style={{ color: "#94a3c0" }}>{v}</span>
                </li>
              ))}
            </ul>
          </Section>
        )}

        {/* Evidence */}
        <Section title={`Evidence (${fir.evidence.length} items)`}>
          <ul className="space-y-1">
            {fir.evidence.map((e, i) => (
              <li key={i} className="flex items-center gap-2">
                <span
                  className="w-1.5 h-1.5 rounded-full shrink-0"
                  style={{ background: "#30d158" }}
                />
                <span className="text-xs" style={{ color: "#94a3c0" }}>{e}</span>
              </li>
            ))}
          </ul>
        </Section>

        {/* Tags */}
        <Section title="Tags">
          <div className="flex flex-wrap gap-1.5">
            {fir.tags.map((tag) => (
              <span
                key={tag}
                className="flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full"
                style={{
                  background: "rgba(0,112,243,0.1)",
                  border: "1px solid rgba(0,112,243,0.2)",
                  color: "#2b91ff",
                }}
              >
                <Tag className="w-2.5 h-2.5" />
                {tag}
              </span>
            ))}
          </div>
        </Section>
      </div>
    </motion.div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <p
        className="text-[10px] font-semibold uppercase tracking-widest mb-2"
        style={{ color: "#2a3a55" }}
      >
        {title}
      </p>
      {children}
    </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────

export default function FIRSearchInterface() {
  const [query, setQuery]         = useState("");
  const [crimeType, setCrimeType] = useState("all");
  const [riskLevel, setRiskLevel] = useState("all");
  const [status, setStatus]       = useState("all");
  const [district, setDistrict]   = useState("all");
  const [sortKey, setSortKey]     = useState<SortKey>("reportedAt");
  const [sortDir, setSortDir]     = useState<SortDir>("desc");
  const [selected, setSelected]   = useState<MockFIR | null>(null);

  // ── Filtering + sorting ───────────────────────────────────────────────

  const filtered = useMemo(() => {
    let firs = MOCK_FIRS.filter((f) => {
      const q = query.toLowerCase();
      const matchQuery =
        !q ||
        f.firNumber.toLowerCase().includes(q) ||
        f.title.toLowerCase().includes(q) ||
        f.district.toLowerCase().includes(q) ||
        f.assignedTo.toLowerCase().includes(q) ||
        f.crimeType.toLowerCase().includes(q);

      return (
        matchQuery &&
        (crimeType === "all" || f.crimeType === crimeType) &&
        (riskLevel === "all" || f.riskLevel === riskLevel) &&
        (status === "all"    || f.status === status) &&
        (district === "all"  || f.district === district)
      );
    });

    firs.sort((a, b) => {
      let av: number | string, bv: number | string;
      if (sortKey === "riskLevel") {
        av = RISK_ORDER[a.riskLevel];
        bv = RISK_ORDER[b.riskLevel];
      } else if (sortKey === "aiScore") {
        av = a.aiScore; bv = b.aiScore;
      } else if (sortKey === "reportedAt") {
        av = new Date(a.reportedAt).getTime();
        bv = new Date(b.reportedAt).getTime();
      } else {
        av = a[sortKey]; bv = b[sortKey];
      }
      if (av < bv) return sortDir === "asc" ? -1 : 1;
      if (av > bv) return sortDir === "asc" ? 1 : -1;
      return 0;
    });

    return firs;
  }, [query, crimeType, riskLevel, status, district, sortKey, sortDir]);

  const handleSort = (key: SortKey) => {
    if (key === sortKey) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else { setSortKey(key); setSortDir("desc"); }
  };

  const clearFilters = () => {
    setQuery(""); setCrimeType("all"); setRiskLevel("all");
    setStatus("all"); setDistrict("all");
  };

  const hasFilters = query || crimeType !== "all" || riskLevel !== "all" || status !== "all" || district !== "all";

  const selectStyle = {
    background: "rgba(255,255,255,0.04)",
    border: "1px solid rgba(255,255,255,0.09)",
    color: "#94a3c0",
    outline: "none",
    borderRadius: "0.5rem",
    padding: "0.375rem 0.75rem",
    fontSize: "0.75rem",
  };

  // ── Column headers ──────────────────────────────────────────────────────
  const COLS: { label: string; key?: SortKey; w?: string }[] = [
    { label: "FIR No.",   key: "firNumber",  w: "140px" },
    { label: "Title" },
    { label: "Type",                         w: "130px" },
    { label: "Risk",      key: "riskLevel",  w: "90px" },
    { label: "Status",    key: "status",     w: "110px" },
    { label: "District",                     w: "140px" },
    { label: "AI Score",  key: "aiScore",    w: "100px" },
    { label: "Reported",  key: "reportedAt", w: "110px" },
    { label: "",                             w: "40px" },
  ];

  return (
    <div className="flex h-[calc(100vh-4rem)] -m-6 overflow-hidden">

      {/* ═══ Left: search + table ═══ */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">

        {/* ── Top bar: search + filters ── */}
        <div
          className="px-6 py-4 space-y-3 shrink-0"
          style={{
            background: "rgba(10,15,30,0.95)",
            borderBottom: "1px solid rgba(255,255,255,0.06)",
            backdropFilter: "blur(12px)",
          }}
        >
          {/* Search */}
          <div className="relative">
            <Search
              className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none"
              style={{ color: "#526080" }}
            />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by FIR number, title, district, officer…"
              className="w-full h-11 pl-11 pr-4 rounded-xl text-sm text-white outline-none transition-all"
              style={{
                background: "rgba(255,255,255,0.05)",
                border: "1px solid rgba(255,255,255,0.09)",
                caretColor: "#0070f3",
              }}
              onFocus={(e) => (e.target.style.borderColor = "rgba(0,112,243,0.5)")}
              onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.09)")}
            />
            {query && (
              <button
                className="absolute right-3 top-1/2 -translate-y-1/2"
                onClick={() => setQuery("")}
              >
                <X className="w-4 h-4" style={{ color: "#526080" }} />
              </button>
            )}
          </div>

          {/* Filters row */}
          <div className="flex items-center gap-2 flex-wrap">
            <Filter className="w-3.5 h-3.5 shrink-0" style={{ color: "#2a3a55" }} />

            {[
              { label: "Crime Type", value: crimeType, set: setCrimeType, opts: ["all", ...CRIME_TYPES], display: (v: string) => v === "all" ? "All Types" : v },
              { label: "Risk",       value: riskLevel, set: setRiskLevel, opts: ["all", "critical", "high", "medium", "low"], display: (v: string) => v === "all" ? "All Risk" : v.charAt(0).toUpperCase() + v.slice(1) },
              { label: "Status",     value: status,    set: setStatus,    opts: ["all", "open", "investigating", "closed", "escalated"], display: (v: string) => v === "all" ? "All Status" : STATUS_CFG[v as CrimeStatus]?.label ?? v },
              { label: "District",   value: district,  set: setDistrict,  opts: ["all", ...DISTRICTS], display: (v: string) => v === "all" ? "All Districts" : v },
            ].map(({ label, value, set, opts, display }) => (
              <select
                key={label}
                value={value}
                onChange={(e) => set(e.target.value)}
                style={selectStyle}
              >
                {opts.map((o) => (
                  <option key={o} value={o} style={{ background: "#0d1322" }}>
                    {display(o)}
                  </option>
                ))}
              </select>
            ))}

            {hasFilters && (
              <button
                onClick={clearFilters}
                className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg transition-colors"
                style={{
                  background: "rgba(255,45,85,0.08)",
                  border: "1px solid rgba(255,45,85,0.2)",
                  color: "#ff2d55",
                }}
              >
                <X className="w-3 h-3" />
                Clear
              </button>
            )}

            {/* Stats */}
            <div className="ml-auto flex items-center gap-3 text-xs" style={{ color: "#526080" }}>
              <span>
                <strong className="text-white">{filtered.length}</strong> results
              </span>
              <span
                className="px-2 py-0.5 rounded-full text-[10px] font-bold"
                style={{ background: "rgba(255,45,85,0.12)", color: "#ff2d55" }}
              >
                {filtered.filter((f) => f.riskLevel === "critical").length} critical
              </span>
            </div>
          </div>
        </div>

        {/* ── Table ── */}
        <div className="flex-1 overflow-auto">
          <table className="w-full text-xs border-separate border-spacing-0">
            <thead className="sticky top-0 z-10">
              <tr style={{ background: "#080b12" }}>
                {COLS.map((col) => (
                  <th
                    key={col.label}
                    className="px-4 py-3 text-left font-semibold uppercase tracking-wider whitespace-nowrap"
                    style={{
                      color: sortKey === col.key ? "#2b91ff" : "#2a3a55",
                      borderBottom: "1px solid rgba(255,255,255,0.06)",
                      width: col.w,
                      cursor: col.key ? "pointer" : "default",
                    }}
                    onClick={() => col.key && handleSort(col.key)}
                  >
                    <div className="flex items-center gap-1.5">
                      {col.label}
                      {col.key && (
                        <SortIcon col={col.key} sortKey={sortKey} sortDir={sortDir} />
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              <AnimatePresence>
                {filtered.map((fir, i) => {
                  const risk   = RISK_CFG[fir.riskLevel];
                  const status = STATUS_CFG[fir.status];
                  const isSelected = selected?.id === fir.id;

                  return (
                    <motion.tr
                      key={fir.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: i * 0.03 }}
                      onClick={() => setSelected(isSelected ? null : fir)}
                      className="cursor-pointer transition-colors"
                      style={{
                        background: isSelected
                          ? "rgba(0,112,243,0.07)"
                          : "transparent",
                        borderLeft: isSelected
                          ? "2px solid #0070f3"
                          : "2px solid transparent",
                      }}
                      onMouseEnter={(e) => {
                        if (!isSelected)
                          (e.currentTarget as HTMLTableRowElement).style.background =
                            "rgba(255,255,255,0.025)";
                      }}
                      onMouseLeave={(e) => {
                        if (!isSelected)
                          (e.currentTarget as HTMLTableRowElement).style.background =
                            "transparent";
                      }}
                    >
                      {/* FIR No */}
                      <td
                        className="px-4 py-3 whitespace-nowrap"
                        style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                      >
                        <span className="font-mono font-bold" style={{ color: "#2b91ff" }}>
                          {fir.firNumber}
                        </span>
                      </td>

                      {/* Title */}
                      <td
                        className="px-4 py-3"
                        style={{ borderBottom: "1px solid rgba(255,255,255,0.04)", maxWidth: 220 }}
                      >
                        <p className="font-medium text-white line-clamp-1">{fir.title}</p>
                        <p className="text-[10px] mt-0.5 truncate" style={{ color: "#2a3a55" }}>
                          {fir.ps}
                        </p>
                      </td>

                      {/* Crime Type */}
                      <td
                        className="px-4 py-3 whitespace-nowrap"
                        style={{ color: "#526080", borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                      >
                        {fir.crimeType}
                      </td>

                      {/* Risk */}
                      <td
                        className="px-4 py-3 whitespace-nowrap"
                        style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                      >
                        <span
                          className="px-2 py-0.5 rounded-full text-[10px] font-bold"
                          style={{ background: risk.bg, color: risk.color }}
                        >
                          {risk.label}
                        </span>
                      </td>

                      {/* Status */}
                      <td
                        className="px-4 py-3 whitespace-nowrap"
                        style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                      >
                        <span
                          className="px-2 py-0.5 rounded-full text-[10px] font-semibold"
                          style={{ background: status.bg, color: status.color }}
                        >
                          {status.label}
                        </span>
                      </td>

                      {/* District */}
                      <td
                        className="px-4 py-3 whitespace-nowrap text-xs"
                        style={{ color: "#526080", borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                      >
                        {fir.district}
                      </td>

                      {/* AI Score */}
                      <td
                        className="px-4 py-3 whitespace-nowrap"
                        style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                      >
                        <div className="flex items-center gap-2">
                          <div
                            className="h-1 rounded-full overflow-hidden"
                            style={{ background: "rgba(255,255,255,0.07)", width: 44 }}
                          >
                            <div
                              className="h-full rounded-full"
                              style={{
                                width: `${fir.aiScore}%`,
                                background:
                                  fir.aiScore >= 80 ? "#ff2d55" :
                                  fir.aiScore >= 60 ? "#ff8c00" : "#30d158",
                              }}
                            />
                          </div>
                          <span
                            className="font-mono font-bold text-[11px]"
                            style={{
                              color:
                                fir.aiScore >= 80 ? "#ff2d55" :
                                fir.aiScore >= 60 ? "#ff8c00" : "#30d158",
                            }}
                          >
                            {fir.aiScore}
                          </span>
                        </div>
                      </td>

                      {/* Reported */}
                      <td
                        className="px-4 py-3 whitespace-nowrap text-[11px]"
                        style={{ color: "#2a3a55", borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                      >
                        {formatRelativeTime(fir.reportedAt)}
                      </td>

                      {/* View */}
                      <td
                        className="px-4 py-3"
                        style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                      >
                        <ChevronRight
                          className="w-4 h-4 transition-transform"
                          style={{
                            color: isSelected ? "#2b91ff" : "#2a3a55",
                            transform: isSelected ? "rotate(90deg)" : "rotate(0deg)",
                          }}
                        />
                      </td>
                    </motion.tr>
                  );
                })}
              </AnimatePresence>

              {filtered.length === 0 && (
                <tr>
                  <td colSpan={9} className="text-center py-16">
                    <AlertTriangle className="w-8 h-8 mx-auto mb-3" style={{ color: "#2a3a55" }} />
                    <p className="text-sm" style={{ color: "#526080" }}>
                      No FIRs match your search criteria.
                    </p>
                    <button
                      onClick={clearFilters}
                      className="mt-2 text-xs"
                      style={{ color: "#0070f3" }}
                    >
                      Clear all filters
                    </button>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* ═══ Right: Detail Panel ═══ */}
      <AnimatePresence>
        {selected && (
          <FIRDetailPanel fir={selected} onClose={() => setSelected(null)} />
        )}
      </AnimatePresence>
    </div>
  );
}
