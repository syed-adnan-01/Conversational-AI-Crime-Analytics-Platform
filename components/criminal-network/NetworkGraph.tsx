"use client";

import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Shield,
  MapPin,
  AlertTriangle,
  FileText,
  Brain,
  Search,
  Users,
  TrendingUp,
  ChevronRight,
} from "lucide-react";
import {
  NETWORK_NODES,
  NETWORK_EDGES,
  TIER_CONFIG,
  STATUS_CONFIG,
  EDGE_CONFIG,
  type NetworkNode,
} from "@/lib/mock-data/network";

// ─── SVG dimensions ───────────────────────────────────────────────────────────
const W = 900;
const H = 560;

// ─── Initials helper ──────────────────────────────────────────────────────────
function initials(name: string) {
  return name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2);
}

// ─── Node Detail Panel ────────────────────────────────────────────────────────
function NodeDetail({ node, onClose }: { node: NetworkNode; onClose: () => void }) {
  const tier   = TIER_CONFIG[node.tier];
  const status = STATUS_CONFIG[node.status];
  const edges  = NETWORK_EDGES.filter(
    (e) => e.source === node.id || e.target === node.id
  );
  const connectedNodes = edges.map((e) => {
    const otherId = e.source === node.id ? e.target : e.source;
    return NETWORK_NODES.find((n) => n.id === otherId)!;
  });

  return (
    <motion.div
      initial={{ x: "100%", opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: "100%", opacity: 0 }}
      transition={{ type: "spring", damping: 28, stiffness: 280 }}
      className="flex flex-col h-full shrink-0 overflow-hidden"
      style={{
        width: 360,
        background: "#0a0f1e",
        borderLeft: "1px solid rgba(255,255,255,0.07)",
      }}
    >
      {/* Header */}
      <div
        className="p-5 shrink-0"
        style={{ borderBottom: "1px solid rgba(255,255,255,0.06)" }}
      >
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center text-sm font-bold text-white shrink-0"
              style={{
                background: `${tier.color}20`,
                border: `2px solid ${tier.color}60`,
                color: tier.color,
              }}
            >
              {initials(node.name)}
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">{node.name}</h3>
              <p className="text-xs" style={{ color: "#526080" }}>
                {node.alias}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-7 h-7 rounded-lg flex items-center justify-center"
            style={{
              background: "rgba(255,255,255,0.05)",
              border: "1px solid rgba(255,255,255,0.08)",
            }}
          >
            <X className="w-3.5 h-3.5" style={{ color: "#526080" }} />
          </button>
        </div>

        {/* Badges row */}
        <div className="flex flex-wrap gap-2">
          <span
            className="text-[10px] font-bold px-2.5 py-1 rounded-full"
            style={{ background: `${tier.color}18`, color: tier.color }}
          >
            Tier {node.tier} — {tier.label}
          </span>
          <span
            className="text-[10px] font-bold px-2.5 py-1 rounded-full flex items-center gap-1"
            style={{
              background: `${status.color}15`,
              color: status.color,
            }}
          >
            <span
              className="w-1.5 h-1.5 rounded-full"
              style={{ background: status.color }}
            />
            {status.label}
          </span>
        </div>
      </div>

      {/* Body */}
      <div className="flex-1 overflow-y-auto p-5 space-y-5">
        {/* Threat Score */}
        <div
          className="rounded-xl p-4"
          style={{
            background: "rgba(191,90,242,0.06)",
            border: "1px solid rgba(191,90,242,0.18)",
          }}
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <Brain className="w-3.5 h-3.5" style={{ color: "#bf5af2" }} />
              <span className="text-xs font-bold" style={{ color: "#bf5af2" }}>
                AI Threat Score
              </span>
            </div>
            <span
              className="text-xl font-bold tabular-nums"
              style={{
                color:
                  node.threatScore >= 80 ? "#ff2d55" :
                  node.threatScore >= 60 ? "#ff8c00" : "#ffd60a",
              }}
            >
              {node.threatScore}
              <span className="text-xs font-normal text-gray-500">/100</span>
            </span>
          </div>
          <div
            className="w-full h-2 rounded-full overflow-hidden"
            style={{ background: "rgba(255,255,255,0.07)" }}
          >
            <motion.div
              className="h-full rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${node.threatScore}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              style={{
                background:
                  node.threatScore >= 80
                    ? "linear-gradient(90deg, #ff8c00, #ff2d55)"
                    : node.threatScore >= 60
                    ? "linear-gradient(90deg, #ffd60a, #ff8c00)"
                    : "#ffd60a",
              }}
            />
          </div>
        </div>

        {/* Bio */}
        <div>
          <p className="text-[10px] uppercase tracking-widest font-semibold mb-2" style={{ color: "#2a3a55" }}>
            Intelligence Brief
          </p>
          <p className="text-xs leading-relaxed" style={{ color: "#94a3c0" }}>
            {node.bio}
          </p>
        </div>

        {/* Details */}
        <div>
          <p className="text-[10px] uppercase tracking-widest font-semibold mb-2" style={{ color: "#2a3a55" }}>
            Profile Details
          </p>
          <div className="space-y-2">
            {[
              { icon: Shield,    label: "Role",      value: node.role },
              { icon: MapPin,    label: "Last Seen",  value: node.lastLocation },
              { icon: TrendingUp,label: "Crime Types", value: node.crimeTypes.join(", ") },
            ].map(({ icon: Icon, label, value }) => (
              <div key={label} className="flex items-start gap-2">
                <Icon className="w-3 h-3 shrink-0 mt-0.5" style={{ color: "#2a3a55" }} />
                <span className="text-[11px] shrink-0 w-20" style={{ color: "#526080" }}>
                  {label}
                </span>
                <span className="text-[11px] text-white">{value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Linked FIRs */}
        {node.linkedFIRs.length > 0 && (
          <div>
            <p className="text-[10px] uppercase tracking-widest font-semibold mb-2" style={{ color: "#2a3a55" }}>
              Linked FIRs
            </p>
            <div className="space-y-1">
              {node.linkedFIRs.map((fir) => (
                <div
                  key={fir}
                  className="flex items-center gap-2 text-xs px-2.5 py-1.5 rounded-lg"
                  style={{
                    background: "rgba(0,112,243,0.08)",
                    border: "1px solid rgba(0,112,243,0.15)",
                  }}
                >
                  <FileText className="w-3 h-3" style={{ color: "#2b91ff" }} />
                  <span className="font-mono" style={{ color: "#2b91ff" }}>{fir}</span>
                  <ChevronRight className="w-3 h-3 ml-auto" style={{ color: "#2a3a55" }} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Connections */}
        <div>
          <p className="text-[10px] uppercase tracking-widest font-semibold mb-2" style={{ color: "#2a3a55" }}>
            Known Connections ({connectedNodes.length})
          </p>
          <div className="space-y-2">
            {connectedNodes.map((cn, i) => {
              const cTier   = TIER_CONFIG[cn.tier];
              const cStatus = STATUS_CONFIG[cn.status];
              const edge    = edges[i];
              return (
                <div
                  key={cn.id}
                  className="flex items-center gap-2.5 rounded-lg px-3 py-2"
                  style={{
                    background: "rgba(255,255,255,0.025)",
                    border: "1px solid rgba(255,255,255,0.06)",
                  }}
                >
                  <div
                    className="w-7 h-7 rounded-lg flex items-center justify-center text-[10px] font-bold shrink-0"
                    style={{
                      background: `${cTier.color}15`,
                      color: cTier.color,
                    }}
                  >
                    {initials(cn.name)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-white truncate">{cn.name}</p>
                    <p className="text-[10px] truncate" style={{ color: "#526080" }}>
                      {edge.type} · {edge.strength}
                    </p>
                  </div>
                  <span
                    className="w-1.5 h-1.5 rounded-full shrink-0"
                    style={{ background: cStatus.color }}
                  />
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────
export default function NetworkGraph() {
  const [selected, setSelected]   = useState<string | null>(null);
  const [hovered,  setHovered]    = useState<string | null>(null);
  const [search,   setSearch]     = useState("");
  const [filterTier, setFilterTier] = useState<string>("all");

  const activeId = selected ?? hovered;

  // IDs connected to the active node
  const connectedIds = useMemo(() => {
    if (!activeId) return new Set<string>();
    const s = new Set<string>();
    NETWORK_EDGES.forEach((e) => {
      if (e.source === activeId) s.add(e.target);
      if (e.target === activeId) s.add(e.source);
    });
    return s;
  }, [activeId]);

  // Filter nodes for left panel
  const filteredNodes = useMemo(() => {
    return NETWORK_NODES.filter((n) => {
      const q = search.toLowerCase();
      const matchQ = !q || n.name.toLowerCase().includes(q) || n.role.toLowerCase().includes(q);
      const matchTier = filterTier === "all" || String(n.tier) === filterTier;
      return matchQ && matchTier;
    }).sort((a, b) => b.threatScore - a.threatScore);
  }, [search, filterTier]);

  const selectedNode = NETWORK_NODES.find((n) => n.id === selected) ?? null;

  // Edge colour based on type
  const edgeColor: Record<string, string> = {
    operational:   "#0070f3",
    financial:     "#30d158",
    communication: "#bf5af2",
    family:        "#ff8c00",
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] -m-6 overflow-hidden">

      {/* ═══ LEFT: Criminal List ═══ */}
      <div
        className="hidden lg:flex w-[260px] shrink-0 flex-col"
        style={{
          background: "#0a0f1e",
          borderRight: "1px solid rgba(255,255,255,0.06)",
        }}
      >
        {/* Header */}
        <div
          className="px-4 py-4 shrink-0"
          style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}
        >
          <p className="text-sm font-bold text-white mb-3">Criminal Registry</p>

          {/* Search */}
          <div className="relative mb-2">
            <Search
              className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none"
              style={{ color: "#526080" }}
            />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search criminals…"
              className="w-full h-9 pl-9 pr-3 rounded-lg text-xs text-white outline-none"
              style={{
                background: "rgba(255,255,255,0.05)",
                border: "1px solid rgba(255,255,255,0.08)",
              }}
            />
          </div>

          {/* Tier filter */}
          <div className="flex gap-1">
            {["all", "1", "2", "3"].map((t) => (
              <button
                key={t}
                onClick={() => setFilterTier(t)}
                className="flex-1 text-[10px] py-1 rounded-md font-semibold transition-colors"
                style={{
                  background: filterTier === t ? "rgba(0,112,243,0.18)" : "rgba(255,255,255,0.04)",
                  border: filterTier === t ? "1px solid rgba(0,112,243,0.3)" : "1px solid rgba(255,255,255,0.07)",
                  color: filterTier === t ? "#2b91ff" : "#526080",
                }}
              >
                {t === "all" ? "All" : `T${t}`}
              </button>
            ))}
          </div>
        </div>

        {/* Node list */}
        <div className="flex-1 overflow-y-auto py-2 px-2 space-y-1">
          {filteredNodes.map((node) => {
            const tier   = TIER_CONFIG[node.tier];
            const status = STATUS_CONFIG[node.status];
            const isActive = selected === node.id;

            return (
              <button
                key={node.id}
                onClick={() => setSelected(isActive ? null : node.id)}
                className="w-full text-left rounded-lg px-3 py-2.5 transition-all group"
                style={{
                  background: isActive ? "rgba(0,112,243,0.12)" : "transparent",
                  border: isActive ? "1px solid rgba(0,112,243,0.22)" : "1px solid transparent",
                }}
              >
                <div className="flex items-center gap-2.5">
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center text-[10px] font-bold shrink-0"
                    style={{
                      background: `${tier.color}15`,
                      border: `1px solid ${tier.color}40`,
                      color: tier.color,
                    }}
                  >
                    {initials(node.name)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-white truncate">
                      {node.name}
                    </p>
                    <p className="text-[10px] truncate" style={{ color: "#526080" }}>
                      {node.role}
                    </p>
                  </div>
                  <div className="flex flex-col items-end gap-1 shrink-0">
                    <span
                      className="text-[10px] font-bold tabular-nums"
                      style={{
                        color:
                          node.threatScore >= 80 ? "#ff2d55" :
                          node.threatScore >= 60 ? "#ff8c00" : "#ffd60a",
                      }}
                    >
                      {node.threatScore}
                    </span>
                    <span
                      className="w-1.5 h-1.5 rounded-full"
                      style={{ background: status.color }}
                    />
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        {/* Legend */}
        <div
          className="px-4 py-3 shrink-0 space-y-2"
          style={{ borderTop: "1px solid rgba(255,255,255,0.05)" }}
        >
          <p className="text-[9px] uppercase tracking-widest font-semibold" style={{ color: "#2a3a55" }}>
            Edge Type Legend
          </p>
          {Object.entries(edgeColor).map(([type, color]) => (
            <div key={type} className="flex items-center gap-2">
              <div
                className="h-0.5 w-6 rounded"
                style={{ background: color }}
              />
              <span className="text-[10px] capitalize" style={{ color: "#526080" }}>
                {type}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* ═══ CENTER: Network Graph ═══ */}
      <div
        className="flex-1 relative overflow-hidden flex flex-col"
        style={{ background: "#080b12" }}
      >
        {/* Graph header */}
        <div
          className="flex items-center justify-between px-6 py-3 shrink-0"
          style={{
            background: "rgba(10,15,30,0.9)",
            borderBottom: "1px solid rgba(255,255,255,0.06)",
          }}
        >
          <div className="flex items-center gap-3">
            <Users className="w-4 h-4" style={{ color: "#526080" }} />
            <span className="text-sm font-bold text-white">
              Arun Singh Criminal Network
            </span>
            <span
              className="text-[10px] px-2 py-0.5 rounded-full font-semibold"
              style={{
                background: "rgba(255,45,85,0.1)",
                color: "#ff2d55",
              }}
            >
              {NETWORK_NODES.filter((n) => n.status === "wanted").length} Wanted
            </span>
            <span
              className="text-[10px] px-2 py-0.5 rounded-full font-semibold"
              style={{
                background: "rgba(48,209,88,0.1)",
                color: "#30d158",
              }}
            >
              {NETWORK_NODES.filter((n) => n.status === "arrested").length} Arrested
            </span>
          </div>
          <p className="text-xs" style={{ color: "#2a3a55" }}>
            Click a node to inspect · Hover to preview connections
          </p>
        </div>

        {/* SVG Canvas */}
        <div className="flex-1 relative overflow-hidden">
          {/* Grid background */}
          <div
            className="absolute inset-0 opacity-30"
            style={{
              backgroundImage:
                "linear-gradient(rgba(0,112,243,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(0,112,243,0.07) 1px, transparent 1px)",
              backgroundSize: "40px 40px",
            }}
          />

          <svg
            viewBox={`0 0 ${W} ${H}`}
            className="w-full h-full"
            preserveAspectRatio="xMidYMid meet"
          >
            {/* SVG defs: filters */}
            <defs>
              {["#ff2d55", "#ff8c00", "#ffd60a", "#30d158", "#0070f3", "#bf5af2"].map((color) => (
                <filter key={color} id={`glow-${color.replace("#", "")}`}>
                  <feGaussianBlur stdDeviation="4" result="blur" />
                  <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
              ))}
            </defs>

            {/* ── Edges ── */}
            {NETWORK_EDGES.map((edge) => {
              const src = NETWORK_NODES.find((n) => n.id === edge.source)!;
              const tgt = NETWORK_NODES.find((n) => n.id === edge.target)!;
              const cfg = EDGE_CONFIG[edge.strength];
              const color = edgeColor[edge.type];

              const isHighlighted =
                activeId &&
                (edge.source === activeId || edge.target === activeId);
              const isDimmed = activeId && !isHighlighted;

              return (
                <motion.line
                  key={edge.id}
                  x1={src.x} y1={src.y}
                  x2={tgt.x} y2={tgt.y}
                  stroke={color}
                  strokeWidth={isHighlighted ? cfg.width * 2 : cfg.width}
                  strokeDasharray={cfg.dash === "none" ? undefined : cfg.dash}
                  opacity={
                    isDimmed
                      ? 0.05
                      : isHighlighted
                      ? 1
                      : cfg.opacity
                  }
                  animate={{
                    opacity: isDimmed
                      ? 0.05
                      : isHighlighted
                      ? 1
                      : cfg.opacity,
                  }}
                  transition={{ duration: 0.25 }}
                />
              );
            })}

            {/* ── Nodes ── */}
            {NETWORK_NODES.map((node) => {
              const tier   = TIER_CONFIG[node.tier];
              const status = STATUS_CONFIG[node.status];
              const r      = tier.radius;

              const isSelected   = selected === node.id;
              const isHovered    = hovered  === node.id;
              const isConnected  = activeId ? connectedIds.has(node.id) : false;
              const isDimmed     = activeId && !isSelected && !isConnected && node.id !== activeId;

              return (
                <g
                  key={node.id}
                  style={{ cursor: "pointer" }}
                  onClick={() => setSelected(isSelected ? null : node.id)}
                  onMouseEnter={() => setHovered(node.id)}
                  onMouseLeave={() => setHovered(null)}
                >
                  {/* Glow ring (selected / wanted) */}
                  {(isSelected || node.status === "wanted") && (
                    <motion.circle
                      cx={node.x} cy={node.y}
                      r={r + 8}
                      fill="none"
                      stroke={isSelected ? "#0070f3" : status.color}
                      strokeWidth={isSelected ? 2 : 1}
                      opacity={isSelected ? 0.8 : 0.3}
                      animate={{ r: [r + 6, r + 12, r + 6] }}
                      transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                    />
                  )}

                  {/* Main circle */}
                  <motion.circle
                    cx={node.x} cy={node.y}
                    r={r}
                    fill={`${tier.color}18`}
                    stroke={isSelected ? "#0070f3" : status.color}
                    strokeWidth={isSelected ? 3 : isHovered ? 2 : 1.5}
                    opacity={isDimmed ? 0.2 : 1}
                    animate={{
                      r: isSelected ? r + 3 : isHovered ? r + 2 : r,
                      opacity: isDimmed ? 0.2 : 1,
                    }}
                    transition={{ duration: 0.2 }}
                  />

                  {/* Initials */}
                  <text
                    x={node.x} y={node.y}
                    textAnchor="middle"
                    dominantBaseline="central"
                    fontSize={node.tier === 1 ? 13 : node.tier === 2 ? 10 : 8}
                    fontWeight="bold"
                    fill={isDimmed ? "#2a3a55" : tier.color}
                    style={{ userSelect: "none", transition: "fill 0.2s" }}
                  >
                    {initials(node.name)}
                  </text>

                  {/* Name label */}
                  <text
                    x={node.x}
                    y={node.y + r + 14}
                    textAnchor="middle"
                    fontSize={node.tier === 1 ? 11 : 9}
                    fontWeight={isSelected ? "700" : "500"}
                    fill={isDimmed ? "#1a2640" : isSelected ? "white" : "#94a3c0"}
                    style={{ userSelect: "none", transition: "fill 0.2s" }}
                  >
                    {node.name.split(" ")[0]}
                  </text>

                  {/* Threat score badge */}
                  {(isSelected || isHovered) && (
                    <g>
                      <rect
                        x={node.x + r - 4}
                        y={node.y - r - 16}
                        width={30}
                        height={14}
                        rx={4}
                        fill={
                          node.threatScore >= 80 ? "#ff2d5530" :
                          node.threatScore >= 60 ? "#ff8c0030" : "#ffd60a30"
                        }
                        stroke={
                          node.threatScore >= 80 ? "#ff2d55" :
                          node.threatScore >= 60 ? "#ff8c00" : "#ffd60a"
                        }
                        strokeWidth={0.8}
                      />
                      <text
                        x={node.x + r + 11}
                        y={node.y - r - 6}
                        textAnchor="middle"
                        dominantBaseline="middle"
                        fontSize={8}
                        fontWeight="700"
                        fill={
                          node.threatScore >= 80 ? "#ff2d55" :
                          node.threatScore >= 60 ? "#ff8c00" : "#ffd60a"
                        }
                      >
                        {node.threatScore}
                      </text>
                    </g>
                  )}
                </g>
              );
            })}
          </svg>
        </div>

        {/* Stats footer */}
        <div
          className="flex items-center gap-6 px-6 py-2.5 shrink-0 text-xs"
          style={{
            background: "rgba(10,15,30,0.9)",
            borderTop: "1px solid rgba(255,255,255,0.05)",
            color: "#2a3a55",
          }}
        >
          <span>
            <strong className="text-white">{NETWORK_NODES.length}</strong> nodes
          </span>
          <span>
            <strong className="text-white">{NETWORK_EDGES.length}</strong> connections
          </span>
          <span>
            <strong style={{ color: "#ff2d55" }}>
              {NETWORK_NODES.filter((n) => n.status === "wanted").length}
            </strong>{" "}
            still at large
          </span>
          <span>
            <strong style={{ color: "#30d158" }}>
              {NETWORK_NODES.filter((n) => n.status === "arrested").length}
            </strong>{" "}
            arrested
          </span>
          <span>
            <strong style={{ color: "#ff8c00" }}>
              {NETWORK_NODES.filter((n) => n.status === "unknown").length}
            </strong>{" "}
            unknown
          </span>
          <span className="ml-auto flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" style={{ color: "#ff2d55" }} />
            Active Interpol Red Notice: Arun Singh
          </span>
        </div>
      </div>

      {/* ═══ RIGHT: Detail Panel ═══ */}
      <AnimatePresence>
        {selectedNode && (
          <NodeDetail
            node={selectedNode}
            onClose={() => setSelected(null)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
