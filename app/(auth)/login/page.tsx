import type { Metadata } from "next";
import LoginForm from "@/components/auth/LoginForm";

export const metadata: Metadata = {
  title: "Secure Login",
  description:
    "Authenticate to access the CrimeSphere AI Crime Intelligence Platform. Authorized personnel only.",
};

export default function LoginPage() {
  return <LoginForm />;
}
