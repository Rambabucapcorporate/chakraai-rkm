// src/lib/api.ts

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/** Chat stream timeout — 5 min default; increase for peak load / queue wait */
export const CHAT_TIMEOUT_MS =
  Number(import.meta.env.VITE_CHAT_TIMEOUT_MS) || 5 * 60 * 1000;

// Helper for making fetch requests with Auth header if needed
async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = localStorage.getItem("access_token");
  const headers = new Headers(options.headers || {});

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  
  if (!headers.has("Content-Type") && !(options.body instanceof FormData)) {
      headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "API request failed");
  }

  return response.json();
}

export const api = {
  auth: {
    login: async (credentials: any) => {
      // Fastapi expects JSON according to our Pydantic setup
      const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Login failed");
      }
      return res.json();
    },
    register: async (userData: any) => {
      const res = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || "Registration failed");
      }
      return res.json();
    },
    getMe: () => fetchWithAuth("/api/auth/me"),
  },
  admin: {
    stats: () => fetchWithAuth("/api/admin/stats"),
    gpu: () => fetchWithAuth("/api/admin/gpu"),
    users: (qs = "") => fetchWithAuth(`/api/admin/users${qs}`),
    chats: (qs = "") => fetchWithAuth(`/api/admin/chats${qs}`),
    activity: (qs = "") => fetchWithAuth(`/api/admin/activity${qs}`),
  },
};
