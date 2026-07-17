import type { Metadata } from "next";
import ReportsInterface from "@/components/reports/ReportsInterface";

export const metadata: Metadata = {
  title: "Reports",
};

export default function ReportsPage() {
  return <ReportsInterface />;
}
