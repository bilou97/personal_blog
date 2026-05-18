<template>
  <div>
    <h1>Inscription</h1>
    <form @submit.prevent="handleRegister">
      <input v-model="form.username" placeholder="Nom d'utilisateur" required />
      <input v-model="form.email" type="email" placeholder="Email" required />
      <input v-model="form.password" type="password" placeholder="Mot de passe" required />
      <p v-if="error">{{ error }}</p>
      <button type="submit">S'inscrire</button>
    </form>
    <RouterLink to="/login">Déjà un compte ?</RouterLink>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const auth = useAuthStore();
const form = ref({ username: "", email: "", password: "" });
const error = ref("");

async function handleRegister() {
  error.value = "";
  try {
    await auth.register(form.value);
    router.push("/");
  } catch (e) {
    error.value = e.response?.data?.detail ?? "Erreur lors de l'inscription.";
  }
}
</script>
