<script setup lang="ts">
import { computed } from "vue";
import WordCell from "../components/WordCell.vue";
import { CardStateString } from "../util/util";

const props = defineProps<{
  words: string[];
  colors: (CardStateString | undefined)[];
  revealed: boolean[];
  leaderMode?: boolean;
}>();

const emit = defineEmits<{ (e: "cellClicked", index: number): void }>();

const leaderMode = computed(() => !!props.leaderMode);

function cellColor(index: number): CardStateString | undefined {
  if (props.revealed[index] || leaderMode.value) {
    return props.colors[index];
  } else {
    return undefined;
  }
}
</script>

<template>
  <div class="wordBox">
    <WordCell
      class="wordCell"
      v-for="cellIndex in 25"
      @click="emit('cellClicked', cellIndex - 1)"
      :word="props.words[cellIndex - 1] || '?'"
      :color="cellColor(cellIndex - 1)"
      :striked-through="leaderMode && revealed[cellIndex - 1]"
      :key="cellIndex"
    />
  </div>
</template>

<style scoped>
.wordBox {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(5, 1fr);
  height: 100%;
  width: 100%;
}

.wordCell {
  border: 3px solid black;
  box-sizing: border-box;
}
</style>
