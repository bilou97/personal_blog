<template>
  <div class="flex gap-3 py-6 border-t border-gray-100 dark:border-gray-800">
    <button
      v-for="r in REACTIONS"
      :key="r.key"
      @click="toggle(r.key)"
      :class="[
        'flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm border transition-all select-none',
        active(r.key)
          ? 'bg-indigo-50 dark:bg-indigo-900/30 border-indigo-300 dark:border-indigo-600 text-indigo-700 dark:text-indigo-300'
          : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600',
      ]"
    >
      <span class="text-base leading-none">{{ r.emoji }}</span>
      <span class="font-medium tabular-nums">{{ counts[r.key] }}</span>
    </button>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import api from "../api";

const props = defineProps({ slug: { type: String, required: true } });

const REACTIONS = [
  { key: "like", emoji: "👍" },
  { key: "love", emoji: "❤️" },
  { key: "fire", emoji: "🔥" },
];

const counts = reactive({ like: 0, love: 0, fire: 0 });
const userReactions = ref([]);

onMounted(async () => {
  try {
    const { data } = await api.get(`/posts/${props.slug}/reactions`);
    counts.like = data.like;
    counts.love = data.love;
    counts.fire = data.fire;
    userReactions.value = data.user_reactions;
  } catch {}
});

function active(key) {
  return userReactions.value.includes(key);
}

async function toggle(key) {
  const had = active(key);
  if (had) {
    userReactions.value = userReactions.value.filter((k) => k !== key);
    counts[key]--;
  } else {
    userReactions.value.push(key);
    counts[key]++;
  }
  try {
    const { data } = await api.post(`/posts/${props.slug}/reactions`, {
      emoji: key,
    });
    counts.like = data.like;
    counts.love = data.love;
    counts.fire = data.fire;
    userReactions.value = data.user_reactions;
  } catch {
    if (had) {
      userReactions.value.push(key);
      counts[key]++;
    } else {
      userReactions.value = userReactions.value.filter((k) => k !== key);
      counts[key]--;
    }
  }
}
</script>
