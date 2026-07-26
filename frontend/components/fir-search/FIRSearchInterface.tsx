"use client";

import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  X,
  ChevronUp,
  ChevronDown,
  ChevronsUpDown,
  User,
  Clock,
  Shield,
  AlertTriangle,
  FileText,
  ChevronRight,
} from "lucide-react";
import { searchCases, getCase, CaseSummary, CaseResponse } from "@/lib/services/cases";
import { formatRelativeTime, formatDate } from "@/lib/utils";

// ─── Config maps ─────────────────────────────────────────────────────────

const STATUS_CFG: Record<number, { label: string; color: string; bg: string }> = {
  1: { label: "Registered", color: "#2b91ff", bg: "rgba(43,145,255,0.1)" },
  2: { label: "Under Investigation", color: "#ffd60a", bg: "rgba(255,214,10,0.1)" },
  3: { label: "Closed", color: "#30d158", bg: "rgba(48,209,88,0.1)" },
  4: { label: "Chargesheet Filed", color: "#bf5af2", bg: "rgba(191,90,242,0.1)" },
  0: { label: "Unknown", color: "#526080", bg: "rgba(82,96,128,0.1)" },
};

type SortKey = "crime_no" | "registered_date" | "status" | "aiScore";
type SortDir = "asc" | "desc";

function SortIcon({ col, sortKey, sortDir }: { col: SortKey; sortKey: SortKey; sortDir: SortDir }) {
  if (col !== sortKey) return <ChevronsUpDown className="w-3 h-3 opacity-30" />;
  return sortDir === "asc"
    ? <ChevronUp className="w-3 h-3 text-blue-400" />
    : <ChevronDown className="w-3 h-3 text-blue-400" />;
}

// ─── Detail Panel ─────────────────────────────────────────────────────────

