<template>
  <div>
    <h1 class="text-3xl font-bold mb-8">Articles</h1>
    <p v-if="loading" class="text-gray-500 dark:text-gray-400">Chargement...</p>
    <p v-else-if="!posts.length" class="text-gray-500 dark:text-gray-400">Aucun article pour l'instant.</p>
    <div class="space-y-8">
      <article v-for="post in posts" :key="post.id" class="border-b border-gray-200 dark:border-gray-800 pb-8">
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
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { RouterLink } from "vue-router";
import api from "../api";

const posts = ref([]);
const loading = ref(true);

onMounted(async () => {
  const { data } = await api.get("/posts");
  posts.value = data;
  loading.value = false;
});

function formatDate(date) {
  return new Date(date).toLocaleDateString("fr-CH");
}
</script>
