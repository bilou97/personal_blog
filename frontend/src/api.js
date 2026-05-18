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
  (error) => {
    const status = error.response?.status;
    const notifications = useNotificationsStore();

    if (status === 401) {
      const auth = useAuthStore();
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
