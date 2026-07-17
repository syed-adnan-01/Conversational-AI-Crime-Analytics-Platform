import { redirect } from "next/navigation";

// Root page — always redirects to /login
export default function Home() {
  redirect("/login");
}