function FIRDetailPanel({ caseId, onClose }: { caseId: string; onClose: () => void }) {
  const [detail, setDetail] = useState<CaseResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    getCase(caseId)
      .then((data) => {
        if (mounted) setDetail(data);
      })
      .catch(console.error)
      .finally(() => {
        if (mounted) setLoading(false);
      });
    return () => { mounted = false; };
  }, [caseId]);

  return (
    <motion.div
      initial={{ x: "100%", opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: "100%", opacity: 0 }}
      transition={{ type: "spring", damping: 28, stiffness: 280 }}
      className="flex flex-col h-full overflow-hidden relative"
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
              {detail?.crime_no || "Loading..."}
            </span>
            {detail?.case_status_id !== undefined && (
              <span
                className="text-[10px] font-semibold px-2 py-0.5 rounded-full"
                style={{ 
                  background: STATUS_CFG[detail.case_status_id]?.bg || STATUS_CFG[0].bg, 
                  color: STATUS_CFG[detail.case_status_id]?.color || STATUS_CFG[0].color 
                }}
              >
                {STATUS_CFG[detail.case_status_id]?.label || `Status ${detail.case_status_id}`}
              </span>
            )}
          </div>
          <h3 className="text-sm font-bold text-white leading-snug">
            {detail?.case_no || "Case Details"}
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
        {loading ? (
          <div className="flex items-center justify-center h-32">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2b91ff]" />
          </div>
        ) : !detail ? (
          <div className="text-center py-10">
            <p className="text-sm" style={{ color: "#526080" }}>Failed to load details.</p>
          </div>
        ) : (
          <>
            {/* Description */}
            {detail.brief_facts && (
              <Section title="Incident Description">
                <p className="text-xs leading-relaxed" style={{ color: "#94a3c0" }}>
                  {detail.brief_facts}
                </p>
              </Section>
            )}

            {/* Details grid */}
            <Section title="Case Details">
              <div className="space-y-2">
                {[
                  { icon: FileText, label: "Crime Type ID",  value: detail.crime_major_head_id || "N/A" },
                  { icon: Shield,   label: "Police Stn. ID", value: detail.police_station_id },
                  { icon: User,     label: "Assigned To ID", value: detail.police_person_id || "Unassigned" },
                  { icon: Clock,    label: "Registered",    value: detail.crime_registered_date ? formatDate(detail.crime_registered_date) : "N/A" },
                  { icon: Clock,    label: "Updated",     value: detail.updated_at ? formatRelativeTime(detail.updated_at) : "N/A" },
                ].map(({ icon: Icon, label, value }) => (
                  <div key={label} className="flex items-start gap-2">
                    <Icon className="w-3 h-3 shrink-0 mt-0.5" style={{ color: "#2a3a55" }} />
                    <span className="text-[11px] shrink-0 w-24" style={{ color: "#526080" }}>
                      {label}
                    </span>
                    <span className="text-[11px] text-white flex-1">{value}</span>
                  </div>
                ))}
              </div>
            </Section>
          </>
        )}
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
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  
  const [firs, setFirs] = useState<CaseSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortKey, setSortKey] = useState<SortKey>("registered_date");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [selectedId, setSelectedId] = useState<string | null>(null);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedQuery(query), 400);
    return () => clearTimeout(timer);
  }, [query]);

  useEffect(() => {
    let mounted = true;
    
    // We can map query to crime_no if it matches pattern, but for now we'll just send it
    searchCases({
      crime_no: debouncedQuery || undefined,
      page: 1,
      page_size: 50
    })
      .then((res) => {
        if (mounted) setFirs(res.items);
      })
      .catch(console.error)
      .finally(() => {
        if (mounted) setLoading(false);
      });
      
    return () => { mounted = false; };
  }, [debouncedQuery]);

  // Client-side sorting for now since backend doesn't seem to expose all sort fields in CaseSearchParams yet
  const sorted = useMemo(() => {
    const list = [...firs];
    list.sort((a, b) => {
      let av: number | string = 0, bv: number | string = 0;
      if (sortKey === "registered_date") {
        av = new Date(a.crime_registered_date).getTime();
        bv = new Date(b.crime_registered_date).getTime();
      } else if (sortKey === "crime_no") {
        av = a.crime_no; bv = b.crime_no;
      } else if (sortKey === "status") {
        av = a.case_status_id || 0; bv = b.case_status_id || 0;
      }
      if (av < bv) return sortDir === "asc" ? -1 : 1;
      if (av > bv) return sortDir === "asc" ? 1 : -1;
      return 0;
    });
    return list;
  }, [firs, sortKey, sortDir]);

  const handleSort = (key: SortKey) => {
    if (key === sortKey) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else { setSortKey(key); setSortDir("desc"); }
  };

  const clearFilters = () => {
    setQuery("");
  };

  const selectStyle = {
    background: "rgba(255,255,255,0.04)",
    border: "1px solid rgba(255,255,255,0.09)",
    color: "#94a3c0",
    outline: "none",
    borderRadius: "0.5rem",
    padding: "0.375rem 0.75rem",
    fontSize: "0.75rem",
  };

  const COLS: { label: string; key?: SortKey; w?: string }[] = [
    { label: "FIR No.",   key: "crime_no",  w: "140px" },
    { label: "Case No." },
    { label: "Type (ID)",                   w: "130px" },
    { label: "Risk",                        w: "90px" },
    { label: "Status",    key: "status",    w: "110px" },
    { label: "Station",                     w: "140px" },
    { label: "AI Score",                    w: "100px" },
    { label: "Reported",  key: "registered_date", w: "110px" },
    { label: "",                            w: "40px" },
  ];

  return (
    <div className="flex h-[calc(100vh-4rem)] -m-6 overflow-hidden">
      {/* ═══ Left: search + table ═══ */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        {/* ── Top bar: search + filters ── */}
        <div
          className="px-6 py-4 space-y-3 shrink-0"
          style={{
            background: "rgba(10,15,30,0.95)",
            borderBottom: "1px solid rgba(255,255,255,0.06)",
            backdropFilter: "blur(12px)",
          }}
        >
          <div className="relative">
            <Search
              className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none"
              style={{ color: "#526080" }}
            />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by FIR number..."
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

          <div className="flex items-center gap-2 flex-wrap">
            <div className="ml-auto flex items-center gap-3 text-xs" style={{ color: "#526080" }}>
              <span>
                <strong className="text-white">{firs.length}</strong> results
              </span>
            </div>
          </div>
        </div>

        {/* ── Table ── */}
        <div className="flex-1 overflow-auto relative">
          {loading && (
            <div className="absolute inset-0 flex items-center justify-center bg-[#080b12]/50 z-20">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2b91ff]" />
            </div>
          )}
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
                {!loading && sorted.map((fir, i) => {
                  const status = STATUS_CFG[fir.case_status_id || 0] || STATUS_CFG[0];
                  const isSelected = selectedId === fir.case_master_id;

                  return (
                    <motion.tr
                      key={fir.case_master_id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: i * 0.03 }}
                      onClick={() => setSelectedId(isSelected ? null : fir.case_master_id)}
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
                      <td className="px-4 py-3 whitespace-nowrap" style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                        <span className="font-mono font-bold" style={{ color: "#2b91ff" }}>
                          {fir.crime_no}
                        </span>
                      </td>

                      <td className="px-4 py-3" style={{ borderBottom: "1px solid rgba(255,255,255,0.04)", maxWidth: 220 }}>
                        <p className="font-medium text-white line-clamp-1">{fir.case_no || "N/A"}</p>
                      </td>

                      <td className="px-4 py-3 whitespace-nowrap" style={{ color: "#526080", borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                        {fir.crime_major_head_id || "N/A"}
                      </td>

                      <td className="px-4 py-3 whitespace-nowrap" style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                        <span className="text-[10px] text-[#526080]">-</span>
                      </td>

                      <td className="px-4 py-3 whitespace-nowrap" style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                        <span
                          className="px-2 py-0.5 rounded-full text-[10px] font-semibold"
                          style={{ background: status.bg, color: status.color }}
                        >
                          {status.label}
                        </span>
                      </td>

                      <td className="px-4 py-3 whitespace-nowrap text-xs" style={{ color: "#526080", borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                        ID {fir.police_station_id}
                      </td>

                      <td className="px-4 py-3 whitespace-nowrap" style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                        <span className="text-[10px] text-[#526080]">N/A</span>
                      </td>

                      <td className="px-4 py-3 whitespace-nowrap text-[11px]" style={{ color: "#2a3a55", borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
                        {formatRelativeTime(fir.crime_registered_date)}
                      </td>

                      <td className="px-4 py-3" style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}>
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

              {!loading && firs.length === 0 && (
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
        {selectedId && (
          <FIRDetailPanel caseId={selectedId} onClose={() => setSelectedId(null)} />
        )}
      </AnimatePresence>
    </div>
  );
}
