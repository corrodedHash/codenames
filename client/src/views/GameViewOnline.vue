<script setup lang="ts">
import GameBoard from "../components/GameBoard.vue";

import { GameRole, useRoomStore } from "../store";
import { CardStateString } from "../util/util";
import { ref, watch } from "vue";
import { clickCell, getRoomInfo, subscribe } from "../api";
import { onUnmounted } from "vue";
import { computed } from "vue";

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

function handleTick(event: MessageEvent) {
  const message = JSON.parse(event.data);
  switch (message["event"]) {
    case "click":
      const clicked_word =
        gameinfo.value?.words[message["cell"]] || message["cell"];
      appendSnackbar(`${message["displayname"]} clicked "${clicked_word}"`);
      updateOnlineRoom();

      break;
    case "roomchange":
      appendSnackbar(`${message["displayname"]} recreated room`);
      updateOnlineRoom();
      break;
    case "useronline":
      appendSnackbar(`${message["displayname"]} came online`);
      break;
    case "useroffline":
      appendSnackbar(`${message["displayname"]} went offline`);
      break;
    default:
      console.warn("Unknown message: ", event.data);
      break;
  }
}

watch(
  () => ({ role: props.role, roomID: props.roomID }),
  async ({ roomID }) => {
    updateOnlineRoom();
    w?.close();
    w = await subscribe(roomID, roomStore.rooms[roomID].sessiontoken);
    w.onmessage = handleTick;
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
const snackbar = computed({
  get: () => snackbar_text.value !== undefined,
  set(v) {
    if (!v) snackbar_text.value = undefined;
  },
});
const snackbar_text = ref(undefined as undefined | string);
let snackbar_disappear = undefined as undefined | NodeJS.Timeout;
function appendSnackbar(text: string) {
  if (snackbar_text.value === undefined) {
    snackbar_text.value = text;
  } else {
    snackbar_text.value += "\n" + text;
  }
}

watch(snackbar_text, (v) => {
  clearTimeout(snackbar_disappear);

  if (v === undefined) return;
  snackbar_disappear = setTimeout(
    () => (snackbar_text.value = undefined),
    4000
  );
});
</script>
<template>
  <div class="game-box">
    <v-snackbar v-model="snackbar" class="nobreak">
      {{ snackbar_text }}

      <template v-slot:actions>
        <v-btn color="pink" variant="text" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
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
.nobreak {
  white-space: pre;
}
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
