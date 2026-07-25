import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("token");
      window.location.href = "/auth";
    }
    return Promise.reject(error);
  }
);

export default api;

// ---- Auth ----
export const authAPI = {
  register: (data: { email: string; password: string; full_name: string; organization?: string }) =>
    api.post("/auth/register", data),
  login: (data: { email: string; password: string }) => api.post("/auth/login", data),
  me: () => api.get("/auth/me"),
};

// ---- Deals ----
export const dealsAPI = {
  list: (params?: { status?: string; skip?: number; limit?: number }) =>
    api.get("/deals/", { params }),
  get: (id: string) => api.get(`/deals/${id}`),
  create: (data: { name: string; industry?: string; stage?: string; [key: string]: any }) =>
    api.post("/deals/", data),
  update: (id: string, data: Record<string, any>) => api.patch(`/deals/${id}`, data),
  delete: (id: string) => api.delete(`/deals/${id}`),
};

// ---- Documents ----
export const documentsAPI = {
  upload: (dealId: string, file: File, category: string) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("document_category", category);
    return api.post(`/documents/upload/${dealId}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  list: (dealId: string) => api.get(`/documents/deal/${dealId}`),
  delete: (id: string) => api.delete(`/documents/${id}`),
};

// ---- Analysis ----
export const analysisAPI = {
  trigger: (dealId: string, agentTypes?: string[]) =>
    api.post("/analysis/trigger", { deal_id: dealId, agent_types: agentTypes }),
  list: (dealId: string) => api.get(`/analysis/deal/${dealId}`),
  get: (id: string) => api.get(`/analysis/${id}`),
};

// ---- Reports ----
export const reportsAPI = {
  generate: (dealId: string) => api.post(`/reports/generate/${dealId}`),
  list: (dealId: string) => api.get(`/reports/deal/${dealId}`),
};

// ---- Dashboard ----
export const dashboardAPI = {
  stats: () => api.get("/dashboard/stats"),
  pipeline: () => api.get("/dashboard/pipeline"),
};
