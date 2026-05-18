<template>
  <Teleport to="body">
    <div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
      <TransitionGroup
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-2"
      >
        <div
          v-for="item in notifications.items"
          :key="item.id"
          class="pointer-events-auto flex items-start gap-3 px-4 py-3 rounded-lg shadow-lg text-sm max-w-sm"
          :class="{
            'bg-red-600 text-white': item.type === 'error',
            'bg-green-600 text-white': item.type === 'success',
            'bg-gray-800 text-white': item.type === 'info',
          }"
        >
          <span class="flex-1">{{ item.message }}</span>
          <button @click="notifications.remove(item.id)" class="opacity-70 hover:opacity-100 transition-opacity shrink-0">✕</button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useNotificationsStore } from "../stores/notifications";

const notifications = useNotificationsStore();
</script>
