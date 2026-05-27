import { defineStore } from "pinia";
import { computed, ref } from "vue";
import api from "../api";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token"));
  const username = ref(localStorage.getItem("username") || "");

  const isLoggedIn = computed(() => !!token.value);

  function setTokens(accessToken, refreshToken) {
    token.value = accessToken;
    localStorage.setItem("token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
  }

  async function login(credentials) {
    const { data } = await api.post("/auth/login", credentials);
    setTokens(data.access_token, data.refresh_token);
  }

  async function register(userData) {
    const { data } = await api.post("/auth/register", userData);
    setTokens(data.access_token, data.refresh_token);
  }

  function logout() {
    token.value = null;
    username.value = "";
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("username");
  }

  return { token, username, isLoggedIn, setTokens, login, register, logout };
});
