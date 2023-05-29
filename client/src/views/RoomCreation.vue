<template>
  <div class="contentBox">
    <div class="optionsBox">
      <input type="checkbox" v-model="optionStore.showVertical" />
      <span> Vertical: </span>
      <input type="checkbox" v-model="optionStore.showMirrored" />
      <span> Horizontal: </span>
      <input type="checkbox" v-model="optionStore.leaderMode" />
      <span> Leader Mode: </span>
      <input type="checkbox" v-model="optionStore.revealer" />
      <span> Revealer Mode: </span>
    </div>
    <router-link to="/play" class="startButton">Start</router-link>
    <textarea v-model="formattedWords"></textarea>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
import { useOptionStore, useWordStore } from "../store";
const wordStore = useWordStore();
const optionStore = useOptionStore();
const formattedWords = computed({
  get() {
    return wordStore.words.join("\n");
  },
  set(newValue) {
    wordStore.setWords(newValue);
  },
});
</script>

<style scoped>
.startButton {
  margin: 2em;
}
.optionsBox {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
.contentBox {
  margin: 1em;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
