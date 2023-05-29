<template>
  <div>
    <input type="checkbox" v-model="optionStore.showVertical" />
    <input type="checkbox" v-model="optionStore.leaderMode" />
    <br />
    <router-link to="/play">Start</router-link>
  </div>
  <textarea v-model="formattedWords"></textarea>
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
