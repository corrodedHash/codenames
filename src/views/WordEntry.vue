<template>
  <div>
    <div>
      Vertical:
      <input type="checkbox" v-model="optionStore.showVertical" />
    </div>
    <div>
      Horizontal:
      <input type="checkbox" v-model="optionStore.showMirrored" />
    </div>
    <div>
      Leader mode:
      <input type="checkbox" v-model="optionStore.leaderMode" />
    </div>
    <div>
      Revealer mode:
      <input type="checkbox" v-model="optionStore.revealer" />
    </div>
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
