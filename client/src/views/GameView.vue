<script setup lang="ts">
import GameBoard from "../components/GameBoard.vue";
import BoardSettings from "../components/BoardSettings.vue";

import { GameRole, useAPIStore } from "../store";
import { nextState } from "../util/util";
import { computed, ref } from "vue";

const props = defineProps<{
  offline: boolean;
  roomID: string;
  role: GameRole;
}>();
const apiStore = useAPIStore();
const gameinfo = computed(() => {
  if (props.offline) {
    const room = apiStore.offlineRooms[parseInt(props.roomID)];
    if (room === undefined) throw Error("Could not find roomid");
    return room;
  } else {
    throw Error("Online not supported");
  }
});

function handleCellClick(index: number) {
  if (props.offline) {
    switch (props.role) {
      case "leader":
        gameinfo.value.revealed.splice(index, 1, true);
        break;
      case "revealer":
        gameinfo.value.revealed.splice(index, 1, true);
        break;
      case "spectator":
        if (!gameinfo.value.revealed[index]) {
          gameinfo.value.revealed.splice(index, 1, true);
          gameinfo.value.colors.splice(index, 1, "red");
        } else {
          gameinfo.value.colors.splice(
            index,
            1,
            nextState(gameinfo.value.colors[index])
          );
        }
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
