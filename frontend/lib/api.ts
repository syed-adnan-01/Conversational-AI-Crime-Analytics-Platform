import axios from "axios";

const TOKEN_STORAGE_KEY = "crimesphere.access_token";

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

/** Shared HTTP client for CrimeSphere backend requests. */
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 15_000,
});

api.interceptors.request.use((config) => {
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

export { TOKEN_STORAGE_KEY };
export default api;
