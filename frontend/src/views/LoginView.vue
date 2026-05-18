<template>
  <div class="max-w-sm mx-auto">
    <h1 class="text-2xl font-bold mb-6">Connexion</h1>
    <form @submit.prevent="handleLogin" class="space-y-4">
      <input
        v-model="form.username"
        placeholder="Nom d'utilisateur"
        required
        class="w-full rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400"
      />
      <input
        v-model="form.password"
        type="password"
        placeholder="Mot de passe"
        required
        class="w-full rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400"
      />
      <p v-if="error" class="text-red-500 dark:text-red-400 text-sm">{{ error }}</p>
      <button
        type="submit"
        class="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors"
      >
        Se connecter
      </button>
    </form>
    <p class="mt-4 text-sm text-gray-500 dark:text-gray-400">
      Pas encore de compte ?
      <RouterLink to="/register" class="text-indigo-600 dark:text-indigo-400 hover:underline">S'inscrire</RouterLink>
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useHead } from "../composables/useHead";
import { useAuthStore } from "../stores/auth";

useHead({ title: "Connexion | papobilou" });

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
