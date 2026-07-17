"use client";

import { useState } from "react";
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
import {
  MONTHLY_TREND,
  CRIME_TYPE_BREAKDOWN,
  STATUS_DISTRIBUTION,
  TOP_DISTRICTS,
  YOY_STATS,
  HEATMAP_DATA,
  DAYS_OF_WEEK,
  HOURS,
} from "@/lib/mock-data/analytics";

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

// ─── KPI card ─────────────────────────────────────────────────────────────────
function KPICard({ stat, index }: { stat: typeof YOY_STATS[0]; index: number }) {
  const delta = stat.current - stat.previous;
  const pct   = Math.abs(((delta) / stat.previous) * 100).toFixed(1);
  const up    = delta > 0;
  const good  = stat.lowerIsBetter ? !up : up;

  return (
    <motion.div
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
      <p className="text-[10px] mt-1" style={{ color: "#2a3a55" }}>
        vs {stat.previous.toLocaleString("en-IN")}{stat.unit} last year
      </p>
    </motion.div>
  );
}

// ─── Heatmap ──────────────────────────────────────────────────────────────────
function CrimeHeatmap() {
  const [hovered, setHovered] = useState<{ d: number; h: number } | null>(null);

  return (
    <Card title="Crime Intensity Heatmap" subtitle="Day of week × Hour of day · Jan–Jun 2024">
      <div className="overflow-x-auto">
        {/* Hour labels */}
        <div className="flex mb-1 pl-10">
          {HOURS.map((h, i) => (
            <div
              key={i}
              className="flex-1 text-center text-[9px] shrink-0"
              style={{
                color: i % 3 === 0 ? "#526080" : "transparent",
                minWidth: 24,
              }}
            >
              {h}
            </div>
          ))}
        </div>

        {/* Grid */}
        {HEATMAP_DATA.map((dayData, d) => (
          <div key={d} className="flex items-center mb-1">
            <span
              className="text-[10px] w-10 shrink-0 text-right pr-2"
              style={{ color: "#526080" }}
            >
              {DAYS_OF_WEEK[d]}
            </span>
            {dayData.map((val, h) => {
              const isHov = hovered?.d === d && hovered?.h === h;
              return (
                <div
                  key={h}
                  className="flex-1 rounded-sm transition-all cursor-default"
                  style={{
                    background: heatColor(val),
                    minWidth: 22,
                    height: 22,
                    margin: "0 1px",
                    outline: isHov ? "1.5px solid rgba(255,255,255,0.5)" : "none",
                    transform: isHov ? "scale(1.3)" : "scale(1)",
                    transition: "transform 0.1s, outline 0.1s",
                    zIndex: isHov ? 10 : 0,
                    position: "relative",
                  }}
                  onMouseEnter={() => setHovered({ d, h })}
                  onMouseLeave={() => setHovered(null)}
                  title={`${DAYS_OF_WEEK[d]} ${HOURS[h]}: ${val} incidents`}
                />
              );
            })}
          </div>
        ))}

        {/* Colour scale legend */}
        <div className="flex items-center gap-2 mt-3 justify-end">
          <span className="text-[10px]" style={{ color: "#2a3a55" }}>Low</span>
          {[0, 2, 4, 6, 8, 10].map((v) => (
            <div
              key={v}
              className="w-5 h-4 rounded-sm"
              style={{ background: heatColor(v) }}
            />
          ))}
          <span className="text-[10px]" style={{ color: "#2a3a55" }}>High</span>
        </div>
      </div>
    </Card>
  );
}

// ─── Top Districts ────────────────────────────────────────────────────────────
function TopDistrictsChart() {
  const max = Math.max(...TOP_DISTRICTS.map((d) => d.crimes));

  return (
    <Card title="Top Districts by Crime Volume" subtitle="Resolution rate shown as overlay">
      <div className="space-y-3">
        {TOP_DISTRICTS.map((d, i) => (
          <motion.div
            key={d.name}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.06 }}
          >
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs text-white truncate max-w-[140px]">{d.name}</span>
              <div className="flex items-center gap-2">
                <span
                  className="text-[10px] font-semibold px-1.5 py-0.5 rounded"
                  style={{
                    background: d.rate >= 75 ? "rgba(48,209,88,0.12)" : "rgba(255,140,0,0.12)",
                    color: d.rate >= 75 ? "#30d158" : "#ff8c00",
                  }}
                >
                  {d.rate}% resolved
                </span>
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
                animate={{ width: `${(d.crimes / max) * 100}%` }}
                transition={{ duration: 0.8, delay: i * 0.06, ease: "easeOut" }}
                style={{ background: d.color }}
              />
              {/* Resolution overlay */}
              <motion.div
                className="absolute left-0 top-0 h-full rounded-full opacity-30"
                initial={{ width: 0 }}
                animate={{ width: `${(d.resolved / max) * 100}%` }}
                transition={{ duration: 0.8, delay: i * 0.06 + 0.2, ease: "easeOut" }}
                style={{ background: "#30d158" }}
              />
            </div>
          </motion.div>
        ))}
      </div>
    </Card>
  );
}

