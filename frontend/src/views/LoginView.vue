<template>
  <div>
    <h1>Connexion</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="form.username" placeholder="Nom d'utilisateur" required />
      <input v-model="form.password" type="password" placeholder="Mot de passe" required />
      <p v-if="error">{{ error }}</p>
      <button type="submit">Se connecter</button>
    </form>
    <RouterLink to="/register">Pas encore de compte ?</RouterLink>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const auth = useAuthStore();
const form = ref({ username: "", password: "" });
const error = ref("");

async function handleLogin() {
  error.value = "";
  try {
    await auth.login(form.value);
    router.push("/");
  } catch {
    error.value = "Identifiants incorrects.";
  }
}
</script>
