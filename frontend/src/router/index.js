import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import PostView from "../views/PostView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import NotFoundView from "../views/NotFoundView.vue";
import SearchView from "../views/SearchView.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: HomeView },
    { path: "/post/:slug", component: PostView },
    { path: "/search", component: SearchView },
    { path: "/login", component: LoginView },
    { path: "/register", component: RegisterView },
    { path: "/:pathMatch(.*)*", component: NotFoundView },
  ],
});
