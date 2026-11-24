import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ||
    "https://piki-ora.onrender.com",
  withCredentials: true,
});

let csrfToken = null;

api.interceptors.response.use((response) => {
  if (response.config.url?.includes("/api/accounts/csrf/")) {
    csrfToken = response.data.csrfToken;
  }

  return response;
});

api.interceptors.request.use((config) => {
  const method = config.method?.toLowerCase();

  if (csrfToken && ["post", "put", "patch", "delete"].includes(method)) {
    config.headers.set("X-CSRFToken", csrfToken);
  }

  return config;
});

export default api;