import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    watch: {
      usePolling: true,
    },
    proxy: {
      "/api": { target: "http://backend:8000", changeOrigin: true },
      "/media": { target: "http://backend:8000", changeOrigin: true },
    },
  },
});
