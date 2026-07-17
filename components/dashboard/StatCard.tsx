"use client";

import { motion } from "framer-motion";
import {
  FileText,
  AlertTriangle,
  CheckCircle2,
  Brain,
  TrendingUp,
  TrendingDown,
  Minus,
} from "lucide-react";

const ICON_MAP: Record<string, React.ElementType> = {
  FileText,
  AlertTriangle,
  CheckCircle2,
  Brain,
};

interface StatCardProps {
  id: string;
  label: string;
  value: string;
  change: string;
  changeLabel: string;
  trend: "up" | "down" | "flat";
  color: string;
  glowColor: string;
  borderColor: string;
  icon: string;
  description: string;
  index?: number;
}

export default function StatCard({
  label,
  value,
  change,
  changeLabel,
  trend,
  color,
  glowColor,
  borderColor,
  icon,
  description,
  index = 0,
}: StatCardProps) {
  const Icon = ICON_MAP[icon] ?? FileText;
  const TrendIcon =
    trend === "up" ? TrendingUp : trend === "down" ? TrendingDown : Minus;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.08, ease: "easeOut" }}
      className="relative rounded-xl p-5 overflow-hidden"
      style={{
        background: "#0d1322",
        border: `1px solid ${borderColor}`,
        boxShadow: `0 0 30px ${glowColor}, 0 4px 24px rgba(0,0,0,0.3)`,
      }}
    >
      {/* Background glow blob */}
      <div
        className="absolute top-0 right-0 w-32 h-32 rounded-full blur-3xl opacity-30 pointer-events-none"
        style={{ background: color, transform: "translate(40%, -40%)" }}
      />

      {/* Top row */}
      <div className="flex items-start justify-between mb-4 relative z-10">
        <div
          className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
          style={{ background: glowColor, border: `1px solid ${borderColor}` }}
        >
          <Icon className="w-5 h-5" style={{ color }} />
        </div>

        {/* Trend badge */}
        <div
          className="flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold"
          style={{
            background:
              trend === "up"
                ? "rgba(48,209,88,0.1)"
                : trend === "down"
                ? "rgba(255,45,85,0.1)"
                : "rgba(255,255,255,0.05)",
            color:
              trend === "up"
                ? "#30d158"
                : trend === "down"
                ? "#ff2d55"
                : "#526080",
          }}
        >
          <TrendIcon className="w-3 h-3" />
          {change}
        </div>
      </div>

      {/* Value */}
      <div className="relative z-10">
        <div
          className="text-3xl font-bold tabular-nums mb-1"
          style={{ color }}
        >
          {value}
        </div>
        <div className="text-sm font-medium text-white mb-1">{label}</div>
        <div className="text-xs" style={{ color: "#2a3a55" }}>
          {description}
        </div>
        <div className="text-[11px] mt-1" style={{ color: "#2a3a55" }}>
          {changeLabel}
        </div>
      </div>
    </motion.div>
  );
}
