"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Send,
  Plus,
  Brain,
  Copy,
  RotateCcw,
  Sparkles,
  FileText,
  MapPin,
  Network,
  TrendingUp,
  MessageSquare,
  Clock,
  ChevronRight,
  Shield,
  Check,
} from "lucide-react";
import {
  quickPrompts,
  initialMessages,
  type ChatMessage,
} from "@/lib/mock-data/chat";
import { formatRelativeTime } from "@/lib/utils";
import { cn } from "@/lib/utils";
import { ai } from "@/lib/services/ai";
import { searchCases } from "@/lib/services/cases";

// ─── Icon map for quick prompts ───────────────────────────────────────────
const PROMPT_ICONS: Record<string, React.ElementType> = {
  FileText,
  MapPin,
  Network,
  TrendingUp,
  Clock,
};

// ─── Simple markdown renderer ─────────────────────────────────────────────
function formatInline(text: string | undefined): React.ReactNode[] {
  if (!text) return [];
  const parts = text.split(/\*\*(.*?)\*\*/g);
  return parts.map((part, i) => {
    if (i % 2 === 1) {
      return (
        <strong key={i} className="font-semibold text-white">
          {part}
        </strong>
      );
    }
    
    // Render legal acts as badges
    const badgeRegex = /(IPC\s\d+|BNS\s\d+|BSA\s\d+|CrPC\s\d+)/g;
    const subParts = part.split(badgeRegex);
    if (subParts.length === 1) return part;
    
    return subParts.map((sp, j) => {
      if (badgeRegex.test(sp)) {
        return (
          <span key={`${i}-${j}`} className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20 mx-0.5">
            <Shield className="w-2.5 h-2.5 mr-1" />
            {sp}
          </span>
        );
      }
      return sp;
    });
  });
}

function MessageContent({ content }: { content: string | undefined }) {
  const blocks = (content ?? "").split(/\n\n+/);

  return (
    <div className="space-y-2.5 text-sm leading-relaxed">
      {blocks.map((block, i) => {
        const trimmed = block.trim();

        if (trimmed === "---") {
          return (
            <hr
              key={i}
              style={{ borderColor: "rgba(255,255,255,0.08)", marginBlock: "0.75rem" }}
            />
          );
        }

        const lines = trimmed.split("\n");
        const isList = lines.every((l) => l.startsWith("- ") || l === "");
        if (isList && lines.some((l) => l.startsWith("- "))) {
          return (
            <ul key={i} className="space-y-1.5">
              {lines
                .filter((l) => l.startsWith("- "))
                .map((item, j) => (
                  <li key={j} className="flex items-start gap-2">
                    <span
                      className="w-1.5 h-1.5 rounded-full mt-2 shrink-0"
                      style={{ background: "#0070f3" }}
                    />
                    <span style={{ color: "#94a3c0" }}>
                      {formatInline(item.slice(2))}
                    </span>
                  </li>
                ))}
            </ul>
          );
        }

        const isNumbered = lines.every(
          (l) => /^\d+\.\s/.test(l) || l === ""
        );
        if (isNumbered && lines.some((l) => /^\d+\.\s/.test(l))) {
          return (
            <ol key={i} className="space-y-1.5">
              {lines
                .filter((l) => /^\d+\.\s/.test(l))
                .map((item, j) => (
                  <li key={j} className="flex items-start gap-2">
                    <span
                      className="text-xs font-bold tabular-nums shrink-0 mt-0.5"
                      style={{ color: "#0070f3", minWidth: 16 }}
                    >
                      {j + 1}.
                    </span>
                    <span style={{ color: "#94a3c0" }}>
                      {formatInline(item.replace(/^\d+\.\s/, ""))}
                    </span>
                  </li>
                ))}
            </ol>
          );
        }

        if (lines.length > 1) {
          return (
            <div key={i} className="space-y-1">
              {lines.map((line, j) => (
                <p key={j} style={{ color: "#94a3c0" }}>
                  {formatInline(line)}
                </p>
              ))}
            </div>
          );
        }

        return (
          <p key={i} style={{ color: "#94a3c0" }}>
            {formatInline(trimmed)}
          </p>
        );
      })}
    </div>
  );
}

