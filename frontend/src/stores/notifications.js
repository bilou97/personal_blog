import { defineStore } from "pinia";
import { ref } from "vue";

export const useNotificationsStore = defineStore("notifications", () => {
  const items = ref([]);

  function add(message, type = "error") {
    const id = Date.now();
    items.value.push({ id, message, type });
    setTimeout(() => remove(id), 4000);
  }

  function remove(id) {
    items.value = items.value.filter((n) => n.id !== id);
  }

  return { items, add, remove };
});
