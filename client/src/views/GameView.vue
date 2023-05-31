<script setup lang="ts">
import GameBoard from "../components/GameBoard.vue";
import { useOptionStore, useWordStore } from "../store";
import { nextState } from "../util";
const wordStore = useWordStore();
const configStore = useOptionStore();
function handleCellClick(index: number) {
  if (configStore.gamemode === "revealer") {
    wordStore.revealed.splice(index, 1, true);
  } else if (configStore.gamemode === "offline") {
    wordStore.colors.splice(index, 1, nextState(wordStore.colors[index]));
  }
}
</script>
<template>
  <GameBoard
    :words="wordStore.words"
    :colors="wordStore.colors"
    :revealed="wordStore.revealed"
    :leader-mode="configStore.gamemode === 'leader'"
    @cell-clicked="handleCellClick"
  ></GameBoard>
</template>
