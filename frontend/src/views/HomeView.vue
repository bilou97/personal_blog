<template>
  <div>
    <h1 class="text-3xl font-bold mb-8">Articles</h1>
    <p v-if="!loading && !posts.length" class="text-gray-500 dark:text-gray-400">Aucun article pour l'instant.</p>

    <div class="space-y-8">
      <!-- Skeleton loaders -->
      <template v-if="loading">
        <div
          v-for="n in 5"
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
            <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-4/6"></div>
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
          <h2 class="text-xl font-semibold group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
            {{ post.title }}
          </h2>
        </RouterLink>
        <div class="flex items-center gap-3 mb-3 text-sm text-gray-500 dark:text-gray-400">
          <span v-if="post.category" class="bg-gray-100 dark:bg-gray-800 px-2 py-0.5 rounded text-xs font-medium">
            {{ post.category.name }}
          </span>
          <time v-if="post.published_at">{{ formatDate(post.published_at) }}</time>
        </div>
        <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">{{ post.excerpt }}</p>
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
        <span v-if="p === '…'" class="px-2 text-gray-400 dark:text-gray-500 select-none">…</span>
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

    <SubscribeForm />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { RouterLink, useRoute, useRouter } from "vue-router";
import SubscribeForm from "../components/SubscribeForm.vue";
import { useHead } from "../composables/useHead";
import api from "../api";

useHead({
  title: "papobilou",
  meta: [{ name: "description", content: "Le blog de papobilou — articles, tutoriels et pensées." }],
});

const route = useRoute();
const router = useRouter();

const posts = ref([]);
const loading = ref(true);
const total = ref(0);
const pageSize = 10;

const page = computed(() => Number(route.query.page) || 1);
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

async function fetchPosts() {
  loading.value = true;
  const params = { page: page.value, page_size: pageSize };
  if (route.query.category) params.category = route.query.category;
  if (route.query.tag) params.tag = route.query.tag;
  const { data } = await api.get("/posts", { params });
  posts.value = data.results;
  total.value = data.total;
  loading.value = false;
}

function goTo(p) {
  router.push({ query: { ...route.query, page: p } });
}

onMounted(fetchPosts);
watch(() => [route.query.page, route.query.category, route.query.tag], fetchPosts);

function formatDate(date) {
  return new Date(date).toLocaleDateString("fr-CH");
}
</script>
