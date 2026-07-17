"use client";

import { recentFIRs } from "@/lib/mock-data/dashboard";
import { formatRelativeTime } from "@/lib/utils";
import type { RiskLevel, CrimeStatus } from "@/types";

const RISK_CONFIG: Record<RiskLevel, { label: string; color: string; bg: string }> = {
  critical: { label: "Critical", color: "#ff2d55", bg: "rgba(255,45,85,0.12)" },
  high:     { label: "High",     color: "#ff8c00", bg: "rgba(255,140,0,0.12)" },
  medium:   { label: "Medium",   color: "#ffd60a", bg: "rgba(255,214,10,0.12)" },
  low:      { label: "Low",      color: "#30d158", bg: "rgba(48,209,88,0.12)" },
};

const STATUS_CONFIG: Record<CrimeStatus, { label: string; color: string; bg: string }> = {
  open:          { label: "Open",          color: "#2b91ff", bg: "rgba(43,145,255,0.1)" },
  investigating: { label: "Investigating", color: "#ffd60a", bg: "rgba(255,214,10,0.1)" },
  closed:        { label: "Closed",        color: "#30d158", bg: "rgba(48,209,88,0.1)" },
  escalated:     { label: "Escalated",     color: "#ff2d55", bg: "rgba(255,45,85,0.1)" },
  pending:       { label: "Pending",       color: "#526080", bg: "rgba(82,96,128,0.1)" },
};

export default function RecentFIRsTable() {
  return (
    <div
      className="rounded-xl overflow-hidden"
      style={{
        background: "#0d1322",
        border: "1px solid rgba(255,255,255,0.06)",
      }}
    >
      {/* Header */}
      <div
        className="flex items-center justify-between px-5 py-4"
        style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}
      >
        <div>
          <h3 className="text-sm font-bold text-white">Recent FIRs</h3>
          <p className="text-xs mt-0.5" style={{ color: "#526080" }}>
            Latest registered cases — sorted by report time
          </p>
        </div>
        <button
          className="text-xs px-3 py-1.5 rounded-lg transition-colors"
          style={{
            background: "rgba(0,112,243,0.1)",
            border: "1px solid rgba(0,112,243,0.2)",
            color: "#2b91ff",
          }}
        >
          View all FIRs →
        </button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
              {["FIR No.", "Title", "Crime Type", "Risk", "Status", "District", "AI Score", "Reported"].map((h) => (
                <th
                  key={h}
                  className="px-4 py-3 text-left font-semibold uppercase tracking-wider whitespace-nowrap"
                  style={{ color: "#2a3a55" }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {recentFIRs.map((fir, i) => {
              const risk   = RISK_CONFIG[fir.riskLevel];
              const status = STATUS_CONFIG[fir.status];
              const isLast = i === recentFIRs.length - 1;

              return (
                <tr
                  key={fir.id}
                  className="group transition-colors cursor-pointer"
                  style={{
                    borderBottom: isLast ? "none" : "1px solid rgba(255,255,255,0.04)",
                  }}
                  onMouseEnter={(e) =>
                    ((e.currentTarget as HTMLTableRowElement).style.background = "rgba(255,255,255,0.025)")
                  }
                  onMouseLeave={(e) =>
                    ((e.currentTarget as HTMLTableRowElement).style.background = "transparent")
                  }
                >
                  {/* FIR No */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="font-mono font-semibold" style={{ color: "#2b91ff" }}>
                      {fir.firNumber}
                    </span>
                  </td>

                  {/* Title */}
                  <td className="px-4 py-3 max-w-[180px]">
                    <span className="text-white font-medium line-clamp-1">{fir.title}</span>
                    <span className="block text-[10px] mt-0.5" style={{ color: "#2a3a55" }}>
                      {fir.assignedTo}
                    </span>
                  </td>

                  {/* Crime Type */}
                  <td className="px-4 py-3 whitespace-nowrap" style={{ color: "#526080" }}>
                    {fir.crimeType}
                  </td>

                  {/* Risk */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span
                      className="px-2 py-0.5 rounded-full text-[10px] font-bold"
                      style={{ background: risk.bg, color: risk.color }}
                    >
                      {risk.label}
                    </span>
                  </td>

                  {/* Status */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span
                      className="px-2 py-0.5 rounded-full text-[10px] font-semibold"
                      style={{ background: status.bg, color: status.color }}
                    >
                      {status.label}
                    </span>
                  </td>

                  {/* District */}
                  <td className="px-4 py-3 whitespace-nowrap" style={{ color: "#526080" }}>
                    {fir.district}
                  </td>

                  {/* AI Score */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <div className="flex items-center gap-2">
                      <div
                        className="flex-1 h-1 rounded-full overflow-hidden"
                        style={{ background: "rgba(255,255,255,0.07)", width: 48 }}
                      >
                        <div
                          className="h-full rounded-full"
                          style={{
                            width: `${fir.aiScore}%`,
                            background:
                              fir.aiScore >= 80
                                ? "#ff2d55"
                                : fir.aiScore >= 60
                                ? "#ff8c00"
                                : "#30d158",
                          }}
                        />
                      </div>
                      <span
                        className="font-mono font-bold text-[11px]"
                        style={{
                          color:
                            fir.aiScore >= 80
                              ? "#ff2d55"
                              : fir.aiScore >= 60
                              ? "#ff8c00"
                              : "#30d158",
                        }}
                      >
                        {fir.aiScore}
                      </span>
                    </div>
                  </td>

                  {/* Reported */}
                  <td className="px-4 py-3 whitespace-nowrap" style={{ color: "#2a3a55" }}>
                    {formatRelativeTime(fir.reportedAt)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
