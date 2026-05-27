import "./style.css";
import "highlight.js/styles/github-dark.css";
import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import { vReveal } from "./directives/reveal";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.directive("reveal", vReveal);
app.mount("#app");
