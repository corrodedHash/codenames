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
import ShareReceiverOnline from "./views/ShareReceiverOnline.vue";
import ShareReceiverOffline from "./views/ShareReceiverOffline.vue";

function handleRoomID(route: RouteLocationNormalized) {
  const roomID = route.params.roomID;
  if (typeof roomID !== "string")
    throw Error("Unknown roomID" + typeof roomID + `${roomID}`);
  return roomID;
}

const routes: RouteRecordRaw[] = [
  { path: "/create", component: RoomCreation },
  {
    path: `/play/x/:roomID/:role`,
    name: "playOffline",
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
    path: `/play/o/:roomID/:role`,
    name: "playOnline",
    component: GameView,
    props: (route) => {
      return {
        role: route.params.role,
        roomID: handleRoomID(route),
        offline: false,
      };
    },
  },
  {
    path: `/join/x/:roomID`,
    name: "joinOffline",
    component: RoomJoin,
    props: (route) => ({ roomID: handleRoomID(route), offline: true }),
  },
  {
    path: `/join/o/:roomID`,
    name: "joinOnline",
    component: RoomJoin,
    props: (route) => ({ roomID: handleRoomID(route), offline: false }),
  },
  {
    path: `/s/x/:shareinfo`,
    name: "shareReceiveOffline",
    component: ShareReceiverOffline,
    props: (route) => ({
      shareinfo: route.params.shareinfo,
      offline: true,
    }),
  },
  {
    path: `/s/o/:roomID/:usertoken`,
    name: "shareReceiveOnline",
    component: ShareReceiverOnline,
    props: true,
  },
  { path: "/", component: RoomList },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
