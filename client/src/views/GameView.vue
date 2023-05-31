<script setup lang="ts">
import GameBoard from "../components/GameBoard.vue";
import { useWordStore } from "../store";
const wordStore = useWordStore();
</script>
<template>
  <GameBoard
    :words="wordStore.words"
    :colors="wordStore.colors"
    :revealed="wordStore.revealed"
  ></GameBoard>
</template>
