<script setup lang="ts">
import GameBoard from "../components/GameBoard.vue";
import BoardSettings from "../components/BoardSettings.vue";

import { GameRole, useOfflineRoomStore, useRoomStore } from "../store";
import { CardStateString, nextState } from "../util/util";
import { ref } from "vue";
import { clickCell, getRoomInfo, heartBeat } from "../api";
import { watchEffect } from "vue";
import { onUnmounted } from "vue";

const props = defineProps<{
  offline: boolean;
  roomID: string;
  role: GameRole;
}>();
const apiStore = useOfflineRoomStore();
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
let refreshInterval = undefined as undefined | NodeJS.Timer;
const lastState = { clickState: 0, roomState: 0 };

function updateOnlineRoom() {
  getRoomInfo(props.roomID, roomStore.rooms[props.roomID]).then((v) => {
    gameinfo.value = {
      colors: v.colors,
      words: v.words,
      revealed: v.revealed,
    };
  });
}
watchEffect(() => {
  clearInterval(refreshInterval);
  lastState.clickState = 0;
  lastState.roomState = 0;
  if (props.offline) {
    const room = apiStore.offlineRooms[parseInt(props.roomID)];
    if (room === undefined) throw Error("Could not find roomid");
    gameinfo.value = room;
  } else {
    updateOnlineRoom();
    refreshInterval = setInterval(() => {
      heartBeat(props.roomID, roomStore.rooms[props.roomID]).then((v) => {
        if (
          v.clickState === lastState.clickState &&
          v.roomState === lastState.roomState
        )
          return;
        lastState.clickState = v.clickState;
        lastState.roomState = v.roomState;
        updateOnlineRoom();
      });
    }, 1000);
  }
});
onUnmounted(() => {
  clearInterval(refreshInterval);
});

function handleCellClick(index: number) {
  if (props.offline) {
    const room = apiStore.offlineRooms[parseInt(props.roomID)];
    switch (props.role) {
      case "leader":
      case "revealer":
        room.revealed.splice(index, 1, true);
        break;
      case "spectator":
        if (!room.revealed[index]) {
          room.revealed.splice(index, 1, true);
          room.colors.splice(index, 1, "red");
        } else {
          room.colors.splice(index, 1, nextState(room.colors[index]));
        }
    }
  } else {
    switch (props.role) {
      case "leader":
      case "revealer":
        clickCell(props.roomID, index, roomStore.rooms[props.roomID]).then(
          () => {
            updateOnlineRoom();
          }
        );
        break;
      case "spectator":
        break;
    }
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
