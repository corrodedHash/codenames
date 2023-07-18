import { createApp } from "vue";
import "./style.css";

import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";

import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

import { aliases, mdi } from "vuetify/iconsets/mdi-svg";

const vuetify = createVuetify({
  components,
  directives,
  icons: { defaultSet: "mdi", aliases, sets: { mdi } },
});

const pinia = createPinia();

createApp(App).use(pinia).use(router).use(vuetify).mount("#app");
