"use client";

import { useEffect, useState } from "react";
import StatCard from "./StatCard";
import { getDashboardSummary, DashboardSummary } from "@/lib/services/dashboard";
import { Activity, Shield, FolderOpen, AlertTriangle } from "lucide-react";

export default function DashboardKPIs() {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    getDashboardSummary()
      .then(setData)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-32 rounded-xl bg-white/5 animate-pulse" />
        ))}
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-4 rounded-xl bg-red-500/10 text-red-400 text-sm border border-red-500/20">
        Failed to load dashboard summary.
      </div>
    );
  }

  const kpis = [
    {
      id: "total",
      label: "Total Cases",
      value: data.total_cases.toString(),
      change: "+12%",
      changeLabel: "vs last month",
      trend: "up" as const,
      color: "#2b91ff",
      glowColor: "rgba(43,145,255,0.15)",
      borderColor: "rgba(43,145,255,0.3)",
      icon: "FileText",
      description: "All registered FIRs",
    },
    {
      id: "open",
      label: "Open Investigations",
      value: data.open_cases.toString(),
      change: "-5%",
      changeLabel: "vs last month",
      trend: "down" as const,
      color: "#ff2d55",
      glowColor: "rgba(255,45,85,0.15)",
      borderColor: "rgba(255,45,85,0.3)",
      icon: "AlertTriangle",
      description: "Active and pending",
    },
    {
      id: "completion",
      label: "Resolution Rate",
      value: `${data.investigation_completion_percent}%`,
      change: "+2.4%",
      changeLabel: "improvement",
      trend: "up" as const,
      color: "#30d158",
      glowColor: "rgba(48,209,88,0.15)",
      borderColor: "rgba(48,209,88,0.3)",
      icon: "CheckCircle2",
      description: "Cases successfully closed",
    },
    {
      id: "evidence",
      label: "Evidence Processed",
      value: data.evidence_uploaded.toString(),
      change: "+1,204",
      changeLabel: "new artifacts",
      trend: "flat" as const,
      color: "#bf5af2",
      glowColor: "rgba(191,90,242,0.15)",
      borderColor: "rgba(191,90,242,0.3)",
      icon: "Brain",
      description: "AI-analyzed items",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      {kpis.map((stat, i) => (
        <StatCard key={stat.id} {...stat} index={i} />
      ))}
    </div>
  );
}
