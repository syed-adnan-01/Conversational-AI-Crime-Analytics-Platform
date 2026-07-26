"use client";

import { useEffect, useState } from "react";
import { getAIInsights, AIInsight } from "@/lib/services/dashboard";
import { formatRelativeTime } from "@/lib/utils";
import { Brain, Sparkles, ChevronRight } from "lucide-react";

export default function AIInsightPanel() {
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAIInsights()
      .then(setInsights)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const getColor = (type: string) => {
    switch (type) {
      case "pattern": return "#bf5af2";
      case "anomaly": return "#ff2d55";
      case "prediction": return "#0070f3";
      default: return "#30d158";
    }
  };

  return (
    <div
      className="rounded-xl p-5 h-full flex flex-col relative"
      style={{
        background: "#0d1322",
        border: "1px solid rgba(255,255,255,0.06)",
      }}
    >
      {/* Header */}
      <div className="flex items-center gap-3 mb-5 shrink-0">
        <div
          className="w-9 h-9 rounded-lg flex items-center justify-center"
          style={{
            background: "rgba(191,90,242,0.15)",
            border: "1px solid rgba(191,90,242,0.3)",
          }}
        >
          <Brain className="w-4.5 h-4.5" style={{ color: "#bf5af2", width: 18, height: 18 }} />
        </div>
        <div>
          <h3 className="text-sm font-bold text-white">AI Insights</h3>
          <p className="text-xs" style={{ color: "#526080" }}>
            CrimeSphere Intelligence Engine
          </p>
        </div>
        <div
          className="ml-auto flex items-center gap-1 px-2 py-1 rounded-lg text-[10px] font-semibold"
          style={{
            background: "rgba(191,90,242,0.1)",
            border: "1px solid rgba(191,90,242,0.2)",
            color: "#bf5af2",
          }}
        >
          <Sparkles style={{ width: 10, height: 10 }} />
          AI Active
        </div>
      </div>

      {/* Insights */}
      <div className="flex-1 space-y-3 overflow-y-auto relative min-h-[150px]">
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-[#0d1322]/80 z-10">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#bf5af2]" />
          </div>
        )}
        {!loading && insights.length === 0 && (
          <div className="absolute inset-0 flex items-center justify-center z-10">
            <p style={{ color: "#526080" }} className="text-sm">No new AI insights available.</p>
          </div>
        )}
        {insights.map((insight, i) => {
          const color = getColor(insight.type);
          return (
            <div
              key={insight.id}
              className="rounded-lg p-3.5 cursor-pointer group transition-all"
              style={{
                background: "rgba(255,255,255,0.025)",
                border: "1px solid rgba(255,255,255,0.06)",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLDivElement).style.borderColor = color + "50";
                (e.currentTarget as HTMLDivElement).style.background = `${color}08`;
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLDivElement).style.borderColor = "rgba(255,255,255,0.06)";
                (e.currentTarget as HTMLDivElement).style.background = "rgba(255,255,255,0.025)";
              }}
            >
              {/* Top row */}
              <div className="flex items-start justify-between gap-2 mb-2">
                <div className="flex items-center gap-2 flex-1 min-w-0">
                  <span
                    className="w-2 h-2 rounded-full shrink-0"
                    style={{ background: color }}
                  />
                  <p className="text-xs font-bold text-white truncate">
                    {insight.title}
                  </p>
                </div>
                <ChevronRight
                  className="w-3.5 h-3.5 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity"
                  style={{ color: color }}
                />
              </div>

              <p className="text-xs leading-relaxed mb-3" style={{ color: "#526080" }}>
                {insight.description}
              </p>

              {/* Footer: confidence + time */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-[10px]" style={{ color: "#2a3a55" }}>Confidence</span>
                  <div className="flex items-center gap-1.5">
                    <div
                      className="h-1 rounded-full overflow-hidden"
                      style={{ background: "rgba(255,255,255,0.07)", width: 56 }}
                    >
                      <div
                        className="h-full rounded-full transition-all"
                        style={{
                          width: `${insight.confidence}%`,
                          background: color,
                        }}
                      />
                    </div>
                    <span
                      className="text-[10px] font-bold tabular-nums"
                      style={{ color: color }}
                    >
                      {insight.confidence}%
                    </span>
                  </div>
                </div>
              </div>

              <div
                className="mt-2 pt-2"
                style={{ borderTop: "1px solid rgba(255,255,255,0.05)" }}
              >
                <button
                  className="text-[10px] font-semibold transition-colors"
                  style={{ color: color }}
                >
                  Take Action →
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer */}
      <div
        className="mt-4 pt-3 text-center shrink-0"
        style={{ borderTop: "1px solid rgba(255,255,255,0.05)" }}
      >
        <p className="text-[10px]" style={{ color: "#2a3a55" }}>
          Model: CrimeSphere GPT-L · v2.4 · Accuracy 94.7%
        </p>
      </div>
    </div>
  );
}
