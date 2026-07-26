"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import {
  TrendingUp,
  TrendingDown,
  Activity,
  Filter,
} from "lucide-react";

import { analytics, MonthlyTrend } from "@/lib/services/analytics";

// ─── Helpers ──────────────────────────────────────────────────────────────────

function heatColor(v: number): string {
  if (v === 0) return "rgba(0,112,243,0.04)";
  if (v <= 2)  return "rgba(0,112,243,0.35)";
  if (v <= 4)  return "rgba(255,140,0,0.45)";
  if (v <= 6)  return "rgba(255,45,85,0.55)";
  if (v <= 8)  return "rgba(255,45,85,0.75)";
  return "rgba(255,45,85,0.95)";
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div
      className="rounded-xl px-4 py-3 text-xs"
      style={{
        background: "rgba(13,19,34,0.98)",
        border: "1px solid rgba(255,255,255,0.1)",
        boxShadow: "0 16px 32px rgba(0,0,0,0.6)",
      }}
    >
      <p className="font-bold text-white mb-2">{label}</p>
      {payload.map((e: { color: string; name: string; value: number }) => (
        <div key={e.name} className="flex items-center justify-between gap-6 mb-1">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full" style={{ background: e.color }} />
            <span style={{ color: "#94a3c0" }}>{e.name}</span>
          </div>
          <span className="font-semibold tabular-nums" style={{ color: e.color }}>
            {e.value.toLocaleString("en-IN")}
          </span>
        </div>
      ))}
    </div>
  );
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function PieTooltip({ active, payload }: any) {
  if (!active || !payload?.length) return null;
  const p = payload[0];
  return (
    <div
      className="rounded-xl px-3 py-2 text-xs"
      style={{
        background: "rgba(13,19,34,0.98)",
        border: "1px solid rgba(255,255,255,0.1)",
      }}
    >
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full" style={{ background: p.payload.color }} />
        <span className="font-bold text-white">{p.name}</span>
        <span className="font-mono" style={{ color: p.payload.color }}>
          {p.value.toLocaleString("en-IN")}
        </span>
      </div>
    </div>
  );
}

// ─── Card wrapper ─────────────────────────────────────────────────────────────
function Card({ title, subtitle, children, className = "" }: {
  title: string; subtitle?: string; children: React.ReactNode; className?: string;
}) {
  return (
    <div
      className={`rounded-xl p-5 flex flex-col ${className}`}
      style={{ background: "#0d1322", border: "1px solid rgba(255,255,255,0.06)" }}
    >
      <div className="mb-4 shrink-0">
        <h3 className="text-sm font-bold text-white">{title}</h3>
        {subtitle && <p className="text-xs mt-0.5" style={{ color: "#526080" }}>{subtitle}</p>}
      </div>
      {children}
    </div>
  );
}

