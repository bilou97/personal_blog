<template>
  <div
    class="overflow-hidden bg-gray-100 dark:bg-gray-800"
    :class="containerClass"
  >
    <img
      :src="src"
      :alt="alt"
      loading="lazy"
      :class="[imgClass, loaded ? 'opacity-100' : 'opacity-0']"
      class="w-full h-full object-cover transition-opacity duration-500"
      @load="loaded = true"
      @error="loaded = true"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";

defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: "" },
  containerClass: { type: String, default: "" },
  imgClass: { type: String, default: "" },
});

const loaded = ref(false);
</script>
