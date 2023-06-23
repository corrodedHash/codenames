<script setup lang="ts">
import GameBoard from "../components/GameBoard.vue";
import BoardSettings from "../components/BoardSettings.vue";

import { GameRole, useRoomStore } from "../store";
import { CardStateString } from "../util/util";
import { ref, watch } from "vue";
import { clickCell, getRoomInfo, subscribe } from "../api";
import { onUnmounted } from "vue";

const props = defineProps<{
  roomID: string;
  role: GameRole;
}>();

const roomStore = useRoomStore();
const gameinfo = ref(
  undefined as
    | undefined
    | {
        words: string[];
        colors: (CardStateString | undefined)[];
        revealed: boolean[];
      }
);
let w = undefined as undefined | WebSocket;

function updateOnlineRoom() {
  getRoomInfo(props.roomID, roomStore.rooms[props.roomID].sessiontoken).then(
    (v) => {
      gameinfo.value = {
        colors: v.colors,
        words: v.words,
        revealed: v.revealed,
      };
    }
  );
}

watch(
  () => ({ role: props.role, roomID: props.roomID }),
  async ({ roomID }) => {
    updateOnlineRoom();
    w?.close();
    w = await subscribe(roomID, roomStore.rooms[roomID].sessiontoken);
    w.onmessage = updateOnlineRoom;
  },
  { immediate: true }
);
onUnmounted(() => {
  w?.close();
});

function handleCellClick(index: number) {
  switch (props.role) {
    case "leader":
    case "revealer":
      clickCell(
        props.roomID,
        index,
        roomStore.rooms[props.roomID].sessiontoken
      ).then(() => {
        updateOnlineRoom();
      });
      break;
    case "spectator":
      break;
  }
}
const showSettings = ref(false);
</script>
<template>
  <div class="game-box">
    <div class="settings-button" @click="showSettings = !showSettings">
      Settings
    </div>
    <div v-if="showSettings" class="settings-modal">
      <BoardSettings />
    </div>
    <GameBoard
      v-if="gameinfo !== undefined"
      :words="gameinfo.words"
      :colors="gameinfo.colors"
      :revealed="gameinfo.revealed"
      :leader-mode="role === 'leader'"
      @cell-clicked="handleCellClick"
    />
  </div>
</template>

<style scoped>
.settings-modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 2em;
  z-index: 1;
  border: 0.2em solid black;
}
.game-box {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
}
</style>
