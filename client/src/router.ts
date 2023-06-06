import { RouteRecordRaw, createRouter, createWebHashHistory } from "vue-router";
import GameView from "./views/GameView.vue";
import RoomCreation from "./views/RoomCreation.vue";
import RoomList from "./views/RoomList.vue";
import RoomJoin from "./views/RoomJoin.vue";

function handleRoomID(route: RouteLocationNormalized) {
  const roomID = route.params.roomID;
  if (typeof roomID !== "string")
    throw Error("Unknown roomID" + typeof roomID + `${roomID}`);
  const offlineMap: Record<string, boolean> = { x: true, o: false };
  if (!Object.keys(offlineMap).includes(route.params.offline as string))
    throw Error("Unknown offline status");
  const offline = offlineMap[route.params.offline as string];
  return { offline, roomID };
}

const routes: RouteRecordRaw[] = [
  { path: "/create", component: RoomCreation },
  {
    path: "/play/:offline/:roomID/:role",
    name: "play",
    component: GameView,
    props: (route) => {
      return {
        role: route.params.role,
        ...handleRoomID(route),
      };
    },
  },
  {
    path: "/join/:offline/:roomID",
    name: "join",
    component: RoomJoin,
    props: handleRoomID,
  },

  { path: "/", component: RoomList },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