// ─── Main Dashboard ───────────────────────────────────────────────────────────
export default function AnalyticsDashboard() {
  const [activeFilter, setActiveFilter] = useState("6M");
  const total = CRIME_TYPE_BREAKDOWN.reduce((s, c) => s + c.value, 0);

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
        {YOY_STATS.map((s, i) => <KPICard key={s.label} stat={s} index={i} />)}
      </div>

      {/* ── Row 2: Monthly Bar Chart + Donut ── */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        {/* Monthly bar chart (2/3) */}
        <Card
          title="Monthly Crime Volume by Category"
          subtitle="Jan – Jun 2024 · All Districts"
          className="xl:col-span-2"
        >
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={MONTHLY_TREND} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
              <XAxis dataKey="month" tick={{ fill: "#526080", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#526080", fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip content={<ChartTooltip />} cursor={{ fill: "rgba(255,255,255,0.03)" }} />
              <Legend formatter={(v) => <span style={{ color: "#94a3c0", fontSize: 11 }}>{v}</span>} />
              <Bar dataKey="violent"   name="Violent"   fill="#ff2d55" radius={[3,3,0,0]} maxBarSize={18} />
              <Bar dataKey="property"  name="Property"  fill="#0070f3" radius={[3,3,0,0]} maxBarSize={18} />
              <Bar dataKey="cyber"     name="Cyber"     fill="#bf5af2" radius={[3,3,0,0]} maxBarSize={18} />
              <Bar dataKey="narcotics" name="Narcotics" fill="#ff8c00" radius={[3,3,0,0]} maxBarSize={18} />
              <Bar dataKey="financial" name="Financial" fill="#30d158" radius={[3,3,0,0]} maxBarSize={18} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Donut: Status distribution (1/3) */}
        <Card title="Case Status Distribution" subtitle="Current snapshot · All districts">
          <div className="flex flex-col items-center justify-center flex-1">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={STATUS_DISTRIBUTION}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={3}
                  dataKey="value"
                >
                  {STATUS_DISTRIBUTION.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip content={<PieTooltip />} />
              </PieChart>
            </ResponsiveContainer>

            {/* Legend */}
            <div className="w-full space-y-1.5 mt-2">
              {STATUS_DISTRIBUTION.map((s) => (
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
                      {((s.value / STATUS_DISTRIBUTION.reduce((a,x)=>a+x.value,0))*100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Card>
      </div>

      {/* ── Row 3: Heatmap ── */}
      <CrimeHeatmap />

      {/* ── Row 4: Top Districts + Crime Type Breakdown ── */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        <TopDistrictsChart />

        {/* Crime type breakdown */}
        <Card title="Crime Type Breakdown" subtitle="Volume and YoY change · Jan–Jun 2024">
          <div className="space-y-3 flex-1">
            {CRIME_TYPE_BREAKDOWN.map((c, i) => {
              const delta = c.value - c.prev;
              const up = delta > 0;
              const pct = Math.abs(((delta) / c.prev) * 100).toFixed(1);

              return (
                <motion.div
                  key={c.name}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.06 }}
                  className="flex items-center gap-3"
                >
                  <span className="text-xs w-20 shrink-0 text-white font-medium">{c.name}</span>

                  {/* Bar */}
                  <div
                    className="flex-1 h-2 rounded-full overflow-hidden"
                    style={{ background: "rgba(255,255,255,0.06)" }}
                  >
                    <motion.div
                      className="h-full rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: `${(c.value / total) * 100 * 3}%` }}
                      transition={{ duration: 0.8, delay: i * 0.06 }}
                      style={{ background: c.color, maxWidth: "100%" }}
                    />
                  </div>

                  <span className="text-xs font-bold tabular-nums text-white w-14 text-right shrink-0">
                    {c.value.toLocaleString("en-IN")}
                  </span>

                  <div
                    className="flex items-center gap-1 text-[10px] font-semibold w-16 shrink-0"
                    style={{ color: up ? "#ff2d55" : "#30d158" }}
                  >
                    {up ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
                    {pct}%
                  </div>
                </motion.div>
              );
            })}

            {/* Total */}
            <div
              className="flex items-center justify-between pt-3 mt-1"
              style={{ borderTop: "1px solid rgba(255,255,255,0.07)" }}
            >
              <span className="text-xs font-bold text-white">Total Crimes</span>
              <span className="text-lg font-bold tabular-nums" style={{ color: "#2b91ff" }}>
                {total.toLocaleString("en-IN")}
              </span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
