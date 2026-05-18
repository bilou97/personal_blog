import { defineStore } from "pinia";
import { computed, ref } from "vue";
import api from "../api";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token"));
  const username = ref(localStorage.getItem("username") || "");

  const isLoggedIn = computed(() => !!token.value);

  async function login(credentials) {
    const { data } = await api.post("/auth/login", credentials);
    token.value = data.access_token;
    localStorage.setItem("token", data.access_token);
  }

  async function register(userData) {
    const { data } = await api.post("/auth/register", userData);
    token.value = data.access_token;
    localStorage.setItem("token", data.access_token);
  }

  function logout() {
    token.value = null;
    username.value = "";
    localStorage.removeItem("token");
    localStorage.removeItem("username");
  }

  return { token, username, isLoggedIn, login, register, logout };
});
