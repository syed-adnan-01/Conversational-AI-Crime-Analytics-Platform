import api from "@/lib/api";

export interface MonthlyTrend {
  period: string;
  cases: number;
}

export const analytics = {
  getMonthlyTrends: (): Promise<MonthlyTrend[]> =>
    api.get("/analytics/monthly").then((res) => res.data),
  getCrimeTypes: (): Promise<Record<string, number>> =>
    api.get("/analytics/crime-types").then((res) => res.data),
  getOfficers: (): Promise<Record<string, number>> =>
    api.get("/analytics/officers").then((res) => res.data),
  getDistricts: (): Promise<Record<string, number>> =>
    api.get("/analytics/districts").then((res) => res.data),
};
