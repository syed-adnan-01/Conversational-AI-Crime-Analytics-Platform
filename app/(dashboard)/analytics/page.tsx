import type { Metadata } from "next";
import { BarChart3 } from "lucide-react";

export const metadata: Metadata = { title: "Crime Analytics" };

export default function Page() {
  return (
    <div className="flex flex-col items-center justify-center h-[60vh] text-center">
      <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4"
        style={{ background: "rgba(0,112,243,0.1)", border: "1px solid rgba(0,112,243,0.2)" }}>
        <BarChart3 className="w-8 h-8 text-blue-400" />
      </div>
      <h2 className="text-xl font-bold text-white mb-2">Crime Analytics</h2>
      <p style={{ color: "#526080" }} className="text-sm">Coming next — deep-dive statistical analysis.</p>
    </div>
  );
}
