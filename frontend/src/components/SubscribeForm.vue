<template>
  <div class="mt-12 border-t border-gray-200 dark:border-gray-800 pt-10">
    <h2 class="text-lg font-semibold mb-1">Newsletter</h2>
    <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
      Recevez un email à chaque nouvel article.
    </p>
    <form v-if="!done" @submit.prevent="submit" class="flex gap-2">
      <input
        v-model="email"
        type="email"
        required
        placeholder="votre@email.ch"
        class="flex-1 px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-colors"
      />
      <button
        type="submit"
        :disabled="loading"
        class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white text-sm font-medium transition-colors"
      >
        S'abonner
      </button>
    </form>
    <p v-else class="text-sm text-green-600 dark:text-green-400 font-medium">
      ✓ Vous êtes abonné(e) — à bientôt !
    </p>
    <p v-if="error" class="mt-2 text-sm text-red-500 dark:text-red-400">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../api";

const email = ref("");
const loading = ref(false);
const done = ref(false);
const error = ref("");

async function submit() {
  loading.value = true;
  error.value = "";
  try {
    await api.post("/newsletter/subscribe", { email: email.value });
    done.value = true;
  } catch (e) {
    const detail = e.response?.data?.detail;
    error.value =
      detail === "Already subscribed"
        ? "Cette adresse est déjà abonnée."
        : "Une erreur est survenue, veuillez réessayer.";
  } finally {
    loading.value = false;
  }
}
</script>
