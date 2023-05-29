import { createApp } from "vue";
import "./style.css";
import Display from "./views/Display.vue";
import WordEntry from "./views/WordEntry.vue";
import App from "./App.vue";
import { createRouter, createWebHashHistory } from "vue-router";

import { createPinia } from "pinia";
import { useWordStore } from "./store";

const pinia = createPinia();

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  { path: "/", component: WordEntry },
  { path: "/play", component: Display },
];

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
});

createApp(App).use(pinia).use(router).mount("#app");

const wordStore = useWordStore();
wordStore.init();
