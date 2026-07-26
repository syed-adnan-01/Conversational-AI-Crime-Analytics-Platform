"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FileText, BarChart3, Network, Calendar, AlertTriangle,
  FolderOpen, Download, Eye, Plus,
  Clock, CheckCircle2, XCircle, Loader2, ChevronRight,
  Shield, User, Search,
} from "lucide-react";
import {
  REPORT_TEMPLATES, TYPE_CFG, CLASS_CFG,
  type ReportType,
} from "@/lib/mock-data/reports";
import { formatRelativeTime, formatDate } from "@/lib/utils";
import { reportsService, ReportSummary, ReportDetail } from "@/lib/services/reports";

// ─── Icon map ─────────────────────────────────────────────────────────────────
const TEMPLATE_ICONS: Record<string, React.ElementType> = {
  FileText, BarChart3, Network, Calendar, AlertTriangle, FolderOpen,
};

// ─── Status config ────────────────────────────────────────────────────────────
interface StatusCfgItem {
  icon: React.ElementType;
  color: string;
  label: string;
  bg: string;
}

const STATUS_CFG: Record<string, StatusCfgItem> = {
  READY:      { icon: CheckCircle2, color: "#30d158", label: "Ready",      bg: "rgba(48,209,88,0.1)"  },
  GENERATING: { icon: Loader2,      color: "#ffd60a", label: "Generating", bg: "rgba(255,214,10,0.1)" },
  FAILED:     { icon: XCircle,      color: "#ff2d55", label: "Failed",     bg: "rgba(255,45,85,0.1)"  },
  SCHEDULED:  { icon: Clock,        color: "#0070f3", label: "Scheduled",  bg: "rgba(0,112,243,0.1)"  },
};

