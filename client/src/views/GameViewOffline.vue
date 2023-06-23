<script setup lang="ts">
import GameBoard from "../components/GameBoard.vue";

import { GameRole, useOfflineRoomStore } from "../store";
import { CardStateString, nextState } from "../util/util";
import { ref } from "vue";
import { watchEffect } from "vue";

const props = defineProps<{
  roomID: string;
  role: GameRole;
}>();
const apiStore = useOfflineRoomStore();
const gameinfo = ref(
  undefined as
    | undefined
    | {
        words: string[];
        colors: (CardStateString | undefined)[];
        revealed: boolean[];
      }
);

watchEffect(() => {
  const room = apiStore.offlineRooms[parseInt(props.roomID)];
  if (room === undefined) throw Error("Could not find roomid");
  gameinfo.value = room;
});

function handleCellClick(index: number) {
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
}
</script>
<template>
  <div class="game-box">
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
