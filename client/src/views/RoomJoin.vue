<script setup lang="ts">
import { useRouter } from "vue-router";
import { GameRole, useOfflineRoomStore, useRoomStore } from "../store";
import { watchEffect, ref, computed } from "vue";
import { getRoomInfo, getUser } from "../api";
import { RoomRole } from "../util/roomInfo";
import { CardStateString } from "../util/util";
import SillySelect from "../components/SillySelect.vue";

const router = useRouter();
const apiStore = useOfflineRoomStore();
const roomStore = useRoomStore();

const props = defineProps<{ offline: boolean; roomID: string }>();

const roomInfo = ref(undefined as undefined | RoomInfo);

interface RoomInfo {
  words: string[];
  colors: (CardStateString | undefined)[];
  readAccess: boolean;
  writeAccess: boolean;
  isAdmin: boolean;
  roomID: string;
  role: RoomRole;
  displayname: string;
}

async function getOnlineRoom(): Promise<RoomInfo> {
  const fetchRoomInfo = getRoomInfo(
    props.roomID,
    roomStore.rooms[props.roomID].sessiontoken
  );
  const fetchRoomRole = getUser(
    props.roomID,
    roomStore.rooms[props.roomID].sessiontoken
  );
  const [v, r] = await Promise.all([fetchRoomInfo, fetchRoomRole]);
  return {
    words: v.words,
    colors: v.colors,
    readAccess: ["admin", "spymaster"].includes(r.role),
    writeAccess: ["admin", "spymaster", "revealer"].includes(r.role),
    roomID: props.roomID,
    isAdmin: r.role === "admin",
    role: r.role,
    displayname: r.displayname,
  };
}

watchEffect(() => {
  if (!props.offline) {
    roomInfo.value = undefined;
    getOnlineRoom().then((v) => (roomInfo.value = v));
    return;
  }

  const room = apiStore.offlineRooms[parseInt(props.roomID)];
  if (room === undefined) throw Error("Unknown room");
  roomInfo.value = {
    words: room.words,
    colors: room.colors,
    readAccess: room.owned,
    writeAccess: room.owned,
    roomID: props.roomID,
    isAdmin: true,
    role: "admin",
    displayname: "Local",
  };
});

function handleJoin(role: GameRole) {
  if (roomInfo.value === undefined) throw Error("Room info is undefined");
  router.push({
    name: props.offline ? "playOffline" : "playOnline",
    params: {
      roomID: roomInfo.value.roomID,
      role,
    },
  });
}

function handleRecreate() {
  if (roomInfo.value === undefined) return;
  router.push({
    name: "create",
    query: { s: roomInfo.value.roomID },
  });
}

const select_options = computed(() => {
  if (roomInfo.value === undefined) throw Error();
  const leader = roomInfo.value.readAccess
    ? [{ value: "leader", title: "Spymaster" }]
    : [];
  const revealer = roomInfo.value.writeAccess
    ? [{ value: "revealer", title: "Revealer" }]
    : [];
  const spectator = { value: "spectator", title: "Revealer" };
  return [...leader, ...revealer, spectator] as {
    title: string;
    value: GameRole;
  }[];
});
</script>

<template>
  <div class="box" v-if="roomInfo !== undefined">
    <span class="titleBox">{{ roomInfo.words.slice(0, 3).join("") }}</span>

    <ShareBox
      :roomID="props.roomID"
      :role="roomInfo.role"
      v-if="!props.offline"
    />
    <ShareBoxOffline :roomID="parseInt(props.roomID)" v-else />

    <div>{{ roomInfo.displayname }}</div>

    <div class="selectionBox">
      <div class="selectionBoxTitle">Join as</div>
      <SillySelect
        :options="select_options"
        @selected="(x) => handleJoin(x as
      GameRole)"
      />
    </div>
    <user-list :roomID="roomID" />
    <v-btn v-if="!props.offline && roomInfo.isAdmin" @click="handleRecreate()">
      Recreate Room
    </v-btn>
    <BoardSettings />
  </div>
</template>
<style scoped>
.selectionBoxTitle {
  text-align: center;
  font-weight: bold;
}
.titleBox {
  border-bottom: 0.1em double black;
  padding-left: 1em;
  padding-right: 1em;
  font-size: 200%;
  margin-bottom: 0.3em;
}
.box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
