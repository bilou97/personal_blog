<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Recherche</h1>

    <form @submit.prevent="submitSearch" class="flex gap-2 mb-8">
      <input
        ref="inputEl"
        v-model="localQ"
        type="search"
        placeholder="Rechercher dans les articles…"
        class="flex-1 px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-400 text-sm transition-colors"
        autofocus
      />
      <button
        type="submit"
        class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium transition-colors"
      >
        Rechercher
      </button>
    </form>

    <template v-if="q">
      <p v-if="!loading" class="text-sm text-gray-500 dark:text-gray-400 mb-6">
        <template v-if="total">
          {{ total }} résultat{{ total > 1 ? "s" : "" }} pour
          <strong>«&nbsp;{{ q }}&nbsp;»</strong>
        </template>
        <template v-else>
          Aucun résultat pour <strong>«&nbsp;{{ q }}&nbsp;»</strong>
        </template>
      </p>

      <div class="space-y-8">
        <template v-if="loading">
          <div
            v-for="n in 3"
            :key="n"
            class="border-b border-gray-200 dark:border-gray-800 pb-8 animate-pulse"
          >
            <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded w-2/3 mb-3"></div>
            <div class="flex gap-3 mb-3">
              <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
              <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24"></div>
            </div>
            <div class="space-y-2">
              <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
              <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
            </div>
          </div>
        </template>

        <article
          v-else
          v-for="(post, index) in posts"
          :key="post.id"
          v-reveal="{ delay: index * 60 }"
          class="border-b border-gray-200 dark:border-gray-800 pb-8"
        >
          <RouterLink :to="`/post/${post.slug}`" class="group block mb-2">
            <h2
              class="text-xl font-semibold group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors"
            >
              {{ post.title }}
            </h2>
          </RouterLink>
          <div
            class="flex items-center gap-3 mb-3 text-sm text-gray-500 dark:text-gray-400"
          >
            <span
              v-if="post.category"
              class="bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded text-xs font-medium"
            >
              {{ post.category.name }}
            </span>
            <time v-if="post.published_at">{{ formatDate(post.published_at) }}</time>
          </div>
          <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
            {{ post.excerpt }}
          </p>
        </article>
      </div>

      <nav v-if="totalPages > 1" class="flex items-center justify-center gap-1 mt-12">
        <button
          @click="goTo(page - 1)"
          :disabled="page === 1"
          class="px-3 py-1.5 rounded-lg text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          ← Précédent
        </button>

        <template v-for="p in pageRange" :key="p">
          <span
            v-if="p === '…'"
            class="px-2 text-gray-400 dark:text-gray-500 select-none"
            >…</span
          >
          <button
            v-else
            @click="goTo(p)"
            :class="[
              'w-8 h-8 rounded-lg text-sm font-medium transition-colors',
              p === page
                ? 'bg-indigo-600 text-white'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800',
            ]"
          >
            {{ p }}
          </button>
        </template>

        <button
          @click="goTo(page + 1)"
          :disabled="page === totalPages"
          class="px-3 py-1.5 rounded-lg text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          Suivant →
        </button>
      </nav>
    </template>

    <p v-else class="text-sm text-gray-500 dark:text-gray-400">
      Saisissez un terme pour rechercher dans les articles.
    </p>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import { useHead } from "../composables/useHead";
import api from "../api";

useHead({ title: "Recherche — papobilou" });

const route = useRoute();
const router = useRouter();

const posts = ref([]);
const loading = ref(false);
const total = ref(0);
const pageSize = 10;

const q = computed(() => route.query.q ?? "");
const page = computed(() => Number(route.query.page) || 1);
const localQ = ref(q.value);
const totalPages = computed(() => Math.ceil(total.value / pageSize));

const pageRange = computed(() => {
  const n = totalPages.value;
  const cur = page.value;
  if (n <= 7) return Array.from({ length: n }, (_, i) => i + 1);
  const pages = new Set([1, n, cur, cur - 1, cur + 1].filter((p) => p >= 1 && p <= n));
  const sorted = [...pages].sort((a, b) => a - b);
  const result = [];
  for (let i = 0; i < sorted.length; i++) {
    if (i > 0 && sorted[i] - sorted[i - 1] > 1) result.push("…");
    result.push(sorted[i]);
  }
  return result;
});

async function fetchResults() {
  if (!q.value) {
    posts.value = [];
    total.value = 0;
    return;
  }
  loading.value = true;
  try {
    const { data } = await api.get("/search", {
      params: { q: q.value, page: page.value, page_size: pageSize },
    });
    posts.value = data.results;
    total.value = data.total;
  } finally {
    loading.value = false;
  }
}

function submitSearch() {
  if (!localQ.value.trim()) return;
  router.push({ path: "/search", query: { q: localQ.value.trim() } });
}

function goTo(p) {
  router.push({ query: { ...route.query, page: p } });
}

function formatDate(date) {
  return new Date(date).toLocaleDateString("fr-CH");
}

watch(() => [q.value, page.value], fetchResults, { immediate: true });
watch(q, (val) => { localQ.value = val; });
</script>
