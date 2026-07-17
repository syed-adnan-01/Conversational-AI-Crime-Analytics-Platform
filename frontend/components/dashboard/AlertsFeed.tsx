"use client";

import { motion } from "framer-motion";
import { AlertTriangle, Zap, Info, Clock, ExternalLink } from "lucide-react";
import { recentAlerts } from "@/lib/mock-data/dashboard";
import { formatRelativeTime } from "@/lib/utils";

const TYPE_CONFIG = {
  critical: {
    icon: AlertTriangle,
    color: "#ff2d55",
    bg: "rgba(255,45,85,0.08)",
    border: "rgba(255,45,85,0.2)",
    dot: "#ff2d55",
    label: "CRITICAL",
  },
  warning: {
    icon: Zap,
    color: "#ff8c00",
    bg: "rgba(255,140,0,0.08)",
    border: "rgba(255,140,0,0.2)",
    dot: "#ff8c00",
    label: "WARNING",
  },
  info: {
    icon: Info,
    color: "#0070f3",
    bg: "rgba(0,112,243,0.08)",
    border: "rgba(0,112,243,0.2)",
    dot: "#0070f3",
    label: "INFO",
  },
};

export default function AlertsFeed() {
  return (
    <div
      className="rounded-xl p-5 h-full flex flex-col"
      style={{
        background: "#0d1322",
        border: "1px solid rgba(255,255,255,0.06)",
      }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4 shrink-0">
        <div>
          <h3 className="text-sm font-bold text-white">Live Alerts</h3>
          <p className="text-xs mt-0.5" style={{ color: "#526080" }}>
            Real-time · Auto-refreshing
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" style={{ background: "#ff2d55" }} />
            <span className="relative inline-flex rounded-full h-2 w-2" style={{ background: "#ff2d55" }} />
          </span>
          <span className="text-xs" style={{ color: "#ff2d55" }}>
            {recentAlerts.filter((a) => a.actionRequired).length} urgent
          </span>
        </div>
      </div>

      {/* Alert list */}
      <div className="flex-1 space-y-2.5 overflow-y-auto pr-1">
        {recentAlerts.map((alert, i) => {
          const cfg = TYPE_CONFIG[alert.type] ?? TYPE_CONFIG.info;
          const Icon = cfg.icon;

          return (
            <motion.div
              key={alert.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.07 }}
              className="rounded-lg p-3 cursor-pointer group transition-all"
              style={{
                background: cfg.bg,
                border: `1px solid ${cfg.border}`,
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLDivElement).style.borderColor = cfg.color;
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLDivElement).style.borderColor = cfg.border;
              }}
            >
              <div className="flex items-start gap-2.5">
                {/* Icon */}
                <div
                  className="w-7 h-7 rounded-md flex items-center justify-center shrink-0 mt-0.5"
                  style={{ background: `${cfg.color}20` }}
                >
                  <Icon className="w-3.5 h-3.5" style={{ color: cfg.color }} />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-0.5">
                    <span
                      className="text-[9px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded"
                      style={{ background: `${cfg.color}20`, color: cfg.color }}
                    >
                      {cfg.label}
                    </span>
                    {alert.actionRequired && (
                      <span
                        className="text-[9px] font-semibold uppercase px-1.5 py-0.5 rounded"
                        style={{ background: "rgba(255,45,85,0.1)", color: "#ff2d55" }}
                      >
                        Action Required
                      </span>
                    )}
                  </div>

                  <p className="text-xs font-semibold text-white mb-0.5 leading-snug">
                    {alert.title}
                  </p>
                  <p className="text-xs leading-snug line-clamp-2" style={{ color: "#526080" }}>
                    {alert.message}
                  </p>

                  <div className="flex items-center gap-3 mt-1.5">
                    <div className="flex items-center gap-1" style={{ color: "#2a3a55" }}>
                      <Clock className="w-2.5 h-2.5" />
                      <span className="text-[10px]">{formatRelativeTime(alert.timestamp)}</span>
                    </div>
                    <span className="text-[10px]" style={{ color: "#2a3a55" }}>
                      {alert.district}
                    </span>
                    <span
                      className="ml-auto text-[10px] flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
                      style={{ color: cfg.color }}
                    >
                      <ExternalLink className="w-2.5 h-2.5" />
                      {alert.linkedFIR}
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Footer */}
      <div
        className="pt-3 mt-3 text-center shrink-0"
        style={{ borderTop: "1px solid rgba(255,255,255,0.05)" }}
      >
        <button className="text-xs transition-colors" style={{ color: "#2a3a55" }}
          onMouseEnter={(e) => ((e.currentTarget as HTMLButtonElement).style.color = "#0070f3")}
          onMouseLeave={(e) => ((e.currentTarget as HTMLButtonElement).style.color = "#2a3a55")}
        >
          View all {recentAlerts.length} alerts →
        </button>
      </div>
    </div>
  );
}