// ─── Report Preview Panel ─────────────────────────────────────────────────────
function ReportPreview({ reportId, onClose }: { reportId: string; onClose: () => void }) {
  const [report, setReport] = useState<ReportDetail & { sections?: { title?: string; content?: unknown }[] } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    reportsService.getReport(reportId).then((res) => {
      setReport(res);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [reportId]);

  if (loading) {
    return (
      <motion.div
        initial={{ x: "100%", opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: "100%", opacity: 0 }}
        className="flex flex-col h-full shrink-0 overflow-hidden items-center justify-center text-white"
        style={{ width: 400, background: "#0a0f1e", borderLeft: "1px solid rgba(255,255,255,0.07)" }}
      >
        <Loader2 className="w-8 h-8 animate-spin mb-2" />
        <p>Loading report...</p>
      </motion.div>
    );
  }

  if (!report) {
    return (
      <motion.div
        initial={{ x: "100%", opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: "100%", opacity: 0 }}
        className="flex flex-col h-full shrink-0 overflow-hidden items-center justify-center text-white"
        style={{ width: 400, background: "#0a0f1e", borderLeft: "1px solid rgba(255,255,255,0.07)" }}
      >
        <XCircle className="w-8 h-8 text-red-500 mb-2" />
        <p>Failed to load report</p>
        <button onClick={onClose} className="mt-4 underline text-blue-400">Close</button>
      </motion.div>
    );
  }

  const typeCfg = (TYPE_CFG as Record<string, { label: string; color: string }>)[report.report_type] || TYPE_CFG["fir-summary"];
  const classCfg = (CLASS_CFG as Record<string, { color: string; bg: string }>)[String(report.metadata?.classification || "Restricted")] || CLASS_CFG["Restricted"];
  const status = STATUS_CFG[report.status] || STATUS_CFG["FAILED"];

  return (
    <motion.div
      initial={{ x: "100%", opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: "100%", opacity: 0 }}
      transition={{ type: "spring", damping: 28, stiffness: 280 }}
      className="flex flex-col h-full shrink-0 overflow-hidden"
      style={{ width: 400, background: "#0a0f1e", borderLeft: "1px solid rgba(255,255,255,0.07)" }}
    >
      {/* Panel header */}
      <div className="px-5 py-4 shrink-0" style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold" style={{ color: "#526080" }}>Report Preview</span>
          <div className="flex items-center gap-2">
            {report.status === "READY" && (
              <button 
                onClick={() => {
                  reportsService.exportReport(reportId).then(res => {
                    alert("Report exported!");
                  }).catch(e => console.error(e));
                }}
                className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg transition-colors"
                style={{ background: "rgba(0,112,243,0.12)", border: "1px solid rgba(0,112,243,0.25)", color: "#2b91ff" }}>
                <Download className="w-3 h-3" /> Export
              </button>
            )}
            <button onClick={onClose} className="w-7 h-7 rounded-lg flex items-center justify-center"
              style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)" }}>
              <XCircle className="w-3.5 h-3.5" style={{ color: "#526080" }} />
            </button>
          </div>
        </div>

        {/* Classification banner */}
        <div className="w-full text-center py-1.5 rounded-lg font-bold text-xs tracking-widest uppercase mb-3"
          style={{ background: classCfg.bg, color: classCfg.color, border: `1px solid ${classCfg.color}30` }}>
          ⚠ {String(report.metadata?.classification || "RESTRICTED")} — Government of India ⚠
        </div>

        <h3 className="text-sm font-bold text-white mb-1 leading-snug">{report.title}</h3>
        <div className="flex flex-wrap gap-2 text-[10px]" style={{ color: "#526080" }}>
          <span className="flex items-center gap-1"><User className="w-3 h-3" />{report.generated_by}</span>
        </div>
      </div>

      {/* Document preview body */}
      <div className="flex-1 overflow-y-auto p-5">
        {report.status === "GENERATING" ? (
          <div className="flex flex-col items-center justify-center h-full text-center gap-4">
            <motion.div animate={{ rotate: 360 }} transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}>
              <Loader2 className="w-10 h-10" style={{ color: "#ffd60a" }} />
            </motion.div>
            <div>
              <p className="text-sm font-semibold text-white mb-1">Generating Report…</p>
              <p className="text-xs" style={{ color: "#526080" }}>CrimeSphere AI is compiling data and generating your report.</p>
            </div>
          </div>
        ) : report.status === "FAILED" ? (
          <div className="flex flex-col items-center justify-center h-full text-center gap-4">
            <XCircle className="w-10 h-10" style={{ color: "#ff2d55" }} />
            <div>
              <p className="text-sm font-semibold text-white mb-1">Generation Failed</p>
            </div>
          </div>
        ) : (
          /* Actual report preview */
          <div className="space-y-5">
            {/* Report "header" - looks like a printed document */}
            <div className="rounded-xl overflow-hidden" style={{ border: "1px solid rgba(255,255,255,0.08)" }}>
              {/* Doc header */}
              <div className="px-5 py-4" style={{ background: "rgba(0,112,243,0.08)", borderBottom: "1px solid rgba(255,255,255,0.07)" }}>
                <div className="flex items-center gap-2 mb-2">
                  <Shield className="w-4 h-4" style={{ color: "#0070f3" }} />
                  <span className="text-xs font-bold" style={{ color: "#0070f3" }}>CrimeSphere AI · National Crime Intelligence Platform</span>
                </div>
                <p className="text-[10px]" style={{ color: "#2a3a55" }}>
                  Generated: {formatDate(report.generated_at)} · Doc ID: {(report.report_id || "").toUpperCase().split('-')[0]}
                </p>
              </div>

              {/* Summary */}
              <div className="px-5 py-4">
                <p className="text-[10px] uppercase tracking-widest font-semibold mb-2" style={{ color: "#2a3a55" }}>Executive Summary</p>
                <p className="text-xs leading-relaxed" style={{ color: "#94a3c0" }}>{String(report.metadata?.summary || "No summary available.")}</p>
              </div>
            </div>

            {/* Sections */}
            {(report.sections || []).map((section: { title?: string; content?: unknown }, i: number) => (
              <motion.div key={i} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
                className="rounded-xl p-4" style={{ background: "rgba(255,255,255,0.025)", border: "1px solid rgba(255,255,255,0.06)" }}>
                <p className="text-xs font-bold text-white mb-2">{i + 1}. {section.title || "Section"}</p>
                <div className="text-xs leading-relaxed whitespace-pre-line" style={{ color: "#94a3c0" }}>
                  {typeof section.content === "string" ? section.content : JSON.stringify(section.content, null, 2)}
                </div>
              </motion.div>
            ))}

            {/* Footer */}
            <div className="rounded-xl px-5 py-3" style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)" }}>
              <p className="text-[10px] text-center" style={{ color: "#2a3a55" }}>
                This document is classified {String(report.metadata?.classification || "RESTRICTED")}.
                <br />Generated by CrimeSphere AI v2.4
              </p>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
}

// ─── Generate Report Modal ────────────────────────────────────────────────────
function GenerateModal({ onClose, onGenerate }: { onClose: () => void, onGenerate: () => void }) {
  const [selectedType, setSelectedType] = useState<ReportType | null>(null);
  const [generating, setGenerating] = useState(false);

  const handleGenerate = async () => {
    if (!selectedType) return;
    setGenerating(true);
    try {
      await reportsService.generateReport({ report_type: selectedType, case_id: "default" });
      onGenerate();
    } catch (err) {
      console.error(err);
    } finally {
      setGenerating(false);
      onClose();
    }
  };

  return (
    <motion.div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <motion.div className="relative rounded-2xl w-full max-w-xl overflow-hidden z-10"
        initial={{ scale: 0.95, y: 20 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.95, y: 20 }}
        style={{ background: "#0d1322", border: "1px solid rgba(255,255,255,0.1)", boxShadow: "0 32px 64px rgba(0,0,0,0.8)" }}>

        {/* Header */}
        <div className="flex items-center justify-between px-6 py-5" style={{ borderBottom: "1px solid rgba(255,255,255,0.07)" }}>
          <div>
            <h3 className="text-base font-bold text-white">Generate New Report</h3>
            <p className="text-xs mt-0.5" style={{ color: "#526080" }}>Select a template to generate a classified report</p>
          </div>
          <button onClick={onClose} className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)" }}>
            <XCircle className="w-4 h-4" style={{ color: "#526080" }} />
          </button>
        </div>

        {/* Templates grid */}
        <div className="p-6 grid grid-cols-2 gap-3">
          {REPORT_TEMPLATES.map((tpl) => {
            const Icon = TEMPLATE_ICONS[tpl.icon] ?? FileText;
            const isSelected = selectedType === tpl.type;
            return (
              <button key={tpl.id} onClick={() => setSelectedType(tpl.type as ReportType)}
                className="text-left rounded-xl p-4 transition-all"
                style={{
                  background: isSelected ? `${tpl.color}12` : "rgba(255,255,255,0.025)",
                  border: isSelected ? `1.5px solid ${tpl.color}50` : "1px solid rgba(255,255,255,0.07)",
                }}>
                <div className="w-8 h-8 rounded-lg flex items-center justify-center mb-3"
                  style={{ background: `${tpl.color}18`, border: `1px solid ${tpl.color}30` }}>
                  <Icon className="w-4 h-4" style={{ color: tpl.color }} />
                </div>
                <p className="text-xs font-bold text-white mb-1">{tpl.name}</p>
                <p className="text-[10px] leading-snug mb-2" style={{ color: "#526080" }}>{tpl.description}</p>
              </button>
            );
          })}
        </div>

        {/* Actions */}
        <div className="px-6 pb-6 flex gap-3">
          <button onClick={onClose} className="flex-1 py-2.5 rounded-xl text-sm font-semibold transition-colors"
            style={{ background: "rgba(255,255,255,0.05)", color: "#526080" }}>
            Cancel
          </button>
          <button onClick={handleGenerate} disabled={!selectedType || generating}
            className="flex-1 py-2.5 rounded-xl text-sm font-bold transition-all flex items-center justify-center gap-2"
            style={{
              background: selectedType && !generating ? "#0070f3" : "rgba(0,112,243,0.3)",
              color: selectedType && !generating ? "white" : "#526080",
              cursor: selectedType && !generating ? "pointer" : "not-allowed",
            }}>
            {generating ? <><motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: "linear" }}><Loader2 className="w-4 h-4" /></motion.div>Generating…</> : <><Plus className="w-4 h-4" />Generate Report</>}
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────
export default function ReportsInterface() {
  const [reports, setReports] = useState<ReportSummary[]>([]);
  const [selected, setSelected] = useState<ReportSummary | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [search, setSearch] = useState("");
  const [filterType, setFilterType] = useState("all");
  const [filterStatus, setFilterStatus] = useState("all");

  const fetchReports = () => {
    reportsService.listReports().then((res) => {
      const list = res?.reports ?? [];
      setReports(list);
      if (list.length > 0 && !selected) {
        setSelected(list[0]);
      }
    }).catch((err) => {
      console.error("Failed to load reports:", err);
      setReports([]);
    });
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const filtered = reports.filter((r) => {
    const q = search.toLowerCase();
    const matchQ = !q || (r.title || "").toLowerCase().includes(q);
    const matchT = filterType === "all" || r.report_type === filterType;
    const matchS = filterStatus === "all" || (r.status || "").toLowerCase() === filterStatus;
    return matchQ && matchT && matchS;
  });

  return (
    <div className="flex h-[calc(100vh-4rem)] -m-6 overflow-hidden">

      {/* ═══ MAIN: Reports List ═══ */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden" style={{ background: "#080b12" }}>

        {/* Top bar */}
        <div className="px-6 py-4 shrink-0"
          style={{ background: "rgba(10,15,30,0.95)", borderBottom: "1px solid rgba(255,255,255,0.06)", backdropFilter: "blur(12px)" }}>

          <div className="flex items-center justify-between gap-4 mb-4">
            <div>
              <h2 className="text-base font-bold text-white">Reports</h2>
              <p className="text-xs" style={{ color: "#526080" }}>
                {reports.filter((r) => r.status === "READY").length} ready · {reports.filter((r) => r.status === "GENERATING").length} generating
              </p>
            </div>
            <button onClick={() => setShowModal(true)}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition-all"
              style={{ background: "#0070f3", color: "white" }}>
              <Plus className="w-4 h-4" />
              Generate Report
            </button>
          </div>

          {/* Filters */}
          <div className="flex items-center gap-3 flex-wrap">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none" style={{ color: "#526080" }} />
              <input type="text" value={search} onChange={(e) => setSearch(e.target.value)}
                placeholder="Search reports…"
                className="w-full h-9 pl-9 pr-3 rounded-lg text-xs text-white outline-none"
                style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.09)" }} />
            </div>
            <select value={filterType} onChange={(e) => setFilterType(e.target.value)}
              className="h-9 px-3 rounded-lg text-xs text-white outline-none"
              style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.09)" }}>
              <option value="all" style={{ background: "#0d1322" }}>All Types</option>
              {Object.entries(TYPE_CFG).map(([k, v]) => <option key={k} value={k} style={{ background: "#0d1322" }}>{v.label}</option>)}
            </select>
            <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}
              className="h-9 px-3 rounded-lg text-xs text-white outline-none"
              style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.09)" }}>
              <option value="all" style={{ background: "#0d1322" }}>All Status</option>
              {["ready","generating","failed","scheduled"].map((s) => <option key={s} value={s} style={{ background: "#0d1322" }} className="capitalize">{s.charAt(0).toUpperCase()+s.slice(1)}</option>)}
            </select>
            <span className="text-xs ml-auto" style={{ color: "#526080" }}>
              <strong className="text-white">{filtered.length}</strong> reports
            </span>
          </div>
        </div>

        {/* Report list */}
        <div className="flex-1 overflow-y-auto p-6 space-y-3">
          <AnimatePresence>
            {filtered.map((report, i) => {
              const typeCfg   = (TYPE_CFG as Record<string, { label: string; color: string }>)[report.report_type] || TYPE_CFG["fir-summary"];
              const statusCfg = STATUS_CFG[report.status] || STATUS_CFG["FAILED"];
              const StatusIcon = statusCfg.icon;
              const isSelected = selected?.report_id === report.report_id;

              return (
                <motion.div key={report.report_id}
                  initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}
                  onClick={() => setSelected(isSelected ? null : report)}
                  className="rounded-xl p-4 cursor-pointer transition-all group"
                  style={{
                    background: isSelected ? "rgba(0,112,243,0.07)" : "#0d1322",
                    border: isSelected ? "1px solid rgba(0,112,243,0.3)" : "1px solid rgba(255,255,255,0.07)",
                  }}
                  onMouseEnter={(e) => { if (!isSelected) (e.currentTarget as HTMLDivElement).style.borderColor = "rgba(255,255,255,0.12)"; }}
                  onMouseLeave={(e) => { if (!isSelected) (e.currentTarget as HTMLDivElement).style.borderColor = "rgba(255,255,255,0.07)"; }}>

                  <div className="flex items-start gap-4">
                    {/* Icon */}
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
                      style={{ background: `${typeCfg.color}15`, border: `1px solid ${typeCfg.color}30` }}>
                      <FileText className="w-5 h-5" style={{ color: typeCfg.color }} />
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2 mb-1.5">
                        <p className="text-sm font-bold text-white leading-snug">{report.title}</p>
                        <div className="flex items-center gap-1.5 shrink-0">
                          {/* Status */}
                          <span className="flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full"
                            style={{ background: statusCfg.bg, color: statusCfg.color }}>
                            <StatusIcon className={`w-2.5 h-2.5 ${report.status === "GENERATING" ? "animate-spin" : ""}`} />
                            {statusCfg.label}
                          </span>
                        </div>
                      </div>

                      <div className="flex flex-wrap gap-2 mb-2">
                        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full"
                          style={{ background: `${typeCfg.color}15`, color: typeCfg.color }}>
                          {typeCfg.label}
                        </span>
                      </div>

                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3 text-[10px]" style={{ color: "#2a3a55" }}>
                          <span className="flex items-center gap-1"><User className="w-2.5 h-2.5" />{report.generated_by}</span>
                          <span className="flex items-center gap-1"><Clock className="w-2.5 h-2.5" />{formatRelativeTime(report.generated_at)}</span>
                        </div>

                        <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button onClick={(e) => { e.stopPropagation(); setSelected(report); }}
                            className="p-1.5 rounded-lg transition-colors"
                            style={{ color: "#526080" }} title="Preview">
                            <Eye className="w-3.5 h-3.5" />
                          </button>
                          <ChevronRight className="w-3.5 h-3.5" style={{ color: isSelected ? "#2b91ff" : "#2a3a55" }} />
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>

          {filtered.length === 0 && (
            <div className="text-center py-20">
              <FileText className="w-10 h-10 mx-auto mb-3" style={{ color: "#2a3a55" }} />
              <p className="text-sm" style={{ color: "#526080" }}>No reports match your search.</p>
            </div>
          )}
        </div>
      </div>

      {/* ═══ RIGHT: Preview Panel ═══ */}
      <AnimatePresence>
        {selected && <ReportPreview reportId={selected.report_id} onClose={() => setSelected(null)} />}
      </AnimatePresence>

      {/* ═══ Generate Modal ═══ */}
      <AnimatePresence>
        {showModal && <GenerateModal onClose={() => setShowModal(false)} onGenerate={fetchReports} />}
      </AnimatePresence>
    </div>
  );
}
