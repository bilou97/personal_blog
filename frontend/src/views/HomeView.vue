<template>
  <div>
    <h1>Articles</h1>
    <p v-if="loading">Chargement...</p>
    <p v-else-if="!posts.length">Aucun article pour l'instant.</p>
    <article v-for="post in posts" :key="post.id">
      <RouterLink :to="`/post/${post.slug}`">
        <h2>{{ post.title }}</h2>
      </RouterLink>
      <p v-if="post.category">{{ post.category.name }}</p>
      <p>{{ post.excerpt }}</p>
      <time v-if="post.published_at">{{ formatDate(post.published_at) }}</time>
    </article>
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
