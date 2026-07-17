import type { Metadata } from "next";
import InvestigationWorkspace from "@/components/investigation/InvestigationWorkspace";

export const metadata: Metadata = {
  title: "Investigation Workspace",
};

export default function InvestigationPage() {
  return <InvestigationWorkspace />;
}
