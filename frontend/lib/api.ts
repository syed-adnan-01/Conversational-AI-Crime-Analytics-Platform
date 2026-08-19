import axios from "axios";

const TOKEN_STORAGE_KEY = "crimesphere.access_token";
const API_URL_STORAGE_KEY = "crimesphere.api_url";
const DEFAULT_CATALYST_BACKEND = "https://crimesphere-backend-60077232301.development.catalystserverless.com";

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status?: number,
    public readonly details?: unknown,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Dynamically resolves the API base URL based on runtime environment.
 * If running on live hosting (Zoho Slate, Zoho Catalyst, etc.), avoids falling back to localhost.
 */
export function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    // 1. Check for manual override in localStorage
    const storedUrl = window.localStorage.getItem(API_URL_STORAGE_KEY);
    if (storedUrl && storedUrl.trim()) {
      return storedUrl.trim().replace(/\/$/, "");
    }

    const hostname = window.location.hostname;
    const isLocalhost = hostname === "localhost" || hostname === "127.0.0.1";

    const envUrl = (process.env.NEXT_PUBLIC_API_URL || "").trim().replace(/\/$/, "");

    // 2. If running live (not localhost), force live backend URL if env is localhost or relative
    if (!isLocalhost) {
      if (!envUrl || envUrl.includes("localhost") || envUrl.includes("127.0.0.1")) {
        return DEFAULT_CATALYST_BACKEND;
      }
      return envUrl;
    }

    if (envUrl) return envUrl;
  }

  return (process.env.NEXT_PUBLIC_API_URL || "").trim().replace(/\/$/, "") || "http://localhost:8000";
}

/** Shared HTTP client for CrimeSphere backend requests. */
const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 15_000,
});

api.interceptors.request.use((config) => {
  // Ensure baseURL is dynamically evaluated at request time
  config.baseURL = getApiBaseUrl();

  if (typeof window !== "undefined") {
    const token = window.localStorage.getItem(TOKEN_STORAGE_KEY);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (!axios.isAxiosError(error)) {
      return Promise.reject(new ApiError("An unexpected error occurred."));
    }

    const status = error.response?.status;
    const body = error.response?.data as { detail?: unknown; message?: string } | undefined;
    const detail = body?.detail ?? body?.message;
    const message =
      status === 401 ? "Your session has expired. Please sign in again."
      : status === 403 ? "You do not have permission to perform this action."
      : status === 404 ? "The requested resource was not found."
      : status === 422 ? "Please correct the highlighted information and try again."
      : status && status >= 500 ? "The service is temporarily unavailable. Please try again."
      : error.code === "ECONNABORTED" ? "The request timed out. Please try again."
      : "Unable to connect to CrimeSphere. Check your network connection.";

    if (status === 401 && typeof window !== "undefined") {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY);
    }
    return Promise.reject(new ApiError(typeof detail === "string" ? detail : message, status, detail));
  },
);

export { TOKEN_STORAGE_KEY, API_URL_STORAGE_KEY };
export default api;