// ─── Typing Indicator ─────────────────────────────────────────────────────
function TypingIndicator() {
  const [loadingStep, setLoadingStep] = useState(0);
  const steps = [
    "Thinking...",
    "Retrieving Knowledge Base...",
    "Searching FIR...",
    "Generating Investigation...",
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setLoadingStep((prev) => (prev + 1) % steps.length);
    }, 2000);
    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="flex items-start gap-3">
      <div
        className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0"
        style={{
          background: "rgba(191,90,242,0.15)",
          border: "1px solid rgba(191,90,242,0.3)",
        }}
      >
        <Brain className="w-4 h-4" style={{ color: "#bf5af2" }} />
      </div>
      <div
        className="rounded-xl px-4 py-3 flex items-center gap-3"
        style={{
          background: "rgba(13,19,34,0.9)",
          border: "1px solid rgba(255,255,255,0.07)",
        }}
      >
        <div className="flex items-center gap-1.5">
          {[0, 1, 2].map((i) => (
            <motion.span
              key={i}
              className="w-1.5 h-1.5 rounded-full"
              style={{ background: "#bf5af2" }}
              animate={{ y: [0, -4, 0], opacity: [0.4, 1, 0.4] }}
              transition={{
                duration: 0.8,
                repeat: Infinity,
                delay: i * 0.15,
                ease: "easeInOut",
              }}
            />
          ))}
        </div>
        <AnimatePresence mode="wait">
          <motion.span
            key={loadingStep}
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -5 }}
            className="text-xs font-medium"
            style={{ color: "#94a3c0" }}
          >
            {steps[loadingStep]}
          </motion.span>
        </AnimatePresence>
      </div>
    </div>
  );
}

// ─── Copy button ──────────────────────────────────────────────────────────
function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="flex items-center gap-1 text-[10px] px-2 py-1 rounded-md transition-colors"
      style={{
        color: copied ? "#30d158" : "#2a3a55",
        background: copied ? "rgba(48,209,88,0.1)" : "transparent",
      }}
    >
      {copied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
      {copied ? "Copied" : "Copy"}
    </button>
  );
}

interface Session {
  id: string;
  title: string;
  preview: string;
  timestamp: string;
  messageCount: number;
}

