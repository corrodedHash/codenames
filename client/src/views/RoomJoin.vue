<script setup lang="ts">
import { useRouter } from "vue-router";
import { GameRole, useOfflineRoomStore, useRoomStore } from "../store";
import { watchEffect, ref } from "vue";
import { getRoomInfo, getRoomRole } from "../api";
import { CardStateString } from "../util/util";
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
  roomID: string;
}

watchEffect(() => {
  if (props.offline) {
    const room = apiStore.offlineRooms[parseInt(props.roomID)];
    if (room === undefined) throw Error("Unknown room");
    roomInfo.value = {
      words: room.words,
      colors: room.colors,
      readAccess: room.owned,
      writeAccess: room.owned,
      roomID: props.roomID,
    };
  } else {
    roomInfo.value = undefined;
    const fetchRoomInfo = getRoomInfo(
      props.roomID,
      roomStore.rooms[props.roomID]
    );
    const fetchRoomRole = getRoomRole(
      props.roomID,
      roomStore.rooms[props.roomID]
    );
    Promise.all([fetchRoomInfo, fetchRoomRole]).then(([v, r]) => {
      roomInfo.value = {
        words: v.words,
        colors: v.colors,
        readAccess: ["admin", "spymaster"].includes(r),
        writeAccess: ["admin", "spymaster", "revealer"].includes(r),
        roomID: props.roomID,
      };
    });
  }
});

function handleJoin(role: GameRole) {
  if (roomInfo.value === undefined) throw Error("Room info is undefined");
  if (props.offline) {
    router.push({
      name: "playOffline",
      params: {
        roomID: roomInfo.value.roomID,
        role,
      },
    });
  } else {
    router.push({
      name: "playOnline",
      params: {
        roomID: roomInfo.value.roomID,
        role,
      },
    });
  }
}
</script>

<template>
  <div class="box" v-if="roomInfo !== undefined">
    <span class="titleBox">{{ roomInfo.words.slice(0, 3).join("") }}</span>
    <div class="selectionBox">
      <div class="selectionBoxTitle">Join as</div>
      <div class="selectionOptionBox">
        <div
          class="selectionBoxOption"
          @click="handleJoin('leader')"
          v-if="roomInfo.readAccess"
        >
          Spymaster
        </div>
        <div
          class="selectionBoxOption"
          @click="handleJoin('revealer')"
          v-if="roomInfo.writeAccess"
        >
          Revealer
        </div>
        <div class="selectionBoxOption" @click="handleJoin('spectator')">
          Spectator
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.selectionOptionBox {
  display: flex;
  flex-direction: row;
}
.selectionBoxOption {
  border: 1px solid black;
  margin: 0.2em;
  padding: 0.2em;
  transition: font-size ease 0.5s;
}
.selectionBoxOption:hover {
  /* transform: scale(1.5); */
  font-size: 200%;
  background-color: white;
}
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
