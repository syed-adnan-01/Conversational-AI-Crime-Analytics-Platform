import type { Metadata } from "next";
import { kpiStats } from "@/lib/mock-data/dashboard";
import StatCard from "@/components/dashboard/StatCard";
import CrimeTrendChart from "@/components/dashboard/CrimeTrendChart";
import AlertsFeed from "@/components/dashboard/AlertsFeed";
import RecentFIRsTable from "@/components/dashboard/RecentFIRsTable";
import AIInsightPanel from "@/components/dashboard/AIInsightPanel";

export const metadata: Metadata = {
  title: "Command Dashboard",
};

export default function DashboardPage() {
  return (
    <div className="space-y-6 max-w-[1600px] mx-auto">

      {/* ── KPI Cards ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {kpiStats.map((stat, i) => (
          <StatCard key={stat.id} {...stat} index={i} />
        ))}
      </div>

      {/* ── Crime Trend + Alerts ── */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        {/* Chart takes 2/3 */}
        <div className="xl:col-span-2">
          <CrimeTrendChart />
        </div>
        {/* Alerts take 1/3 */}
        <div className="xl:col-span-1" style={{ minHeight: 380 }}>
          <AlertsFeed />
        </div>
      </div>

      {/* ── Recent FIRs + AI Insights ── */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        {/* FIRs table takes 2/3 */}
        <div className="xl:col-span-2">
          <RecentFIRsTable />
        </div>
        {/* AI insights take 1/3 */}
        <div className="xl:col-span-1">
          <AIInsightPanel />
        </div>
      </div>
    </div>
  );
}
