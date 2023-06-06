import { createRouter, createWebHashHistory } from "vue-router";
import GameView from "./views/GameView.vue";
import RoomCreation from "./views/RoomCreation.vue";
import RoomList from "./views/RoomList.vue";
import RoomJoin from "./views/RoomJoin.vue";

const routes = [
  { path: "/create", component: RoomCreation },
  { path: "/play", component: GameView },
  { path: "/join", component: RoomJoin },
  { path: "/", component: RoomList },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
