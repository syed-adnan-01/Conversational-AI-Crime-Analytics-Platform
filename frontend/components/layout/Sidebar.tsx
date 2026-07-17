"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  MessageSquareText,
  Search,
  Network,
  FolderOpen,
  BarChart3,
  FileText,
  Settings2,
  Shield,
  ChevronRight,
  LogOut,
  UserCircle2,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";

// ─── Nav Configuration ────────────────────────────────────────────────────

const NAV_GROUPS = [
  {
    label: "Intelligence",
    items: [
      { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { label: "AI Crime Chat", href: "/ai-chat", icon: MessageSquareText, badge: 3 },
      { label: "Criminal Network", href: "/criminal-network", icon: Network },
    ],
  },
  {
    label: "Operations",
    items: [
      { label: "FIR Search", href: "/fir-search", icon: Search },
      { label: "Investigation", href: "/investigation", icon: FolderOpen, badge: 1 },
    ],
  },
  {
    label: "Analytics",
    items: [
      { label: "Crime Analytics", href: "/analytics", icon: BarChart3 },
      { label: "Reports", href: "/reports", icon: FileText },
    ],
  },
  {
    label: "System",
    items: [
      { label: "Admin Panel", href: "/admin", icon: Settings2 },
    ],
  },
];

// ─── Component ────────────────────────────────────────────────────────────

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside
      className="hidden lg:flex flex-col h-screen w-[240px] shrink-0 overflow-y-auto"
      style={{
        background: "#0a0f1e",
        borderRight: "1px solid rgba(255,255,255,0.06)",
      }}
    >
      {/* ── Logo ── */}
      <div
        className="flex items-center gap-3 px-5 h-16 shrink-0"
        style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}
      >
        <div
          className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0"
          style={{
            background: "rgba(0,112,243,0.15)",
            border: "1px solid rgba(0,112,243,0.35)",
          }}
        >
          <Shield className="w-4 h-4 text-blue-400" />
        </div>
        <div>
          <div className="text-sm font-bold text-white leading-tight">
            CrimeSphere<span className="text-blue-400"> AI</span>
          </div>
          <div className="text-[10px] uppercase tracking-widest" style={{ color: "#2a3a55" }}>
            v2.4.1 — Classified
          </div>
        </div>
      </div>

      {/* ── AI Status Banner ── */}
      <div
        className="mx-3 mt-3 rounded-lg px-3 py-2 flex items-center gap-2"
        style={{
          background: "rgba(0,112,243,0.08)",
          border: "1px solid rgba(0,112,243,0.18)",
        }}
      >
        <Zap className="w-3.5 h-3.5 text-blue-400 shrink-0" />
        <div>
          <div className="text-[11px] font-medium text-blue-300">AI Engine Active</div>
          <div className="text-[10px]" style={{ color: "#526080" }}>Processing 1,203 signals</div>
        </div>
        <span className="ml-auto w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse shrink-0" />
      </div>

      {/* ── Navigation ── */}
      <nav className="flex-1 px-3 py-4 space-y-6">
        {NAV_GROUPS.map((group) => (
          <div key={group.label}>
            {/* Group label */}
            <p
              className="text-[10px] font-semibold uppercase tracking-[0.15em] px-2 mb-1.5"
              style={{ color: "#2a3a55" }}
            >
              {group.label}
            </p>

            {/* Items */}
            <ul className="space-y-0.5">
              {group.items.map((item) => {
                const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
                const Icon = item.icon;

                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={cn(
                        "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 group relative",
                        isActive
                          ? "text-white"
                          : "hover:text-white"
                      )}
                      style={{
                        background: isActive
                          ? "rgba(0,112,243,0.15)"
                          : "transparent",
                        color: isActive ? "white" : "#526080",
                        border: isActive
                          ? "1px solid rgba(0,112,243,0.25)"
                          : "1px solid transparent",
                      }}
                      onMouseEnter={(e) => {
                        if (!isActive) {
                          (e.currentTarget as HTMLAnchorElement).style.background = "rgba(255,255,255,0.04)";
                          (e.currentTarget as HTMLAnchorElement).style.color = "#94a3c0";
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (!isActive) {
                          (e.currentTarget as HTMLAnchorElement).style.background = "transparent";
                          (e.currentTarget as HTMLAnchorElement).style.color = "#526080";
                        }
                      }}
                    >
                      {/* Active indicator */}
                      {isActive && (
                        <span
                          className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 rounded-full"
                          style={{ background: "#0070f3" }}
                        />
                      )}

                      <Icon
                        className="w-4 h-4 shrink-0"
                        style={{ color: isActive ? "#2b91ff" : "inherit" }}
                      />
                      <span className="flex-1 truncate">{item.label}</span>

                      {/* Badge */}
                      {"badge" in item && item.badge && (
                        <span
                          className="text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[18px] text-center"
                          style={{
                            background: "#ff2d55",
                            color: "white",
                          }}
                        >
                          {item.badge}
                        </span>
                      )}

                      {/* Active arrow */}
                      {isActive && (
                        <ChevronRight className="w-3 h-3 shrink-0 text-blue-400" />
                      )}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* ── User Profile ── */}
      <div
        className="mx-3 mb-3 rounded-xl p-3"
        style={{
          background: "rgba(255,255,255,0.03)",
          border: "1px solid rgba(255,255,255,0.06)",
        }}
      >
        <div className="flex items-center gap-3 mb-3">
          <div
            className="w-9 h-9 rounded-full flex items-center justify-center shrink-0 text-sm font-bold text-white"
            style={{ background: "linear-gradient(135deg, #0070f3, #bf5af2)" }}
          >
            RK
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-semibold text-white truncate">SP Rajesh Kumar</div>
            <div className="text-[11px] truncate" style={{ color: "#526080" }}>
              IPS-2024-0042 · L-3
            </div>
          </div>
          <UserCircle2 className="w-4 h-4 shrink-0" style={{ color: "#2a3a55" }} />
        </div>

        {/* Clearance badge */}
        <div
          className="text-[10px] font-semibold uppercase tracking-wider text-center rounded-md py-1 mb-2"
          style={{
            background: "rgba(0,112,243,0.1)",
            border: "1px solid rgba(0,112,243,0.2)",
            color: "#2b91ff",
          }}
        >
          Clearance Level 3 — Confidential
        </div>

        <button
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors"
          style={{ color: "#526080" }}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLButtonElement).style.color = "#ff2d55";
            (e.currentTarget as HTMLButtonElement).style.background = "rgba(255,45,85,0.08)";
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLButtonElement).style.color = "#526080";
            (e.currentTarget as HTMLButtonElement).style.background = "transparent";
          }}
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}
