import api from "@/lib/api";

export interface AdminUserRecord {
  user_id: string;
  employee_id: string;
  name: string;
  email?: string;
  department?: string;
  role?: string;
  status: string;
}

export interface OfficerRecord {
  id: string;
  name: string;
  badge_number: string;
  email?: string;
  role?: string;
  district?: string;
  clearance_level?: number;
  mfa_enabled?: boolean;
  status: string;
  last_login?: string;
}

export interface RoleRecord {
  id?: string;
  name: string;
  clearance_level: number;
  description: string;
  userCount?: number;
  permissions: string[];
}

export interface AuditRecord {
  id: string;
  action: string;
  user_name?: string;
  user_id?: string;
  module: string;
  description: string;
  timestamp: string;
  ip_address: string;
  success: boolean;
}

export const adminService = {
  getUsers: (): Promise<AdminUserRecord[]> =>
    api.get<AdminUserRecord[]>("/admin/users").then((res) => res.data),

  getOfficers: (): Promise<OfficerRecord[]> =>
    api.get<OfficerRecord[]>("/admin/officers").then((res) => res.data),

  getRoles: (): Promise<RoleRecord[]> =>
    api.get<RoleRecord[]>("/admin/roles").then((res) => res.data),

  getDepartments: (): Promise<string[]> =>
    api.get<string[]>("/admin/departments").then((res) => res.data),

  getAudit: (): Promise<AuditRecord[]> =>
    api.get<AuditRecord[]>("/admin/audit").then((res) => res.data),
};
