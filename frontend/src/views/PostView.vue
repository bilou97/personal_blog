<template>
  <div v-if="post">
    <h1>{{ post.title }}</h1>
    <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" />
    <div v-html="post.content"></div>

    <section>
      <h2>Commentaires ({{ post.comments.length }})</h2>
      <div v-for="comment in post.comments" :key="comment.id">
        <strong>{{ comment.author.username }}</strong>
        <time>{{ formatDate(comment.created_at) }}</time>
        <p>{{ comment.content }}</p>
      </div>

      <form v-if="auth.isLoggedIn" @submit.prevent="submitComment">
        <textarea v-model="newComment" placeholder="Votre commentaire..." required></textarea>
        <button type="submit" :disabled="submitting">Publier</button>
      </form>
      <p v-else>
        <RouterLink to="/login">Connectez-vous</RouterLink> pour laisser un commentaire.
      </p>
    </section>
  </div>
  <p v-else-if="loading">Chargement...</p>
  <p v-else>Article introuvable.</p>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import api from "../api";
import { useAuthStore } from "../stores/auth";

const route = useRoute();
const auth = useAuthStore();
const post = ref(null);
const loading = ref(true);
const newComment = ref("");
const submitting = ref(false);

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
