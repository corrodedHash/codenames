<script setup lang="ts">
import Wordcell from "../components/Wordcell.vue";
import { CardStateString } from "../util";

const props = defineProps<{
  words: string[];
  colors: CardStateString[];
  revealed: boolean[];
}>();
</script>

<template>
  <div class="wordBox">
    <Wordcell
      class="wordCell"
      v-for="cellIndex in 25"
      :word="props.words[cellIndex - 1] || '?'"
      :color="props.colors[cellIndex - 1] || 'black'"
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
