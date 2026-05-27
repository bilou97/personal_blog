<template>
  <div class="py-16 text-center">
    <p v-if="loading" class="text-gray-500 dark:text-gray-400">
      Traitement en cours…
    </p>
    <template v-else-if="success">
      <p class="text-lg font-semibold mb-2">Vous êtes désabonné(e).</p>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
        Vous ne recevrez plus d'emails de papobilou.
      </p>
      <RouterLink
        to="/"
        class="text-indigo-600 dark:text-indigo-400 hover:underline text-sm"
      >
        ← Retour à l'accueil
      </RouterLink>
    </template>
    <template v-else>
      <p class="text-red-500 dark:text-red-400 mb-4">
        Lien invalide ou déjà utilisé.
      </p>
      <RouterLink
        to="/"
        class="text-indigo-600 dark:text-indigo-400 hover:underline text-sm"
      >
        ← Retour à l'accueil
      </RouterLink>
    </template>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { useHead } from "../composables/useHead";
import api from "../api";

useHead({ title: "Désabonnement — papobilou" });

const route = useRoute();
const loading = ref(true);
const success = ref(false);

onMounted(async () => {
  try {
    await api.get("/newsletter/unsubscribe", {
      params: { token: route.query.token },
    });
    success.value = true;
  } catch {
    success.value = false;
  } finally {
    loading.value = false;
  }
});
</script>
