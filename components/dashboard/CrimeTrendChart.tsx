"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { crimeMonthlyData } from "@/lib/mock-data/dashboard";

const SERIES = [
  { key: "violent",   name: "Violent",   color: "#ff2d55" },
  { key: "property",  name: "Property",  color: "#0070f3" },
  { key: "cyber",     name: "Cyber",     color: "#bf5af2" },
  { key: "narcotics", name: "Narcotics", color: "#ff8c00" },
];

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;

  return (
    <div
      className="rounded-xl px-4 py-3 text-xs"
      style={{
        background: "rgba(13,19,34,0.98)",
        border: "1px solid rgba(255,255,255,0.1)",
        boxShadow: "0 16px 32px rgba(0,0,0,0.6)",
        minWidth: 160,
      }}
    >
      <p className="font-bold text-white mb-2">{label} 2024</p>
      {payload.map((entry: { color: string; name: string; value: number }) => (
        <div key={entry.name} className="flex items-center justify-between gap-4 mb-1">
          <div className="flex items-center gap-1.5">
            <span
              className="w-2 h-2 rounded-full inline-block"
              style={{ background: entry.color }}
            />
            <span style={{ color: "#94a3c0" }}>{entry.name}</span>
          </div>
          <span className="font-semibold tabular-nums" style={{ color: entry.color }}>
            {entry.value.toLocaleString("en-IN")}
          </span>
        </div>
      ))}
      <div
        className="flex items-center justify-between mt-2 pt-2"
        style={{ borderTop: "1px solid rgba(255,255,255,0.07)" }}
      >
        <span style={{ color: "#526080" }}>Total</span>
        <span className="font-bold text-white">
          {payload.reduce((s: number, e: { value: number }) => s + e.value, 0).toLocaleString("en-IN")}
        </span>
      </div>
    </div>
  );
}

export default function CrimeTrendChart() {
  return (
    <div
      className="rounded-xl p-5 h-full"
      style={{
        background: "#0d1322",
        border: "1px solid rgba(255,255,255,0.06)",
      }}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-sm font-bold text-white">Crime Trend Analysis</h3>
          <p className="text-xs mt-0.5" style={{ color: "#526080" }}>
            Feb – Jul 2024 · All districts
          </p>
        </div>
        <div className="flex gap-2">
          {(["1M", "3M", "6M", "1Y"] as const).map((r, i) => (
            <button
              key={r}
              className="text-xs px-2.5 py-1 rounded-lg transition-colors"
              style={{
                background: i === 2 ? "rgba(0,112,243,0.15)" : "rgba(255,255,255,0.04)",
                border: i === 2 ? "1px solid rgba(0,112,243,0.3)" : "1px solid rgba(255,255,255,0.07)",
                color: i === 2 ? "#2b91ff" : "#526080",
              }}
            >
              {r}
            </button>
          ))}
        </div>
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={240}>
        <AreaChart data={crimeMonthlyData} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
          <defs>
            {SERIES.map((s) => (
              <linearGradient key={s.key} id={`grad-${s.key}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor={s.color} stopOpacity={0.25} />
                <stop offset="95%" stopColor={s.color} stopOpacity={0.01} />
              </linearGradient>
            ))}
          </defs>

          <CartesianGrid
            strokeDasharray="3 3"
            stroke="rgba(255,255,255,0.04)"
            vertical={false}
          />
          <XAxis
            dataKey="month"
            tick={{ fill: "#526080", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: "#526080", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ paddingTop: 16 }}
            formatter={(value) => (
              <span style={{ color: "#94a3c0", fontSize: 11 }}>{value}</span>
            )}
          />

          {SERIES.map((s) => (
            <Area
              key={s.key}
              type="monotone"
              dataKey={s.key}
              name={s.name}
              stroke={s.color}
              strokeWidth={2}
              fill={`url(#grad-${s.key})`}
              dot={false}
              activeDot={{ r: 5, strokeWidth: 2, stroke: s.color, fill: "#0d1322" }}
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
