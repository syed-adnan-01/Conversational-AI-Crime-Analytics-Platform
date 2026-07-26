"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { AlertTriangle, Zap, Info, Clock, ExternalLink } from "lucide-react";
import { getAlerts, AlertData } from "@/lib/services/dashboard";
import { formatRelativeTime } from "@/lib/utils";

const TYPE_CONFIG: Record<string, { icon: React.ElementType; color: string; bg: string; border: string; dot: string; label: string }> = {
  critical: {
    icon: AlertTriangle,
    color: "#ff2d55",
    bg: "rgba(255,45,85,0.08)",
    border: "rgba(255,45,85,0.2)",
    dot: "#ff2d55",
    label: "CRITICAL",
  },
  high: {
    icon: Zap,
    color: "#ff8c00",
    bg: "rgba(255,140,0,0.08)",
    border: "rgba(255,140,0,0.2)",
    dot: "#ff8c00",
    label: "HIGH",
  },
  medium: {
    icon: Zap,
    color: "#ffd60a",
    bg: "rgba(255,214,10,0.08)",
    border: "rgba(255,214,10,0.2)",
    dot: "#ffd60a",
    label: "WARNING",
  },
  low: {
    icon: Info,
    color: "#0070f3",
    bg: "rgba(0,112,243,0.08)",
    border: "rgba(0,112,243,0.2)",
    dot: "#0070f3",
    label: "INFO",
  },
};

export default function AlertsFeed() {
  const [alerts, setAlerts] = useState<AlertData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAlerts()
      .then(setAlerts)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div
      className="rounded-xl p-5 h-full flex flex-col relative"
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
            {alerts.filter((a) => !a.read).length} unread
          </span>
        </div>
      </div>

      {/* Alert list */}
      <div className="flex-1 space-y-2.5 overflow-y-auto pr-1 relative">
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-[#0d1322]/80 z-10">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2b91ff]" />
          </div>
        )}
        {!loading && alerts.length === 0 && (
          <div className="absolute inset-0 flex items-center justify-center z-10">
            <p style={{ color: "#526080" }} className="text-sm">No new alerts.</p>
          </div>
        )}
        {alerts.map((alert, i) => {
          const cfg = TYPE_CONFIG[alert.severity] ?? TYPE_CONFIG.low;
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
                    {!alert.read && (
                      <span
                        className="text-[9px] font-semibold uppercase px-1.5 py-0.5 rounded"
                        style={{ background: "rgba(255,45,85,0.1)", color: "#ff2d55" }}
                      >
                        New
                      </span>
                    )}
                  </div>

                  <p className="text-xs font-semibold text-white mb-0.5 leading-snug">
                    {alert.title}
                  </p>
                  <p className="text-xs leading-snug line-clamp-2" style={{ color: "#526080" }}>
                    {alert.description}
                  </p>

                  <div className="flex items-center gap-3 mt-1.5">
                    <div className="flex items-center gap-1" style={{ color: "#2a3a55" }}>
                      <Clock className="w-2.5 h-2.5" />
                      <span className="text-[10px]">{formatRelativeTime(alert.time)}</span>
                    </div>
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
          View all {alerts.length} alerts →
        </button>
      </div>
    </div>
  );
}
