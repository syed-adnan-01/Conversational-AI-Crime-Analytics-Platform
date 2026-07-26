"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { ApiError, TOKEN_STORAGE_KEY } from "@/lib/api";
import { currentUser, login as loginRequest, type AuthUser, type LoginPayload } from "@/lib/services/auth";

type AuthContextValue = {
  user: AuthUser | null;
  loading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (!token) {
      Promise.resolve().then(() => setLoading(false));
      return;
    }
    currentUser().then(setUser).catch(() => localStorage.removeItem(TOKEN_STORAGE_KEY)).finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (payload: LoginPayload) => {
    const { access_token } = await loginRequest(payload);
    localStorage.setItem(TOKEN_STORAGE_KEY, access_token);
    setUser(await currentUser());
  }, []);
  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    setUser(null);
  }, []);

  return <AuthContext.Provider value={{ user, loading, login, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used within AuthProvider");
  return value;
}

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  useEffect(() => {
    if (!loading && !user) router.replace(`/login?next=${encodeURIComponent(pathname)}`);
  }, [loading, pathname, router, user]);
  if (loading || !user) return <div className="min-h-screen" style={{ background: "#080b12" }} />;
  return <>{children}</>;
}

export function authErrorMessage(error: unknown) {
  return error instanceof ApiError ? error.message : "Unable to sign in. Please try again.";
}
