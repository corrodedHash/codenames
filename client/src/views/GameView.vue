<script setup lang="ts">
import GameBoard from "../components/GameBoard.vue";
import BoardSettings from "../components/BoardSettings.vue";

import { useOptionStore, useWordStore } from "../store";
import { nextState } from "../util";
import { ref } from "vue";

const wordStore = useWordStore();
const configStore = useOptionStore();
function handleCellClick(index: number) {
  if (configStore.gamemode === "revealer") {
    wordStore.revealed.splice(index, 1, true);
  } else if (configStore.gamemode === "offline") {
    wordStore.colors.splice(index, 1, nextState(wordStore.colors[index]));
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
      :words="wordStore.words"
      :colors="wordStore.colors"
      :revealed="wordStore.revealed"
      :leader-mode="configStore.gamemode === 'leader'"
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
