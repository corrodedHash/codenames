<script setup lang="ts">
import Wordcell from "../components/Wordcell.vue";
import { useWordStore } from "../store";

const wordStore = useWordStore();
</script>

<template>
  <div class="wordBox">
    <Wordcell
      class="wordCell"
      v-for="cellIndex in 25"
      :word="wordStore.words[cellIndex - 1] || '?'"
      :color="wordStore.colors[cellIndex - 1] || 'black'"
      :key="cellIndex"
    />
  </div>
</template>

<style scoped>
.wordBox {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr 1fr 1fr 1fr;
  height: 100vh;
  width: 100vw;
}
.wordCell {
  border: 3px solid black;
  box-sizing: border-box;
}
</style>
