import type { Metadata } from "next";
import FIRSearchInterface from "@/components/fir-search/FIRSearchInterface";

export const metadata: Metadata = {
  title: "FIR Search",
};

export default function FIRSearchPage() {
  return <FIRSearchInterface />;
}