// ─── Main Component ───────────────────────────────────────────────────────
export default function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [activeSession, setActiveSession] = useState("s1");
  const [caseId, setCaseId] = useState<string | null>(null);
  
  // Basic mock sessions for the sidebar to look good
  const [sessions, setSessions] = useState<Session[]>([
    {
      id: "s1",
      title: "New Investigation",
      preview: "Hello, I am CrimeSphere AI...",
      timestamp: new Date().toISOString(),
      messageCount: 1,
    }
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Fetch a default case ID on mount
  useEffect(() => {
    searchCases({ page: 1, page_size: 1 })
      .then((res) => {
        if (res.items.length > 0) {
          setCaseId(res.items[0].case_master_id);
        } else {
          setCaseId("default-case-id"); // fallback
        }
      })
      .catch((err) => {
        console.error("Failed to fetch default case", err);
        setCaseId("default-case-id");
      });
  }, []);

  // Fetch session history when activeSession changes
  useEffect(() => {
    if (activeSession === "new") {
      return;
    }

    ai.copilotHistory(activeSession)
      .then((res) => {
        if (res.messages && res.messages.length > 0) {
          const newMessages: ChatMessage[] = [];

          // Backend get_history returns ConversationMessage objects: { role, content, timestamp, message_id }
          // Check format: if objects have 'role' field it's ConversationMessage, else it's turn pairs
          const firstMsg = res.messages[0];
          if (firstMsg && firstMsg.role) {
            // ConversationMessage format: { role, content, timestamp, message_id }
            res.messages.forEach((msg: { role?: string; content?: string; timestamp?: string; message_id?: string }, idx: number) => {
              newMessages.push({
                id: msg.message_id ?? `hist-${idx}`,
                role: (msg.role === "user" ? "user" : "assistant") as "user" | "assistant",
                content: msg.content ?? "",
                timestamp: msg.timestamp ?? new Date().toISOString(),
                sources: msg.role === "assistant" ? [] : undefined,
              });
            });
          } else {
            // Turn-pair format: { turn_id, user_message, ai_response, timestamp }
            res.messages.forEach((turn: { turn_id?: string | number; user_message?: string; ai_response?: string; timestamp?: string }, idx: number) => {
              const tid = turn.turn_id ?? idx;
              const ts = turn.timestamp ?? new Date().toISOString();
              newMessages.push({
                id: `u-${tid}`,
                role: "user",
                content: turn.user_message ?? "",
                timestamp: ts,
              });
              newMessages.push({
                id: `a-${tid}`,
                role: "assistant",
                content: turn.ai_response ?? "",
                timestamp: ts,
                sources: [],
              });
            });
          }

          setMessages(newMessages.length > 0 ? newMessages : initialMessages);
        } else {
          setMessages(initialMessages);
        }
      })
      .catch((err) => {
        console.error("Failed to fetch session history", err);
        setMessages(initialMessages);
      });
  }, [activeSession]);

  // Auto-scroll on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 160) + "px";
  }, [input]);

  const handleSend = useCallback(
    async (overrideQuery?: string) => {
      const q = (overrideQuery ?? input).trim();
      if (!q || isTyping) return;

      const userMsg: ChatMessage = {
        id: `u-${Date.now()}`,
        role: "user",
        content: q,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMsg]);
      setInput("");
      setIsTyping(true);

      // If it's a "new" session, create an ID and add to sessions
      let sessionId = activeSession;
      if (sessionId === "new") {
        sessionId = `sess-${Date.now()}`;
        setActiveSession(sessionId);
        setSessions(prev => [
          {
            id: sessionId,
            title: q.substring(0, 30) + "...",
            preview: "Started just now",
            timestamp: new Date().toISOString(),
            messageCount: 2,
          },
          ...prev
        ]);
      } else {
        // Update existing session message count and preview
        setSessions(prev => prev.map(s => 
          s.id === sessionId 
            ? { ...s, preview: q.substring(0, 30), messageCount: s.messageCount + 2, timestamp: new Date().toISOString() } 
            : s
        ));
      }

      try {
        const response = await ai.copilotChat({
          session_id: sessionId,
          case_id: caseId || "default",
          message: q,
        });

        const aiMsg: ChatMessage = {
          id: `a-${Date.now()}`,
          role: "assistant",
          // Backend CopilotResponse uses 'answer' field (not 'response')
          content: response.answer ?? response.response ?? response.message ?? "(no response)",
          timestamp: new Date().toISOString(),
          sources: [response.provider_used ?? "CrimeSphere AI"],
          provider: response.provider_used,
          citations: response.citations || [],
          confidence: response.confidence,
        };
        
        setIsTyping(false);
        setMessages((prev) => [...prev, aiMsg]);
      } catch (error) {
        console.error("Error from AI copilot:", error);
        
        const aiMsg: ChatMessage = {
          id: `a-${Date.now()}`,
          role: "assistant",
          content: "I encountered an error while trying to process your request. Please try again.",
          timestamp: new Date().toISOString(),
          sources: [],
        };
        
        setIsTyping(false);
        setMessages((prev) => [...prev, aiMsg]);
      }
    },
    [input, isTyping, activeSession, caseId]
  );

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const showWelcomePrompts = messages.length === 1 && !isTyping;

  return (
    // -m-6 cancels the parent's p-6 so we can fill the full height
    <div
      className="-m-6 flex overflow-hidden"
      style={{ height: "calc(100vh - 4rem)" }}
    >
      {/* ═══ LEFT: Sessions Panel ═══ */}
      <div
        className="hidden lg:flex w-[260px] shrink-0 flex-col"
        style={{
          background: "#0a0f1e",
          borderRight: "1px solid rgba(255,255,255,0.06)",
        }}
      >
        {/* Header */}
        <div
          className="flex items-center justify-between px-4 py-4 shrink-0"
          style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}
        >
          <span className="text-sm font-bold text-white">Conversations</span>
          <button
            className="flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-lg transition-colors"
            style={{
              background: "rgba(0,112,243,0.12)",
              border: "1px solid rgba(0,112,243,0.25)",
              color: "#2b91ff",
            }}
            onClick={() => {
              setMessages(initialMessages);
              setActiveSession("new");
            }}
          >
            <Plus className="w-3 h-3" />
            New
          </button>
        </div>

        {/* Session list */}
        <div className="flex-1 overflow-y-auto py-3 px-3 space-y-1">
          <p
            className="text-[10px] uppercase tracking-widest font-semibold px-2 mb-2"
            style={{ color: "#2a3a55" }}
          >
            Recent
          </p>

          {sessions.map((session) => {
            const isActive = activeSession === session.id;
            return (
              <button
                key={session.id}
                onClick={() => setActiveSession(session.id)}
                className="w-full text-left rounded-lg px-3 py-2.5 transition-all group"
                style={{
                  background: isActive
                    ? "rgba(0,112,243,0.12)"
                    : "transparent",
                  border: isActive
                    ? "1px solid rgba(0,112,243,0.22)"
                    : "1px solid transparent",
                }}
              >
                <div className="flex items-start gap-2">
                  <MessageSquare
                    className="w-3.5 h-3.5 shrink-0 mt-0.5"
                    style={{ color: isActive ? "#2b91ff" : "#2a3a55" }}
                  />
                  <div className="flex-1 min-w-0">
                    <p
                      className="text-xs font-medium truncate"
                      style={{ color: isActive ? "white" : "#526080" }}
                    >
                      {session.title}
                    </p>
                    <p
                      className="text-[10px] truncate mt-0.5"
                      style={{ color: "#2a3a55" }}
                    >
                      {session.preview}
                    </p>
                    <div
                      className="flex items-center gap-1 mt-1"
                      style={{ color: "#2a3a55" }}
                    >
                      <Clock className="w-2.5 h-2.5" />
                      <span className="text-[10px]">
                        {formatRelativeTime(session.timestamp)}
                      </span>
                      <span className="text-[10px] ml-auto">
                        {session.messageCount} msgs
                      </span>
                    </div>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        {/* Model info footer */}
        <div
          className="px-4 py-3 shrink-0"
          style={{ borderTop: "1px solid rgba(255,255,255,0.05)" }}
        >
          <div className="flex items-center gap-2">
            <div
              className="w-6 h-6 rounded-md flex items-center justify-center"
              style={{
                background: "rgba(191,90,242,0.15)",
                border: "1px solid rgba(191,90,242,0.3)",
              }}
            >
              <Brain className="w-3.5 h-3.5" style={{ color: "#bf5af2" }} />
            </div>
            <div>
              <p className="text-[10px] font-semibold text-white">
                CrimeSphere GPT-L
              </p>
              <p className="text-[9px]" style={{ color: "#2a3a55" }}>
                v2.4 · Accuracy 94.7%
              </p>
            </div>
            <span
              className="ml-auto w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"
            />
          </div>
        </div>
      </div>

      {/* ═══ RIGHT: Chat Area ═══ */}
      <div className="flex-1 flex flex-col min-w-0" style={{ background: "#080b12" }}>

        {/* ── Chat Header ── */}
        <div
          className="flex items-center justify-between px-6 py-4 shrink-0"
          style={{
            background: "rgba(10,15,30,0.95)",
            borderBottom: "1px solid rgba(255,255,255,0.06)",
            backdropFilter: "blur(12px)",
          }}
        >
          <div className="flex items-center gap-3">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center"
              style={{
                background: "rgba(191,90,242,0.15)",
                border: "1px solid rgba(191,90,242,0.3)",
              }}
            >
              <Brain className="w-4.5 h-4.5" style={{ color: "#bf5af2", width: 18, height: 18 }} />
            </div>
            <div>
              <h2 className="text-sm font-bold text-white">
                CrimeSphere Intelligence
              </h2>
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
                <span className="text-xs" style={{ color: "#526080" }}>
                  Online · Processing 1,203 signals
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs"
              style={{
                background: "rgba(191,90,242,0.08)",
                border: "1px solid rgba(191,90,242,0.2)",
                color: "#bf5af2",
              }}
            >
              <Sparkles className="w-3 h-3" />
              GPT-L v2.4
            </div>
            <button
              onClick={() => setMessages(initialMessages)}
              className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs transition-colors"
              style={{
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.08)",
                color: "#526080",
              }}
            >
              <RotateCcw className="w-3 h-3" />
              Clear
            </button>
          </div>
        </div>

        {/* ── Messages ── */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">

          {/* Welcome quick prompts */}
          <AnimatePresence>
            {showWelcomePrompts && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6"
              >
                {quickPrompts.map((prompt, i) => {
                  const Icon = PROMPT_ICONS[prompt.icon] ?? FileText;
                  return (
                    <motion.button
                      key={prompt.id}
                      initial={{ opacity: 0, y: 12 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.3 + i * 0.08 }}
                      onClick={() => handleSend(prompt.query)}
                      className="flex items-start gap-3 rounded-xl p-4 text-left transition-all group"
                      style={{
                        background: "rgba(13,19,34,0.8)",
                        border: "1px solid rgba(255,255,255,0.07)",
                      }}
                      onMouseEnter={(e) => {
                        (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(0,112,243,0.35)";
                        (e.currentTarget as HTMLButtonElement).style.background = "rgba(0,112,243,0.06)";
                      }}
                      onMouseLeave={(e) => {
                        (e.currentTarget as HTMLButtonElement).style.borderColor = "rgba(255,255,255,0.07)";
                        (e.currentTarget as HTMLButtonElement).style.background = "rgba(13,19,34,0.8)";
                      }}
                    >
                      <div
                        className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0"
                        style={{
                          background: "rgba(0,112,243,0.1)",
                          border: "1px solid rgba(0,112,243,0.2)",
                        }}
                      >
                        <Icon className="w-4 h-4 text-blue-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-semibold text-white mb-0.5">
                          {prompt.label}
                        </p>
                        <p className="text-xs" style={{ color: "#526080" }}>
                          {prompt.description}
                        </p>
                      </div>
                      <ChevronRight
                        className="w-4 h-4 shrink-0 self-center opacity-0 group-hover:opacity-100 transition-opacity"
                        style={{ color: "#2b91ff" }}
                      />
                    </motion.button>
                  );
                })}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Message bubbles */}
          <AnimatePresence initial={false}>
            {messages.map((msg, i) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, ease: "easeOut" }}
                className={cn(
                  "flex gap-3",
                  msg.role === "user" ? "flex-row-reverse" : "flex-row"
                )}
              >
                {/* Avatar */}
                {msg.role === "assistant" ? (
                  <div
                    className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 self-start"
                    style={{
                      background: "rgba(191,90,242,0.15)",
                      border: "1px solid rgba(191,90,242,0.3)",
                    }}
                  >
                    <Brain className="w-4 h-4" style={{ color: "#bf5af2" }} />
                  </div>
                ) : (
                  <div
                    className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 self-start text-xs font-bold text-white"
                    style={{
                      background: "linear-gradient(135deg, #0070f3, #bf5af2)",
                    }}
                  >
                    RK
                  </div>
                )}

                {/* Bubble */}
                <div
                  className={cn(
                    "max-w-[75%] rounded-2xl px-4 py-3",
                    msg.role === "user" ? "rounded-tr-sm" : "rounded-tl-sm"
                  )}
                  style={
                    msg.role === "user"
                      ? {
                          background:
                            "linear-gradient(135deg, #0058cc, #0070f3)",
                          color: "white",
                        }
                      : {
                          background: "rgba(13,19,34,0.9)",
                          border: "1px solid rgba(255,255,255,0.07)",
                        }
                  }
                >
                  {msg.role === "assistant" ? (
                    <MessageContent content={msg.content} />
                  ) : (
                    <p className="text-sm leading-relaxed text-white">
                      {msg.content}
                    </p>
                  )}

                  {/* Footer */}
                  <div
                    className={cn(
                      "flex items-center gap-2 mt-2.5 pt-2",
                      msg.role === "user" ? "justify-end" : "justify-between"
                    )}
                    style={{
                      borderTop:
                        msg.role === "assistant"
                          ? "1px solid rgba(255,255,255,0.05)"
                          : "1px solid rgba(255,255,255,0.15)",
                    }}
                  >
                    {msg.role === "assistant" && (
                      <div className="flex flex-col gap-2 w-full">
                        <div className="flex items-center justify-between">
                          <div className="flex flex-wrap items-center gap-1.5">
                            {msg.provider && (
                              <div
                                className="flex items-center gap-1 px-1.5 py-0.5 rounded text-[9px] font-medium"
                                style={{
                                  background: msg.provider === "QuickML" ? "rgba(191,90,242,0.1)" : "rgba(255,255,255,0.04)",
                                  border: msg.provider === "QuickML" ? "1px solid rgba(191,90,242,0.2)" : "1px solid rgba(255,255,255,0.08)",
                                  color: msg.provider === "QuickML" ? "#bf5af2" : "#94a3c0",
                                }}
                              >
                                <Brain className="w-2.5 h-2.5" />
                                {msg.provider}
                              </div>
                            )}
                            {msg.confidence !== undefined && (
                              <div className="text-[10px] text-green-400">
                                {(msg.confidence * 100).toFixed(0)}% Confidence
                              </div>
                            )}
                          </div>
                          <div className="flex items-center gap-3">
                            <CopyButton text={msg.content} />
                            <span className="text-[9px] text-[#526080]">
                              {new Date(msg.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                            </span>
                          </div>
                        </div>

                        {msg.citations && msg.citations.length > 0 && (
                          <div className="mt-2 space-y-1">
                            <div className="text-[10px] text-[#94a3c0] font-medium mb-1">Sources:</div>
                            {msg.citations.map((c, idx) => (
                              <div key={idx} className="flex items-start gap-1.5 text-[10px] text-gray-400 p-1.5 rounded bg-white/5 border border-white/5">
                                <FileText className="w-3 h-3 mt-0.5 shrink-0" />
                                <span className="line-clamp-2">{c}</span>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}

                    {msg.role === "user" && (
                      <div className="flex items-center gap-3">
                        <span
                          className="text-[9px]"
                          style={{
                            color: "rgba(255,255,255,0.6)",
                          }}
                        >
                          {new Date(msg.timestamp).toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} className="h-2" />
        </div>

        {/* ── Chat Input ── */}
        <div
          className="p-4 shrink-0"
          style={{
            background: "rgba(10,15,30,0.95)",
            borderTop: "1px solid rgba(255,255,255,0.06)",
            backdropFilter: "blur(12px)",
          }}
        >
          <div className="max-w-4xl mx-auto relative">
            <textarea
              ref={textareaRef}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask CrimeSphere AI about cases, suspects, or patterns..."
              className="w-full bg-transparent text-sm text-white placeholder-gray-500 rounded-xl px-4 py-3.5 pr-12 resize-none focus:outline-none scrollbar-hide"
              style={{
                background: "rgba(255,255,255,0.03)",
                border: "1px solid rgba(255,255,255,0.1)",
                boxShadow: "inset 0 2px 4px rgba(0,0,0,0.2)",
              }}
            />
            <button
              onClick={() => handleSend()}
              disabled={!input.trim() || isTyping}
              className="absolute right-2 bottom-2 w-8 h-8 rounded-lg flex items-center justify-center transition-all disabled:opacity-50"
              style={{
                background:
                  input.trim() && !isTyping
                    ? "linear-gradient(135deg, #0070f3, #bf5af2)"
                    : "rgba(255,255,255,0.05)",
                color: input.trim() && !isTyping ? "white" : "#526080",
              }}
            >
              <Send className="w-4 h-4 ml-0.5" />
            </button>
          </div>
          <p className="text-center text-[10px] mt-3" style={{ color: "#526080" }}>
            CrimeSphere AI can make mistakes. Always verify critical investigation
            details against official records.
          </p>
        </div>
      </div>
    </div>
  );
}
