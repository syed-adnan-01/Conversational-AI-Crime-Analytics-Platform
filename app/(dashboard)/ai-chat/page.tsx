import type { Metadata } from "next";
import ChatInterface from "@/components/ai-chat/ChatInterface";

export const metadata: Metadata = {
  title: "AI Crime Chat",
};

export default function AIChatPage() {
  return <ChatInterface />;
}
