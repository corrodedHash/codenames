import {
  RouteLocationNormalized,
  RouteRecordRaw,
  createRouter,
  createWebHashHistory,
} from "vue-router";
import GameView from "./views/GameView.vue";
import RoomCreation from "./views/RoomCreation.vue";
import RoomList from "./views/RoomList.vue";
import RoomJoin from "./views/RoomJoin.vue";
import ShareReceiver from "./views/ShareReceiver.vue";

const offlineTag = "x";
const onlineTag = "o";

function handleRoomID(route: RouteLocationNormalized) {
  const roomID = route.params.roomID;
  if (typeof roomID !== "string")
    throw Error("Unknown roomID" + typeof roomID + `${roomID}`);
  return roomID;
}

const routes: RouteRecordRaw[] = [
  { path: "/create", component: RoomCreation },
  {
    path: `/play/${offlineTag}/:roomID/:role`,
    name: "play",
    component: GameView,
    props: (route) => {
      return {
        role: route.params.role,
        roomID: handleRoomID(route),
        offline: true,
      };
    },
  },
  {
    path: `/join/${offlineTag}/:roomID`,
    name: "join",
    component: RoomJoin,
    props: (route) => ({ roomID: handleRoomID(route), offline: true }),
  },
  {
    path: `/s/${offlineTag}/:shareinfo`,
    name: "shareReceive",
    component: ShareReceiver,
    props: true,
  },
  { path: "/", component: RoomList },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
