import api from "@/lib/api";

export interface LoginPayload {
  employee_id: string;
  password: string;
  department: string;
}

export interface AuthUser {
  user_id: string;
  employee_id: string;
  name: string;
  email: string;
  department: string;
  role: string;
  is_active: boolean;
}

export async function login(payload: LoginPayload) {
  const { data } = await api.post<{ access_token: string }>("/auth/login", payload);
  return data;
}

export async function currentUser() {
  const { data } = await api.get<AuthUser>("/auth/me");
  return data;
}
