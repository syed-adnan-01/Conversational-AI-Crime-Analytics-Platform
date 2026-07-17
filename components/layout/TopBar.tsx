"use client";

import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import {
  Bell,
  Search,
  RefreshCcw,
  ChevronDown,
  Shield,
  Wifi,
} from "lucide-react";
import { recentAlerts } from "@/lib/mock-data/dashboard";
import { formatRelativeTime } from "@/lib/utils";

// Map pathnames to readable page titles
const PAGE_TITLES: Record<string, { title: string; subtitle: string }> = {
  "/dashboard":         { title: "Command Dashboard",      subtitle: "Real-time crime intelligence overview" },
  "/ai-chat":           { title: "AI Crime Chat",           subtitle: "Converse with CrimeSphere Intelligence" },
  "/fir-search":        { title: "FIR Search",              subtitle: "Search and filter all registered FIRs" },
  "/criminal-network":  { title: "Criminal Network",        subtitle: "Visualise criminal associations and networks" },
  "/investigation":     { title: "Investigation Workspace", subtitle: "Active cases and evidence management" },
  "/analytics":         { title: "Crime Analytics",         subtitle: "Statistical insights and trend analysis" },
  "/reports":           { title: "Reports",                 subtitle: "Generate and manage official reports" },
  "/admin":             { title: "Admin Panel",             subtitle: "System configuration and user management" },
};

