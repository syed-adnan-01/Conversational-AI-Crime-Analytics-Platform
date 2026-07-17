"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";
import {
  Shield,
  Eye,
  EyeOff,
  AlertTriangle,
  Lock,
  User,
  ChevronRight,
  Fingerprint,
  Activity,
  Globe,
  Zap,
  Radio,
  CheckCircle2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

// ─── Static data ─────────────────────────────────────────────────────────────

const DEPARTMENTS = [
  { value: "cyber-crime", label: "Cyber Crime Division" },
  { value: "homicide", label: "Homicide Investigation Unit" },
  { value: "narcotics", label: "Narcotics Control Bureau" },
  { value: "anti-terrorism", label: "Anti-Terrorism Squad" },
  { value: "financial-crime", label: "Financial Crime Unit" },
  { value: "organized-crime", label: "Organized Crime Cell" },
  { value: "special-branch", label: "Special Branch" },
  { value: "state-police", label: "State Police Headquarters" },
  { value: "central-bureau", label: "Central Bureau of Investigation" },
];

const LIVE_STATS = [
  {
    label: "Active FIRs",
    value: "2,847",
    Icon: Radio,
    color: "#ff8c00",
    bg: "rgba(255,140,0,0.08)",
    border: "rgba(255,140,0,0.2)",
  },
  {
    label: "AI Alerts",
    value: "18",
    Icon: Zap,
    color: "#ff2d55",
    bg: "rgba(255,45,85,0.08)",
    border: "rgba(255,45,85,0.2)",
  },
  {
    label: "Jurisdictions",
    value: "36",
    Icon: Globe,
    color: "#2b91ff",
    bg: "rgba(43,145,255,0.08)",
    border: "rgba(43,145,255,0.2)",
  },
  {
    label: "Officers Online",
    value: "1,203",
    Icon: Activity,
    color: "#30d158",
    bg: "rgba(48,209,88,0.08)",
    border: "rgba(48,209,88,0.2)",
  },
];

const STATUS_INDICATORS = [
  { dot: "#30d158", pulse: false, text: "All Systems Operational" },
  { dot: "#2b91ff", pulse: false, text: "AI Engine Active" },
  { dot: "#ffd60a", pulse: true, text: "18 Alerts Pending" },
];

// Demo credentials hint
const DEMO_ID = "IPS-2024-0042";
const DEMO_PASS = "admin@123";

// ─── Component ────────────────────────────────────────────────────────────────

export default function LoginForm() {
  const router = useRouter();

  const [employeeId, setEmployeeId] = useState("");
  const [password, setPassword] = useState("");
  const [department, setDepartment] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [error, setError] = useState("");
  const [currentTime, setCurrentTime] = useState("");

  // Live clock
  useEffect(() => {
    const tick = () => {
      setCurrentTime(
        new Date().toLocaleString("en-IN", {
          timeZone: "Asia/Kolkata",
          hour12: false,
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!employeeId.trim() || !password.trim() || !department) {
      setError("All fields are required for secure authentication.");
      return;
    }

    setIsLoading(true);

    // Simulate multi-step auth
    const steps = [
      "Verifying credentials…",
      "Checking clearance level…",
      "Establishing secure channel…",
      "Loading intelligence data…",
    ];

    for (let i = 0; i < steps.length; i++) {
      setLoadingStep(i);
      await new Promise((r) => setTimeout(r, 500));
    }

    setIsLoading(false);
    router.push("/dashboard");
  };

  return (
    <div className="relative min-h-screen w-full overflow-hidden flex items-center justify-center"
      style={{ backgroundColor: "#080b12" }}>

      {/* ── Animated Background Blobs ── */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute rounded-full blur-[120px]"
          style={{
            width: 500,
            height: 500,
            top: "-15%",
            left: "-10%",
            background: "radial-gradient(circle, rgba(0,112,243,0.12) 0%, transparent 70%)",
          }}
          animate={{ scale: [1, 1.1, 1], opacity: [0.6, 1, 0.6] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute rounded-full blur-[120px]"
          style={{
            width: 400,
            height: 400,
            bottom: "-15%",
            right: "-8%",
            background: "radial-gradient(circle, rgba(94,92,230,0.1) 0%, transparent 70%)",
          }}
          animate={{ scale: [1.1, 1, 1.1], opacity: [0.6, 1, 0.6] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 2 }}
        />
        <motion.div
          className="absolute rounded-full blur-[80px]"
          style={{
            width: 250,
            height: 250,
            top: "40%",
            left: "30%",
            background: "radial-gradient(circle, rgba(191,90,242,0.06) 0%, transparent 70%)",
          }}
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 12, repeat: Infinity, ease: "easeInOut", delay: 4 }}
        />
      </div>

      {/* ── Grid Overlay ── */}
      <div className="absolute inset-0 opacity-50 pointer-events-none bg-grid" />

      {/* ── Scan Line ── */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute left-0 right-0 h-px"
          style={{
            background:
              "linear-gradient(90deg, transparent 0%, rgba(0,112,243,0.4) 50%, transparent 100%)",
          }}
          animate={{ top: ["-2px", "100%"] }}
          transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
        />
      </div>

      {/* ── Main Layout ── */}
      <div className="relative z-10 w-full max-w-6xl mx-auto px-4 py-10 flex flex-col lg:flex-row items-center gap-12 lg:gap-20">

        {/* ═══ LEFT: Brand Panel ═══ */}
        <motion.div
          className="flex-1 w-full text-center lg:text-left"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.9, ease: "easeOut" }}
        >
          {/* Logo */}
          <div className="flex items-center justify-center lg:justify-start gap-4 mb-10">
            <div className="relative shrink-0">
              <div
                className="w-14 h-14 rounded-2xl flex items-center justify-center"
                style={{
                  background: "rgba(0,112,243,0.15)",
                  border: "1px solid rgba(0,112,243,0.35)",
                  boxShadow: "0 0 24px rgba(0,112,243,0.2)",
                }}
              >
                <Shield className="w-7 h-7 text-blue-400" />
              </div>
              {/* Online dot */}
              <span
                className="absolute -top-1 -right-1 w-3.5 h-3.5 bg-green-400 rounded-full"
                style={{ border: "2.5px solid #080b12" }}
              />
            </div>
            <div>
              <div className="text-2xl font-bold tracking-tight text-white">
                CrimeSphere
                <span className="text-blue-400"> AI</span>
              </div>
              <div
                className="text-xs uppercase tracking-[0.2em] mt-0.5"
                style={{ color: "#526080" }}
              >
                Intelligence Platform
              </div>
            </div>
          </div>

          {/* Headline */}
          <h1 className="text-4xl lg:text-5xl font-bold text-white leading-tight mb-5">
            National Crime
            <br />
            <span
              style={{
                background: "linear-gradient(135deg, #2b91ff 0%, #32ade6 50%, #bf5af2 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
                backgroundClip: "text",
              }}
            >
              Intelligence Network
            </span>
          </h1>

          <p className="text-lg leading-relaxed mb-10 max-w-md mx-auto lg:mx-0" style={{ color: "#526080" }}>
            AI-powered investigation platform connecting law enforcement
            agencies across all 36 states & union territories of India.
          </p>

          {/* Status Indicators */}
          <div className="flex flex-wrap gap-2 justify-center lg:justify-start mb-10">
            {STATUS_INDICATORS.map((item, i) => (
              <div
                key={i}
                className="flex items-center gap-2 rounded-full px-3 py-1.5"
                style={{
                  background: "rgba(255,255,255,0.04)",
                  border: "1px solid rgba(255,255,255,0.08)",
                }}
              >
                <span className="relative flex h-2 w-2">
                  {item.pulse && (
                    <span
                      className="absolute inline-flex h-full w-full rounded-full opacity-75 animate-ping"
                      style={{ backgroundColor: item.dot }}
                    />
                  )}
                  <span
                    className="relative inline-flex rounded-full h-2 w-2"
                    style={{ backgroundColor: item.dot }}
                  />
                </span>
                <span className="text-xs" style={{ color: "#94a3c0" }}>
                  {item.text}
                </span>
              </div>
            ))}
          </div>

          {/* Live Stats Grid */}
          <div className="grid grid-cols-2 gap-3 max-w-sm mx-auto lg:mx-0">
            {LIVE_STATS.map((stat, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 + i * 0.1, duration: 0.5 }}
                className="rounded-xl p-4"
                style={{
                  background: stat.bg,
                  border: `1px solid ${stat.border}`,
                }}
              >
                <stat.Icon
                  className="w-4 h-4 mb-2"
                  style={{ color: stat.color }}
                />
                <div
                  className="text-2xl font-bold tabular-nums"
                  style={{ color: stat.color }}
                >
                  {stat.value}
                </div>
                <div className="text-xs mt-0.5" style={{ color: "#526080" }}>
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* ═══ RIGHT: Login Card ═══ */}
        <motion.div
          className="w-full max-w-[440px] shrink-0"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.9, ease: "easeOut", delay: 0.15 }}
        >
          <div
            className="rounded-2xl overflow-hidden"
            style={{
              background: "rgba(13,19,34,0.92)",
              backdropFilter: "blur(28px)",
              WebkitBackdropFilter: "blur(28px)",
              border: "1px solid rgba(255,255,255,0.08)",
              boxShadow:
                "0 32px 64px rgba(0,0,0,0.5), 0 0 0 1px rgba(0,112,243,0.05), inset 0 1px 0 rgba(255,255,255,0.05)",
            }}
          >
            {/* ── Warning Banner ── */}
            <div
              className="flex items-center gap-2.5 px-6 py-3"
              style={{
                background: "rgba(255,45,85,0.08)",
                borderBottom: "1px solid rgba(255,45,85,0.15)",
              }}
            >
              <AlertTriangle className="w-3.5 h-3.5 shrink-0" style={{ color: "#ff2d55" }} />
              <span
                className="text-xs font-semibold uppercase tracking-widest"
                style={{ color: "#ff6b7a" }}
              >
                Restricted Access — Authorised Personnel Only
              </span>
            </div>

            <div className="p-8">
              {/* ── Card Header ── */}
              <div className="text-center mb-8">
                <div
                  className="inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-4"
                  style={{
                    background: "rgba(0,112,243,0.12)",
                    border: "1px solid rgba(0,112,243,0.3)",
                  }}
                >
                  <Lock className="w-7 h-7 text-blue-400" />
                </div>
                <h2 className="text-xl font-bold text-white">Secure Authentication</h2>
                <p className="text-sm mt-1" style={{ color: "#526080" }}>
                  Enter your credentials to access the platform
                </p>
                {/* Demo hint */}
                <div
                  className="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 mt-3 text-xs"
                  style={{
                    background: "rgba(0,112,243,0.08)",
                    border: "1px solid rgba(0,112,243,0.2)",
                    color: "#2b91ff",
                  }}
                >
                  <CheckCircle2 className="w-3 h-3" />
                  Demo: ID&nbsp;<strong>{DEMO_ID}</strong>&nbsp;/ Pass&nbsp;<strong>{DEMO_PASS}</strong>
                </div>
              </div>

              {/* ── Form ── */}
              <form onSubmit={handleSubmit} className="space-y-5">

                {/* Employee ID */}
                <div className="space-y-1.5">
                  <Label htmlFor="employeeId" className="text-sm font-medium" style={{ color: "#94a3c0" }}>
                    Employee ID / Badge Number
                  </Label>
                  <div className="relative">
                    <User
                      className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none"
                      style={{ color: "#526080" }}
                    />
                    <Input
                      id="employeeId"
                      type="text"
                      placeholder="e.g. IPS-2024-0042"
                      value={employeeId}
                      onChange={(e) => setEmployeeId(e.target.value)}
                      autoComplete="off"
                      className={cn(
                        "pl-10 h-11 text-white placeholder:text-[#2a3a55]",
                        "transition-all duration-200",
                        "focus-visible:ring-2 focus-visible:ring-blue-500/30 focus-visible:border-blue-500/60"
                      )}
                      style={{ background: "rgba(255,255,255,0.05)", borderColor: "rgba(255,255,255,0.1)" }}
                    />
                  </div>
                </div>

                {/* Password */}
                <div className="space-y-1.5">
                  <Label htmlFor="password" className="text-sm font-medium" style={{ color: "#94a3c0" }}>
                    Password
                  </Label>
                  <div className="relative">
                    <Lock
                      className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none"
                      style={{ color: "#526080" }}
                    />
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="••••••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className={cn(
                        "pl-10 pr-11 h-11 text-white placeholder:text-[#2a3a55]",
                        "transition-all duration-200",
                        "focus-visible:ring-2 focus-visible:ring-blue-500/30 focus-visible:border-blue-500/60"
                      )}
                      style={{ background: "rgba(255,255,255,0.05)", borderColor: "rgba(255,255,255,0.1)" }}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 transition-colors"
                      style={{ color: "#526080" }}
                      tabIndex={-1}
                    >
                      {showPassword ? (
                        <EyeOff className="w-4 h-4 hover:text-white" />
                      ) : (
                        <Eye className="w-4 h-4 hover:text-white" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Department */}
                <div className="space-y-1.5">
                  <Label htmlFor="department" className="text-sm font-medium" style={{ color: "#94a3c0" }}>
                    Department
                  </Label>
                  <select
                    id="department"
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    className="w-full h-11 px-3 rounded-md text-sm transition-all duration-200 outline-none focus:ring-2"
                    style={{
                      background: "rgba(255,255,255,0.05)",
                      border: "1px solid rgba(255,255,255,0.1)",
                      color: department ? "white" : "#2a3a55",
                      focusRingColor: "rgba(0,112,243,0.3)",
                    }}
                  >
                    <option value="" disabled style={{ background: "#0d1322", color: "#526080" }}>
                      Select your department…
                    </option>
                    {DEPARTMENTS.map((dept) => (
                      <option
                        key={dept.value}
                        value={dept.value}
                        style={{ background: "#0d1322", color: "white" }}
                      >
                        {dept.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Error */}
                <AnimatePresence>
                  {error && (
                    <motion.div
                      initial={{ opacity: 0, y: -8, scale: 0.98 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: -8, scale: 0.98 }}
                      className="flex items-start gap-2.5 rounded-lg px-4 py-3 text-sm"
                      style={{
                        background: "rgba(255,45,85,0.08)",
                        border: "1px solid rgba(255,45,85,0.2)",
                        color: "#ff6b7a",
                      }}
                    >
                      <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                      {error}
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Submit */}
                <Button
                  type="submit"
                  disabled={isLoading}
                  className="w-full h-11 font-semibold text-white rounded-lg transition-all duration-200 group relative overflow-hidden"
                  style={{ background: "#0070f3" }}
                >
                  {/* shimmer effect */}
                  {!isLoading && (
                    <span
                      className="absolute inset-0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"
                      style={{
                        background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)",
                      }}
                    />
                  )}
                  <span className="relative flex items-center justify-center gap-2">
                    {isLoading ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        <span className="text-sm font-medium text-white/80">
                          {["Verifying…", "Checking clearance…", "Securing channel…", "Loading data…"][loadingStep]}
                        </span>
                      </>
                    ) : (
                      <>
                        <span>Authenticate</span>
                        <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" />
                      </>
                    )}
                  </span>
                </Button>

                {/* Divider */}
                <div className="relative flex items-center gap-3">
                  <div className="flex-1 h-px" style={{ background: "rgba(255,255,255,0.06)" }} />
                  <span className="text-xs" style={{ color: "#2a3a55" }}>or</span>
                  <div className="flex-1 h-px" style={{ background: "rgba(255,255,255,0.06)" }} />
                </div>

                {/* Biometric */}
                <button
                  type="button"
                  className="w-full h-11 rounded-lg flex items-center justify-center gap-2 text-sm font-medium transition-all duration-200"
                  style={{
                    background: "rgba(255,255,255,0.04)",
                    border: "1px solid rgba(255,255,255,0.09)",
                    color: "#526080",
                  }}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLButtonElement).style.color = "#94a3c0";
                    (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(255,255,255,0.15)";
                    (e.currentTarget as HTMLButtonElement).style.background = "rgba(255,255,255,0.07)";
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLButtonElement).style.color = "#526080";
                    (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(255,255,255,0.09)";
                    (e.currentTarget as HTMLButtonElement).style.background = "rgba(255,255,255,0.04)";
                  }}
                >
                  <Fingerprint className="w-4 h-4" />
                  Biometric Authentication
                </button>
              </form>
            </div>

            {/* ── Card Footer ── */}
            <div
              className="px-8 py-4 flex items-center justify-between"
              style={{ borderTop: "1px solid rgba(255,255,255,0.05)" }}
            >
              <div className="flex items-center gap-2">
                <span
                  className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"
                />
                <span
                  className="text-xs font-mono tabular-nums"
                  style={{ color: "#2a3a55" }}
                >
                  {currentTime} IST
                </span>
              </div>
              <div className="flex items-center gap-1.5" style={{ color: "#2a3a55" }}>
                <Lock className="w-3 h-3" />
                <span className="text-xs">256-bit TLS</span>
              </div>
            </div>
          </div>

          {/* Legal disclaimer */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="text-center text-xs leading-relaxed mt-4"
            style={{ color: "#2a3a55" }}
          >
            Unauthorised access is a punishable offence under the IT Act 2000, Section 43A.
            <br />
            All activities are logged, monitored, and audited.
          </motion.p>
        </motion.div>
      </div>
    </div>
  );
}
