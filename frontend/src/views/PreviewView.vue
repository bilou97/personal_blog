<template>
  <div>
    <div
      v-if="post"
      class="mb-6 px-4 py-3 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700 text-amber-800 dark:text-amber-300 text-sm flex items-center gap-2"
    >
      <span class="font-semibold">Aperçu brouillon</span>
      <span class="text-amber-600 dark:text-amber-400">— cet article n'est pas encore publié.</span>
    </div>

    <article v-if="post">
      <LazyImage
        v-if="post.cover_image"
        :src="post.cover_image"
        :alt="post.title"
        container-class="rounded-lg mb-8 max-h-72"
        img-class="max-h-72"
      />
      <h1 class="text-3xl font-bold mb-2">{{ post.title }}</h1>
      <div class="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400 mb-8">
        <time v-if="post.published_at">{{ formatDate(post.published_at) }}</time>
        <span v-if="post.published_at && minutes" class="select-none">·</span>
        <span v-if="minutes">{{ minutes }} min de lecture</span>
      </div>

      <nav
        v-if="toc.length"
        class="mb-8 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-800 text-sm"
      >
        <p class="font-semibold mb-2 text-gray-700 dark:text-gray-300">Dans cet article</p>
        <ul class="space-y-1">
          <li v-for="item in toc" :key="item.id" :class="item.depth === 3 ? 'ml-4' : ''">
            <a :href="`#${item.id}`" class="text-indigo-600 dark:text-indigo-400 hover:underline">
              {{ item.text }}
            </a>
          </li>
        </ul>
      </nav>

      <div
        ref="contentRef"
        class="prose dark:prose-invert max-w-none"
        v-html="html"
      ></div>
    </article>

    <div v-else-if="loading" class="animate-pulse">
      <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4"></div>
      <div class="flex gap-3 mb-8">
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24"></div>
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-20"></div>
      </div>
      <div class="space-y-3">
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
      </div>
    </div>

    <div v-else class="text-center py-16">
      <p class="text-gray-500 dark:text-gray-400 mb-2">Aperçu invalide ou expiré.</p>
      <RouterLink to="/" class="text-indigo-600 dark:text-indigo-400 hover:underline text-sm">
        ← Retour à l'accueil
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from "vue";
import { RouterLink, useRoute } from "vue-router";
import LazyImage from "../components/LazyImage.vue";
import { useHead } from "../composables/useHead";
import { parseMarkdown } from "../composables/useMarkdown";
import { readingTime } from "../composables/useReadingTime";
import api from "../api";

const route = useRoute();
const post = ref(null);
const loading = ref(true);
const contentRef = ref(null);

const parsed = computed(() =>
  post.value ? parseMarkdown(post.value.content) : { html: "", toc: [] }
);
const html = computed(() => parsed.value.html);
const toc = computed(() => parsed.value.toc);
const minutes = computed(() => (post.value ? readingTime(post.value.content) : 0));

useHead({
  title: computed(() =>
    post.value ? `[Aperçu] ${post.value.title} | papobilou` : "Aperçu"
  ),
});

onMounted(async () => {
  try {
    const { data } = await api.get(`/preview/${route.params.token}`);
    post.value = data;
  } catch {
    post.value = null;
  } finally {
    loading.value = false;
  }
});

watch(html, async () => {
  if (!html.value) return;
  await nextTick();
  addCopyButtons();
});

function addCopyButtons() {
  if (!contentRef.value) return;
  contentRef.value.querySelectorAll(".hljs-pre code").forEach((code) => {
    const pre = code.parentElement;
    if (!pre || pre.querySelector(".copy-btn")) return;
    pre.classList.add("relative", "group");
    const btn = document.createElement("button");
    btn.textContent = "Copier";
    btn.className =
      "copy-btn absolute right-2 top-2 opacity-0 group-hover:opacity-100 text-xs px-2 py-1 rounded bg-gray-700 hover:bg-gray-600 text-gray-200 transition-opacity";
    btn.addEventListener("click", () => {
      navigator.clipboard.writeText(code.textContent ?? "");
      btn.textContent = "Copié !";
      setTimeout(() => {
        btn.textContent = "Copier";
      }, 2000);
    });
    pre.appendChild(btn);
  });
}

function formatDate(date) {
  return new Date(date).toLocaleDateString("fr-CH");
}
</script>
