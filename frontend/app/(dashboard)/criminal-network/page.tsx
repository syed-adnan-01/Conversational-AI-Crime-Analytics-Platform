import type { Metadata } from "next";
import NetworkGraph from "@/components/criminal-network/NetworkGraph";

export const metadata: Metadata = {
  title: "Criminal Network",
};

export default function CriminalNetworkPage() {
  return <NetworkGraph />;
}
