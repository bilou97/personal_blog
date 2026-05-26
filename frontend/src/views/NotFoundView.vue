<template>
  <div class="text-center py-24">
    <p class="text-7xl font-bold text-gray-200 dark:text-gray-800 mb-6 select-none">404</p>
    <h1 class="text-2xl font-semibold mb-3">Page introuvable</h1>
    <p class="text-gray-500 dark:text-gray-400 mb-8">Cette page n'existe pas ou a été déplacée.</p>
    <RouterLink
      to="/"
      class="inline-block px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors"
    >
      Retour à l'accueil
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useHead } from "../composables/useHead";

useHead({ title: "404 — Page introuvable | papobilou" });
</script>
