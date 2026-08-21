import axios from "axios";

const API_BASE_URL = "/api";

// Эндпоинты публичного каталога — токен им не нужен даже если он есть в localStorage
const PUBLIC_ENDPOINTS = ["/products", "/categories", "/exchange-rate"];

const isPublicEndpoint = (url = "") => {
  // Проверяем если это GET запрос к публичным эндпоинтам
  // Админские действия (create, update, delete) должны всегда передавать токен
  return PUBLIC_ENDPOINTS.some((path) => url?.includes(path));
};

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  // Всегда отправляем токен, если он есть, особенно для POST/PATCH/DELETE
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    // Убеждаемся что токен передаётся даже при multipart/form-data
    if (config.data instanceof FormData) {
      delete config.headers["Content-Type"];
    }
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");

      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
            refresh: refreshToken,
          });

          localStorage.setItem("access_token", response.data.access);
          api.defaults.headers.common.Authorization = `Bearer ${response.data.access}`;
          originalRequest.headers.Authorization = `Bearer ${response.data.access}`;

          return api(originalRequest);
        } catch (err) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");

          // Редиректим на /admin/login только если пользователь и так был в админке
          if (window.location.pathname.startsWith("/admin")) {
            window.location.href = "/admin/login";
          }
        }
      }
    }

    return Promise.reject(error);
  },
);

export default api;
