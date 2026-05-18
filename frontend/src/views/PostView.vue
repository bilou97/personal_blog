<template>
  <article v-if="post">
    <img
      v-if="post.cover_image"
      :src="post.cover_image"
      :alt="post.title"
      class="w-full rounded-lg mb-8 object-cover max-h-72"
    />
    <h1 class="text-3xl font-bold mb-2">{{ post.title }}</h1>
    <time v-if="post.published_at" class="text-sm text-gray-500 dark:text-gray-400 block mb-8">
      {{ formatDate(post.published_at) }}
    </time>

    <div class="prose dark:prose-invert max-w-none mb-12" v-html="renderedContent"></div>

    <section class="border-t border-gray-200 dark:border-gray-800 pt-8">
      <h2 class="text-xl font-semibold mb-6">Commentaires ({{ post.comments.length }})</h2>

      <div v-if="post.comments.length" class="space-y-4 mb-8">
        <div
          v-for="comment in post.comments"
          :key="comment.id"
          class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4"
        >
          <div class="flex items-center gap-2 mb-2">
            <strong class="text-sm font-semibold">{{ comment.author.username }}</strong>
            <time class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(comment.created_at) }}</time>
          </div>
          <p class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{{ comment.content }}</p>
        </div>
      </div>
      <p v-else class="text-sm text-gray-500 dark:text-gray-400 mb-8">Aucun commentaire.</p>

      <form v-if="auth.isLoggedIn" @submit.prevent="submitComment" class="space-y-3">
        <textarea
          v-model="newComment"
          placeholder="Votre commentaire..."
          required
          rows="4"
          class="w-full rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 resize-none"
        ></textarea>
        <button
          type="submit"
          :disabled="submitting"
          class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
        >
          Publier
        </button>
      </form>
      <p v-else class="text-sm text-gray-500 dark:text-gray-400">
        <RouterLink to="/login" class="text-indigo-600 dark:text-indigo-400 hover:underline">Connectez-vous</RouterLink>
        pour laisser un commentaire.
      </p>
    </section>
  </article>
  <p v-else-if="loading" class="text-gray-500 dark:text-gray-400">Chargement...</p>
  <p v-else class="text-gray-500 dark:text-gray-400">Article introuvable.</p>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { marked } from "marked";
import DOMPurify from "dompurify";
import { RouterLink, useRoute } from "vue-router";
import { useHead } from "../composables/useHead";
import api from "../api";
import { useAuthStore } from "../stores/auth";

const route = useRoute();
const auth = useAuthStore();
const post = ref(null);
const loading = ref(true);
const newComment = ref("");
const submitting = ref(false);

const renderedContent = computed(() =>
  post.value ? DOMPurify.sanitize(marked.parse(post.value.content)) : ""
);

useHead({
  title: computed(() => post.value ? `${post.value.title} | papobilou` : "papobilou"),
  meta: computed(() => [
    { name: "description", content: post.value?.excerpt ?? "" },
    { property: "og:title", content: post.value?.title ?? "" },
    { property: "og:description", content: post.value?.excerpt ?? "" },
    { property: "og:type", content: "article" },
    ...(post.value?.cover_image ? [{ property: "og:image", content: post.value.cover_image }] : []),
  ]),
});

onMounted(async () => {
  try {
    const { data } = await api.get(`/posts/${route.params.slug}`);
    post.value = data;
  } finally {
    loading.value = false;
  }
});

async function submitComment() {
  submitting.value = true;
  try {
    const { data } = await api.post(`/posts/${route.params.slug}/comments`, {
      content: newComment.value,
    });
    post.value.comments.push(data);
    newComment.value = "";
  } finally {
    submitting.value = false;
  }
}

function formatDate(date) {
  return new Date(date).toLocaleDateString("fr-CH");
}
</script>
