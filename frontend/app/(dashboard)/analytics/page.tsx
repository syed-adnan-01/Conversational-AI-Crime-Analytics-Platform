import type { Metadata } from "next";
import AnalyticsDashboard from "@/components/analytics/AnalyticsDashboard";

export const metadata: Metadata = {
  title: "Crime Analytics",
};

export default function AnalyticsPage() {
  return <AnalyticsDashboard />;
}