export default function TopBar() {
  const pathname = usePathname();
  const [currentTime, setCurrentTime] = useState("");
  const [showNotifs, setShowNotifs] = useState(false);
  const [unreadCount] = useState(
    recentAlerts.filter((a) => a.actionRequired).length
  );

  const pageInfo = PAGE_TITLES[pathname] ?? {
    title: "CrimeSphere AI",
    subtitle: "National Crime Intelligence Platform",
  };

  // Live clock
  useEffect(() => {
    const tick = () =>
      setCurrentTime(
        new Date().toLocaleString("en-IN", {
          timeZone: "Asia/Kolkata",
          hour12: false,
          weekday: "short",
          day: "2-digit",
          month: "short",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = () => setShowNotifs(false);
    if (showNotifs) window.addEventListener("click", handler);
    return () => window.removeEventListener("click", handler);
  }, [showNotifs]);

  return (
    <header
      className="h-16 shrink-0 flex items-center px-6 gap-4 relative z-30"
      style={{
        background: "rgba(10,15,30,0.95)",
        borderBottom: "1px solid rgba(255,255,255,0.06)",
        backdropFilter: "blur(12px)",
      }}
    >
      {/* ── Page Title ── */}
      <div className="flex-1 min-w-0">
        <h1 className="text-base font-bold text-white leading-tight truncate">
          {pageInfo.title}
        </h1>
        <p className="text-xs truncate" style={{ color: "#2a3a55" }}>
          {pageInfo.subtitle}
        </p>
      </div>

      {/* ── Right Controls ── */}
      <div className="flex items-center gap-3 shrink-0">

        {/* Search */}
        <div
          className="hidden md:flex items-center gap-2 h-9 px-3 rounded-lg text-sm"
          style={{
            background: "rgba(255,255,255,0.04)",
            border: "1px solid rgba(255,255,255,0.08)",
            color: "#526080",
            minWidth: 200,
          }}
        >
          <Search className="w-3.5 h-3.5 shrink-0" />
          <span className="text-sm">Search anything…</span>
          <kbd
            className="ml-auto text-[10px] px-1.5 py-0.5 rounded"
            style={{ background: "rgba(255,255,255,0.06)", color: "#2a3a55" }}
          >
            ⌘K
          </kbd>
        </div>

        {/* System status */}
        <div
          className="hidden sm:flex items-center gap-1.5 h-9 px-3 rounded-lg text-xs"
          style={{
            background: "rgba(48,209,88,0.06)",
            border: "1px solid rgba(48,209,88,0.15)",
            color: "#30d158",
          }}
        >
          <Wifi className="w-3 h-3" />
          <span>Live</span>
        </div>

        {/* Clock */}
        <div
          className="hidden xl:block text-xs font-mono tabular-nums px-3 py-1.5 rounded-lg"
          style={{
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(255,255,255,0.07)",
            color: "#2a3a55",
          }}
        >
          {currentTime} IST
        </div>

        {/* Refresh */}
        <button
          className="w-9 h-9 rounded-lg flex items-center justify-center transition-colors"
          style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)" }}
          title="Refresh data"
          onMouseEnter={(e) => ((e.currentTarget as HTMLButtonElement).style.background = "rgba(255,255,255,0.08)")}
          onMouseLeave={(e) => ((e.currentTarget as HTMLButtonElement).style.background = "rgba(255,255,255,0.04)")}
        >
          <RefreshCcw className="w-3.5 h-3.5" style={{ color: "#526080" }} />
        </button>

        {/* Notifications */}
        <div className="relative">
          <button
            className="relative w-9 h-9 rounded-lg flex items-center justify-center transition-colors"
            style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)" }}
            onClick={(e) => { e.stopPropagation(); setShowNotifs(!showNotifs); }}
          >
            <Bell className="w-3.5 h-3.5" style={{ color: "#526080" }} />
            {unreadCount > 0 && (
              <span
                className="absolute -top-1 -right-1 w-4 h-4 rounded-full text-[9px] font-bold flex items-center justify-center"
                style={{ background: "#ff2d55", color: "white" }}
              >
                {unreadCount}
              </span>
            )}
          </button>

          {/* Notification Dropdown */}
          {showNotifs && (
            <div
              className="absolute right-0 top-11 w-80 rounded-xl overflow-hidden z-50"
              style={{
                background: "#0d1322",
                border: "1px solid rgba(255,255,255,0.08)",
                boxShadow: "0 24px 48px rgba(0,0,0,0.6)",
              }}
              onClick={(e) => e.stopPropagation()}
            >
              <div
                className="flex items-center justify-between px-4 py-3"
                style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}
              >
                <span className="text-sm font-semibold text-white">Alerts</span>
                <span
                  className="text-xs px-2 py-0.5 rounded-full"
                  style={{ background: "rgba(255,45,85,0.15)", color: "#ff2d55" }}
                >
                  {unreadCount} urgent
                </span>
              </div>
              <div className="max-h-72 overflow-y-auto">
                {recentAlerts.slice(0, 4).map((alert) => (
                  <div
                    key={alert.id}
                    className="px-4 py-3 transition-colors cursor-pointer"
                    style={{ borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                    onMouseEnter={(e) => ((e.currentTarget as HTMLDivElement).style.background = "rgba(255,255,255,0.03)")}
                    onMouseLeave={(e) => ((e.currentTarget as HTMLDivElement).style.background = "transparent")}
                  >
                    <div className="flex items-start gap-2.5">
                      <span
                        className="w-2 h-2 rounded-full mt-1.5 shrink-0"
                        style={{
                          background:
                            alert.type === "critical" ? "#ff2d55" :
                            alert.type === "warning"  ? "#ff8c00" : "#0070f3",
                        }}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-semibold text-white truncate">{alert.title}</p>
                        <p className="text-xs mt-0.5 truncate" style={{ color: "#526080" }}>
                          {alert.message}
                        </p>
                        <p className="text-[10px] mt-1" style={{ color: "#2a3a55" }}>
                          {formatRelativeTime(alert.timestamp)} · {alert.district}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div
                className="px-4 py-2.5 text-center"
                style={{ borderTop: "1px solid rgba(255,255,255,0.05)" }}
              >
                <button className="text-xs text-blue-400 hover:text-blue-300 transition-colors">
                  View all alerts →
                </button>
              </div>
            </div>
          )}
        </div>

        {/* User avatar */}
        <div className="flex items-center gap-2 cursor-pointer group">
          <div
            className="w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0"
            style={{ background: "linear-gradient(135deg, #0070f3, #bf5af2)" }}
          >
            RK
          </div>
          <div className="hidden sm:block">
            <div className="text-xs font-semibold text-white leading-tight">SP Rajesh Kumar</div>
            <div className="flex items-center gap-1">
              <Shield className="w-2.5 h-2.5 text-blue-400" />
              <span className="text-[10px]" style={{ color: "#2a3a55" }}>Level 3</span>
            </div>
          </div>
          <ChevronDown className="w-3 h-3 hidden sm:block" style={{ color: "#2a3a55" }} />
        </div>
      </div>
    </header>
  );
}
