import axios from "axios";
import router from "./router";
import { useAuthStore } from "./stores/auth";
import { useNotificationsStore } from "./stores/notifications";

const api = axios.create({ baseURL: "/api" });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error.response?.status;
    const notifications = useNotificationsStore();
    const auth = useAuthStore();

    if (status === 401 && !error.config._retry) {
      const isRefreshEndpoint = error.config.url.includes("/auth/refresh");
      const refreshToken = localStorage.getItem("refresh_token");

      if (!isRefreshEndpoint && refreshToken) {
        error.config._retry = true;
        try {
          const { data } = await api.post("/auth/refresh", {
            refresh_token: refreshToken,
          });
          auth.setTokens(data.access_token, data.refresh_token);
          error.config.headers.Authorization = `Bearer ${data.access_token}`;
          return api(error.config);
        } catch {
          // refresh failed — déconnexion
        }
      }

      auth.logout();
      const path = router.currentRoute.value.path;
      if (path !== "/login" && path !== "/register") {
        router.push("/login");
      }
    } else if (status >= 500) {
      notifications.add("Erreur serveur, veuillez réessayer.");
    } else if (!error.response) {
      notifications.add("Impossible de contacter le serveur.");
    }

    return Promise.reject(error);
  }
);

export default api;
