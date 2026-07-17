import type { Metadata } from "next";
import { Search } from "lucide-react";

export const metadata: Metadata = { title: "FIR Search" };

export default function Page() {
  return (
    <div className="flex flex-col items-center justify-center h-[60vh] text-center">
      <div className="w-16 h-16 rounded-2xl flex items-center justify-center mb-4"
        style={{ background: "rgba(0,112,243,0.1)", border: "1px solid rgba(0,112,243,0.2)" }}>
        <Search className="w-8 h-8 text-blue-400" />
      </div>
      <h2 className="text-xl font-bold text-white mb-2">FIR Search</h2>
      <p style={{ color: "#526080" }} className="text-sm">Coming next — advanced FIR search and filtering.</p>
    </div>
  );
}
