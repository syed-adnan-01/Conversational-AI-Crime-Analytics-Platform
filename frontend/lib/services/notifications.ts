import api from "@/lib/api";

export interface NotificationResponse {
  id: string;
  title: string;
  message: string;
  type: string;
  priority: string;
  read: boolean;
  timestamp: string;
  action_url?: string;
  action_label?: string;
  metadata?: Record<string, unknown>;
}

export interface NotificationCountResponse {
  total: number;
  unread: number;
}

export const notificationsService = {
  getNotifications: (): Promise<NotificationResponse[]> =>
    api.get<NotificationResponse[]>("/notifications").then((res) => res.data),

  getUnreadNotifications: (): Promise<NotificationResponse[]> =>
    api.get<NotificationResponse[]>("/notifications/unread").then((res) => res.data),

  markRead: (id: string): Promise<NotificationResponse> =>
    api.post<NotificationResponse>(`/notifications/read/${id}`).then((res) => res.data),

  markAllRead: (): Promise<{ count: number }> =>
    api.post<{ count: number }>("/notifications/read-all").then((res) => res.data),

  deleteNotification: (id: string): Promise<{ success: boolean }> =>
    api.delete<{ success: boolean }>(`/notifications/${id}`).then((res) => res.data),

  getCount: (): Promise<NotificationCountResponse> =>
    api.get<NotificationCountResponse>("/notifications/count").then((res) => res.data),
};
