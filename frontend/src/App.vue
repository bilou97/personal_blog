<template>
  <div>
    <nav>
      <RouterLink to="/">Accueil</RouterLink>
      <template v-if="auth.isLoggedIn">
        <span>{{ auth.username }}</span>
        <button @click="auth.logout">Déconnexion</button>
      </template>
      <template v-else>
        <RouterLink to="/login">Connexion</RouterLink>
        <RouterLink to="/register">Inscription</RouterLink>
      </template>
    </nav>
    <main>
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useAuthStore } from "./stores/auth";

const auth = useAuthStore();
</script>
