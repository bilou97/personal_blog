<template>
  <div class="min-h-screen bg-white dark:bg-gray-950 text-gray-800 dark:text-gray-100 transition-colors duration-200">
    <nav class="sticky top-0 z-10 border-b border-gray-200 dark:border-gray-800 bg-white/90 dark:bg-gray-950/90 backdrop-blur">
      <div class="max-w-3xl mx-auto px-4 h-14 flex items-center justify-between">
        <RouterLink to="/" class="font-semibold text-lg tracking-tight hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
          papobilou
        </RouterLink>
        <div class="flex items-center gap-4 text-sm">
          <template v-if="auth.isLoggedIn">
            <span class="text-gray-500 dark:text-gray-400">{{ auth.username }}</span>
            <button @click="auth.logout" class="text-gray-600 dark:text-gray-300 hover:text-red-500 dark:hover:text-red-400 transition-colors">
              Déconnexion
            </button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              Connexion
            </RouterLink>
            <RouterLink to="/register" class="text-gray-600 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors">
              Inscription
            </RouterLink>
          </template>
          <button
            @click="toggleDark"
            :title="dark ? 'Mode clair' : 'Mode sombre'"
            class="ml-1 p-1.5 rounded-md text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <svg v-if="dark" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
        </div>
      </div>

      <div
        v-if="route.path === '/' && (categories.length || tags.length)"
        class="max-w-3xl mx-auto px-4 pb-2 flex flex-wrap gap-1.5 text-xs"
      >
        <RouterLink
          to="/"
          :class="filterChipClass(!activeCategory && !activeTag)"
        >
          Tous
        </RouterLink>

        <template v-if="categories.length">
          <span class="text-gray-300 dark:text-gray-700 select-none">|</span>
          <RouterLink
            v-for="cat in categories"
            :key="cat.slug"
            :to="{ path: '/', query: { category: cat.slug } }"
            :class="filterChipClass(activeCategory === cat.slug)"
          >
            {{ cat.name }}
          </RouterLink>
        </template>

        <template v-if="tags.length">
          <span class="text-gray-300 dark:text-gray-700 select-none">|</span>
          <RouterLink
            v-for="tag in tags"
            :key="tag.slug"
            :to="{ path: '/', query: { tag: tag.slug } }"
            :class="filterChipClass(activeTag === tag.slug)"
          >
            #{{ tag.name }}
          </RouterLink>
        </template>
      </div>
    </nav>

    <main class="max-w-3xl mx-auto px-4 py-10">
      <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" :key="$route.fullPath" />
        </Transition>
      </RouterView>
    </main>
    <ToastNotification />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { RouterLink, RouterView, useRoute } from "vue-router";
import { useAuthStore } from "./stores/auth";
import ToastNotification from "./components/ToastNotification.vue";
import api from "./api";

const auth = useAuthStore();
const route = useRoute();
const dark = ref(false);
const categories = ref([]);
const tags = ref([]);

const activeCategory = computed(() => route.query.category ?? null);
const activeTag = computed(() => route.query.tag ?? null);

function filterChipClass(active) {
  return [
    "px-2.5 py-1 rounded-full font-medium transition-colors",
    active
      ? "bg-indigo-600 text-white"
      : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700",
  ];
}

onMounted(async () => {
  dark.value = localStorage.getItem("dark") === "true";
  applyDark();
  const [catsRes, tagsRes] = await Promise.all([
    api.get("/posts/categories"),
    api.get("/posts/tags"),
  ]);
  categories.value = catsRes.data;
  tags.value = tagsRes.data;
});

function toggleDark() {
  dark.value = !dark.value;
  localStorage.setItem("dark", String(dark.value));
  applyDark();
}

function applyDark() {
  document.documentElement.classList.toggle("dark", dark.value);
}
</script>