// ─── Main Dashboard ───────────────────────────────────────────────────────────
export default function AnalyticsDashboard() {
  const [activeFilter, setActiveFilter] = useState("ALL");
  const [loading, setLoading] = useState(true);
  
  const [monthlyTrends, setMonthlyTrends] = useState<MonthlyTrend[]>([]);
  const [crimeTypes, setCrimeTypes] = useState<Record<string, number>>({});
  const [districts, setDistricts] = useState<Record<string, number>>({});
  const [officers, setOfficers] = useState<Record<string, number>>({});

  useEffect(() => {
    async function fetchData() {
      try {
        const [monthly, types, dist, off] = await Promise.all([
          analytics.getMonthlyTrends(),
          analytics.getCrimeTypes(),
          analytics.getDistricts(),
          analytics.getOfficers()
        ]);
        setMonthlyTrends(monthly);
        setCrimeTypes(types);
        setDistricts(dist);
        setOfficers(off);
      } catch (err) {
        console.error("Failed to load analytics", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [activeFilter]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64 text-white">
        <p>Loading Analytics...</p>
      </div>
    );
  }

  // Format Crime Type Breakdown
  const crimeTypeColors = ["#ff2d55", "#0070f3", "#bf5af2", "#ff8c00", "#30d158"];
  const formattedCrimeTypes = Object.entries(crimeTypes).map(([id, count], i) => ({
    name: `Crime Type ${id}`,
    value: count,
    color: crimeTypeColors[i % crimeTypeColors.length],
  })).sort((a, b) => b.value - a.value);

  const totalCrimes = formattedCrimeTypes.reduce((s, c) => s + c.value, 0);

  // Format Districts
  const maxDistrictCount = Math.max(...Object.values(districts), 1);
  const formattedDistricts = Object.entries(districts).map(([id, count], i) => ({
    name: `Police Station ${id}`,
    crimes: count,
    rate: Math.floor(((id.charCodeAt(0) * 17 + i * 13) % 30) + 50),
    resolved: Math.floor(count * 0.7),
    color: ["#0070f3", "#bf5af2", "#ff8c00", "#ff2d55", "#30d158"][i % 5]
  })).sort((a, b) => b.crimes - a.crimes).slice(0, 10);

  // Format Monthly Trend for Bar Chart
  const formattedMonthlyTrends = monthlyTrends.map(item => ({
    month: item.period,
    total: item.cases
  }));

  // Mock KPIs based on overall totals
  const totalOfficers = Object.keys(officers).length;
  const YOY_STATS = [
    { label: "Total Cases", current: totalCrimes, previous: Math.floor(totalCrimes * 0.9), unit: "", lowerIsBetter: true },
    { label: "Active Districts", current: Object.keys(districts).length, previous: Object.keys(districts).length, unit: "", lowerIsBetter: false },
    { label: "Active Officers", current: totalOfficers, previous: Math.floor(totalOfficers * 0.95), unit: "", lowerIsBetter: false },
  ];

  return (
    <div className="space-y-5 max-w-[1600px] mx-auto">

      {/* ── Filter bar ── */}
      <div
        className="flex items-center justify-between rounded-xl px-5 py-3"
        style={{ background: "#0d1322", border: "1px solid rgba(255,255,255,0.06)" }}
      >
        <div className="flex items-center gap-2">
          <Filter className="w-3.5 h-3.5" style={{ color: "#526080" }} />
          <span className="text-xs font-semibold" style={{ color: "#526080" }}>
            Showing:
          </span>
          <span className="text-xs text-white font-bold">All Districts · All Crime Types</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5" style={{ color: "#526080" }} />
          {["1M", "3M", "6M", "1Y", "ALL"].map((r) => (
            <button
              key={r}
              onClick={() => setActiveFilter(r)}
              className="text-xs px-3 py-1.5 rounded-lg transition-colors"
              style={{
                background: activeFilter === r ? "rgba(0,112,243,0.15)" : "rgba(255,255,255,0.04)",
                border: activeFilter === r ? "1px solid rgba(0,112,243,0.3)" : "1px solid rgba(255,255,255,0.07)",
                color: activeFilter === r ? "#2b91ff" : "#526080",
              }}
            >
              {r}
            </button>
          ))}
        </div>
      </div>

      {/* ── KPI Row ── */}
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        {YOY_STATS.map((stat, index) => {
          const delta = stat.current - stat.previous;
          const pct   = stat.previous > 0 ? Math.abs(((delta) / stat.previous) * 100).toFixed(1) : "0.0";
          const up    = delta >= 0;
          const good  = stat.lowerIsBetter ? !up : up;

          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.07 }}
              className="rounded-xl p-5"
              style={{ background: "#0d1322", border: "1px solid rgba(255,255,255,0.06)" }}
            >
              <p className="text-xs mb-1" style={{ color: "#526080" }}>{stat.label}</p>
              <div className="flex items-end justify-between">
                <p className="text-2xl font-bold text-white tabular-nums">
                  {stat.current.toLocaleString("en-IN")}{stat.unit}
                </p>
                <div
                  className="flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-full"
                  style={{
                    background: good ? "rgba(48,209,88,0.1)" : "rgba(255,45,85,0.1)",
                    color: good ? "#30d158" : "#ff2d55",
                  }}
                >
                  {up ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                  {pct}%
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* ── Row 2: Monthly Bar Chart + Donut ── */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        {/* Monthly bar chart (2/3) */}
        <Card
          title="Monthly Crime Volume"
          subtitle="Total cases registered per month"
          className="xl:col-span-2"
        >
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={formattedMonthlyTrends} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
              <XAxis dataKey="month" tick={{ fill: "#526080", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#526080", fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip content={<ChartTooltip />} cursor={{ fill: "rgba(255,255,255,0.03)" }} />
              <Legend formatter={(v) => <span style={{ color: "#94a3c0", fontSize: 11 }}>{v}</span>} />
              <Bar dataKey="total" name="Total Cases" fill="#0070f3" radius={[3,3,0,0]} maxBarSize={32} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Donut: Crime Type distribution (1/3) */}
        <Card title="Crime Types Distribution" subtitle="All registered cases">
          <div className="flex flex-col items-center justify-center flex-1">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={formattedCrimeTypes}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={3}
                  dataKey="value"
                >
                  {formattedCrimeTypes.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip content={<PieTooltip />} />
              </PieChart>
            </ResponsiveContainer>

            {/* Legend */}
            <div className="w-full space-y-1.5 mt-2">
              {formattedCrimeTypes.map((s) => (
                <div key={s.name} className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full" style={{ background: s.color }} />
                    <span style={{ color: "#94a3c0" }}>{s.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold tabular-nums text-white">
                      {s.value.toLocaleString("en-IN")}
                    </span>
                    <span className="text-[10px] w-10 text-right" style={{ color: "#2a3a55" }}>
                      {((s.value / totalCrimes)*100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Card>
      </div>

      {/* ── Row 4: Top Districts ── */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        
        {/* Top districts chart */}
        <Card title="Top Districts by Crime Volume" subtitle="Number of cases per Police Station">
          <div className="space-y-3">
            {formattedDistricts.map((d, i) => (
              <motion.div
                key={d.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.06 }}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-white truncate max-w-[140px]">{d.name}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold tabular-nums" style={{ color: "#526080" }}>
                      {d.crimes}
                    </span>
                  </div>
                </div>
                {/* Bar */}
                <div className="relative h-2 rounded-full overflow-hidden"
                  style={{ background: "rgba(255,255,255,0.06)" }}>
                  <motion.div
                    className="absolute left-0 top-0 h-full rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${(d.crimes / maxDistrictCount) * 100}%` }}
                    transition={{ duration: 0.8, delay: i * 0.06, ease: "easeOut" }}
                    style={{ background: d.color }}
                  />
                </div>
              </motion.div>
            ))}
          </div>
        </Card>

      </div>
    </div>
  );
}
