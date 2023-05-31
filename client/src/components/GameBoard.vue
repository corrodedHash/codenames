<script setup lang="ts">
import WordCell from "../components/WordCell.vue";
import { useOptionStore } from "../store";
import { CardStateString } from "../util";

const configStore = useOptionStore();

const props = defineProps<{
  words: string[];
  colors: CardStateString[];
  revealed: boolean[];
}>();

function cellColor(index: number): CardStateString | undefined {
  if (props.revealed || configStore.leaderMode) {
    return props.colors[index];
  } else {
    return undefined;
  }
}

function handleCellClick(index: number) {}
</script>

<template>
  <div class="wordBox">
    <WordCell
      class="wordCell"
      v-for="cellIndex in 25"
      @click="handleCellClick(cellIndex - 1)"
      :word="props.words[cellIndex - 1] || '?'"
      :color="cellColor(cellIndex - 1)"
      :key="cellIndex"
    />
  </div>
</template>

<style scoped>
.wordBox {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(5, 1fr);
  height: 100vh;
  width: 100vw;
}

.wordCell {
  border: 3px solid black;
  box-sizing: border-box;
}
</style>
