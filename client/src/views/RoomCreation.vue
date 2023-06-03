<script setup lang="ts">
import { computed, ref } from "vue";
import { useWordStore } from "../store";
import { useRouter } from "vue-router";

const wordStore = useWordStore();

const colorSeed = ref(42);
const router = useRouter();

const canStart = computed(
  () => wordStore.words.length >= 25 && colorSeed.value > 0
);

const formattedWords = computed({
  get() {
    return wordStore.words.join("\n");
  },
  set(newValue) {
    wordStore.words = newValue.split("\n");
  },
});

function startGame() {
  router.push("/play");
}
</script>
<template>
  <div class="contentBox">
    <textarea v-model="formattedWords"></textarea>
    <input type="text" v-model.number="colorSeed" />
    <!-- <router-link to="/play" class="startButton">Start</router-link> -->
    <input
      type="button"
      value="Start"
      @click="startGame"
      :disabled="!canStart"
    />
  </div>
</template>
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
