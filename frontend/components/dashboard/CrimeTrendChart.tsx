"use client";

import { useEffect, useState } from "react";
import { getTrends, TrendData } from "@/lib/services/dashboard";
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

const SERIES = [
  { key: "active",   name: "Active",   color: "#ff2d55" },
  { key: "resolved",  name: "Resolved",  color: "#30d158" },
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
      <p className="font-bold text-white mb-2">{label}</p>
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
    </div>
  );
}

function CustomLegend({ payload }: { payload?: { value: string; color: string }[] }) {
  if (!payload) return null;
  return (
    <div className="flex items-center gap-4 justify-center mt-2">
      {payload.map((entry) => (
        <div key={entry.value} className="flex items-center gap-1.5 text-[11px] font-medium" style={{ color: "#94a3c0" }}>
          <span className="w-2 h-2 rounded-full" style={{ background: entry.color }} />
          {entry.value}
        </div>
      ))}
    </div>
  );
}

export default function CrimeTrendChart() {
  const [trends, setTrends] = useState<TrendData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getTrends()
      .then(setTrends)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div
      className="rounded-xl p-5 h-full relative"
      style={{
        background: "#0d1322",
        border: "1px solid rgba(255,255,255,0.06)",
        minHeight: 380,
      }}
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-sm font-bold text-white">Trend Analysis</h3>
          <p className="text-xs mt-0.5" style={{ color: "#526080" }}>
            Monthly active vs resolved cases
          </p>
        </div>
        <select
          className="text-xs bg-transparent border rounded-md px-2 py-1 outline-none"
          style={{ borderColor: "rgba(255,255,255,0.1)", color: "#94a3c0" }}
        >
          <option>Last 6 Months</option>
          <option>Last 12 Months</option>
          <option>Year to Date</option>
        </select>
      </div>

      <div className="h-[260px] w-full">
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-[#0d1322]/80 z-10">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#2b91ff]" />
          </div>
        )}
        {!loading && trends.length === 0 && (
          <div className="absolute inset-0 flex items-center justify-center z-10">
            <p style={{ color: "#526080" }} className="text-sm">No trend data available.</p>
          </div>
        )}
        {trends.length > 0 && (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trends} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
              <defs>
                {SERIES.map((s) => (
                  <linearGradient key={s.key} id={`fill_${s.key}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={s.color} stopOpacity={0.3} />
                    <stop offset="95%" stopColor={s.color} stopOpacity={0} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.04)" vertical={false} />
              <XAxis
                dataKey="month"
                axisLine={false}
                tickLine={false}
                tick={{ fill: "#526080", fontSize: 10, fontWeight: 500 }}
                dy={10}
              />
              <YAxis
                axisLine={false}
                tickLine={false}
                tick={{ fill: "#526080", fontSize: 10, fontWeight: 500 }}
                tickFormatter={(val) => (val >= 1000 ? `${val / 1000}k` : val)}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ stroke: "rgba(255,255,255,0.1)", strokeWidth: 1 }} />
              <Legend content={<CustomLegend />} verticalAlign="top" height={36} />
              {SERIES.map((s) => (
                <Area
                  key={s.key}
                  type="monotone"
                  dataKey={s.key}
                  name={s.name}
                  stroke={s.color}
                  strokeWidth={2}
                  fill={`url(#fill_${s.key})`}
                  activeDot={{ r: 4, strokeWidth: 0, fill: "#fff" }}
                />
              ))}
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
